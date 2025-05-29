-- TOP 10 CLIENTES POR VALOR TOTAL GASTO E POR NÚMERO DE COMPRAS

-- Top 10 total compras
SELECT id_cliente,
        nome_cliente,
        SUM(numero_compras) AS total_compras_cliente
FROM clientes
GROUP BY id_cliente
ORDER BY total_compras_cliente DESC
LIMIT 10;

-- Top 10 valor gasto
SELECT id_cliente,
        nome_cliente,
        total_gasto
FROM clientes
ORDER BY total_gasto DESC
LIMIT 10;

-- VALOR MÉDIO DE COMPRAS POR CLIENTE (AOV) E TICKET MÉDIO

-- Valor médio de compras (apenas compras com status "concluída")
SELECT AVG(total_venda) AS aov_cliente
FROM vendas
WHERE status_venda = 'concluída';