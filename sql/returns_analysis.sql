WITH performance_produtos AS (
    SELECT 
    p.id_produto,
    p.nome_produto,
    p.categoria,
    COUNT(vid.id_item_venda) AS unidades_devolvidas_aprovadas,
    COUNT(CASE
        WHEN vid.id_item_venda IS NULL THEN iv.id_item_venda
    END) AS unidades_vendidas_liquidas
FROM
    itens_venda iv
        JOIN
    produtos p ON iv.id_produto = p.id_produto
        JOIN
    vendas v ON iv.id_venda = v.id_venda
        LEFT JOIN
    vw_itens_devolvidos vid ON iv.id_item_venda = vid.id_item_venda
WHERE
    v.status_venda IN ('concluída' , 'devolvida parcialmente')
GROUP BY p.id_produto , p.nome_produto , p.categoria
)

-- Taxa de devolução dos produtos
SELECT 
    nome_produto,
    categoria,
    unidades_devolvidas_aprovadas,
    unidades_vendidas_liquidas,
    CASE
        WHEN (unidades_devolvidas_aprovadas + unidades_vendidas_liquidas) = 0 THEN 0
        ELSE (unidades_devolvidas_aprovadas * 1.0 / (unidades_devolvidas_aprovadas + unidades_vendidas_liquidas)) * 100
    END AS taxa_devolucao
FROM
    performance_produtos
ORDER BY taxa_devolucao DESC;