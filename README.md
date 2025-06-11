# CosmoLume E-commerce Analytics

Este repositório contém um projeto completo de geração, tratamento e análise de dados sintéticos de um e-commerce fictício especializado em produtos astronômicos. O objetivo principal é demonstrar habilidades técnicas em Python, SQL e Análise de Dados por meio de um portfólio autoral que simula problemas reais enfrentados por empresas de varejo digital.

## Objetivo Geral

Criar uma base sólida de dados sintéticos que represente um cenário realista de vendas, clientes, produtos e transações incluindo ruídos e inconsistências, propositalmente adicionados, para então aplicar técnicas de:

- Limpeza e padronização de dados
- Análise de dados com foco em negócios
- Resolução de problemas de qualidade de dados
- Extração de insights com perguntas simulando demandas de stakeholders
- Construção de um pequeno pipeline estilo ETL

## Estrutura do Projeto

### Geração de Dados
- **scripts/data_generation.py**: Script Python que gera dados sintéticos para o e-commerce, incluindo:
  - Clientes com dados demográficos e histórico de compras
  - Produtos organizados por categorias (Telescópios, Binóculos, Mapas Celestes, etc.)
  - Vendas com múltiplos itens e diferentes status
  - Devoluções com motivos variados e status de processamento
  - Exportação de todos os dados em arquivos CSV

### Modelagem de Dados
- **sql/create_schema.sql**: Definição do esquema relacional com 6 tabelas principais:
  - `clientes`: Dados dos clientes e métricas de compra
  - `produtos`: Catálogo de produtos por categoria
  - `vendas`: Registro de transações de venda
  - `itens_venda`: Itens individuais de cada venda
  - `devolucoes`: Registro de devoluções
  - `itens_devolucao`: Itens individuais devolvidos

### Ingestão de Dados
- **notebooks/ingestion.ipynb**: Notebook para ingestão dos dados CSV para um banco MySQL
- **config/ingestion.json**: Configuração das tabelas e caminhos dos arquivos para ingestão

### Análise de Dados
- **sql/views_customer_behavior.sql**: Views SQL para análise de comportamento do cliente
  - `vw_valor_itens_devolvidos_aprovados_por_venda`: Calcula valores devolvidos
  - `vw_valor_liquido_vendas`: Calcula valor líquido das vendas após devoluções
  - `vw_itens_devolvidos`: Identifica itens efetivamente devolvidos

- **sql/customer_behavior.sql**: Consultas para análise de comportamento do cliente
  - Top clientes por valor gasto
  - Frequência de compras
  - Ticket médio por cliente
  - Distribuição regional de vendas
  - Análise por faixa etária

- **sql/sales_performance.sql**: Consultas para análise de desempenho de vendas
  - Receita líquida por período
  - Produtos e categorias mais rentáveis
  - Métricas de desempenho mensal

### Documentação
- **docs/diagrams/**: Diagramas lógicos do banco de dados

## Conjunto de Dados

O projeto gera e trabalha com dados sintéticos que incluem:
- 3.000 clientes com perfis demográficos variados
- 50 produtos distribuídos em 5 categorias relacionadas à astronomia
- Aproximadamente 15.000 vendas com datas em 2025
- 5% das vendas com devoluções parciais ou totais
- Status variados para vendas e devoluções

## Tecnologias Utilizadas

- **Python**: Geração de dados sintéticos com Faker e Pandas
- **SQL**: Modelagem de dados, views e consultas analíticas
- **MySQL**: Banco de dados relacional
- **Jupyter Notebooks**: Ingestão e processamento de dados
- **SQLAlchemy**: ORM para conexão com o banco de dados

## Por que esse projeto?

Minha intenção é desenvolver um portfólio que vá além da simples visualização de dados, simulando as etapas enfrentadas por profissionais de dados no mundo real. Desde a construção dos dados, passando pela estruturação dos fluxos, até a apresentação final dos resultados. Tudo foi feito com o objetivo de demonstrar autonomia, raciocínio analítico e visão prática da área.

## Tema escolhido: Astronomia

O e-commerce fictício foi inspirado no meu interesse pessoal por astronomia e tecnologia. Os produtos vendidos vão de telescópios a itens decorativos e livros, criando um universo lúdico que torna o processo mais envolvente e único.

---

Este projeto está em construção contínua. Novas entradas, melhorias e visualizações estão sendo adicionadas.