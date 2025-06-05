-- Valor total devolvido efetivamente por vendas
WITH valor_itens_devolvidos_aprovados_por_venda AS (
	SELECT
		d.id_venda,
		SUM(iv.preco_unitario) AS total_valor_devolvido_aprovado
	FROM devolucoes d
	JOIN itens_devolucao idv ON d.id_devolucao = idv.id_devolucao
	JOIN itens_venda iv ON idv.id_item_venda = iv.id_item_venda
	WHERE d.status_devolucao IN ('aprovada', 'finalizada')
	GROUP BY d.id_venda
),

-- Valor líquido das vendas (exclusão das devoluções e vendas canceladas)
valor_liquido_vendas AS (
        SELECT
                v.id_venda,
                v.id_cliente,
                v.data_venda,
                v.canal_venda,
                v.status_venda,
                v.total_venda AS total_venda_bruta,
                COALESCE(vida.total_valor_devolvido_aprovado, 0) AS total_devolvido_venda,
                CASE
                        WHEN v.status_venda = 'cancelada' THEN 0 -- Vendas canceladas não entrarão em valores líquidos
                        ELSE(v.total_venda - COALESCE(vida.total_valor_devolvido_aprovado, 0))
                END AS total_venda_liquida
        FROM vendas v
        LEFT JOIN valor_itens_devolvidos_aprovados_por_venda vida ON v.id_venda = vida.id_venda
)

-- Top 10 clientes por valor gasto
SELECT 
        vlv.id_cliente,
        c.nome_cliente,
        SUM(vlv.total_venda_liquida) AS total_liquido_gasto_cliente
FROM valor_liquido_vendas vlv
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
WHERE status_venda IN ('concluida', 'devolvida parcialmente')
GROUP BY id_cliente, c.nome_cliente
ORDER BY num_compras_validas_cliente DESC
LIMIT 10;