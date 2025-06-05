-- Top 10 clientes por valor gasto
SELECT 
        vlv.id_cliente,
        c.nome_cliente,
        SUM(vlv.total_venda_liquida) AS total_liquido_gasto_cliente
FROM vw_valor_liquido_vendas vlv
JOIN clientes c ON vlv.id_cliente = c.id_cliente
GROUP BY vlv.id_cliente, c.nome_cliente
ORDER BY total_liquido_gasto_cliente DESC
LIMIT 10;

-- Valor médio de compra por cliente (AOV)
SELECT
        vlv.id_cliente,
        AVG(vlv.total_venda_liquida) AS aov_liquido_cliente
FROM vw_valor_liquido_vendas vlv
WHERE vlv.status_venda IN ('concluida', 'devolvida parcialmente')
GROUP BY vlv.id_cliente;

-- Top 10 clientes por compras efetivadas
SELECT
        v.id_cliente,
        c.nome_cliente,
        COUNT(DISTINCT v.id_venda) AS num_compras_validas_cliente
FROM vendas v
JOIN clientes c ON v.id_cliente = c.id_cliente
WHERE v.status_venda IN ('concluida', 'devolvida parcialmente')
GROUP BY id_cliente, c.nome_cliente
ORDER BY num_compras_validas_cliente DESC
LIMIT 10;

