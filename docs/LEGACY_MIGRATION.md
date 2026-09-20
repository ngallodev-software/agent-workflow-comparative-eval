# Legacy TypeSafe v1 migration

The initial comparative evidence used provider-namespaced IDs such as `agent-workflow-typesafe/comparison-observation/v1`.

`upgrade_legacy_record()` returns a copy with the canonical neutral schema ID. It does not mutate the supplied mapping or historical artifact. `downgrade_typesafe_v1_record()` exists only for the plugin's 0.1.x compatibility facade.

Field meanings are preserved. If a future correction changes result meaning, it must use a new canonical schema version rather than silently changing v1.
