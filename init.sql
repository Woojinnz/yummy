CREATE DATABASE "yummy";

\c yummy

CREATE TABLE country (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    iso_code char(2),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE store (
    id  BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country_id integer references country(id),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE item(
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price decimal,
    description VARCHAR(9999),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE store_items(
    id BIGSERIAL PRIMARY KEY,
    store_id BIGINT references store(id) ON DELETE CASCADE,
    item_id BIGINT references item(id) ON DELETE CASCADE,
    -- UNIQUE creates an index on left column (store_id)
    -- Helps for searching for all rows with store_id x
    UNIQUE (store_id, item_id)
);

CREATE TABLE item_image(
    id BIGSERIAL PRIMARY KEY,
    item_id BIGINT references item(id) ON DELETE CASCADE,
    image_url VARCHAR(9999),
    created_at timestamptz NOT NULL DEFAULT now(),
    is_primary BOOLEAN NOT NULL DEFAULT false,
    position INT NOT NULL DEFAULT 1
);

CREATE TABLE cuisine(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE store_cuisines(
    id SERIAL PRIMARY KEY,
    store_id BIGINT references store(id),
    cuisine_id integer references cuisine(id),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE users(
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    default_country integer NOT NULL references country(id),
    password VARCHAR(255), -- need to add hash and salt, not a thing yet
    salt VARCHAR(9999), -- is this how its stored?
    email VARCHAR(255)
);


-- INDEXING FOR THE FUTURE IF REQUIRED

-- -- Index helps to get all stores with country iso x, also checks that it must be unique
-- CREATE UNIQUE INDEX IF NOT EXISTS country_iso_code_uidx ON country(iso_code)

-- -- Index helps with getting all stores in country x and also stores it alphabetically
-- -- As index B tree is sorted then stored.
-- CREATE INDEX IF NOT EXISTS store_country_name_idx ON store(country_id, name);
-- CREATE INDEX IF NOT EXISTS store_items_item_id_idx ON store_items(item_id);

-- -- price index in item, helps searching for a range of food
-- CREATE INDEX IF NOT EXISTS item_price_idx ON item(price);