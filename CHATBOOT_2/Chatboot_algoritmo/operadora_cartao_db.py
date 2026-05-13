
import sqlite3

conexao=sqlite3.connect('operadora_cartoes.db') # faz a conexão com o banco
cursor=conexao.cursor() # permite usar comandos sql
cursor.execute("""
  CREATE TABLE IF NOT EXISTS clientes(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL,
    numero_cartao TEXT NOT NULL,
    limite_total REAL NOT NULL,
    limite_disponivel REAL NOT  NULL,
    fatura_atual REAL NOT NULL,
    vencimento_cartao TEXT NOT NULL, 
    vencimento_fatura TEXT NOT NULL,
    status_cartao TEXT NOT NULL)
""")
conexao.commit() #salva o banco
conexao.close()  #fecha o banco