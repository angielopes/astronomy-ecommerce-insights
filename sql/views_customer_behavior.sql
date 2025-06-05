-- Valor total devolvido efetivamente por vendas
CREATE VIEW vw_valor_itens_devolvidos_aprovados_por_venda AS 
SELECT
		d.id_venda,
		SUM(iv.preco_unitario) AS total_valor_devolvido_aprovado
FROM devolucoes d
JOIN itens_devolucao idv ON d.id_devolucao = idv.id_devolucao
JOIN itens_venda iv ON idv.id_item_venda = iv.id_item_venda
WHERE d.status_devolucao IN ('aprovada', 'finalizada')
GROUP BY d.id_venda;

-- Valor líquido das vendas (exclusão das devoluções e vendas canceladas)
CREATE VIEW vw_valor_liquido_vendas AS
    SELECT 
        v.id_venda,
        v.id_cliente,
        v.data_venda,
        v.canal_venda,
        v.status_venda,
        v.total_venda AS total_venda_bruta,
        COALESCE(vida.total_valor_devolvido_aprovado, 0) AS total_devolvido_venda,
        CASE
            WHEN v.status_venda = 'cancelada' THEN 0
            ELSE (v.total_venda - COALESCE(vida.total_valor_devolvido_aprovado, 0))
        END AS total_venda_liquida
    FROM
        vendas v
            LEFT JOIN
        vw_valor_itens_devolvidos_aprovados_por_venda vida ON v.id_venda = vida.id_venda;

-- Itens efetivamente devolvidos
CREATE VIEW vw_itens_devolvidos AS
    SELECT DISTINCT
        idv.id_item_venda
    FROM
        devolucoes d
            JOIN
        itens_devolucao idv ON d.id_devolucao = idv.id_devolucao
    WHERE
        d.status_devolucao IN ('aprovada' , 'finalizada');