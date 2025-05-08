"""
Script para geração de dados simulados para um sistema de e-commerce de astronomia.

Este script gera dados fictícios para clientes, produtos, vendas, itens de venda, devoluções e itens de devolução.
As datas são restritas ao ano de 2025, até a data de execução definida.
A data de cadastro do cliente é definida pela sua primeira compra.
Os dados gerados são salvos em arquivos CSV na pasta 'data/' para análise posterior.

Principais funcionalidades:
- Geração de clientes com dados fictícios, incluindo e-mails e datas de cadastro realistas (primeira compra).
- Geração de produtos organizados por categorias, com nomes e preços variados.
- Geração de vendas, cada uma podendo conter múltiplos itens, com datas em 2025.
- Atualização dos clientes com número de compras realizadas e total gasto.
- Geração de devoluções com base em uma fração das vendas, incluindo motivos e status variados, com datas em 2025.
- Atualização do status das vendas para refletir devoluções parciais ou totais.
- Exportação dos seguintes arquivos CSV: clientes.csv, produtos.csv, vendas.csv,
  itens_venda.csv, devolucoes.csv, itens_devolucao.csv.
"""

import logging
import pandas as pd
import random
from faker import Faker
import os
from datetime import timedelta, date

# Configurações Globais e Constantes
SEED = 42  # Para reprodutibilidade
N_CLIENTES_TARGET = 1000
# N_VENDAS_INICIAIS_PARA_CLIENTES não é mais usado diretamente da mesma forma.
N_VENDAS_A_GERAR = 6000  # Número total de vendas a serem geradas inicialmente
FRACAO_DEVOLUCAO = 0.05  # 5% das vendas concluídas podem gerar devolução
DATA_OUTPUT_DIR = "data"  # Pasta para salvar os CSVs

# Definição das datas de referência para o ano de 2025
HOJE_DEFINIDO = date(2025, 5, 8)
INICIO_ANO_2025 = date(2025, 1, 1)

# Configuração da semente para reprodutibilidade
random.seed(SEED)
Faker.seed(SEED)
fake = Faker("pt_BR")

# Configuração do logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Dicionário com produtos únicos para cada categoria (mantido como no original)
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


def gerar_clientes_desde_vendas(df_vendas_todas, n_target_clientes):
    """
    Gera um DataFrame com dados de clientes, onde a data de cadastro é a primeira data de compra.
    Seleciona até n_target_clientes.

    Args:
        df_vendas_todas (pd.DataFrame): DataFrame de todas as vendas geradas.
        n_target_clientes (int): Número desejado de clientes.

    Returns:
        pd.DataFrame: DataFrame contendo os dados dos clientes.
    """
    logging.info(
        f"Gerando clientes baseados nas vendas. Alvo: {n_target_clientes} clientes."
    )
    if df_vendas_todas.empty:
        logging.warning("Nenhuma venda fornecida para gerar clientes.")
        return pd.DataFrame()

    if not pd.api.types.is_datetime64_any_dtype(df_vendas_todas["data_venda"]):
        df_vendas_todas["data_venda"] = pd.to_datetime(df_vendas_todas["data_venda"])

    primeira_compra_por_cliente = (
        df_vendas_todas.groupby("id_cliente")["data_venda"].min().reset_index()
    )
    primeira_compra_por_cliente.rename(
        columns={"data_venda": "data_cadastro"}, inplace=True
    )

    if len(primeira_compra_por_cliente) > n_target_clientes:
        clientes_selecionados_df = primeira_compra_por_cliente.sample(
            n=n_target_clientes, random_state=SEED
        )
    else:
        clientes_selecionados_df = primeira_compra_por_cliente
        if len(clientes_selecionados_df) < n_target_clientes:
            logging.warning(
                f"Gerados {len(clientes_selecionados_df)} clientes, menos que o alvo de {n_target_clientes}, pois houve menos clientes únicos nas vendas."
            )

    clientes_data = []
    for _, row in clientes_selecionados_df.iterrows():
        clientes_data.append(
            {
                "id_cliente": row["id_cliente"],
                "nome_cliente": fake.name(),
                "email": fake.email(),
                "idade": random.randint(18, 75),
                "regiao": random.choice(
                    ["Norte", "Nordeste", "Sudeste", "Sul", "Centro-Oeste"]
                ),
                "data_cadastro": row["data_cadastro"],
            }
        )

    df_clientes = pd.DataFrame(clientes_data)
    if not df_clientes.empty:
        df_clientes["data_cadastro"] = pd.to_datetime(df_clientes["data_cadastro"])

    logging.info(f"{len(df_clientes)} clientes finais gerados.")
    return df_clientes


