# Repository Consolidation Progress

P0 verified: Agent #173 `007dbc66365a8c2ca26fa12cbc89d5b544d7339a`; Hub #93 `83dcd6e7a2cba94e5bc0b4975579252da1d5e69a`. GitHub execution Goal published in Agent #174; original input blocker resolved.

| Phase | Status | Branch / PR |
|---|---|---|
| P1 | Consumer dual-read implemented; must merge before P2 | Agent #175 |
| P2 | Hub Catalog consolidated; local authority/registry/32 tests/export/consumer no_op PASS | chore/repository-consolidation-p2 |
| P3 | Await P2 merge full SHA for re-pin | — |
| P4 | Await Artist consumer preparation then producer move | — |
| P5–P8 | In progress / pending final integration | — |

Catalog is now owned by Hub/Registry, Hub/Schemas, Hub/SubAgents, Hub/Tools and Hub/Tests. Authority map is Hub/repository-authority.yaml; admission metadata is Hub/specialist-execution-admission.yaml. No Hub runtime/installer/resolver introduced. Capability/Profile/Provider/UPM IDs and frozen legacy provenance are unchanged. Artist code and compatibility files retain their paths until P4. P0 inventory and import plans remain immutable historical baseline files.

Next: observe Agent #175 merge, then P2 required CI, then Squash Merge and Agent Source Lock re-pin. Unity Editor/License/Player/Visual/device BLOCKED_NOT_RUN; checked-in historical Evidence validators are static shape checks only.
