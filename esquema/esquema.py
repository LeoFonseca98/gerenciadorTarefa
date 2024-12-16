import datetime
from peewee import *

db = PostgresqlDatabase('td_db', port=5432, user='postgres', password='152538')


class BaseModel(Model):
   class Meta:
      database = db


class Usuario(BaseModel):
   id = CharField(primary_key=True)
   nome = CharField(max_length=255, null=False)
   email = CharField(max_length=255, null=False, unique=True)
   senha = CharField(max_length=255, null=False)


class Conta(BaseModel):
   id = CharField(primary_key=True)
   usuario_id = ForeignKeyField(Usuario, on_delete='CASCADE')
   data_criacao = DateTimeField(default=datetime.datetime.now)

   
class Tarefa(BaseModel):
   id = CharField(primary_key=True)
   conta_id = ForeignKeyField(Conta, on_delete='CASCADE')
   descricao = CharField(max_length=255, null=False)
   status = CharField(max_length=255, null=False)
   data_limite = DateTimeField(default=datetime.datetime.now)
   
db.connect()
db.create_tables([Usuario, Conta, Tarefa])
db.close()
print("Tabelas criadas com sucesso!")