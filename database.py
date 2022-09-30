import psycopg2
from credentials import keys

HOST = keys.get('HOST')
DBNAME = keys.get('DBNAME')
USER = keys.get('USER')
PASSWORD = keys.get('PASSWORD')
SSLMODE = keys.get('SSLMODE')

class BD:
    def config(self):
        return "host={0} user={1} dbname={2} password={3} sslmode={4}".format(HOST, USER, DBNAME, PASSWORD, SSLMODE)

class Passagem:
    def __init__(self, origem, destino, hora_emb, hora_desemb, duracao, conexao, preco, data):
        self.origem = origem
        self.destino = destino
        self.hora_emb = hora_emb
        self.hora_desemb = hora_desemb
        self.duracao = duracao
        self.conexao = conexao
        self.preco = preco
        self.data = data
        
    def cadastraPassagem(self):
        conn = psycopg2.connect(BD.config(self))
        cursor = conn.cursor()
        cursor.execute("insert into turismo_schema.passagem_aerea(origem,destino,hora_emb,hora_desemb,duracao,conexao,preco,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);",(self.origem,self.destino,self.hora_emb,self.hora_desemb,self.duracao,self.conexao,self.preco,self.data))
        conn.commit()
        conn.close()
        return print("Passagem cadastrada com sucesso!")

    def consultaPassagem(self, origem, destino, data):
        conn = psycopg2.connect(BD.config(self))
        cursor = conn.cursor()
        cursor.execute("select * from turismo_schema.passagem_aerea where origem = %s and destino = %s and date = %s", (origem, destino, data))
        res = cursor.fetchall()
        conn.commit()
        conn.close()
        list_passagem = []
        for i in res:
            list_passagem.append({
                'origem' : i[0],
                'destino' : i[1],
                'hora_emb' : i[2],
                'hora_desemb' : i[3],
                'duracao' : i[4],
                'conexao' : i[5],
                'preco' : i[6],
                'data' : i[7]
            })

        return list_passagem

class Hotel:
    def __init__(self, nome, preco, foto, ranking_site, stars, url_site, endereco, data, id_cidade):
        self.nome = nome
        self.preco = preco
        self.foto = foto
        self.ranking_site = ranking_site
        self.stars = stars
        self.url_site = url_site
        self.endereco = endereco
        self.data = data
        self.id_cidade = id_cidade
        
    def cadastraHotel(self):
        conn = psycopg2.connect(BD.config(self))
        cursor = conn.cursor()
        cursor.execute("insert into turismo_schema.hotel(nome, endereco, id_cidade, foto, stars, ranking_site, url_site, preco, date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (self.nome, self.endereco, self.id_cidade, self.foto, self.stars, self.ranking_site, self.url_site, self.preco, self.data))
        conn.commit()
        conn.close()
        return print("Hotel cadastrado com sucesso!")

    def consultaHotel(self, cidade):
        conn = psycopg2.connect(BD.config(self))
        cursor = conn.cursor()
        cursor.execute("select * from turismo_schema.hotel where id_cidade = '{0}'" .format(cidade))
        res = cursor.fetchall()
        conn.commit()
        conn.close()
        list_hotel = []
        for i in res:
            list_hotel.append({
                'nome' : i[0],
                'endereco' : i[1],
                'foto' : i[2],
                'stars' : i[3],
                'ranking_site' : i[4],
                'url_site' : i[5],
                'preco' : i[6],
                'data' : i[7]
            })
        return list_hotel
        
class Cidade:
    def __init__(self, location_id, nome):
        self.location_id = location_id
        self.nome = nome
        
    def cadastraCidade(self):
        conn = psycopg2.connect(BD.config(self))
        cursor = conn.cursor()
        cursor.execute("INSERT INTO turismo_schema.cidade(location_id, nome) VALUES (%s,%s);", (self.location_id, self.nome))
        conn.commit()
        conn.close()
        return print("Cidade cadastrada com sucesso!")

    def consultaCidade(self, nome):
        conn = psycopg2.connect(BD.config(self))
        cursor = conn.cursor()
        cursor.execute("select * from turismo_schema.cidade where nome = '{0}'" .format(nome))
        res = cursor.fetchall()
        conn.commit()
        conn.close()
        return res