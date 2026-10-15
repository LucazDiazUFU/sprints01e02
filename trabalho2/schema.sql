PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS controle (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    versao INTEGER NOT NULL DEFAULT 0
);
INSERT OR IGNORE INTO controle (id, versao) VALUES (1, 0);

CREATE TABLE IF NOT EXISTS equipamentos (
    id INTEGER PRIMARY KEY CHECK (id > 0),
    nome TEXT NOT NULL UNIQUE,
    responsavel TEXT NOT NULL,
    setor TEXT NOT NULL,
    tipo INTEGER NOT NULL CHECK (tipo BETWEEN 1 AND 6),
    criticidade TEXT NOT NULL,
    status TEXT NOT NULL,
    descricao TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS vulnerabilidades (
    id INTEGER PRIMARY KEY CHECK (id > 0),
    ativo_id INTEGER NOT NULL REFERENCES equipamentos(id) ON DELETE CASCADE,
    descricao TEXT NOT NULL,
    categoria TEXT NOT NULL,
    severidade TEXT NOT NULL,
    status TEXT NOT NULL,
    cve TEXT NOT NULL DEFAULT '',
    cvss REAL CHECK (cvss IS NULL OR cvss BETWEEN 0 AND 10),
    referencia TEXT NOT NULL DEFAULT '',
    recomendacao TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS dependencias (
    ativo_id INTEGER NOT NULL REFERENCES equipamentos(id) ON DELETE CASCADE,
    dependencia_id INTEGER NOT NULL REFERENCES equipamentos(id) ON DELETE CASCADE,
    peso REAL NOT NULL CHECK (peso >= 0 AND peso < 1),
    PRIMARY KEY (ativo_id, dependencia_id),
    CHECK (ativo_id <> dependencia_id)
);
CREATE INDEX IF NOT EXISTS idx_vulnerabilidades_ativo ON vulnerabilidades(ativo_id);
