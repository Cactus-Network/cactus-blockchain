# Architecture Overview

> Attach this file when starting unfamiliar work or needing first-time
> orientation on the cactus-blockchain codebase.

## Project shape

Python PoST blockchain. **Not a monorepo** — this repository (`cactus-blockchain`)
is the Python node implementation. It depends on several external packages from
the Cactus-Network GitHub org for Rust-accelerated cryptography, proofs, and
puzzle compilation.

## External Cactus dependencies

| Package           | Repo                                                                            | Role                                                                                                                                                        | Used by                                                                    |
| ----------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `cactus_rs`         | [Cactus-Network/cactus_rs](https://github.com/Cactus-Network/cactus_rs)                 | Core Rust FFI: consensus types, BLS signatures, CLVM execution, serialization, condition validation, spend bundle validation, merkle sets, V2 proof solving | Nearly everything — consensus, mempool, wallet, types, solver              |
| `chiapos`         | [Cactus-Network/chiapos](https://github.com/Cactus-Network/chiapos)                 | Proof of Space: plot creation, proof verification, quality computation                                                                                      | `cactus/plotting/`, `cactus/types/blockchain_format/proof_of_space.py`         |
| `chiavdf`         | [Cactus-Network/chiavdf](https://github.com/Cactus-Network/chiavdf)                 | VDF computation and proof verification                                                                                                                      | `cactus/timelord/`, `cactus/types/blockchain_format/vdf.py`, `cactus/simulator/` |
| `clvm`            | [Cactus-Network/clvm](https://github.com/Cactus-Network/clvm)                       | Python CLVM interpreter (used in tooling, not consensus-hot path)                                                                                           | `cactus/types/blockchain_format/program.py`, wallet puzzle drivers           |
| `clvm_tools`      | [Cactus-Network/clvm_tools](https://github.com/Cactus-Network/clvm_tools)           | CLVM utilities: currying, `Program.to()`, disassembly                                                                                                       | Wallet puzzle construction, tests, debugging                               |
| `chialisp`        | [Cactus-Network/chialisp](https://github.com/Cactus-Network/chialisp)               | Rust ChiaLisp compiler — compiles `.clsp` puzzle source to CLVM bytecode                                                                                    | `cactus/wallet/puzzles/load_clvm.py`, puzzle compilation tooling             |
| `cactus-puzzles-py` | [Cactus-Network/cactus-puzzles-py](https://github.com/Cactus-Network/cactus-puzzles-py) | Pre-compiled standard puzzle bytecode (singletons, CATs, DIDs, NFTs, etc.)                                                                                  | Wallet puzzle drivers, pool puzzles, data layer                            |
| `chiabip158`      | [Cactus-Network/chiabip158](https://github.com/Cactus-Network/chiabip158)           | BIP-158 compact block filters for lightweight wallet sync                                                                                                   | Block body validation, mempool manager, wallet sync                        |

**Version pinning**: `cactus_rs` is pinned to a minor range (`>=0.37.0, <0.38`).
Other Cactus packages use minimum-version pins. See `pyproject.toml` for current values.

## Module map

| Module             | Purpose                                                              | Criticality  |
| ------------------ | -------------------------------------------------------------------- | ------------ |
| `cactus/consensus/`  | Block validation, difficulty, fork choice, VDF iters, rewards        | **Critical** |
| `cactus/full_node/`  | Full node state, mempool, stores, fee estimation, weight proofs, RPC | **Critical** |
| `cactus/server/`     | Networking: WebSocket, rate limiting, peer discovery, TLS            | **Critical** |
| `cactus/protocols/`  | Wire protocol message definitions between all node types             | **Critical** |
| `cactus/wallet/`     | Wallet state, coin selection, spend construction, sub-wallets        | **High**     |
| `cactus/farmer/`     | Farming logic, signage point handling, proof forwarding              | **High**     |
| `cactus/harvester/`  | Plot file management, PoS lookups                                    | **Medium**   |
| `cactus/timelord/`   | VDF computation, infusion point management                           | **High**     |
| `cactus/types/`      | Type definitions: blockchain format, mempool items, generators       | **High**     |
| `cactus/util/`       | DB wrapper, streamable, keychain, bech32m, etc.                      | **Medium**   |
| `cactus/simulator/`  | Test blockchain simulator                                            | Low          |
| `cactus/data_layer/` | DataLayer (data-storage singleton)                                   | Medium       |
| `cactus/cmds/`       | CLI command handlers                                                 | Low          |

## `cactus_rs` boundary (largest external dependency)

Nearly all core consensus types live in Rust via `cactus_rs`:

**Types**: `BlockRecord`, `FullBlock`, `ConsensusConstants`, `SpendBundleConditions`,
`CoinRecord`, `SpendBundle`, `EndOfSubSlotBundle`, `HeaderBlock`, `UnfinishedBlock`,
`SubEpochSummary`, `SubEpochChallengeSegment`, `Coin`, `CoinSpend`, `G1Element`,
`G2Element`, `AugSchemeMPL`, `BLSCache`, `PartialProof`.

**Functions**: `validate_clvm_and_signature`, `run_block_generator`,
`run_block_generator2`, `additions_and_removals`, `check_time_locks`,
`compute_merkle_set_root`, `fast_forward_singleton`, `supports_fast_forward`,
`get_flags_for_height_and_constants`, `solution_generator_backrefs`,
`get_puzzle_and_solution_for_coin2`, `is_canonical_serialization`,
`get_conditions_from_spendbundle`, `get_spends_for_trusted_block`,
`solve_proof` (V2 plot solving).

**Rule of thumb**: Consensus-critical _math_ (VDF iteration calculation, difficulty
adjustment, quality computation) is Python. Signature/CLVM/serialization
validation is Rust. VDF proofs are computed by `chiavdf`, PoS proofs by
`chiapos`. Puzzle bytecode comes pre-compiled from `cactus-puzzles-py`.

## Actors

Node roles are defined by `NodeType` in `cactus/protocols/outbound_message.py`:
`FULL_NODE`, `HARVESTER`, `FARMER`, `TIMELORD`, `INTRODUCER`, `WALLET`,
`DATA_LAYER`, `SOLVER`.

### Full Node (central)

- **P2P API**: `FullNodeAPI` in `full_node_api.py` (~2080 lines)
- **RPC API**: `FullNodeRpcApi` in `full_node_rpc_api.py` (~1170 lines)
- **State machine**: `FullNode` in `full_node.py` (~3400 lines)

### Farmer

- **API**: `FarmerAPI` in `farmer_api.py` — receives signage points, forwards proofs
- **RPC**: `FarmerRpcApi` — local management

### Harvester

- **API**: `HarvesterAPI` in `harvester_api.py` — receives challenges, checks plots

### Timelord

- **API**: `TimelordAPI` in `timelord_api.py` — receives peaks, produces VDFs
- **State**: `TimelordState` in `timelord_state.py`

### Wallet

- **P2P**: `WalletNodeAPI` in `wallet_node_api.py` — coin state updates
- **RPC**: `WalletRpcApi` in `wallet_rpc_api.py` (~3600 lines) — full wallet surface
- **State**: `WalletStateManager` in `wallet_state_manager.py` (~3300 lines)

### Introducer

- **Service**: `Introducer` in `introducer.py` — bootstrap peer discovery
- **API**: `IntroducerAPI` in `introducer_api.py` — serves vetted peer lists

### Data Layer

- **Service**: `DataLayer` in `data_layer.py` — singleton-based data store service
- **RPC**: `DataLayerRpcApi` in `data_layer_rpc_api.py` — DataLayer control surface

### Solver

- **Service**: `Solver` in `solver.py` — solves V2 plot partial proofs into full proofs of space
- **API**: `SolverAPI` in `solver_api.py` — receives `SolverInfo` (partial proof, plot_id, k-size) from farmer, returns full proof via `SolverResponse`

## Wire protocol overview

109 message types in `ProtocolMessageTypes` enum. Key flows:

- **Full Node ↔ Full Node**: `new_peak`, `new_transaction`, `request_block(s)`,
  `new_signage_point_or_end_of_sub_slot`, `request_compact_vdf`
- **Full Node ↔ Wallet**: `new_peak_wallet`, `send_transaction`,
  `coin_state_update`, `request_puzzle_state`, `mempool_items_added/removed`
- **Farmer ↔ Full Node**: `new_signage_point`, `declare_proof_of_space`,
  `request_signed_values`
- **Farmer ↔ Harvester**: `new_signage_point_harvester`, `new_proof_of_space`,
  `request_signatures`
- **Full Node ↔ Timelord**: `new_peak_timelord`, `new_infusion_point_vdf`,
  `new_signage_point_vdf`

## Key type files

| File                                                 | Contents                                               |
| ---------------------------------------------------- | ------------------------------------------------------ |
| `cactus/types/blockchain_format/coin.py`               | `Coin` (parent_id, puzzle_hash, amount)                |
| `cactus/types/blockchain_format/vdf.py`                | `VDFInfo`, `VDFProof`                                  |
| `cactus/types/blockchain_format/proof_of_space.py`     | PoS verification                                       |
| `cactus/types/blockchain_format/program.py`            | CLVM program wrappers                                  |
| `cactus/types/blockchain_format/serialized_program.py` | Lazy CLVM deserialization                              |
| `cactus/types/mempool_item.py`                         | `MempoolItem`, `BundleCoinSpend`, `UnspentLineageInfo` |
| `cactus/types/generator_types.py`                      | `BlockGenerator`, `NewBlockGenerator`                  |
| `cactus/types/validation_state.py`                     | `ValidationState`                                      |
| `cactus/types/weight_proof.py`                         | `WeightProof`                                          |
| `cactus/consensus/block_record.py`                     | Re-export of `BlockRecord` from cactus_rs                |
| `cactus/consensus/default_constants.py`                | `DEFAULT_CONSTANTS` with all parameter values          |