def gerar_produtos():
    """
    Gera um DataFrame com dados fictícios de produtos. (Função original mantida)
    """
    logging.info("Gerando produtos...")
    produtos_data = []
    produto_id_counter = 1

    for categoria, lista_produtos_na_categoria in produtos_por_categoria.items():
        for nome_produto, preco in lista_produtos_na_categoria:
            produto = {
                "id_produto": f"prod_{produto_id_counter:04d}",
                "nome_produto": nome_produto,
                "categoria": categoria,
                "preco": preco,
            }
            produtos_data.append(produto)
            produto_id_counter += 1

    df_produtos = pd.DataFrame(produtos_data)
    logging.info(f"{len(df_produtos)} produtos gerados.")
    return df_produtos


def gerar_vendas_e_itens(
    df_clientes_placeholder,
    df_produtos,
    n_vendas,
    data_final_geracao,
    data_inicial_geracao,
):
    """
    Gera DataFrames com dados fictícios de vendas e itens de venda.
    Datas de venda são geradas entre data_inicial_geracao e data_final_geracao.
    A data_cadastro do df_clientes_placeholder é usada como limite inferior inicial para as vendas.

    Args:
        df_clientes_placeholder (pd.DataFrame): DataFrame com 'id_cliente' e 'data_cadastro' (base).
        df_produtos (pd.DataFrame): DataFrame contendo os dados dos produtos.
        n_vendas (int): Número de vendas a serem geradas.
        data_final_geracao (datetime.date): Data máxima para geração de vendas.
        data_inicial_geracao (datetime.date): Data mínima para geração de vendas.


    Returns:
        tuple: (pd.DataFrame_vendas, pd.DataFrame_itens_venda)
    """
    logging.info(
        f"Gerando {n_vendas} vendas e seus itens entre {data_inicial_geracao} e {data_final_geracao}..."
    )
    vendas_data = []
    itens_venda_data = []

    clientes_ids_list = df_clientes_placeholder["id_cliente"].tolist()
    produtos_list_of_dicts = df_produtos.to_dict(orient="records")

    if not clientes_ids_list:
        logging.error("Não há IDs de clientes para gerar vendas.")
        return pd.DataFrame(), pd.DataFrame()
    if not produtos_list_of_dicts:
        logging.error("Não há produtos para gerar vendas.")
        return pd.DataFrame(), pd.DataFrame()

    for i in range(n_vendas):
        id_venda_atual = str(fake.unique.uuid4())
        id_cliente_venda = random.choice(clientes_ids_list)

        data_cadastro_base_cliente = (
            df_clientes_placeholder.loc[
                df_clientes_placeholder["id_cliente"] == id_cliente_venda,
                "data_cadastro",
            ]
            .iloc[0]
            .date()
        )

        start_date_venda_faker = max(data_cadastro_base_cliente, data_inicial_geracao)
        end_date_venda_faker = data_final_geracao

        if start_date_venda_faker > end_date_venda_faker:
            logging.warning(
                f"Intervalo de datas inválido para venda do cliente {id_cliente_venda} ({start_date_venda_faker} > {end_date_venda_faker}). Usando data final."
            )
            data_venda_obj = end_date_venda_faker
        else:
            data_venda_obj = fake.date_between_dates(
                date_start=start_date_venda_faker, date_end=end_date_venda_faker
            )

        status_venda_inicial = random.choices(
            ["concluída", "cancelada"],
            weights=[0.90, 0.10],
            k=1,
        )[0]

        venda_info = {
            "id_venda": id_venda_atual,
            "id_cliente": id_cliente_venda,
            "data_venda": data_venda_obj,
            "canal_venda": random.choice(["site", "marketplace", "app móvel"]),
            "status_venda": status_venda_inicial,
            "total_venda": 0.0,
        }

        num_tipos_de_produto_na_venda = random.randint(1, 3)
        produtos_selecionados_para_venda = random.sample(
            produtos_list_of_dicts, num_tipos_de_produto_na_venda
        )
        total_venda_calculado = 0.0

        for produto_info in produtos_selecionados_para_venda:
            quantidade_comprada = random.randint(1, 3)
            preco_unitario_item = produto_info["preco"]
            preco_total_para_este_item = round(
                preco_unitario_item * quantidade_comprada, 2
            )
            total_venda_calculado += preco_total_para_este_item
            item_info = {
                "id_item_venda": str(fake.unique.uuid4()),
                "id_venda": id_venda_atual,
                "id_produto": produto_info["id_produto"],
                "quantidade": quantidade_comprada,
                "preco_unitario": preco_unitario_item,
                "preco_total_item": preco_total_para_este_item,
            }
            itens_venda_data.append(item_info)

        venda_info["total_venda"] = round(total_venda_calculado, 2)
        vendas_data.append(venda_info)

        if (i + 1) % (n_vendas // 10 if n_vendas >= 10 else 1) == 0:
            logging.info(f"Geradas {i+1}/{n_vendas} vendas...")

    df_vendas = pd.DataFrame(vendas_data)
    df_itens_venda = pd.DataFrame(itens_venda_data)

    if not df_vendas.empty:
        df_vendas["data_venda"] = pd.to_datetime(df_vendas["data_venda"])

    logging.info(
        f"{len(df_vendas)} vendas e {len(df_itens_venda)} itens de venda gerados."
    )
    return df_vendas, df_itens_venda


def atualizar_clientes_com_metricas_venda(df_clientes, df_vendas, df_itens_venda):
    """
    Atualiza o DataFrame de clientes com número de compras e total gasto. (Função original mantida)
    """
    logging.info("Atualizando clientes com métricas de vendas...")
    vendas_consideradas = df_vendas[
        df_vendas["status_venda"].isin(["concluída", "devolvida parcialmente"])
    ]
    compras_por_cliente = vendas_consideradas["id_cliente"].value_counts()

    if not vendas_consideradas.empty and not df_itens_venda.empty:
        itens_com_cliente = df_itens_venda.merge(
            vendas_consideradas[["id_venda", "id_cliente"]], on="id_venda", how="inner"
        )
        gasto_por_cliente = itens_com_cliente.groupby("id_cliente")[
            "preco_total_item"
        ].sum()
    else:
        gasto_por_cliente = pd.Series(dtype="float64")

    df_clientes["numero_compras"] = (
        df_clientes["id_cliente"].map(compras_por_cliente).fillna(0).astype(int)
    )
    df_clientes["total_gasto"] = (
        df_clientes["id_cliente"].map(gasto_por_cliente).fillna(0.0).round(2)
    )

    logging.info("Métricas de clientes atualizadas.")
    return df_clientes


def gerar_devolucoes_e_itens(
    df_vendas,
    df_itens_venda,
    fracao_devolucao,
    data_final_geracao,
    data_inicial_geracao,
):
    """
    Gera DataFrames com dados fictícios de devoluções e itens de devolução.
    Datas de devolução são geradas entre (data da venda + 1 dia) e data_final_geracao,
    respeitando também o data_inicial_geracao.
    """
    logging.info(
        f"Gerando devoluções para aproximadamente {fracao_devolucao*100}% das vendas concluídas..."
    )
    devolucoes_data = []
    itens_devolucao_data = []

    vendas_passiveis_devolucao = df_vendas[
        df_vendas["status_venda"] == "concluída"
    ].copy()

    if vendas_passiveis_devolucao.empty:
        logging.warning("Nenhuma venda 'concluída' encontrada para gerar devoluções.")
        return pd.DataFrame(
            columns=[
                "id_devolucao",
                "id_venda",
                "motivo_geral_devolucao",
                "data_devolucao",
                "status_devolucao",
            ]
        ), pd.DataFrame(
            columns=[
                "id_item_devolucao",
                "id_devolucao",
                "id_item_venda",
                "id_produto",
                "quantidade_devolvida",
                "motivo_especifico_item",
            ]
        )

    if not pd.api.types.is_datetime64_any_dtype(
        vendas_passiveis_devolucao["data_venda"]
    ):
        vendas_passiveis_devolucao["data_venda"] = pd.to_datetime(
            vendas_passiveis_devolucao["data_venda"]
        )

    vendas_para_devolver_sample = vendas_passiveis_devolucao.sample(
        frac=fracao_devolucao, random_state=SEED
    )

    for _, venda_info in vendas_para_devolver_sample.iterrows():
        id_devolucao_atual = str(fake.unique.uuid4())
        id_venda_associada = venda_info["id_venda"]
        data_venda_original_dt = venda_info["data_venda"].date()

        start_date_devolucao_faker = data_venda_original_dt + timedelta(days=1)
        start_date_devolucao_faker = max(
            start_date_devolucao_faker, data_inicial_geracao
        )

        end_date_devolucao_prazo = data_venda_original_dt + timedelta(
            days=random.randint(2, 30)
        )
        end_date_devolucao_faker = min(end_date_devolucao_prazo, data_final_geracao)

        if start_date_devolucao_faker > end_date_devolucao_faker:
            if data_venda_original_dt == data_final_geracao:
                data_devolucao_obj = data_final_geracao
                logging.debug(
                    f"Devolução para venda {id_venda_associada} em {data_venda_original_dt} tem data de início {start_date_devolucao_faker} e fim {end_date_devolucao_faker}. Definindo para data final."
                )
            else:
                data_devolucao_obj = min(
                    data_venda_original_dt + timedelta(days=1), data_final_geracao
                )
                if data_devolucao_obj < start_date_devolucao_faker:
                    logging.warning(
                        f"Não foi possível gerar data de devolução válida para venda {id_venda_associada} (data_venda: {data_venda_original_dt}, start_devolucao: {start_date_devolucao_faker}, end_devolucao: {end_date_devolucao_faker}). Pulando devolução."
                    )
                    continue
        else:
            data_devolucao_obj = fake.date_between_dates(
                date_start=start_date_devolucao_faker, date_end=end_date_devolucao_faker
            )

        devolucao_info = {
            "id_devolucao": id_devolucao_atual,
            "id_venda": id_venda_associada,
            "motivo_geral_devolucao": random.choice(
                [
                    "Produto com defeito",
                    "Arrependimento da compra",
                    "Tamanho/cor inadequado",
                    "Produto diferente do anunciado",
                    "Entrega atrasada e não mais necessário",
                ]
            ),
            "data_devolucao": data_devolucao_obj,
            "status_devolucao": random.choice(
                ["em processamento", "aprovada", "rejeitada", "finalizada"]
            ),
        }
        devolucoes_data.append(devolucao_info)

        itens_originais_da_venda = df_itens_venda[
            df_itens_venda["id_venda"] == id_venda_associada
        ]
        if itens_originais_da_venda.empty:
            logging.warning(
                f"Venda {id_venda_associada} para devolução não possui itens. Pulando itens de devolução."
            )
            continue

        if random.random() < 0.7:
            itens_selecionados_para_devolver = itens_originais_da_venda
        else:
            num_itens_a_devolver = random.randint(1, len(itens_originais_da_venda))
            itens_selecionados_para_devolver = itens_originais_da_venda.sample(
                n=num_itens_a_devolver, random_state=SEED
            )

        for _, item_original_info in itens_selecionados_para_devolver.iterrows():
            quantidade_a_devolver = (
                random.randint(1, item_original_info["quantidade"])
                if random.random() >= 0.8
                else item_original_info["quantidade"]
            )
            item_devolvido_info = {
                "id_item_devolucao": str(fake.unique.uuid4()),
                "id_devolucao": id_devolucao_atual,
                "id_item_venda": item_original_info["id_item_venda"],
                "id_produto": item_original_info["id_produto"],
                "quantidade_devolvida": quantidade_a_devolver,
                "motivo_especifico_item": (
                    random.choice(
                        [
                            "Cor diferente",
                            "Danificado na entrega",
                            "Qualidade inferior ao esperado",
                            "Simplesmente não gostei",
                        ]
                    )
                    if random.random() > 0.3
                    else devolucao_info["motivo_geral_devolucao"]
                ),
            }
            itens_devolucao_data.append(item_devolvido_info)

    df_devolucoes = pd.DataFrame(devolucoes_data)
    df_itens_devolucao = pd.DataFrame(itens_devolucao_data)

    if not df_devolucoes.empty:
        df_devolucoes["data_devolucao"] = pd.to_datetime(
            df_devolucoes["data_devolucao"]
        )

    logging.info(
        f"{len(df_devolucoes)} devoluções e {len(df_itens_devolucao)} itens de devolução gerados."
    )
    return df_devolucoes, df_itens_devolucao


def atualizar_status_venda_pos_devolucao(
    df_vendas, df_devolucoes, df_itens_venda, df_itens_devolucao
):
    """
    Atualiza o status das vendas com base nas devoluções.
    """
    logging.info("Atualizando status das vendas com base nas devoluções...")
    if df_devolucoes.empty or df_devolucoes.dropna(subset=["id_venda"]).empty:
        logging.info("Nenhuma devolução para processar ou devoluções sem id_venda.")
        return df_vendas

    devolucoes_impactantes = df_devolucoes[
        df_devolucoes["status_devolucao"].isin(["finalizada", "aprovada"])
    ].copy()
    if devolucoes_impactantes.empty:
        logging.info("Nenhuma devolução impactante para atualizar status de vendas.")
        return df_vendas

    for id_venda_afetada in devolucoes_impactantes["id_venda"].unique():
        if pd.isna(id_venda_afetada):
            continue

        itens_originais_da_venda = df_itens_venda[
            df_itens_venda["id_venda"] == id_venda_afetada
        ]
        if itens_originais_da_venda.empty:
            continue

        map_item_venda_para_qtd_original = itens_originais_da_venda.set_index(
            "id_item_venda"
        )["quantidade"].to_dict()

        ids_devolucoes_desta_venda = devolucoes_impactantes[
            devolucoes_impactantes["id_venda"] == id_venda_afetada
        ]["id_devolucao"].tolist()

        if not ids_devolucoes_desta_venda:
            continue

        itens_realmente_devolvidos_desta_venda = df_itens_devolucao[
            df_itens_devolucao["id_devolucao"].isin(ids_devolucoes_desta_venda)
        ]
        if itens_realmente_devolvidos_desta_venda.empty:
            continue

        total_qty_devolvida_por_item_original = (
            itens_realmente_devolvidos_desta_venda.groupby("id_item_venda")[
                "quantidade_devolvida"
            ].sum()
        )
        todos_os_itens_totalmente_devolvidos = True
        algum_item_parcialmente_ou_totalmente_devolvido = False

        for (
            id_item_venda_original,
            qtd_original,
        ) in map_item_venda_para_qtd_original.items():
            qtd_devolvida_deste_item = total_qty_devolvida_por_item_original.get(
                id_item_venda_original, 0
            )
            if qtd_devolvida_deste_item > 0:
                algum_item_parcialmente_ou_totalmente_devolvido = True
            if qtd_devolvida_deste_item < qtd_original:
                todos_os_itens_totalmente_devolvidos = False

        idx_venda_no_df = df_vendas["id_venda"] == id_venda_afetada

        if (
            todos_os_itens_totalmente_devolvidos
            and algum_item_parcialmente_ou_totalmente_devolvido
        ):
            df_vendas.loc[idx_venda_no_df, "status_venda"] = "devolvida totalmente"
        elif algum_item_parcialmente_ou_totalmente_devolvido:
            df_vendas.loc[idx_venda_no_df, "status_venda"] = "devolvida parcialmente"

    logging.info("Status das vendas atualizados.")
    return df_vendas


# --- Fluxo Principal de Geração ---
if __name__ == "__main__":
    if not os.path.exists(DATA_OUTPUT_DIR):
        os.makedirs(DATA_OUTPUT_DIR)
        logging.info(f"Diretório '{DATA_OUTPUT_DIR}' criado.")

    df_produtos = gerar_produtos()

    logging.info("Criando IDs de clientes placeholder para geração de vendas...")
    num_ids_placeholder = N_CLIENTES_TARGET * 2
    ids_clientes_placeholder = [
        str(fake.unique.uuid4()) for _ in range(num_ids_placeholder)
    ]
    df_clientes_placeholder = pd.DataFrame(
        {
            "id_cliente": ids_clientes_placeholder,
            "data_cadastro": pd.to_datetime(INICIO_ANO_2025),
        }
    )

    df_total_vendas, df_total_itens_venda = gerar_vendas_e_itens(
        df_clientes_placeholder,
        df_produtos,
        N_VENDAS_A_GERAR,
        HOJE_DEFINIDO,
        INICIO_ANO_2025,
    )

    df_clientes = gerar_clientes_desde_vendas(df_total_vendas, N_CLIENTES_TARGET)

    if df_clientes.empty:
        logging.error(
            "Nenhum cliente foi gerado. Encerrando o script, pois não há como prosseguir."
        )
        exit()

    logging.info("Filtrando vendas e itens para os clientes finais...")
    df_vendas_finais = df_total_vendas[
        df_total_vendas["id_cliente"].isin(df_clientes["id_cliente"])
    ].copy()

    df_vendas_finais = df_vendas_finais.merge(
        df_clientes[["id_cliente", "data_cadastro"]],
        on="id_cliente",
        suffixes=(
            "_original_venda",
            "_cliente",
        ),
    )

    coluna_data_cadastro_do_cliente_no_merge = "data_cadastro"

    df_vendas_finais = df_vendas_finais[
        df_vendas_finais["data_venda"]
        >= df_vendas_finais[coluna_data_cadastro_do_cliente_no_merge]
    ]
    df_vendas_finais.drop(
        columns=[coluna_data_cadastro_do_cliente_no_merge], inplace=True
    )

    df_itens_venda_finais = df_total_itens_venda[
        df_total_itens_venda["id_venda"].isin(df_vendas_finais["id_venda"])
    ].copy()

    logging.info(
        f"Número de vendas finais após filtro de clientes e sanity check: {len(df_vendas_finais)}"
    )
    logging.info(
        f"Número de itens de venda finais após filtro: {len(df_itens_venda_finais)}"
    )

    df_devolucoes, df_itens_devolucao = gerar_devolucoes_e_itens(
        df_vendas_finais,
        df_itens_venda_finais,
        FRACAO_DEVOLUCAO,
        HOJE_DEFINIDO,
        INICIO_ANO_2025,
    )

    df_vendas_finais = atualizar_status_venda_pos_devolucao(
        df_vendas_finais, df_devolucoes, df_itens_venda_finais, df_itens_devolucao
    )

    if not df_clientes.empty and not df_vendas_finais.empty:
        df_clientes = atualizar_clientes_com_metricas_venda(
            df_clientes, df_vendas_finais, df_itens_venda_finais
        )
    else:
        logging.warning(
            "Não foi possível atualizar métricas dos clientes pois não há clientes ou vendas finais."
        )
        if "numero_compras" not in df_clientes.columns:
            df_clientes["numero_compras"] = 0
        if "total_gasto" not in df_clientes.columns:
            df_clientes["total_gasto"] = 0.0

    logging.info(f"Total de clientes finais: {len(df_clientes)}")
    if not df_clientes.empty:
        logging.info(
            f"Clientes sem compras (considerando status da venda): {len(df_clientes[df_clientes['numero_compras'] == 0])}"
        )
    if not df_vendas_finais.empty:
        logging.info(
            f"Distribuição de status das vendas:\n{df_vendas_finais['status_venda'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'}"
        )
    else:
        logging.info("Nenhuma venda final para exibir status.")

    if not df_devolucoes.empty:
        logging.info(
            f"Distribuição de status das devoluções:\n{df_devolucoes['status_devolucao'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'}"
        )
    else:
        logging.info("Nenhuma devolução foi gerada ou processada.")

    date_format_csv = "%d/%m/%Y"

    df_clientes_csv = df_clientes.copy()
    if "data_cadastro" in df_clientes_csv.columns and not df_clientes_csv.empty:
        df_clientes_csv["data_cadastro"] = pd.to_datetime(
            df_clientes_csv["data_cadastro"]
        ).dt.strftime(date_format_csv)

    df_vendas_csv = df_vendas_finais.copy()
    if "data_venda" in df_vendas_csv.columns and not df_vendas_csv.empty:
        df_vendas_csv["data_venda"] = pd.to_datetime(
            df_vendas_csv["data_venda"]
        ).dt.strftime(date_format_csv)

    df_devolucoes_csv = df_devolucoes.copy()
    if not df_devolucoes_csv.empty and "data_devolucao" in df_devolucoes_csv.columns:
        df_devolucoes_csv["data_devolucao"] = pd.to_datetime(
            df_devolucoes_csv["data_devolucao"]
        ).dt.strftime(date_format_csv)

    try:
        if not df_clientes_csv.empty:
            df_clientes_csv.to_csv(
                os.path.join(DATA_OUTPUT_DIR, "clientes.csv"),
                sep=";",
                index=False,
                encoding="utf-8-sig",
            )
        if not df_produtos.empty:
            df_produtos.to_csv(
                os.path.join(DATA_OUTPUT_DIR, "produtos.csv"),
                sep=";",
                index=False,
                encoding="utf-8-sig",
            )
        if not df_vendas_csv.empty:
            df_vendas_csv.to_csv(
                os.path.join(DATA_OUTPUT_DIR, "vendas.csv"),
                sep=";",
                index=False,
                encoding="utf-8-sig",
            )
        if not df_itens_venda_finais.empty:
            df_itens_venda_finais.to_csv(
                os.path.join(DATA_OUTPUT_DIR, "itens_venda.csv"),
                sep=";",
                index=False,
                encoding="utf-8-sig",
            )
        if not df_devolucoes_csv.empty:
            df_devolucoes_csv.to_csv(
                os.path.join(DATA_OUTPUT_DIR, "devolucoes.csv"),
                sep=";",
                index=False,
                encoding="utf-8-sig",
            )
        if not df_itens_devolucao.empty:
            df_itens_devolucao.to_csv(
                os.path.join(DATA_OUTPUT_DIR, "itens_devolucao.csv"),
                sep=";",
                index=False,
                encoding="utf-8-sig",
            )
        logging.info(f"Dados salvos com sucesso na pasta '{DATA_OUTPUT_DIR}'.")
    except Exception as e:
        logging.error(f"Erro ao salvar arquivos CSV: {e}")

    logging.info("Geração de dados concluída.")
