import streamlit as st
import requests
import os

# Verifica se o arquivo secrets.toml existe e lida com a ausência de forma amigável
try:
    data_env = st.secrets.get("LANGFLOW_API_DATA")
    api_url = st.secrets.get("LANGFLOW_API_URL")
    token = st.secrets.get("LANGFLOW_API_TOKEN")
    agent_title = st.secrets.get("AI_AGENT_TITLE")
    agent_description = st.secrets.get("AI_AGENT_DESCRIPTION")
    assistant_message = st.secrets.get("WELCOME_MESSAGE", "Olá! Como posso te ajudar hoje?")
except FileNotFoundError:
    st.warning("**Arquivo de configurações ausente!**")
    st.markdown("""
    Parece que você ainda não configurou o arquivo `secrets.toml` no diretório `.streamlit`. 
    Para corrigir este problema, siga as etapas abaixo:

    1. **Crie o diretório `.streamlit`** (caso não exista):
        ```bash
        mkdir .streamlit
        ```

    2. **Adicione o arquivo `secrets.toml`** dentro da pasta `.streamlit` com o seguinte conteúdo:

        ```toml
        LANGFLOW_API_DATA = '{"input_value": "", "output_type": "chat", "input_type": "chat"}'
        LANGFLOW_API_URL = "<URL_API>"
        LANGFLOW_API_TOKEN = "<API_TOKEN>"
        AI_AGENT_TITLE = "Meu agente de IA no Langflow"
        AI_AGENT_DESCRIPTION = "Este é um exemplo de descrição de agente desenvolvido no LangFlow."
        WELCOME_MESSAGE = "Olá! Como posso te ajudar hoje?"
        ```

    3. **Substitua `<URL_API>` e `<API_TOKEN>`** com suas credenciais corretas.
    """)
    st.stop()

# Validação das variáveis
missing_variables = [
    var_name for var_name, var_value in [
        ("LANGFLOW_API_DATA", data_env),
        ("LANGFLOW_API_URL", api_url),
        ("LANGFLOW_API_TOKEN", token),
        ("AI_AGENT_TITLE", agent_title),
        ("AI_AGENT_DESCRIPTION", agent_description)
    ] if var_value is None
]

if missing_variables:
    st.error(f"Erro: As seguintes variáveis de ambiente estão ausentes no arquivo TOML: {', '.join(missing_variables)}")
    st.stop()

# Conversão de JSON
try:
    data_template = eval(data_env)  # Converte o JSON armazenado na variável para um dicionário Python
except Exception as e:
    st.error(f"Erro ao converter LANGFLOW_API_DATA para JSON: {e}")
    st.stop()

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

        # Ajuste na extração da resposta do assistente
        if "outputs" in response_data and len(response_data["outputs"]) > 0:
            assistant_message = response_data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
        else:
            assistant_message = "Desculpe, não consegui entender a resposta da API."

        # Exibe resposta do assistente
        with st.chat_message("assistant"):
            st.markdown(assistant_message)

        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

    except Exception as e:
        st.error(f"Erro ao consultar a API: {e}")
