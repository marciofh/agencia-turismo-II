import psycopg2

class Cidade:
    def __init__(self, nome_cidade, estado, location_id, aero_code, aero_nome):
        self.nome_cidade = nome_cidade
        self.estado = estado
        self.location_id = location_id
        self.aero_code = aero_code
        self.aero_nome = aero_nome
    
    def criaCidade(_dict):
        return Cidade(_dict['nome_cidade'], _dict['estado'], _dict['location_id'], _dict['aero_code'], _dict['aero_nome'])
    
#     def cadastraCidade(cidade):
#         string_sql = 'INSERT INTO northwind.products (nome_cidade, estado, location_id, aero_code, aero_nome) '\
#                      'VALUES (%s, %s, %s, %s, %s)'
#         record_to_insert = (cidade.nome_cidade, cidade.estado, cidade.location_id, cidade.aero_code, cidade.aero_nome)
#         # conn_string = "host='localhost' dbname='Northwind' user='postgres' password='root'"
        
#         # iniciar a inserção do registro
#         conn = None
#         try:
#             # abrir a conexão
#             conexao = psycopg2.connect(conn_string)
#             # abrir a sessão - a transação começa aqui
#             sessao = conexao.cursor()
#             # Executar a inserção na memória RAM
#             sessao.execute(string_sql, record_to_insert)
#             # Comitar a inserção - fechar a transação
#             conexao.commit()
#             # Encerrar a sessão
#             sessao.close()
#         except psycopg2.Error:
#             print("error")
#         finally:
#             if conn is not None:
#                 print("O registro foi inserido com sucesso")
#                 conn.close()
    
#     def consultaCidade(nome_cidade):
#         string_sql = 'SELECT * FROM northwind.products WHERE nome_cidade = %s;'
#         # conn_string = "host='localhost' dbname='Northwind' user='postgres' password='root'"
        
#         # iniciar a inserção do registro
#         conn = None
#         try:
#             # abrir a conexão
#             conexao = psycopg2.connect(conn_string)
#             # abrir a sessão - a transação começa aqui
#             sessao = conexao.cursor()
#             # Executar a consulta
#             sessao.execute(string_sql, nome_cidade)
#             #Armazenar os resultados
#             registros = sessao.fetchall()
#             # Comitar para fechar a transação
#             conexao.commit()
#             # Encerrar a sessão
#             sessao.close()
#         except psycopg2.Error:
#             print("error")

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

class Pacote:
    def __init__(self):
        pass
    
    def criaPacote(_dict):
        pass
