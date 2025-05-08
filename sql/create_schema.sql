CREATE TABLE `clientes` (
  `id_cliente` char(36) PRIMARY KEY,
  `nome_cliente` varchar(50),
  `email` varchar(50),
  `idade` integer,
  `regiao` varchar(20),
  `data_cadastro` date,
  `numero_compras` integer,
  `total_gasto` decimal(10,2)
);

CREATE TABLE `produtos` (
  `id_produto` char(36) PRIMARY KEY,
  `nome_produto` varchar(100),
  `categoria` varchar(30),
  `preco` decimal(10,2)
);

CREATE TABLE `devolucoes` (
  `id_devolucao` char(36) PRIMARY KEY,
  `id_venda` char(36),
  `motivo_geral_devolucao` varchar(50),
  `data_devolucao` date,
  `status_devolucao` varchar(30)
);

CREATE TABLE `vendas` (
  `id_venda` char(36) PRIMARY KEY,
  `id_cliente` char(36),
  `data_venda` date,
  `canal_venda` varchar(20),
  `status_venda` varchar(30),
  `total_venda` decimal(10,2)
);

CREATE TABLE `itens_venda` (
  `id_item_venda` char(36) PRIMARY KEY,
  `id_venda` char(36),
  `id_produto` char(36),
  `quantidade` integer,
  `preco_unitario` decimal(8,2),
  `preco_total_item` decimal(10,2)
);

CREATE TABLE `itens_devolucao` (
  `id_item_devolucao` char(36) PRIMARY KEY,
  `id_devolucao` char(36),
  `id_item_venda` char(36),
  `id_produto` char(36),
  `quantidade_devolvida` integer,
  `motivo_especifico_item` varchar(50)
);

ALTER TABLE `devolucoes` ADD FOREIGN KEY (`id_venda`) REFERENCES `vendas` (`id_venda`);

ALTER TABLE `vendas` ADD FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`);

ALTER TABLE `itens_venda` ADD FOREIGN KEY (`id_venda`) REFERENCES `vendas` (`id_venda`);

ALTER TABLE `itens_venda` ADD FOREIGN KEY (`id_produto`) REFERENCES `produtos` (`id_produto`);

ALTER TABLE `itens_devolucao` ADD FOREIGN KEY (`id_devolucao`) REFERENCES `devolucoes` (`id_devolucao`);

ALTER TABLE `itens_devolucao` ADD FOREIGN KEY (`id_item_venda`) REFERENCES `itens_venda` (`id_item_venda`);

ALTER TABLE `itens_devolucao` ADD FOREIGN KEY (`id_produto`) REFERENCES `produtos` (`id_produto`);
