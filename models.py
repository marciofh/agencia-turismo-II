import psycopg2
from credentials import keys

HOST = keys.get('HOST')
DBNAME = keys.get('DBNAME')
USER = keys.get('USER')
PASSWORD = keys.get('PASSWORD')

class BD: #ARRUMAR ESSA CLASSE ##############################
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

        try:
            conexao = psycopg2.connect(conn_string) # abrir a conexão
            sessao = conexao.cursor()
            sessao.execute(string_sql, dados)  # executando inserção
            print("Cidade cadastrada com sucesso!")
        except psycopg2.Error:
            print("error")
        finally:
            conexao.commit()
            sessao.close() # encerrando a sessão
    
    def consultaCidade(nome_cidade):
        string_sql = "SELECT * FROM turismo_schema.cidade WHERE nome_cidade = '{0}';"
        conn_string = "host='localhost' dbname='turismo' user='postgres' password='senha'"

        try:
            conexao = psycopg2.connect(conn_string) # abrir a conexão
            sessao = conexao.cursor()
            sessao.execute(string_sql .format(nome_cidade))  # executando inserção
            res = sessao.fetchone()
            if res != None:
                _dict = {
                "location_id": res[0],
                "nome_cidade": res[1],
                "estado": res[2],
                "aero_code": res[3],
                "aero_nome": res[4]
                }
            else:
                _dict = None
        except psycopg2.Error:
            print("error")
        finally:
            conexao.commit()
            sessao.close() # encerrando a sessão
            
            return _dict
            
class Passagem:
    def __init__(self, origem_id, destino_id, preco, duracao, qtde_conn, empresa, data_partida, data_chegada):
        self.origem_id = origem_id
        self.destino_id = destino_id
        self.preco = preco
        self.duracao = duracao
        self.qtde_conn = qtde_conn
        self.empresa = empresa
        self.data_partida = data_partida
        self.data_chegada = data_chegada
    
    def criaPassagem(_dict, origem_id, destino_id):
        return Passagem(origem_id, destino_id, _dict['preco'], _dict['duracao'], _dict['qtde_conn'], _dict['empresa'], _dict['data_partida'], _dict['data_chegada'])
    
    def cadastraPassagens(passagens):
        for passagem in passagens:
            string_sql = 'INSERT INTO turismo_schema.passagem (origem_id,destino_id,preco,duracao,qtde_conn,empresa,data_partida,data_chegada) '\
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            dados = (passagem.origem_id, passagem.destino_id, passagem.preco, passagem.duracao, passagem.qtde_conn, passagem.empresa, passagem.data_partida, passagem.data_chegada)
            conn_string = "host='localhost' dbname='turismo' user='postgres' password='senha'"

            try:
                conexao = psycopg2.connect(conn_string) # abrir a conexão
                sessao = conexao.cursor()
                sessao.execute(string_sql, dados)  # executando inserção
                print("Passagem cadastrada com sucesso!")
            except psycopg2.Error:
                print("error")     
            finally:
                conexao.commit()
                sessao.close() # encerrando a sessão       
    
    def consultaPassagem(origem_id, destino_id, data_partida):
        string_sql = "SELECT * FROM turismo_schema.passagem "\
            "WHERE origem_id = '{0}' AND destino_id = '{1}' AND date(data_partida) = '{2}';"
        conn_string = "host='localhost' dbname='turismo' user='postgres' password='senha'"

        try:
            conexao = psycopg2.connect(conn_string) # abrir a conexão
            sessao = conexao.cursor()
            sessao.execute(string_sql .format(origem_id, destino_id, data_partida)) # executando consulta
            res = sessao.fetchall()
            if len(res) != 0:
                lista_passagem = []
                for i in res:
                    voo = {
                        "preco": i[3],
                        "duracao": i[4],
                        "qtde_conn": i[5],
                        "empresa": i[6],
                        "data_partida": i[7],
                        "data_chegada": i[8]
                    }
                    lista_passagem.append(voo)
                    print(voo)
            else:
                lista_passagem = None
        except psycopg2.Error:
            print("error")
        finally:
            conexao.commit()
            sessao.close() # encerrando a sessão
            
            return lista_passagem
    
    def passagemSelecionada(passagem):
        string_sql = "SELECT passagem_id FROM turismo_schema.passagem "\
            "WHERE preco = '{0}' AND duracao = '{1}' AND qtde_conn = {2} AND empresa = '{3}' AND data_partida = '{4}' AND data_chegada = '{5}';"
        conn_string = "host='localhost' dbname='turismo' user='postgres' password='senha'"

        try:
            conexao = psycopg2.connect(conn_string) # abrir a conexão
            sessao = conexao.cursor()
            sessao.execute(string_sql .format(passagem['preco'], passagem['duracao'], passagem['qtde_conn'], passagem['empresa'], passagem['data_partida'], passagem['data_chegada']))  # executando inserção
            res = sessao.fetchall()
        except psycopg2.Error:
            res = "error"
            print(res)
        finally:
            conexao.commit()
            sessao.close() # encerrando a sessão
            return res
                
