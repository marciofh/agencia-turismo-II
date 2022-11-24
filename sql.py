import psycopg2
import datetime

hospedagem = {'preco': 1494.19, 'duracao': datetime.time(1, 2, 25), 'qtde_conn': 2, 'nome_hotel': 'Novotel Rio De Janeiro Parque Olímpico', 'data_partida': datetime.datetime(2022, 11, 25, 5, 30), 'data_chegada': datetime.datetime(2022, 11, 26, 6, 55)}

string_sql = "SELECT hospedagem_id FROM turismo_schema.hospedagem "\
            "WHERE nome_hotel = '{0}';"
conn_string = "host='localhost' dbname='turismo' user='postgres' password='senha'"
conn = None

try:
    conexao = psycopg2.connect(conn_string) # abrir a conexão
    sessao = conexao.cursor()
    sessao.execute(string_sql .format(hospedagem['nome_hotel']))  # executando inserção
    res = sessao.fetchall()
except psycopg2.Error:
    print("error")
finally:
    conexao.commit()
    sessao.close() # encerrando a sessão
    print(res)


# CREATE SCHEMA turismo_schema;

# DROP TABLE turismo_schema.cidade;
# DROP TABLE turismo_schema.passagem;
# DROP TABLE turismo_schema.hospedagem;
# DROP TABLE turismo_schema.atracao;
# DROP TABLE turismo_schema.pacote;

# select * from turismo_schema.cidade;
# select * from turismo_schema.passagem;
# select * from turismo_schema.hospedagem;
# select * from turismo_schema.atracao;
# select * from turismo_schema.pacote;

# --PASSAGEM
# select origem.nome_cidade as origem, origem.estado, destino.nome_cidade as destino, destino.estado, passagem.preco, passagem.duracao, passagem.qtde_conn, passagem.empresa, passagem.data_partida, passagem.data_chegada
# from turismo_schema.passagem join turismo_schema.cidade as origem
# on passagem.origem_id = origem.location_id
# join turismo_schema.cidade as destino
# on passagem.destino_id = destino.location_id;

# --HOSPEDAGEM
# select cidade.nome_cidade, cidade.estado, hospedagem.nome_hotel, hospedagem.preco, hospedagem.avaliacao, hospedagem.estrelas
# from turismo_schema.hospedagem join turismo_schema.cidade
# on hospedagem.cidade_id = cidade.location_id;

# --ATRACA0
# select cidade.nome_cidade, cidade.estado, atracao.nome_atracao, atracao.categoria, atracao.n_views, atracao.avaliacao
# from turismo_schema.atracao join turismo_schema.cidade
# on atracao.cidade_id = cidade.location_id;

# --PACOTE

# CREATE TABLE turismo_schema.cidade(
# 	location_id integer NOT NULL ,
# 	nome_cidade character varying (50) COLLATE pg_catalog."default" NOT NULL UNIQUE,
# 	estado character varying (2) COLLATE pg_catalog."default" NOT NULL ,
# 	aero_code character varying (3) COLLATE pg_catalog."default" NOT NULL ,
# 	aero_nome character varying (50) COLLATE pg_catalog."default" NOT NULL ,
# 	PRIMARY KEY (location_id)
# );

# CREATE TABLE turismo_schema.passagem(
# 	passagem_id serial NOT NULL,
# 	origem_id integer NOT NULL,
# 	destino_id integer NOT NULL,
# 	preco real NOT NULL,
# 	duracao time without time zone NOT NULL,
# 	qtde_conn integer NOT NULL,
# 	empresa character varying (50) COLLATE pg_catalog."default" NOT NULL,
# 	data_partida timestamp without time zone NOT NULL,
# 	data_chegada timestamp without time zone NOT NULL,
# 	PRIMARY KEY (passagem_id),
# 	FOREIGN KEY (origem_id)
# 	REFERENCES turismo_schema.cidade (location_id),
# 	FOREIGN KEY (destino_id)
# 	REFERENCES turismo_schema.cidade (location_id)
# );

# CREATE TABLE turismo_schema.hospedagem(
# 	hospedagem_id serial NOT NULL,
# 	cidade_id integer NOT NULL,
# 	nome_hotel character varying (50) COLLATE pg_catalog."default" NOT NULL,
# 	preco real NOT NULL,
# 	foto character varying (300) COLLATE pg_catalog."default" NOT NULL,
# 	avaliacao real NOT NULL,
# 	estrelas real NOT NULL,
# 	endereco character varying (150) COLLATE pg_catalog."default" NOT NULL,
# 	PRIMARY KEY (hospedagem_id),
# 	FOREIGN KEY (cidade_id)
# 	REFERENCES turismo_schema.cidade (location_id)
# );

# CREATE TABLE turismo_schema.atracao(
# 	atracao_id serial NOT NULL,
# 	cidade_id integer NOT NULL,
# 	nome_atracao character varying (50) COLLATE pg_catalog."default" NOT NULL,
# 	foto character varying (300) COLLATE pg_catalog."default" NOT NULL,
# 	categoria character varying (50) COLLATE pg_catalog."default" NOT NULL,
# 	endereco character varying (150) COLLATE pg_catalog."default" NOT NULL,
# 	n_views integer NOT NULL,
# 	avaliacao real NOT NULL,	
# 	PRIMARY KEY (atracao_id),
# 	FOREIGN KEY (cidade_id)
# 	REFERENCES turismo_schema.cidade (location_id)
# );

# CREATE TABLE turismo_schema.pacote(
# 	pacote_id serial NOT NULL,
# 	passagem_id_ida integer NOT NULL,
# 	passagem_id_volta integer NOT NULL,
# 	hospedagem_id integer NOT NULL,
# 	valor_total real NOT NULL,	
# 	qtde_passageiro integer NOT NULL,
# 	PRIMARY KEY (pacote_id),
# 	FOREIGN KEY (passagem_id_ida)
# 	REFERENCES turismo_schema.passagem (passagem_id),
# 	FOREIGN KEY (passagem_id_volta)
# 	REFERENCES turismo_schema.passagem (passagem_id),
# 	FOREIGN KEY (hospedagem_id)
# 	REFERENCES turismo_schema.hospedagem (hospedagem_id)
# );