-- TICKET MÉDIO POR CLIENTE
SELECT AVG(total_gasto) AS ticket_medio
FROM clientes;

-- SAZONALIDADE DAS VENDAS POR MÊS
SELECT MONTH(data_venda) AS vendas_mes,
    YEAR(data_venda) AS vendas_ano,
    SUM(total_venda)
FROM vendas
GROUP BY vendas_mes,
    vendas_ano;

-- CATEGORIAS DE PRODUTOS MAIS LUCRATIVAS
SELECT p.categoria,
    SUM(v.total_venda) AS total_venda_categoria,
    COUNT(i.id_produto) AS total_produto_vendido_categoria
FROM produtos p
    JOIN itens_venda i ON p.id_produto = i.id_produto
    JOIN vendas v ON i.id_venda = v.id_venda
GROUP BY p.categoria;

-- PRODUTOS MAIS VENDIDOS EM VOLUME E RECEITA
SELECT nome_produto,
    total_venda_produto,
    total_venda_produto * preco AS total_valor_venda_produto
FROM (
        SELECT p.nome_produto,
            p.preco,
            COUNT(i.id_produto) AS total_venda_produto
        FROM produtos p
            JOIN itens_venda i ON p.id_produto = i.id_produto
        GROUP BY p.nome_produto,
            p.preco
    ) AS quantidade_receita
ORDER BY total_valor_venda_produto DESC;

-- TAXA DE DEVOLUÇÃO POR PRODUTO
