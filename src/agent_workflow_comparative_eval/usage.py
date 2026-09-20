from __future__ import annotations
from collections.abc import Iterable, Mapping
from typing import Any

NUMERIC_FIELDS=("input_tokens","cached_input_tokens","cache_write_input_tokens","output_tokens","reasoning_output_tokens","provider_total_tokens","retry_count","provider_billed_cost","local_estimated_cost","subscription_allocated_cost","provider_elapsed_seconds","first_output_latency_seconds")
ALIASES={
 "input_tokens":("input_tokens","prompt_tokens"),"cached_input_tokens":("cached_input_tokens","cache_read_input_tokens","cache_read_tokens"),"cache_write_input_tokens":("cache_write_input_tokens","cache_creation_input_tokens","cache_creation_tokens"),"output_tokens":("output_tokens","completion_tokens"),"reasoning_output_tokens":("reasoning_output_tokens","reasoning_tokens"),"provider_total_tokens":("provider_total_tokens","total_tokens"),"retry_count":("retry_count","retries"),"provider_elapsed_seconds":("provider_elapsed_seconds","duration_api_ms","duration_api_seconds"),"first_output_latency_seconds":("first_output_latency_seconds","time_to_first_token_seconds")}

def _number(value: object)->int|float|None:
    if value is None or isinstance(value,bool): return None
    return value if isinstance(value,(int,float)) else None

def _first_number(value: Mapping[str,Any],names:Iterable[str])->int|float|None:
    for name in names:
        observed=_number(value.get(name))
        if observed is not None: return float(observed)/1000.0 if name=="duration_api_ms" else observed
    return None

def empty_usage(*,currency:str|None,price_catalog_id:str|None,billing_mode:str="unknown")->dict[str,Any]:
    result={field:None for field in NUMERIC_FIELDS}; result.update(currency=currency,price_catalog_id=price_catalog_id,billing_mode=billing_mode,provider_billed_cost_semantics="unknown",local_estimated_cost_source="unavailable",token_evidence_complete=False,cost_evidence_complete=False,source="unavailable"); return result

def _estimate_cost(tokens:Mapping[str,Any],pricing:Mapping[str,Any]|None)->float|None:
    if not isinstance(pricing,Mapping): return None
    rates=pricing.get("usd_per_million_tokens")
    if not isinstance(rates,Mapping): return None
    input_tokens=_number(tokens.get("input_tokens")); output_tokens=_number(tokens.get("output_tokens"))
    if input_tokens is None or output_tokens is None: return None
    cached=_number(tokens.get("cached_input_tokens")) or 0; cache_write=_number(tokens.get("cache_write_input_tokens")) or 0; reasoning=_number(tokens.get("reasoning_output_tokens")) or 0
    noncached=input_tokens
    if pricing.get("input_tokens_include_cached",True): noncached=max(0,input_tokens-cached-cache_write)
    total=0.0
    for count,rate in ((noncached,rates.get("input")),(cached,rates.get("cached_input",rates.get("input"))),(cache_write,rates.get("cache_write_input",rates.get("input"))),(output_tokens,rates.get("output")),(reasoning,rates.get("reasoning_output",0))):
        if count and _number(rate) is None: return None
        total += float(count)*float(rate or 0)/1_000_000.0
    return round(total,8)

def normalize_usage(value:Mapping[str,Any],*,currency:str|None=None,price_catalog_id:str|None=None,source:str="mapping",billing:Mapping[str,Any]|None=None,pricing:Mapping[str,Any]|None=None)->dict[str,Any]:
    billing=billing or {}; billing_mode=str(billing.get("mode","unknown")); result={field:None for field in NUMERIC_FIELDS}
    for field,aliases in ALIASES.items(): result[field]=_first_number(value,aliases)
    if result["provider_total_tokens"] is None and result["input_tokens"] is not None and result["output_tokens"] is not None: result["provider_total_tokens"]=result["input_tokens"]+result["output_tokens"]
    emitted=_first_number(value,("provider_billed_cost","total_cost_usd","cost_usd","cost")); explicit=_number(value.get("local_estimated_cost")); catalog=_estimate_cost(result,pricing); semantics=str(billing.get("provider_billed_cost_semantics","unknown"))
    if billing_mode=="subscription":
        result["provider_billed_cost"]=None
        if explicit is not None: local,local_source=explicit,"explicit-local"
        elif catalog is not None: local,local_source=catalog,"price-catalog"
        elif emitted is not None: local,local_source=emitted,"provider-emitted-equivalent"
        else: local,local_source=None,"unavailable"
    else:
        result["provider_billed_cost"]=emitted
        if explicit is not None: local,local_source=explicit,"explicit-local"
        elif catalog is not None: local,local_source=catalog,"price-catalog"
        else: local,local_source=None,"unavailable"
    result["local_estimated_cost"]=local; result["local_estimated_cost_source"]=local_source; result["subscription_allocated_cost"]=_number(value.get("subscription_allocated_cost")); result["currency"]=value.get("currency") or currency; result["price_catalog_id"]=value.get("price_catalog_id") or price_catalog_id; result["billing_mode"]=billing_mode; result["provider_billed_cost_semantics"]=semantics
    result["token_evidence_complete"]=all(result[f] is not None for f in ("input_tokens","output_tokens","provider_total_tokens"))
    if billing_mode=="subscription" and semantics=="not-attributable": result["cost_evidence_complete"]=result["local_estimated_cost"] is not None
    elif billing_mode=="synthetic": result["cost_evidence_complete"]=result["provider_billed_cost"] is not None
    else: result["cost_evidence_complete"]=result["provider_billed_cost"] is not None or result["local_estimated_cost"] is not None
    result["source"]=source; return result

def sum_nullable(values:Iterable[int|float|None])->int|float|None:
    items=list(values)
    if not items or any(v is None for v in items): return None
    total=sum(v for v in items if v is not None); return round(total,8) if isinstance(total,float) else total

def aggregate_usage(values:list[Mapping[str,Any]],*,billing:Mapping[str,Any]|None=None)->dict[str,Any]:
    result={field:sum_nullable([_number(v.get(field)) for v in values]) for field in NUMERIC_FIELDS}
    currencies={v.get("currency") for v in values if v.get("currency") is not None}; catalogs={v.get("price_catalog_id") for v in values if v.get("price_catalog_id") is not None}; modes={v.get("billing_mode") for v in values if v.get("billing_mode")}; semantics={v.get("provider_billed_cost_semantics") for v in values if v.get("provider_billed_cost_semantics")}; sources={v.get("local_estimated_cost_source") for v in values if v.get("local_estimated_cost_source")}
    result["currency"]=next(iter(currencies)) if len(currencies)==1 else None; result["price_catalog_id"]=next(iter(catalogs)) if len(catalogs)==1 else None; result["billing_mode"]=next(iter(modes)) if len(modes)==1 else "mixed"; result["provider_billed_cost_semantics"]=next(iter(semantics)) if len(semantics)==1 else "mixed"; result["local_estimated_cost_source"]=next(iter(sources)) if len(sources)==1 else ("mixed" if sources else "unavailable")
    result["token_evidence_complete"]=bool(values) and all(v.get("token_evidence_complete") is True for v in values); result["cost_evidence_complete"]=bool(values) and all(v.get("cost_evidence_complete") is True for v in values)
    allocation=(billing or {}).get("subscription_allocation",{})
    if result["billing_mode"]=="subscription" and isinstance(allocation,Mapping) and allocation.get("method")=="fixed-per-arm-run": result["subscription_allocated_cost"]=_number(allocation.get("amount"))
    result["complete"]=result["token_evidence_complete"]; return result
