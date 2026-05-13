import sqlite3
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# ========================================================
# 1. FUNÇÃO DE CONEXÃO E CONSULTA AO BANCO
# ========================================================
def consultar_banco(cpf, coluna):
    try:
        conn = sqlite3.connect('operadora_cartoes.db')
        cursor = conn.cursor()
        # Busca a coluna específica e o nome do cliente
        query = f"SELECT {coluna}, nome FROM clientes WHERE cpf = ?"
        cursor.execute(query, (cpf,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado 
    except Exception as e:
        return None

# ========================================================
# 2. CONFIGURAÇÃO DA IA (TREINAMENTO COM NOVAS CATEGORIAS)
# ========================================================
frases = [
    # FATURA (VALOR)
    'qual o valor da minha fatura', 'quanto eu devo', 'valor da fatura', 'fatura atual', 'fatura',
    
    # VENCIMENTO FATURA (DATA)
    'qual a data de vencimento da fatura', 'vencimento da fatura', 'quando vence a fatura', 'dia de vencimento', 'que dia vence',
    
    # LIMITE
    'qual meu limite', 'limite disponivel', 'quanto tenho de limite', 'meu limite', 'limite',
    
    # BLOQUEIO / STATUS (Foco em palavras restritivas)
    'bloquear meu cartao', 'quero bloquear', 'status do cartao', 'bloqueio', 'perdi o cartao', 'bloquear', 'cartao bloqueado',
    
    # PARCELAMENTO (Foco em palavras financeiras)
    'quero parcelar', 'parcelar fatura', 'parcelamento', 'dividir fatura', 'pagar parcelado', 'parcelas', 'parcelar',
    
    # SEGUNDA-VIA (Foco em substituição)
    'segunda-via', 'perdi meu cartao', 'pedir novo cartao', 'vencimento cartao', 'outro cartao', 'solicitar nova via', '2 via',
    
    ## SENHA / OUTROS
    'qual minha senha', 'esqueci a senha', 'ver senha', 'quero cancelar o cartao', 'cancelar', 'segunda-via', 'parcelar fatura'
]

categorias = [
    'fatura_valor', 'fatura_valor', 'fatura_valor', 'fatura_valor', 'fatura_valor',
    'fatura_vencimento', 'fatura_vencimento', 'fatura_vencimento', 'fatura_vencimento', 'fatura_vencimento',
    'limite', 'limite', 'limite', 'limite', 'limite',
    'bloqueio', 'bloqueio', 'bloqueio', 'bloqueio', 'bloqueio', 'bloqueio', 'bloqueio',
    'parcelar', 'parcelar', 'parcelar', 'parcelar', 'parcelar', 'parcelar', 'parcelar',
    'segunda-via', 'segunda-via', 'segunda-via', 'segunda-via', 'segunda-via', 'segunda-via', 'segunda-via',
    'senha', 'senha', 'senha', 'cancelar', 'cancelar', 'segunda-via', 'parcelar'
]

vetorizador = CountVectorizer()
x = vetorizador.fit_transform(frases)
modelo = MultinomialNB()
modelo.fit(x, categorias)

# Mapeamento: Categoria da IA -> Coluna exata no SQLite
mapeamento_db = {
    'fatura_valor': 'fatura_atual',
    'fatura_vencimento': 'vencimento_fatura',
    'limite': 'limite_disponivel',
    'segunda-via': 'vencimento_cartao',
    'bloqueio': 'status_cartao'
}

# ========================================================
# 3. INTERAÇÃO DO CHATBOT (ESTILO SIMPÁTICO)
# ========================================================
print('='*40)
print('      SISTEMA DE ATENDIMENTO - CARTÃO')
print('='*40)

cpf_sessao = ""

# Loop de Login Seguro
while True:
    entrada = input("Por favor, digite seu CPF (apenas números): ").strip()
    
    if "python.exe" in entrada or not entrada:
        continue
    
    if entrada.lower() == 'sair':
        print("\nChatbot: Atendimento encerrado. Tenha um excelente dia!")
        exit()

    dados_cliente = consultar_banco(entrada, "nome")
    
    if dados_cliente:
        cpf_sessao = entrada
        nome_usuario = dados_cliente[1]
        print(f"\n✅ Olá, {nome_usuario}! Login realizado com sucesso.")
        break
    else:
        print("❌ CPF não localizado. Verifique os números ou digite 'sair' para encerrar.")

print(f"\nComo posso te ajudar hoje, {nome_usuario}?")
print("(Ex: 'Qual meu limite?' ou 'Quando vence minha fatura?')")

# Loop de Perguntas e Respostas
while True:
    pergunta = input("\nVocê: ").strip().lower()

    if not pergunta or "python.exe" in pergunta:
        continue

    if pergunta == 'sair':
        print(f'Chatbot: Foi um prazer te ajudar, {nome_usuario}! Até logo!')
        break

    # IA identifica a intenção
    pergunta_vetorizada = vetorizador.transform([pergunta])
    categoria_prevista = modelo.predict(pergunta_vetorizada)[0]

    # Respostas baseadas no Banco de Dados
    if categoria_prevista in mapeamento_db:
        coluna_alvo = mapeamento_db[categoria_prevista]
        info_db = consultar_banco(cpf_sessao, coluna_alvo)

        if info_db:
            valor_real = info_db[0]
            
            if categoria_prevista == 'fatura_valor':
                print(f"Chatbot: O valor da sua fatura atual é R$ {valor_real:.2f}.")
            elif categoria_prevista == 'fatura_vencimento':
                print(f"Chatbot: O vencimento da sua fatura é no dia {valor_real}.")
            elif categoria_prevista == 'limite':
                print(f"Chatbot: Você possui R$ {valor_real:.2f} de limite disponível para compras.")
            elif categoria_prevista == 'bloqueio':
                print(f"Chatbot: O status atual do seu cartão é: {valor_real}. Se precisar bloquear por perda ou roubo, recomendo usar o botão 'Bloquear' no nosso App!")
            elif categoria_prevista == 'segunda-via':
                print(f"Chatbot: Seu cartão atual vence em {valor_real}. Solicite uma nova via através do nosso App!")
        else:
            print("Chatbot: Poxa, tive um probleminha ao buscar essa informação. Pode tentar novamente?")
    
    # Respostas para informações gerais (Dicionário fixo)
    else:
        respostas_gerais = {
            'parcelar': 'Você pode parcelar sua fatura em até 12x diretamente pelo nosso App, no menu "Cartões".',
            'senha': 'Por segurança, você pode visualizar sua senha no App através da validação biométrica.',
            'cancelar': 'Lamento que queira nos deixar! Para cancelamentos, por favor, entre em contato com nossa central no 0800 700 1234.',
        }
        print("Chatbot:", respostas_gerais.get(categoria_prevista, "Ainda estou aprendendo e não entendi muito bem. Pode reformular a pergunta?"))