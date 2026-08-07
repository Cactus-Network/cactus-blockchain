-- Cactus block explorer index (PostgreSQL).
--
--   createdb cactus_explorer
--   psql cactus_explorer -f explorer/schema.sql
--
-- Design notes
-- ------------
-- * Puzzle hashes are stored raw (BYTEA) and never as cac1... text.  A text
--   address column would add ~62 bytes to every coin row; at hundreds of
--   millions of coins that is tens of gigabytes of duplicated data.  The API
--   converts with encode_puzzle_hash/decode_puzzle_hash at the edge instead.
-- * `amount` is BIGINT.  A single coin can never exceed the emitted supply
--   (~1.4e19 mojo at the current tip, and the largest single coin is the 210000
--   CAC premine = 2.1e17 mojo), so per-row values fit.  SUMs do NOT fit: cast
--   to numeric in every aggregate (`SUM(amount::numeric)`).
-- * `spent_height = 0` means unspent.  This matches the node's own convention
--   in coin_record.spent_index, which keeps the backfill a straight copy.

BEGIN;

CREATE TABLE IF NOT EXISTS blocks (
    height                  BIGINT PRIMARY KEY,
    header_hash             BYTEA  NOT NULL UNIQUE,
    prev_hash               BYTEA  NOT NULL,
    -- NULL on non-transaction blocks: only transaction blocks carry a
    -- foliage_transaction_block timestamp.  Do not coalesce this to 0.
    timestamp               BIGINT,
    is_transaction_block    BOOLEAN NOT NULL,
    weight                  BIGINT NOT NULL,
    total_iters             BIGINT NOT NULL,
    signage_point_index     SMALLINT NOT NULL,
    farmer_puzzle_hash      BYTEA  NOT NULL,
    pool_puzzle_hash        BYTEA  NOT NULL,
    fees                    BIGINT,          -- NULL on non-transaction blocks
    required_iters          BIGINT NOT NULL,
    deficit                 SMALLINT NOT NULL,
    overflow                BOOLEAN NOT NULL,
    sub_slot_iters          BIGINT NOT NULL,
    farmer_reward           BIGINT NOT NULL, -- 1/8 of block reward
    pool_reward             BIGINT NOT NULL  -- 7/8 of block reward
);

CREATE INDEX IF NOT EXISTS blocks_timestamp_idx  ON blocks (timestamp) WHERE timestamp IS NOT NULL;
CREATE INDEX IF NOT EXISTS blocks_farmer_ph_idx  ON blocks (farmer_puzzle_hash);
CREATE INDEX IF NOT EXISTS blocks_pool_ph_idx    ON blocks (pool_puzzle_hash);

CREATE TABLE IF NOT EXISTS coins (
    coin_name        BYTEA PRIMARY KEY,
    confirmed_height BIGINT  NOT NULL,
    spent_height     BIGINT  NOT NULL DEFAULT 0,  -- 0 = unspent
    coinbase         BOOLEAN NOT NULL,            -- true = farmer/pool reward
    puzzle_hash      BYTEA   NOT NULL,
    parent_coin_name BYTEA   NOT NULL,
    amount           BIGINT  NOT NULL,
    timestamp        BIGINT                       -- of the confirming block
);

-- Address history and balance both ride this index.
CREATE INDEX IF NOT EXISTS coins_puzzle_hash_idx ON coins (puzzle_hash);
CREATE INDEX IF NOT EXISTS coins_confirmed_idx   ON coins (confirmed_height);
CREATE INDEX IF NOT EXISTS coins_spent_idx       ON coins (spent_height) WHERE spent_height > 0;
CREATE INDEX IF NOT EXISTS coins_parent_idx      ON coins (parent_coin_name);

-- Populated only when the tail runs with --with-spends.  Puzzle reveals and
-- solutions are large; this table will outgrow `coins` if you index all of it.
CREATE TABLE IF NOT EXISTS spends (
    coin_name     BYTEA PRIMARY KEY,
    height        BIGINT NOT NULL,
    puzzle_reveal BYTEA  NOT NULL,
    solution      BYTEA  NOT NULL,
    conditions    JSONB
);

CREATE INDEX IF NOT EXISTS spends_height_idx ON spends (height);

-- Watermarks.  Keys used by the indexer:
--   snapshot_height       node peak captured when backfill first ran
--   blocks_backfilled_to  highest height copied by `backfill blocks`
--   coins_backfilled_to   highest confirmed_height copied by `backfill coins`
--   tail_height           highest height applied by the live tail
CREATE TABLE IF NOT EXISTS sync_state (
    key   TEXT   PRIMARY KEY,
    value BIGINT NOT NULL
);

COMMIT;
