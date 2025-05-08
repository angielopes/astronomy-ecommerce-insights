"""
Script para geração de dados simulados para um sistema de e-commerce de astronomia.

Este script gera dados fictícios para clientes, produtos, vendas e devoluções,
incluindo a introdução de ruídos e inconsistências para simular cenários reais.
Os dados gerados são salvos em arquivos CSV para análise posterior.

Principais funcionalidades:
- Geração de clientes com dados fictícios, incluindo e-mails com ruídos.
- Geração de produtos organizados por categorias.
- Geração de vendas com introdução de erros em datas e status.
- Atualização de clientes com número de compras e total gasto.
- Geração de devoluções com base nas vendas devolvidas, incluindo motivos e status.
"""

import pandas as pd
import random
from faker import Faker

# Dicionário com produtos únicos para cada categoria
produtos_por_categoria = {
    "Telescópio": [
        ("Telescópio Reflector 70mm", 199.99),
        ("Telescópio Refrator 120mm", 349.99),
        ("Telescópio Cassegrain 150mm", 899.99),
        ("Telescópio Maksutov 90mm", 499.99),
        ("Telescópio Newtoniano 130mm", 379.99),
        ("Telescópio Refrator 80mm", 250.00),
        ("Telescópio Solar 150mm", 499.00),
        ("Telescópio Catadióptrico 200mm", 700.00),
        ("Telescópio ZWO 80mm", 899.50),
        ("Telescópio SkyWatcher 120mm", 650.00),
    ],
    "Binóculo": [
        ("Binóculo 10x42", 89.99),
        ("Binóculo 12x50", 120.50),
        ("Binóculo 8x32", 65.99),
        ("Binóculo 8x42", 79.99),
        ("Binóculo 10x56", 145.00),
        ("Binóculo 20x80", 250.00),
        ("Binóculo 15x70", 185.50),
        ("Binóculo 10x25", 50.00),
        ("Binóculo 7x35", 80.00),
        ("Binóculo 10x42 Compacto", 99.99),
    ],
    "Mapas Celestes": [
        ("Mapa Celeste de Observação Noturna", 29.99),
        ("Mapa Celeste para Iniciantes", 25.99),
        ("Mapa Celeste de Constelações", 22.50),
        ("Atlas Astronômico", 50.00),
        ("Mapa de Estrelas e Galáxias", 39.99),
        ("Mapa Estelar Interativo", 45.00),
        ("Mapa de Céu Profundo", 60.00),
        ("Mapa do Céu para Astronomia Avançada", 55.00),
        ("Mapa Astronômico do Hemisfério Norte", 30.00),
        ("Mapa do Universo em 3D", 80.00),
    ],
    "Livros de Astronomia": [
        ("O Universo e Seus Mistérios", 39.99),
        ("Astronomia para Iniciantes", 19.99),
        ("Guia Completo de Telescópios", 34.99),
        ("Explorando os Céus", 25.50),
        ("O Cosmos em Detalhes", 29.99),
        ("Guia do Céu Profundo", 45.00),
        ("Astronomia: Uma Nova Perspectiva", 40.00),
        ("Como Observar Estrelas e Galáxias", 37.50),
        ("Astronomia para Todos", 20.99),
        ("O Mistério dos Buracos Negros", 49.99),
    ],
    "Kits de Observação": [
        ("Kit Completo de Observação Astronômica", 249.99),
        ("Kit de Observação Solar", 99.99),
        ("Kit de Observação Lunar", 129.99),
        ("Kit para Observação de Estrelas", 149.99),
        ("Kit de Iniciação à Astronomia", 89.99),
        ("Kit para Fotografia Astronômica", 179.99),
        ("Kit de Observação de Planetas", 199.99),
        ("Kit Completo de Astrofotografia", 399.99),
        ("Kit de Observação de Meteoros", 59.99),
        ("Kit de Observação com Binóculos", 120.00),
    ],
}


def gerar_clientes(n=1000):
    """
    Gera um DataFrame com dados fictícios de clientes.

    Args:
        n (int): Número de clientes a serem gerados. Padrão é 1000.

    Returns:
        pd.DataFrame: DataFrame contendo os dados dos clientes.
    """
    fake = Faker()
    clientes = []
    for _ in range(n):
        cliente = {
            "id_cliente": fake.unique.uuid4(),
            "nome_cliente": fake.name(),
            "email": fake.email(),
            "idade": random.randint(18, 75),
            "regiao": random.choice(["Norte", "Sul", "Leste", "Oeste"]),
            "data_cadastro": fake.date_this_decade(),
            "status": random.choice(["ativo", "inativo"]),
        }

        # Adição de e-mails inválidos ou com falhas aleatórias (ruído)
        if random.random() < 0.05:  # 5% de chance de erro no e-mail
            cliente["email"] = cliente["email"].replace(
                "@", random.choice(["#", "%", "&"])
            )

        clientes.append(cliente)

    return pd.DataFrame(clientes)


