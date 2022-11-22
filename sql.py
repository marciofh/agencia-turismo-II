import psycopg2
import datetime

string_sql = 'INSERT INTO turismo_schema.atracao (nome_atracao,foto,categoria,endereco,n_views,avaliacao) '\
            'VALUES (%s, %s, %s, %s, %s, %s)'
dados = ('nome_atracao', 'foto', 'categoria', 'endereco', 0, 0)
conn_string = "host='localhost' dbname='turismo' user='postgres' password='senha'"
conn = None
conexao = psycopg2.connect(conn_string) # abrir a conexão
sessao = conexao.cursor()
sessao.execute(string_sql, dados)  # executando inserção
conexao.commit()
sessao.close() # 





# CREATE SCHEMA turismo_schema;

# DROP TABLE turismo_schema.cidade;

# CREATE TABLE turismo_schema.cidade(
# 	location_id integer NOT NULL ,
# 	nome_cidade character varying (50) COLLATE pg_catalog."default" NOT NULL UNIQUE,
# 	estado character varying (2) COLLATE pg_catalog."default" NOT NULL ,
# 	aero_code character varying (3) COLLATE pg_catalog."default" NOT NULL ,
# 	aero_nome character varying (50) COLLATE pg_catalog."default" NOT NULL ,
# 	PRIMARY KEY (location_id)
# );

# select * from turismo_schema.cidade;

# INSERT INTO turismo_schema.cidade (location_id, nome_cidade, estado, aero_code, aero_nome)
# VALUES (1, 'teste2', 'TT', 'TES', 'Aeroporto de teste');


# DROP TABLE turismo_schema.passagem;

# CREATE TABLE turismo_schema.passagem(
# 	passagem_id serial NOT NULL,
# 	origem character varying (50) COLLATE pg_catalog."default" NOT NULL,
# 	destino character varying (50) COLLATE pg_catalog."default" NOT NULL,
# 	aero_origem character varying (3) COLLATE pg_catalog."default" NOT NULL,
# 	aero_destino character varying (3) COLLATE pg_catalog."default" NOT NULL,
# 	preco real NOT NULL,
# 	duracao time without time zone NOT NULL,
# 	qtde_conn integer NOT NULL,
# 	empresa character varying (50) COLLATE pg_catalog."default" NOT NULL,
# 	data_partida timestamp without time zone NOT NULL,
# 	data_chegada timestamp without time zone NOT NULL,
# 	PRIMARY KEY (passagem_id)
# );

# select * from turismo_schema.passagem;


# DROP TABLE turismo_schema.hospedagem;

# CREATE TABLE turismo_schema.hospedagem(
# 	hospedagem_id serial NOT NULL,
# 	nome_hotel character varying (50) COLLATE pg_catalog."default" NOT NULL,
# 	preco real NOT NULL,
# 	foto character varying (300) COLLATE pg_catalog."default" NOT NULL,
# 	avaliacao real NOT NULL,
# 	estrelas real NOT NULL,
# 	endereco character varying (150) COLLATE pg_catalog."default" NOT NULL,
# 	PRIMARY KEY (hospedagem_id)
# );

# select * from turismo_schema.hospedagem;


# DROP TABLE turismo_schema.atracao;

# CREATE TABLE turismo_schema.atracao(
# 	atracao_id serial NOT NULL,
# 	nome_atracao character varying (50) COLLATE pg_catalog."default" NOT NULL,
# 	foto character varying (300) COLLATE pg_catalog."default" NOT NULL,
# 	categoria character varying (50) COLLATE pg_catalog."default" NOT NULL,
# 	endereco character varying (150) COLLATE pg_catalog."default" NOT NULL,
# 	n_views integer NOT NULL,
# 	avaliacao real NOT NULL,	
# 	PRIMARY KEY (atracao_id)
# );

# select * from turismo_schema.atracao;