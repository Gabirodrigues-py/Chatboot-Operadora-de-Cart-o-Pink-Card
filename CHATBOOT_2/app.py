from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

# ========================================================
# 1. CONFIGURAÇÃO DE CAMINHOS
# ========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "operadora_cartoes.db")

def consultar_banco(cpf, coluna):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query = f"SELECT {coluna}, nome FROM clientes WHERE cpf = ?"
        cursor.execute(query, (cpf,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado
    except Exception as e:
        print(f"Erro técnico ao acessar o banco: {e}")
        return None

# ========================================================
# 2. INTELIGÊNCIA ARTIFICIAL (TREINAMENTO)
# ========================================================
frases = [
    'qual o valor da minha fatura', 'quanto eu devo', 'fatura atual', 'fatura',
    'qual a data de vencimento da fatura', 'vencimento da fatura', 'quando vence',
    'qual meu limite', 'limite disponivel', 'meu limite', 'limite',
    'bloquear meu cartao', 'quero bloquear', 'status do cartao', 'bloqueio',
    'qual minha senha', 'ver senha', 'esqueci a senha',
    'cancelar cartao', 'quero cancelar', 'encerrar conta',
    'segunda-via', 'perdi o cartao', 'novo cartao', '2 via',
    'parcelar fatura', 'quero parcelar', 'parcelamento', 'dividir conta'
]

categorias = [
    'fatura_valor', 'fatura_valor', 'fatura_valor', 'fatura_valor',
    'fatura_vencimento', 'fatura_vencimento', 'fatura_vencimento',
    'limite', 'limite', 'limite', 'limite',
    'bloqueio', 'bloqueio', 'bloqueio', 'bloqueio',
    'senha', 'senha', 'senha',
    'cancelar', 'cancelar', 'cancelar',
    'segunda_via', 'segunda_via', 'segunda_via', 'segunda_via',
    'parcelar', 'parcelar', 'parcelar', 'parcelar'
]

vetorizador = CountVectorizer()
x = vetorizador.fit_transform(frases)
modelo = MultinomialNB()
modelo.fit(x, categorias)

# Mapeamento para colunas do banco SQL
mapeamento_db = {
    'fatura_valor': 'fatura_atual',
    'fatura_vencimento': 'vencimento_fatura',
    'limite': 'limite_disponivel',
    'bloqueio': 'status_cartao',
    'segunda_via': 'vencimento_cartao'
}

# ========================================================
# 3. ROTAS DO FLASK
# ========================================================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    dados = request.json
    cpf = dados.get('cpf', '').replace('.', '').replace('-', '').strip()
    pergunta = dados.get('pergunta', '').lower().strip()

    # Lógica de Encerramento
    if pergunta == 'sair':
        return jsonify({
            "encerrar": True,
            "resposta": "Atendimento encerrado pela Pink Card. Tenha um ótimo dia!"
        })

    # Validação de Cliente
    info_cliente = consultar_banco(cpf, "nome")
    if not info_cliente:
        return jsonify({"autenticado": False, "resposta": "CPF não localizado no sistema."})

    nome_usuario = info_cliente[1]

    if pergunta == "oi":
        return jsonify({
            "autenticado": True, 
            "resposta": f"✅ Login realizado! Olá {nome_usuario}, como posso ajudar você hoje? (Para encerrar, digite 'sair')."
        })

    # --- PROCESSAMENTO DA IA COM TRAVA DE SEGURANÇA ---
    vetor = vetorizador.transform([pergunta])
    categoria_prevista = modelo.predict(vetor)[0]
    
    # Obtém a probabilidade (certeza) do modelo
    probabilidades = modelo.predict_proba(vetor)[0]
    confianca = max(probabilidades)

    # Se a confiança for menor que 30%, ele não responde sobre finanças
    if confianca < 0.30:
        return jsonify({
            "autenticado": True, 
            "resposta": f"Desculpe {nome_usuario},não entendi sua dúvida. Pode reformular a pergunta?"
        })

    # RESPOSTAS DINÂMICAS (CONSULTA AO BANCO)
    if categoria_prevista in mapeamento_db:
        coluna = mapeamento_db[categoria_prevista]
        resultado = consultar_banco(cpf, coluna)
        
        if resultado:
            valor = resultado[0]
            
            if categoria_prevista == 'fatura_valor':
                return jsonify({"autenticado": True, "resposta": f"O valor da sua fatura atual é R$ {valor:.2f}."})
            
            elif categoria_prevista == 'fatura_vencimento':
                return jsonify({"autenticado": True, "resposta": f"O vencimento da sua fatura é no dia {valor}."})
            
            elif categoria_prevista == 'limite':
                return jsonify({"autenticado": True, "resposta": f"Seu limite disponível agora é R$ {valor:.2f}."})
            
            elif categoria_prevista == 'bloqueio':
                return jsonify({
                    "autenticado": True, 
                    "resposta": f"O Status Atual do Cartão é: {valor}, em caso de necessidade de bloqueio acionar nossa central através do número 0800 7777 8888."
                })
            
            elif categoria_prevista == 'segunda_via':
                return jsonify({
                    "autenticado": True, 
                    "resposta": f"A data de vencimento do cartão é {valor}. Para solicitar segunda via acesse o nosso App Pink Card."
                })

    # RESPOSTAS FIXAS (PROCEDIMENTOS)
    respostas_procedimento = {
        'parcelar': f"Com certeza, {nome_usuario}! Você pode parcelar sua fatura em até 12x diretamente pelo App Pink Card.",
        'senha': "Para sua segurança, a visualização da senha é feita apenas via biometria no nosso aplicativo.",
        'cancelar': "Lamentamos muito. Para cancelamentos, por favor, ligue para nossa central no 0800 700 1234."
    }
    
    msg_final = respostas_procedimento.get(categoria_prevista, "Poderia repetir? Ainda não conheço essa solicitação.")
    return jsonify({"autenticado": True, "resposta": msg_final})

if __name__ == '__main__':
    app.run(debug=True)