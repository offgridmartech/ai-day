# Streamlit LangFlow Agent Tester Template

Este é um projeto simples em **Streamlit** que permite às pessoas rapidamente testar e disponibilizar uma URL pública para seus agentes desenvolvidos no **LangFlow**.

A aplicação fornece uma interface de chat básica, onde o usuário pode interagir com seu agente configurado no LangFlow, passando mensagens em texto e recebendo respostas.

## Funcionalidades

- **Interface de Chat**: Permite enviar mensagens para o agente e receber respostas.
- **Configuração Fácil via `secrets.toml`**: Integre seu agente do LangFlow configurando o arquivo de segredos.
- **Histórico de Mensagens**: O histórico da conversa é exibido na interface.
- **Mensagens Personalizáveis**: Configure mensagens de boas-vindas e descrições no `secrets.toml`.

---

## Configuração do Ambiente

Para executar o projeto, você precisa configurar o arquivo `secrets.toml` localizado no diretório `.streamlit`.

### Modelo de Conteúdo do Arquivo `secrets.toml`

```toml
LANGFLOW_API_DATA = '{"input_value": "", "output_type": "chat", "input_type": "chat"}'
LANGFLOW_API_URL = "<URL_API>"
LANGFLOW_API_TOKEN = "<API_TOKEN>"
AI_AGENT_TITLE = "Meu agente de IA no Langflow"
AI_AGENT_DESCRIPTION = "Este é um exemplo de descrição de agente desenvolvido no LangFlow."
WELCOME_MESSAGE = "Olá! Como posso te ajudar hoje?"
