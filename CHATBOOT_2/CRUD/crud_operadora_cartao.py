import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "operadora_cartoes.db")

def conectar():
    """Conecta ao banco de dados e garante que a tabela exista."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS clientes(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL,
        numero_cartao TEXT NOT NULL,
        limite_total REAL NOT NULL,
        limite_disponivel REAL NOT NULL,
        fatura_atual REAL NOT NULL,
        vencimento_cartao TEXT NOT NULL, 
        vencimento_fatura TEXT NOT NULL,
        status_cartao TEXT NOT NULL)
    """)
    conn.commit()
    return conn

def incluir_cliente():
    print("\n--- Incluir Novo Cliente ---")
    nome = input("Nome: ")
    cpf = input("CPF: ")
    cartao = input("Número do Cartão: ")
    limite_total = float(input("Limite Total: "))
    limite_disp = float(input("Limite Disponível: "))
    fatura = float(input("Fatura Atual: "))
    venc_cartao = input("Vencimento do Cartão (MM/AA): ")
    venc_fatura = input("Dia de Vencimento da Fatura: ")
    status = input("Status do Cartão (Ativo/Bloqueado): ")

    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO clientes (nome, cpf, numero_cartao, limite_total, limite_disponivel, fatura_atual, vencimento_cartao, vencimento_fatura, status_cartao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nome, cpf, cartao, limite_total, limite_disp, fatura, venc_cartao, venc_fatura, status))
        conn.commit()
        print(f"✅ Cliente {nome} cadastrado e salvo com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inserir: {e}")
    finally:
        conn.close()

def consultar_cliente():
    print("\n--- Consultar Cliente ---")
    cpf = input("Digite o CPF para busca: ")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE cpf = ?", (cpf,))
    cliente = cursor.fetchone()
    conn.close()

    if cliente:
        print("\n" + "="*35)
        print(f"ID: {cliente[0]}")
        print(f"Nome: {cliente[1]}")
        print(f"CPF: {cliente[2]}")
        print(f"Cartão: {cliente[3]}")
        print(f"Limite Total: R$ {cliente[4]:.2f}")
        print(f"Limite Disponível: R$ {cliente[5]:.2f}")
        print(f"Fatura Atual: R$ {cliente[6]:.2f}")
        print(f"Vencimento Cartão: {cliente[7]}")
        print(f"Vencimento Fatura (Dia): {cliente[8]}")
        print(f"Status: {cliente[9]}")
        print("="*35)
    else:
        print("❌ Cliente não encontrado no banco de dados.")

def alterar_cliente():
    print("\n--- Alterar Cliente ---")
    cpf = input("Digite o CPF do cliente que deseja alterar: ")
    
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM clientes WHERE cpf = ?", (cpf,))
    cliente = cursor.fetchone()
    
    if not cliente:
        print("❌ Cliente não encontrado.")
        conn.close()
        return

    while True:
        print(f"\nAlterando dados de: {cliente[1]}")
        print("1 - Nome | 2 - Cartão | 3 - Lmt Total | 4 - Lmt Disponível")
        print("5 - Fatura | 6 - Venc Cartão | 7 - Venc Fatura | 8 - Status")
        print("0 - Sair da alteração")
        
        campo_op = input("\nQual campo deseja alterar? ")
        
        campos = {
            '1': 'nome', '2': 'numero_cartao', '3': 'limite_total',
            '4': 'limite_disponivel', '5': 'fatura_atual', 
            '6': 'vencimento_cartao', '7': 'vencimento_fatura', 
            '8': 'status_cartao'
        }

        if campo_op == '0':
            break
        
        if campo_op in campos:
            coluna = campos[campo_op]
            novo_valor = input(f"Digite o novo valor para {coluna.replace('_', ' ')}: ")
            
            try:
                cursor.execute(f"UPDATE clientes SET {coluna} = ? WHERE cpf = ?", (novo_valor, cpf))
                conn.commit()
                print(f"✅ {coluna.capitalize()} atualizado com sucesso!")
            except Exception as e:
                print(f"❌ Erro na atualização: {e}")
            
            continuar = input("\nDeseja alterar mais alguma coisa? (s/n): ").lower()
            if continuar != 's':
                break
        else:
            print("Opção inválida!")

    conn.close()

def deletar_cliente():
    print("\n--- Deletar Cliente ---")
    cpf = input("Digite o CPF do cliente que deseja excluir: ")
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE cpf = ?", (cpf,))
    if cursor.rowcount > 0:
        conn.commit()
        print("⚠️ Registro removido permanentemente do banco.")
    else:
        print("❌ Nenhum cliente encontrado com este CPF.")
    conn.close()

def menu_principal():
    while True:
        print("\n" + "="*35)
        print("      MENU ADMIN OPERADORA")
        print("="*35)
        print("1 - Incluir cliente")
        print("2 - Alterar cliente")
        print("3 - Consultar cliente")
        print("4 - Deletar cliente")
        print("0 - Sair")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            incluir_cliente()
        elif opcao == '2':
            alterar_cliente()
        elif opcao == '3':
            consultar_cliente()
        elif opcao == '4':
            deletar_cliente()
        elif opcao == '0':
            print("Saindo do painel administrativo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_principal()