class Hospedagem:
    def __init__(self, nome_hotel, preco, foto, avaliacao, estrelas, endereco, cidade_id):
        self.nome_hotel = nome_hotel
        self.preco = preco
        self.foto = foto
        self.avaliacao = avaliacao
        self.estrelas = estrelas
        self.endereco = endereco
        self.cidade_id = cidade_id
    
    def criaHospedagem(_dict):
        return Hospedagem(_dict['nome_hotel'], _dict['preco'], _dict['foto'], _dict['avaliacao'], _dict['estrelas'], _dict['endereco'], _dict['cidade_id'])
    
    def cadastraHospedagens(hospedagens):
        for hospedagem in hospedagens:
            string_sql = 'INSERT INTO turismo_schema.hospedagem (nome_hotel, preco, foto, avaliacao, estrelas, endereco, cidade_id) '\
                'VALUES (%s, %s, %s, %s, %s, %s, %s)'
            dados = (hospedagem.nome_hotel, hospedagem.preco, hospedagem.foto, hospedagem.avaliacao, hospedagem.estrelas, hospedagem.endereco, hospedagem.cidade_id)
            conn_string = "host='localhost' dbname='turismo' user='postgres' password='senha'"
        
            try:
                conexao = psycopg2.connect(conn_string) # abrir a conexão
                sessao = conexao.cursor()
                sessao.execute(string_sql, dados)  # executando inserção
                print("Hospedagem cadastrada com sucesso!")
            except psycopg2.Error:
                print("error")
            finally:
                conexao.commit()
                sessao.close() # encerrando a sessão
    
    def consultaHospedagem(cidade_id):
        string_sql = "SELECT * FROM turismo_schema.hospedagem " \
            "WHERE cidade_id = '{0}';"
        conn_string = "host='localhost' dbname='turismo' user='postgres' password='senha'"
        try:
            conexao = psycopg2.connect(conn_string) # abrir a conexão
            sessao = conexao.cursor()
            sessao.execute(string_sql .format(cidade_id))  # executando consulta
            res = sessao.fetchall()
            if len(res) != 0:
                lista_hospedagem = []
                for i in res:
                    hotel = {
                        "nome_hotel": i[2],
                        "preco" : i[3],
                        "foto": i[4],
                        "avaliacao": i[5],
                        "estrelas": i[6],
                        "endereco": i[7]
                    }
                    lista_hospedagem.append(hotel)
                    print(hotel)
            else:
                lista_hospedagem = None
        except psycopg2.Error:
            print("error")
        finally:
            conexao.commit()
            sessao.close() # encerrando a sessão
            return lista_hospedagem 
    
    def hospedagemSelecionada(hospedagem):
        string_sql = "SELECT hospedagem_id FROM turismo_schema.hospedagem "\
            "WHERE nome_hotel = '{0}';"
        conn_string = "host='localhost' dbname='turismo' user='postgres' password='senha'"

        try:
            conexao = psycopg2.connect(conn_string) # abrir a conexão
            sessao = conexao.cursor()
            sessao.execute(string_sql .format(hospedagem['nome_hotel']))  # executando consulta
            res = sessao.fetchall()
        except psycopg2.Error:
            res = "error"
            print(res)
        finally:
            conexao.commit()
            sessao.close() # encerrando a sessão
            return res
                
