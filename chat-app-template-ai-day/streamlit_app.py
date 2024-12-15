import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
data_env = os.getenv("DATA_JSON")
api_url = os.getenv("API_URL")
token = os.getenv("API_TOKEN")
agent_title = os.getenv("AGENT_TITLE")
agent_description = os.getenv("AGENT_DESCRIPTION")
assistant_message = os.getenv("ASSISTANT_INITIAL_MESSAGE")

if not data_env or not api_url or not token or not agent_title or not agent_description:
    st.error("Erro: Uma ou mais variáveis de ambiente necessárias não foram encontradas.")
    st.stop()

data_template = eval(data_env)  # Converte o JSON armazenado na variável para um dicionário Python

st.title(agent_title)

st.markdown(agent_description)

# Initialize session state for storing chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": assistant_message}]

# Display chat messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Digite uma mensagem:"):
    # Display user message in chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Enviar a solicitação para a API atualizada do Langflow
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        # Atualizar o valor do input_value no data_template
        data_template["input_value"] = prompt

        response = requests.post(
            api_url,
            headers=headers,
            json=data_template
        )

        response_data = response.json()

        # Extract the assistant's response
        assistant_message = response_data["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]

        # Display assistant message in chat
        with st.chat_message("assistant"):
            st.markdown(assistant_message)

        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

    except Exception as e:
        st.error(f"Erro: {e}")
