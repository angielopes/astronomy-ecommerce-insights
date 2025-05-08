CREATE TABLE `clientes` (
  `id_cliente` char(36) PRIMARY KEY,
  `nome_cliente` varchar(50),
  `email` varchar(50),
  `idade` integer,
  `regiao` varchar(5),
  `data_cadastro` date,
  `numero_compras` integer,
  `status` enum('ativo','inativo')
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
  `motivo_devolucao` enum('defeito','não gostei','erro na compra','não era o esperado'),
  `data_devolucao` date,
  `status_devolucao` enum('em andamento','finalizada')
);

CREATE TABLE `vendas` (
  `id_venda` char(36) PRIMARY KEY,
  `id_cliente` char(36),
  `id_produto` char(36),
  `quantidade` integer,
  `preco_total` decimal(10,2),
  `data_venda` date,
  `canal_venda` enum('site','loja física','marketplace'),
  `status_venda` enum('em processamento','erro','pendente')
);

ALTER TABLE `devolucoes` ADD FOREIGN KEY (`id_venda`) REFERENCES `vendas` (`id_venda`);

ALTER TABLE `vendas` ADD FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`);

ALTER TABLE `vendas` ADD FOREIGN KEY (`id_produto`) REFERENCES `produtos` (`id_produto`);
