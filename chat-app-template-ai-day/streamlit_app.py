import streamlit as st
import requests

# Carregar variáveis do Streamlit Secrets
data_env = st.secrets["LANGFLOW_API_DATA"]
api_url = st.secrets["LANGFLOW_API_URL"]
token = st.secrets["LANGFLOW_API_TOKEN"]
agent_title = st.secrets["AI_AGENT_TITLE"]
agent_description = st.secrets["AI_AGENT_DESCRIPTION"]
assistant_message = st.secrets["WELCOME_MESSAGE"]

# Validação das variáveis
if not data_env or not api_url or not token or not agent_title or not agent_description:
    st.error("Erro: Uma ou mais variáveis de ambiente necessárias não foram encontradas.")
    st.markdown("""
    Para corrigir esse erro, configure as variáveis de ambiente seguindo os passos abaixo:

    1. **Acesse My Apps**.
    2. Selecione o aplicativo desejado.
    3. Clique no ícone de três pontos (⋮) ao lado do app.
    4. Vá para **Configurações**.
    5. Adicione as variáveis necessárias na seção **Secrets**, preenchendo com os dados do seu LangFlow:

    **Variáveis necessárias:**

    ```plaintext
    # Título do agente
    AI_AGENT_TITLE = "Meu agente de IA no Langflow"

    # Descrição do agente
    AI_AGENT_DESCRIPTION = "Este é um exemplo de descrição de agente desenvolvido no LangFlow. Siga as instruções abaixo para integrar sua API do Langflow ao Streamlit."

    # Mensagem de boas-vindas
    WELCOME_MESSAGE = "Olá! Como posso te ajudar hoje?"

    # URL da API do LangFlow
    LANGFLOW_API_URL = "<URL_API>"

    # Token da API do LangFlow
    LANGFLOW_API_TOKEN = "<API_TOKEN>"

    # Dados do agente em formato JSON
    LANGFLOW_API_DATA = '{"input_value": "", "output_type": "chat", "input_type": "chat"}'
    ```

    **Preencha `<URL_API>` e `<API_TOKEN>` com as informações correspondentes ao seu LangFlow.**
    """)
    st.stop()

data_template = eval(data_env)  # Converte o JSON armazenado na variável para um dicionário Python

# Interface do Streamlit
st.title(agent_title)
st.markdown(agent_description)

# Inicialização do histórico de mensagens
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": assistant_message}]

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Captura entrada do usuário
if prompt := st.chat_input("Digite uma mensagem:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Envio para API do Langflow
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        # Atualiza o valor do input_value no data_template
        data_template["input_value"] = prompt

        response = requests.post(
            api_url,
            headers=headers,
            json=data_template
        )

        response_data = response.json()

        # Extrai a resposta do assistente
        assistant_message = response_data["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]

        # Exibe resposta do assistente
        with st.chat_message("assistant"):
            st.markdown(assistant_message)

        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

    except Exception as e:
        st.error(f"Erro: {e}")
