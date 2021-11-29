CREATE TABLE IF NOT EXISTS spellers
(
    speller_id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(128),
    last_name VARCHAR(128),
    address VARCHAR(128),
    phone VARCHAR(128)
)