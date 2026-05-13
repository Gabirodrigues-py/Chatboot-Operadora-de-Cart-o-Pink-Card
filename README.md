
# 🎀 Pink Card - Assistente Virtual 

O **Pink Card** é um chatbot de autoatendimento desenvolvido para facilitar a jornada de clientes de uma operadora de cartões de crédito. O projeto integra uma interface a um motor de **Inteligência Artificial** capaz de consultar dados em tempo real e guiar o usuário para a consulta de informações do seu cartão..

---

## 🚀 Funcionalidades

* **Autenticação por CPF:** Proteção inicial que valida o cliente antes de liberar o chat.
* **Consultas Dinâmicas (SQL):**
* Saldo de fatura atual e data de vencimento.
* Consulta de limite disponível.
* Status do cartão (Ativo/Bloqueado).
* **IA com Filtro de Confiança:** O bot avalia o grau de certeza da resposta; se a pergunta estiver fora do contexto (ex: "quero uma pizza"), ele solicita que o usuário reformule.
* **Fluxos de Procedimento:** Orientações sobre parcelamento, segunda via e bloqueio via central 0800.
* **Encerramento:** Comando "sair" para finalizar a sessão de forma amigável.
* **Admin:** O projeto conta com um arquivo de CRUD para manipulação dos clientes no banco de dados
---

## 🛠️ Tecnologias Utilizadas

* **Python**: Sistema e processamento de dados.
* **Flask**: Gerenciamento de rotas e integração entre Front e Back.
* **SQLite3**: Banco de dados relacional para persistência de dados dos clientes.
* **HTML5 & CSS3**: Interface responsiva.
* **JavaScript**: Manipulação do DOM e requisições assíncronas (Fetch API).

---

## 🧠 O Algoritmo: Naive Bayes (MultinomialNB)
Para o processamento de linguagem natural (NLP), o projeto utiliza o classificador **Naive Bayes**, via biblioteca `scikit-learn`.
O Naive Bayes é um algoritmo de aprendizado de máquina supervisionado baseado no **Teorema de Bayes**. 
O algoritmo funciona assim:
1. **Treinamento:** Ele analisa frases de exemplo para entender quais palavras são mais comuns em cada intenção (ex: "fatura", "pagar", "vencimento").
2. **Cálculo de Probabilidade:** Quando o usuário digita algo, o bot calcula a probabilidade de aquela frase pertencer a cada categoria treinada.
3. **Classificação:** A categoria com a maior nota vence.
4. **Threshold (Limiar):** Possui uma trava de segurança que analisa a porcentagem de confiança. Se a maior probabilidade for muito baixa, o bot identifica que a pergunta está fora do escopo e pede esclarecimentos.
O uso do `MultinomialNB` foi utilizado para este projeto por ser extremamente rápido, eficiente com poucos dados e excelente para lidar com frequências de termos em mensagens de chat.
---

## 📂 Estrutura do Projeto

```text
├── app.py                # Servidor Flask, Treinamento da IA e Lógica de Negócio
├── operadora_cartoes.db  # Banco de Dados SQLite
├── static/               # Recursos Visuais (CSS e Imagens)
│   ├── css/style.css     # Design estilizado da Pink Card
│   ├── logo_pink.png     # Logo do cabeçalho
│   └── icone_bot.png     # Ícone redondo da atendente
└── templates/
    └── index.html        # Interface do usuário (Frontend)

```
---

## ⚙️ Instalação e Execução

1. **Instale as dependências:**
```bash
pip install flask scikit-learn
```

2. **Inicie a aplicação:**
```bash
python app.py
```
3. **Acesse:** `http://127.0.0.1:5000`
---
4.**Dados de CPF para teste**
```text
45829304155
71294038522
10928374611
88273645100
33495867288
```
## 👩‍💻 Desenvolvido por

**Gabriella Rodrigues** .

---