class Atracao:
    def __init__(self, nome_atracao, foto, categoria, endereco, views, avaliacao, cidade_id):
        self.nome_atracao = nome_atracao
        self.foto = foto
        self.categoria = categoria
        self.endereco = endereco
        self.views = views
        self.avaliacao = avaliacao
        self.cidade_id = cidade_id
    
    def criaAtracao(_dict):
        return Atracao(_dict['nome_atracao'], _dict['foto'], _dict['categoria'], _dict['endereco'], _dict['views'], _dict['avaliacao'], _dict['cidade_id'])
    
    def cadastraAtracoes(atracoes):
        for atracao in atracoes:
            string_sql = 'INSERT INTO turismo_schema.atracao (nome_atracao,foto,categoria,endereco,n_views,avaliacao,cidade_id) '\
                'VALUES (%s, %s, %s, %s, %s, %s, %s)'
            dados = (atracao.nome_atracao, atracao.foto, atracao.categoria, atracao.endereco, atracao.views, atracao.avaliacao, atracao.cidade_id)
            conn_string = "host='localhost' dbname='turismo' user='postgres' password='senha'"

            try:
                conexao = psycopg2.connect(conn_string) # abrir a conexão
                sessao = conexao.cursor()
                sessao.execute(string_sql, dados)  # executando inserção
                print("Atração cadastrada com sucesso!")        
            except psycopg2.Error:
                print("error")
            finally:
                conexao.commit()
                sessao.close() # encerrando a sessão
    
    def consultaAtracao(cidade_id):
        string_sql = "SELECT * FROM turismo_schema.atracao "\
            "WHERE cidade_id = '{0}';"
        conn_string = "host='localhost' dbname='turismo' user='postgres' password='senha'"
        try:
            conexao = psycopg2.connect(conn_string) # abrir a conexão
            sessao = conexao.cursor()
            sessao.execute(string_sql .format(cidade_id))  # executando consulta
            res = sessao.fetchall()
            if len(res) != 0:
                lista_atracao = []
                for i in res:
                    atracao = {
                        "nome_atracao": i[2],
                        "foto": i[3],
                        "categoria": i[4],
                        "endereco": i[5],
                        "views": i[6],
                        "avaliacao": i[7]
                    }
                    lista_atracao.append(atracao)
                    print(atracao)
            else:
                lista_atracao = None
        except psycopg2.Error:
            print("error")
        finally:
            conexao.commit()
            sessao.close()
            return lista_atracao

class Pacote:
    def __init__(self, passagem_id_ida, passagem_id_volta, hospedagem_id, valor_total, qtde_passageiro):
        self.passagem_id_ida = passagem_id_ida
        self.passagem_id_volta = passagem_id_volta
        self.hospedagem_id = hospedagem_id
        self.valor_total = valor_total
        self.qtde_passageiro = qtde_passageiro
    
    def criaPacote(passagem_ida, passagem_volta, hospedagem_id, valor_pacote, passageiros):
        return Pacote(passagem_ida, passagem_volta, hospedagem_id, valor_pacote, passageiros)
    
    def cadastraPacote(pacote):
        string_sql = 'INSERT INTO turismo_schema.pacote (passagem_id_ida,passagem_id_volta,hospedagem_id,valor_total,qtde_passageiro) '\
            'VALUES (%s, %s, %s, %s, %s)'
        dados = (pacote.passagem_id_ida, pacote.passagem_id_volta, pacote.hospedagem_id, pacote.valor_total, pacote.qtde_passageiro)
        conn_string = "host='localhost' dbname='turismo' user='postgres' password='senha'"

        try:
            conexao = psycopg2.connect(conn_string) # abrir a conexão
            sessao = conexao.cursor()
            sessao.execute(string_sql, dados)  # executando inserção
            print("Pacote cadastrado com sucesso!")
        except psycopg2.Error:
            print("error")
        finally:
            conexao.commit()
            sessao.close() # encerrando a sessão