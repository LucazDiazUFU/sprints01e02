SELECT id, nome, tipo, setor FROM equipamentos ORDER BY id;
SELECT id, descricao, cvss FROM vulnerabilidades WHERE ativo_id = 101;
SELECT e.nome, COUNT(v.id) AS total FROM equipamentos e LEFT JOIN vulnerabilidades v ON v.ativo_id = e.id GROUP BY e.id;
SELECT ativo_id, dependencia_id, peso FROM dependencias ORDER BY ativo_id, dependencia_id;
