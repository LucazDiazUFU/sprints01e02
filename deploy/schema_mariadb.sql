CREATE TABLE IF NOT EXISTS trabalho2_controle (
    id TINYINT UNSIGNED PRIMARY KEY,
    versao BIGINT UNSIGNED NOT NULL DEFAULT 0,
    CONSTRAINT chk_trabalho2_controle CHECK (id = 1)
) ENGINE=InnoDB;

INSERT IGNORE INTO trabalho2_controle (id, versao) VALUES (1, 0);

CREATE TABLE IF NOT EXISTS trabalho2_equipamentos (
    id BIGINT PRIMARY KEY,
    dados JSON NOT NULL,
    CONSTRAINT chk_trabalho2_id CHECK (id > 0),
    CONSTRAINT chk_trabalho2_objeto CHECK (JSON_TYPE(dados) = 'OBJECT'),
    CONSTRAINT chk_trabalho2_id_json CHECK (
        JSON_EXTRACT(dados, '$.id') IS NOT NULL
        AND JSON_TYPE(JSON_EXTRACT(dados, '$.id')) = 'INTEGER'
        AND CAST(JSON_UNQUOTE(JSON_EXTRACT(dados, '$.id')) AS SIGNED) = id
    )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
