# Architecture

```text
                   agent-workflow-comparative-eval
                   contracts / datasets / metrics
                         /               \
                        /                 \
               Agent-Workflow      candidate plugin(s)
               host authority      provider execution
```

The shared package is intentionally acyclic. It has no imports from `agent_workflow`, `agent_workflow_typesafe`, or `typesafe_sdk`.

## Migration boundary

Generic mechanics extracted from the TypeSafe plugin:
- canonical hashing;
- arm measurement and observation construction;
- static-case iteration;
- comparison schemas;
- frozen oracle datasets.

Semantics mirrored from Agent-Workflow where selected for reuse:
- missing usage stays missing rather than becoming zero;
- provider billed cost and local estimated cost stay distinct;
- subscription allocation remains separately labeled;
- Wilson intervals;
- deterministic paired bootstrap;
- p90 eligibility at 20 observations and p95 at 40.

Provider-specific telemetry and host lifecycle/persistence do not move here.
