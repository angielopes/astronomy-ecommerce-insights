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

-- Valor médio de compra por cliente (AOV)
SELECT
        vlv.id_cliente,
        AVG(vlv.total_venda_liquida) AS aov_liquido_cliente
FROM vw_valor_liquido_vendas
WHERE status_venda IN ('concluida', 'devolvida parcialmente')
GROUP BY id_cliente;

-- Ticket médio geral
SELECT
        AVG(total_venda_liquida) AS ticket_medio_geral
FROM vw_valor_liquido_vendas
WHERE status_venda IN ('concluída', 'devolvida parcialmente');

-- Distribuição de clientes por região
SELECT
        c.regiao,
        SUM(vlv.total_venda_liquida) AS receita_liquida_total
FROM vw_valor_liquido_vendas vlv
JOIN clientes c ON vlv.id_cliente = c.id_cliente
GROUP BY c.regiao
ORDER BY receita_liquida_total DESC;

-- Receita por faixa etária e região
SELECT
        c.idade,
        SUM(vlv.total_venda_liquida) as receita_por_idade
FROM vw_valor_liquido_vendas vlv
JOIN clientes c ON vlv.id_cliente = c.id_cliente
GROUP BY c.idade
ORDER BY receita_por_idade DESC;

-- Última compra válida por cliente
SELECT
        id_cliente,
        MAX(data_venda) AS data_ultima_compra_valida
FROM vendas
WHERE status_venda IN ('concluída', 'devolvida parcialmente')
GROUP BY id_cliente
ORDER BY data_ultima_compra_valida DESC;

-- Frequência de compras válidas
SELECT
        id_cliente, COUNT(DISTINCT id_venda) AS num_compras_validas
FROM vendas
WHERE status_venda IN ('concluída', 'devolvida parcialmente')
GROUP BY id_cliente;

-- Total gasto líquido por cliente
SELECT
        id_cliente,
        SUM(total_venda_liquida) AS total_liquido_gasto
FROM vw_valor_liquido_vendas
GROUP BY id_cliente;