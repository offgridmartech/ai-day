# Streamlit LangFlow Agent Tester Template

Este é um projeto simples em **Streamlit** que permite às pessoas rapidamente testar e disponibilizar uma URL pública para seus agentes desenvolvidos no **LangFlow**. 

A aplicação fornece uma interface de chat básica, onde o usuário pode interagir com seu agente configurado no LangFlow, passando mensagens em texto e recebendo respostas.

## Funcionalidades

- **Interface de Chat**: Permite enviar mensagens para o agente e receber respostas.
- **Configuração Rápida**: Integre seu agente do LangFlow apenas preenchendo o arquivo `.env`.
- **Histórico de Mensagens**: O histórico da conversa é exibido na interface.
- **Pronto para Uso**: Inclui um modelo básico que pode ser facilmente customizado.

---

## Configuração do Ambiente

Para executar o projeto, basta preencher o arquivo `.env` com as informações do seu agente LangFlow. Este arquivo já está incluído no projeto e precisa ser ajustado com os valores corretos.

### Exemplo de Conteúdo do Arquivo `.env`

Abra o arquivo `.env.example` e preencha os campos conforme o exemplo abaixo:

```env

# Corpo da solicitação à API do Langflow (alteração é opcional)
DATA_JSON={"input_value": "", "output_type": "chat", "input_type": "chat"}

# URL da sua API
API_URL=<URL_DA_API>

# TOKEN DE ACESSO À API DO LANGFLOW
API_TOKEN=<TOKEN_DA_API>

# TÍTULO CRIATIVO DO SEU AGENTE DE ia
AGENT_TITLE=🔎Meu agente de IA

# DESCRIÇÃO DO SEU AGENTE DE IA
AGENT_DESCRIPTION= Exemplo de descrição de agente de IA.

# PERGUNTA INICIAL DA IA
ASSISTANT_INITIAL_MESSAGE=Olá, como posso te ajudar hoje?

## Limitações

- **Entrada Limitada a Texto**: O chat suporta apenas entradas textuais, sem suporte para upload de arquivos, envio de imagens ou outros tipos de dados.
- **Saídas Simples**: As respostas geradas pelo agente são textuais e não incluem elementos sofisticados, como gráficos ou visualizações.
- **Casos Simples**: Ideal para agentes que já possuem, no LangFlow, acesso integrado a todas as informações necessárias, sem necessidade de inputs adicionais.

Este projeto é indicado para testes rápidos e agentes configurados para lidar com interações básicas.
