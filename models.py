import psycopg2
from credentials import keys

HOST = keys.get('HOST')
DBNAME = keys.get('DBNAME')
USER = keys.get('USER')
PASSWORD = keys.get('PASSWORD')

class BD:
    def config(self):
        return "host={0} dbname={1} user={2} password={3}".format(HOST, DBNAME, USER, PASSWORD)

class Cidade:
    def __init__(self, nome_cidade, estado, location_id, aero_code, aero_nome):
        self.nome_cidade = nome_cidade
        self.estado = estado
        self.location_id = location_id
        self.aero_code = aero_code
        self.aero_nome = aero_nome
    
    def criaCidade(_dict):
        return Cidade(_dict['nome_cidade'], _dict['estado'], _dict['location_id'], _dict['aero_code'], _dict['aero_nome'])
    
    def cadastraCidade(cidade):
        string_sql = 'INSERT INTO turismo_schema.cidade (nome_cidade, estado, location_id, aero_code, aero_nome) '\
                     'VALUES (%s, %s, %s, %s, %s)'
        dados = (cidade.nome_cidade, cidade.estado, cidade.location_id, cidade.aero_code, cidade.aero_nome)
        conn_string = "host='localhost' dbname='turismo' user='postgres' password='senha'"
        conn = None

        try:
            conexao = psycopg2.connect(conn_string) # abrir a conexão
            sessao = conexao.cursor()
            sessao.execute(string_sql, dados)  # executando inserção
            conexao.commit()
            sessao.close() # encerrando a sessão
        except psycopg2.Error:
            print("error")
        finally:
            print("Cidade cadastrada com sucesso!")
            
    
    def consultaCidade(nome_cidade, self):
        string_sql = 'SELECT * FROM northwind.products WHERE nome_cidade = %s;'
        # conn_string = "host='localhost' dbname='Northwind' user='postgres' password='root'"
        conn = None

        try:
            conexao = psycopg2.connect(BD.config(self)) # abrir a conexão
            sessao = conexao.cursor()
            sessao.execute(string_sql, nome_cidade)
            registros = sessao.fetchall() #armazenando os resultados
            conexao.commit()
            sessao.close() # encerrando a sessão
        except psycopg2.Error:
            print("error")

class Passagem:
    def __init__(self, origem, destino, aero_origem, aero_destino, preco, duracao, qtde_conn, empresa, data_partida, data_chegada):
        self.origem = origem
        self.destino = destino
        self.aero_origem = aero_origem
        self.aero_destino = aero_destino
        self.preco = preco
        self.duracao = duracao
        self.qtde_conn = qtde_conn
        self.empresa = empresa
        self.data_partida = data_partida
        self.data_chegada = data_chegada
    
    def criaPassagem(_dict):
        return Passagem(_dict['origem'], _dict['destino'], _dict['aero_origem'],_dict['aero_destino'],_dict['preco'], _dict['duracao'],_dict['qtde_conn'], _dict['empresa'], _dict['data_partida'], _dict['data_chegada'])
    
    def cadastraPassagens(passagens):
        for passagem in passagens:
            string_sql = 'INSERT INTO turismo_schema.passagem (origem,destino,aero_origem,aero_destino,preco,duracao,qtde_conn,empresa,data_partida,data_chegada) '\
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            dados = (passagem.origem, passagem.destino, passagem.aero_origem, passagem.aero_destino, passagem.preco, passagem.duracao, passagem.qtde_conn, passagem.empresa, passagem.data_partida, passagem.data_chegada)
            conn_string = "host='localhost' dbname='turismo' user='postgres' password='senha'"
            conn = None

            try:
                conexao = psycopg2.connect(conn_string) # abrir a conexão
                sessao = conexao.cursor()
                sessao.execute(string_sql, dados)  # executando inserção
            except psycopg2.Error:
                print("error")
            finally:
                conexao.commit()
                sessao.close() # encerrando a sessão
                print("Passagem cadastrada com sucesso!")
                

class Hospedagem:
    def __init__(self, nome_hotel, preco, foto, avaliacao, estrelas, endereco):
        self.nome_hotel = nome_hotel
        self.preco = preco
        self.foto = foto
        self.avaliacao = avaliacao
        self.estrelas = estrelas
        self.endereco = endereco
    
    def criaHospedagem(_dict):
        return Hospedagem(_dict['nome_hotel'], _dict['preco'], _dict['foto'], _dict['avaliacao'], _dict['estrelas'], _dict['endereco'])
    
    def cadastraHospedagens(hospedagens):
        for hospedagem in hospedagens:
            string_sql = 'INSERT INTO turismo_schema.hospedagem (nome_hotel, preco, foto, avaliacao, estrelas, endereco) '\
                'VALUES (%s, %s, %s, %s, %s, %s)'
            dados = (hospedagem.nome_hotel, hospedagem.preco, hospedagem.foto, hospedagem.avaliacao, hospedagem.estrelas, hospedagem.endereco)
            conn_string = "host='localhost' dbname='turismo' user='postgres' password='senha'"
            conn = None
        
            try:
                conexao = psycopg2.connect(conn_string) # abrir a conexão
                sessao = conexao.cursor()
                sessao.execute(string_sql, dados)  # executando inserção
            except psycopg2.Error:
                print("error")
            finally:
                conexao.commit()
                sessao.close() # encerrando a sessão
                print("Hospedagem cadastrada com sucesso!")
                

class Atracao:
    def __init__(self, nome_atracao, foto, categoria, endereco, views, avaliacao):
        self.nome_atracao = nome_atracao
        self.foto = foto
        self.categoria = categoria
        self.endereco = endereco
        self.views = views
        self.avaliacao = avaliacao
    
    def criaAtracao(_dict):
        return Atracao(_dict['nome_atracao'], _dict['foto'], _dict['categoria'], _dict['endereco'], _dict['views'], _dict['avaliacao'])
    
    def cadastraAtracoes(atracoes):
        for atracao in atracoes:
            string_sql = 'INSERT INTO turismo_schema.atracao (nome_atracao,foto,categoria,endereco,n_views,avaliacao) '\
                'VALUES (%s, %s, %s, %s, %s, %s)'
            dados = (atracao.nome_atracao, atracao.foto, atracao.categoria, atracao.endereco, atracao.views, atracao.avaliacao)
            conn_string = "host='localhost' dbname='turismo' user='postgres' password='senha'"
            conn = None

            try:
                conexao = psycopg2.connect(conn_string) # abrir a conexão
                sessao = conexao.cursor()
                sessao.execute(string_sql, dados)  # executando inserção
            except psycopg2.Error:
                print("error")
            finally:
                conexao.commit()
                sessao.close() # encerrando a sessão
                print("Atração cadastrada com sucesso!")
                

class Pacote:
    def __init__(self):
        pass
    
    def criaPacote(_dict):
        pass