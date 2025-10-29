CREATE DATABASE "yummy";

\c yummy

CREATE TABLE country (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    iso_code char(2) UNIQUE,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE store (
    id  BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country_id integer references country(id) NOT NULL,
    normalized_name VARCHAR(255) UNIQUE NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE users(
    id BIGSERIAL PRIMARY KEY,
    google_sub: VARCHAR(255) UNIQUE,
    email: VARCHAR(255) UNIQUE NOT NULL,
    name: VARCHAR(255) NOT NULL,
    picture: VARCHAR(9999),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE item(
    -- item is a global item, so ice cream is just the existence of ice cream not connected to anything.
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    normalized_name VARCHAR(255) UNIQUE NOT NULL,
    created_by BIGINT references users(id),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE store_items(
    id BIGSERIAL PRIMARY KEY,
    store_id BIGINT NOT NULL references store(id) ON DELETE CASCADE ,
    item_id BIGINT NOT NULL references item(id) ON DELETE CASCADE,
    price DECIMAL,
    created_at timestamptz NOT NULL DEFAULT now(),
    -- A store can only have one row for a given item
    UNIQUE (store_id, item_id)
);

create TABLE item_review(
    id BIGSERIAL PRIMARY KEY,
    store_item_id BIGINT NOT NULL references store_items(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL references users(id) ON DELETE CASCADE,
    description VARCHAR(9999),
    stars DECIMAL NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE item_image(
    id BIGSERIAL PRIMARY KEY,
    store_item_id BIGINT NOT NULL references store_items(id) ON DELETE CASCADE,
    image_url VARCHAR(9999),
    created_at timestamptz NOT NULL DEFAULT now(),
    is_primary BOOLEAN NOT NULL DEFAULT false,
    position INT NOT NULL DEFAULT 1
);

ALTER TABLE item_image
  ADD CONSTRAINT item_image_unique_position_per_item
  UNIQUE (store_item_id, position);

ALTER TABLE item_image
  ADD CONSTRAINT item_image_position_positive CHECK (position >= 1);

CREATE OR REPLACE FUNCTION item_image_enforce_single_primary()
RETURNS trigger AS $$
BEGIN
  IF NEW.is_primary THEN
    UPDATE item_image
       SET is_primary = FALSE
     WHERE store_item_id = NEW.store_item_id
       AND id <> COALESCE(NEW.id, -1)
       AND is_primary = TRUE;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_item_image_single_primary
BEFORE INSERT OR UPDATE OF is_primary, store_item_id
ON item_image
FOR EACH ROW
EXECUTE FUNCTION item_image_enforce_single_primary();


CREATE UNIQUE INDEX item_image_one_primary_per_store_item
ON item_image (store_item_id)
WHERE is_primary;

CREATE TABLE cuisine(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    normalized_name VARCHAR(255) UNIQUE,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE store_cuisines(
    id SERIAL PRIMARY KEY,
    store_id BIGINT references store(id),
    cuisine_id integer references cuisine(id),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (store_id, cuisine_id)
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