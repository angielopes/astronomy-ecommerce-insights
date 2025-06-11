-- Receita líquida total, número de vendas válidas e ticket médio líquido por mês/ano
SELECT 
    YEAR(data_venda) AS ano,
    MONTH(data_venda) AS mes,
    SUM(total_venda_liquida) AS receita_liquida_total,
    COUNT(DISTINCT CASE
            WHEN status_venda IN ('concluída', 'devolvida parcialmente') THEN id_venda
            ELSE NULL
        END) AS num_vendas_validas,
    AVG(total_venda_liquida) AS ticket_medio_liquido
FROM
    vw_valor_liquido_vendas
GROUP BY ano, mes;

-- Produtos e categorias que geram mais receita líquida
SELECT 
    p.id_produto,
    p.nome_produto,
    p.categoria,
    SUM(CASE
        WHEN v.status_venda = 'cancelada' THEN 0
        WHEN vid.id_item_venda IS NULL THEN iv.preco_unitario
        ELSE 0
    END) AS receita_liquida_produtos
FROM
    itens_venda iv
        JOIN
    produtos p ON iv.id_produto = p.id_produto
        JOIN
    vendas v ON iv.id_venda = v.id_venda
        LEFT JOIN
    vw_itens_devolvidos vid ON iv.id_item_venda = vid.id_item_venda
GROUP BY p.id_produto , p.nome_produto , p.categoria
ORDER BY receita_liquida_produtos DESC;

-- 