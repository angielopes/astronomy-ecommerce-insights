-- Active: 1747169584658@@127.0.0.1@3306
-- TICKET MÉDIO POR CLIENTE
SELECT 
    AVG(total_gasto) AS ticket_medio
FROM
    clientes;

-- PRODUTOS MAIS VENDIDOS EM VOLUME E RECEITA
SELECT 
    nome_produto,
    total_venda_produto,
    total_venda_produto * preco AS total_valor_venda_produto
FROM
    (SELECT 
        p.nome_produto,
            p.preco,
            COUNT(i.id_produto) AS total_venda_produto
    FROM
        produtos p
    JOIN itens_venda i ON p.id_produto = i.id_produto
    GROUP BY p.nome_produto , p.preco) AS quantidade_receita
ORDER BY total_valor_venda_produto DESC;
