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