def gerar_produtos():
    """
    Gera um DataFrame com dados fictícios de produtos.

    Returns:
        pd.DataFrame: DataFrame contendo os dados dos produtos.
    """
    produtos = []
    produto_id = 1

    for categoria, lista_produtos in produtos_por_categoria.items():
        for nome_produto, preco in lista_produtos:
            produto = {
                "id_produto": f"prod_{produto_id}",
                "nome_produto": nome_produto,
                "categoria": categoria,
                "preco": preco,
            }
            produtos.append(produto)
            produto_id += 1

    return pd.DataFrame(produtos)


def gerar_vendas(clientes, produtos, n=5000):
    """
    Gera um DataFrame com dados fictícios de vendas.

    Args:
        clientes (pd.DataFrame): DataFrame contendo os dados dos clientes.
        produtos (pd.DataFrame): DataFrame contendo os dados dos produtos.
        n (int): Número de vendas a serem geradas. Padrão é 5000.

    Returns:
        pd.DataFrame: DataFrame contendo os dados das vendas.
    """
    fake = Faker()
    vendas = []

    # Garantir que todos os clientes tenham pelo menos uma venda
    clientes_ids = clientes["id_cliente"].tolist()
    produtos_list = produtos.to_dict(orient="records")

    for _ in range(n):
        produto = random.choice(produtos_list)
        quantidade = random.randint(1, 5)
        preco_total = round(produto["preco"] * quantidade, 2)
        id_cliente = random.choice(clientes_ids)

        data_venda = fake.date_this_year()
        data_venda_errada = data_venda.strftime("%d/%m/%Y")

        # Introduzir erro de formatação nas datas de venda
        if random.random() < 0.05:  # 5% de chance de erro na data
            data_venda_errada = f"{random.randint(1, 31)}-{random.choice(['abc', 'def', 'ghi'])}-{random.randint(2000, 2023)}"

        # Probabilidades dos status
        status_venda = random.choices(
            ["concluída", "cancelada", "devolvida"],
            weights=[0.85, 0.10, 0.05],
            k=1,
        )[0]

        venda = {
            "id_venda": fake.unique.uuid4(),
            "id_cliente": id_cliente,
            "id_produto": produto["id_produto"],
            "quantidade": quantidade,
            "preco_total": preco_total,
            "data_venda": data_venda_errada,
            "canal_venda": random.choice(["site", "marketplace"]),
            "status_venda": status_venda,
        }

        # Vendas com status incorreto ou com erro na data (ruído)
        if random.random() < 0.05:
            venda["status_venda"] = random.choice(
                ["em processamento", "erro", "pendente"]
            )

        vendas.append(venda)

    return pd.DataFrame(vendas)


def atualizar_clientes(clientes, vendas):
    """
    Atualiza os clientes com número de compras e total gasto baseado nas vendas.
    """
    # Calcular totais por cliente
    vendas_validas = vendas[vendas["status_venda"] == "concluída"]
    compras_por_cliente = vendas_validas["id_cliente"].value_counts()
    gasto_por_cliente = vendas_validas.groupby("id_cliente")["preco_total"].sum()

    # Atualizar clientes
    clientes["numero_compras"] = (
        clientes["id_cliente"].map(compras_por_cliente).fillna(0).astype(int)
    )
    clientes["total_gasto"] = (
        clientes["id_cliente"].map(gasto_por_cliente).fillna(0).round(2)
    )

    return clientes


def gerar_devolucoes(vendas):
    """
    Gera um DataFrame com dados fictícios de devoluções com base nas vendas devolvidas.

    Args:
        vendas (pd.DataFrame): DataFrame contendo os dados das vendas.

    Returns:
        pd.DataFrame: DataFrame contendo os dados das devoluções.
    """
    # Filtrar as vendas que têm status "devolvida"
    vendas_devolvidas = vendas[vendas["status_venda"] == "devolvida"]

    # Verificar se há vendas devolvidas para criar devoluções
    if vendas_devolvidas.empty:
        print("Não há vendas com status 'devolvida' para gerar devoluções.")
        return pd.DataFrame()  # Retorna um DataFrame vazio caso não haja devoluções

    # Criação de devoluções a partir das vendas com status == "devolvida"
    fake = Faker()
    devolucoes = []

    for _, venda in vendas_devolvidas.iterrows():
        devolucao = {
            "id_devolucao": fake.unique.uuid4(),
            "id_venda": venda["id_venda"],
            "motivo_devolucao": random.choice(
                ["defeito", "não gostei", "erro na compra", "não era o esperado"]
            ),
            "data_devolucao": fake.date_this_year(),
            "status_devolucao": random.choice(["em andamento", "finalizada"]),
        }

        devolucoes.append(devolucao)

    return pd.DataFrame(devolucoes)


clientes = gerar_clientes(1000)
produtos = gerar_produtos()
vendas = gerar_vendas(clientes, produtos, 5000)
clientes = atualizar_clientes(clientes, vendas)
devolucoes = gerar_devolucoes(vendas)

logging.info("Clientes sem compras: %d", len(clientes[clientes["numero_compras"] == 0]))
logging.info("Vendas por status:\n%s", vendas["status_venda"].value_counts())

clientes.to_csv("data/clientes.csv", sep=";", index=False)
produtos.to_csv("data/produtos.csv", sep=";", index=False)
vendas.to_csv("data/vendas.csv", sep=";", index=False)
devolucoes.to_csv("data/devolucoes.csv", sep=";", index=False)
