CREATE TABLE IF NOT EXISTS produto (
nome_produto INTEGER PRIMARY KEY,
quantidade_produto NUMBER NOT NULL,
validade_produto DATE NOT NULL,
descricao_produto TEXT NOT NULL,
dropdown_produto TEXT NOT NULL,
composicao_produto TEXT NOT NULL,
img_produto TEXT NOT NULL
);