"""
Script para geração de dados simulados para um sistema de e-commerce de astronomia.

Este script gera dados fictícios para clientes, produtos, vendas e devoluções,
incluindo a introdução de ruídos e inconsistências para simular cenários reais.
Os dados gerados são salvos em arquivos CSV para análise posterior.
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
            "total_gasto": round(random.uniform(100, 10000), 2),
            "numero_compras": random.randint(1, 50),
            "status": random.choice(["ativo", "inativo"]),
        }

        # Introduzindo ruídos: adição de e-mails inválidos ou com falhas aleatórias
        if random.random() < 0.05:  # 5% de chance de erro no e-mail
            cliente["email"] = cliente["email"].replace(
                "@", random.choice(["#", "%", "&"])
            )  # Corrompendo o símbolo @

        # Ruído nos gastos totais: alguns valores podem ser errados
        if random.random() < 0.05:  # 5% de chance de erro no valor total gasto
            cliente["total_gasto"] = round(
                random.uniform(1000, 50000), 2
            )  # Erro de valores muito altos

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

    for _ in range(n):
        produto = random.choice(produtos.to_dict(orient="records"))
        quantidade = random.randint(1, 5)  # Quantidade aleatória de produtos
        preco_total = round(produto["preco"] * quantidade, 2)

        data_venda = fake.date_this_year()  # Data real gerada corretamente
        data_venda_errada = data_venda.strftime("%d/%m/%Y")  # Formato correto

        # Introduzir erro de formatação nas datas de venda
        if random.random() < 0.05:  # 5% de chance de erro na data
            data_venda_errada = f"{random.randint(1, 31)}-{random.choice(['abc', 'def', 'ghi'])}-{random.randint(2000, 2023)}"  # Erro proposital de formatação

        # Ajustar as probabilidades dos status
        status_venda = random.choices(
            ["concluída", "cancelada", "devolvida"],
            weights=[0.8, 0.15, 0.05],  # Probabilidades ajustadas
            k=1,
        )[0]

        venda = {
            "id_venda": fake.unique.uuid4(),
            "id_cliente": random.choice(clientes["id_cliente"]),
            "id_produto": produto["id_produto"],
            "quantidade": quantidade,
            "preco_total": preco_total,
            "data_venda": data_venda_errada,  # Data errada
            "canal_venda": random.choice(["site", "loja física", "marketplace"]),
            "status_venda": status_venda,
        }

        # Introduzindo ruídos: vendas com status incorreto ou com erro na data
        if random.random() < 0.05:  # 5% de chance de erro no status
            venda["status_venda"] = random.choice(
                ["em processamento", "erro", "pendente"]
            )

        vendas.append(venda)

    return pd.DataFrame(vendas)


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

    # Agora, criar as devoluções a partir das vendas devolvidas
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

        # Introduzindo ruídos: status incorreto ou motivo de devolução inválido
        if random.random() < 0.05:  # 5% de chance de erro no status da devolução
            devolucao["status_devolucao"] = random.choice(["pendente", "cancelado"])

        if random.random() < 0.05:  # 5% de chance de motivo de devolução inválido
            devolucao["motivo_devolucao"] = "erro técnico de processamento"

        devolucoes.append(devolucao)

    return pd.DataFrame(devolucoes)


clientes = gerar_clientes(1000)
produtos = gerar_produtos()
vendas = gerar_vendas(clientes, produtos, 5000)
devolucoes = gerar_devolucoes(vendas)

print(clientes.head())
print(produtos.head())
print(vendas.head())
print(devolucoes.head())

clientes.to_csv("../data/clientes.csv", sep=";", index=False)
produtos.to_csv("../data/produtos.csv", sep=";", index=False)
vendas.to_csv("../data/vendas.csv", sep=";", index=False)
devolucoes.to_csv("../data/devolucoes.csv", sep=";", index=False)
