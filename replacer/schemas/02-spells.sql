CREATE TABLE IF NOT EXISTS spells
(
    spell_id        BIGSERIAL PRIMARY KEY,
    speller_id      BIGSERIAL,
    element         VARCHAR(128),
    attack          INT,
    healing         INT,
    magic_defence   INT
)