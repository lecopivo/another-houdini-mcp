# Glue Cluster (SOP)

## What This Node Is For

`gluecluster` assigns glue-network bond strengths from cluster membership, enabling clustered rigid pieces to behave as stronger internal groups with weaker inter-group bonds.

## Session Status

- Status: deep-studied
- Docs read: yes (`nodes/sop/gluecluster.txt`)
- Example set reviewed: yes (`examples/nodes/sop/gluecluster/glueclusterexample.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs + stickies):
  - Constraints connecting points in same cluster get "internal" strength.
  - Cross-cluster (or cluster=0 detached) constraints get "inter" strength.
  - Optional noise and random detach reshape cluster topology before strength assignment.
- Observed (live play on `/obj/academy_deep_gluecluster/torus_object1/gluecluster`):
  - Baseline strengths are binary from configured values (`-1.0` and `1.0` in example defaults).
  - With `intracluster=1000`, `intercluster=0.5`:
    - strengths became exactly `{1000, 0.5}` with expected split (`448` internal vs `3093` inter constraints).
  - `randomdetach=1`, `detachratio=0.6` significantly increased detached points (`cluster==0` rose from `59` to `301`).
  - `addclusternoise=1` with smaller cluster size (`0.5`) removed detached zeros and increased cluster diversity (`8 -> 66` unique cluster ids), shifting more constraints into internal-strength bucket.
  - `visualizecluster=0` removed point `Cd` visualization attribute while preserving cluster logic attrs.
- Mismatches: none.

## Minimum Repro Setup

- Example network: fracture constraints merged from voronoi fracture into `gluecluster`.
- Validate by inspecting:
  - point `cluster` distribution,
  - primitive `strength` value histogram,
  - optional visualization attrs (`Cd`).

## Key Parameter Interactions

- `intracluster` vs `intercluster` define two strength tiers; set clear physical ratio.
- `randomdetach` + `detachratio` pushes pieces into detached state (`cluster=0`), forcing inter-strength behavior.
- `addclusternoise` can repopulate/refine cluster IDs, often reducing zeros and increasing intra-cluster bonds.
- `visualizecluster` is debug-only presentation aid; do not rely on it as data contract.

## Gotchas and Failure Modes

- Negative/low internal strengths can unintentionally make clusters weaker than inter-cluster bonds.
- If many points remain `cluster=0`, results may look like clustering failed (but logic is working as configured).
- Always inspect constraint-strength distribution, not just geometry color, when validating glue behavior.
