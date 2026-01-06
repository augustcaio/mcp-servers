# 🐳 Portainer Expert MCP Server

Um servidor MCP (Model Context Protocol) especializado em **Portainer**, oferecendo ferramentas para gerenciar containers Docker, stacks, volumes, networks e imagens através da API do Portainer.

## ✨ Funcionalidades

### 🔧 Ferramentas Disponíveis

| Ferramenta | Descrição |
|------------|-----------|
| `authenticate_portainer` | Autentica no Portainer e retorna JWT token para uso em outras operações |
| `list_containers` | Lista todos os containers no ambiente Docker especificado |
| `container_action` | Executa ações em containers: start, stop, restart ou remove |
| `list_stacks` | Lista todas as stacks (Docker Compose) no ambiente |
| `create_stack` | Cria uma nova stack usando Docker Compose |
| `list_volumes` | Lista todos os volumes Docker no ambiente |
| `list_images` | Lista todas as imagens Docker no ambiente |
| `list_networks` | Lista todas as networks Docker no ambiente |

### 📚 Recursos (Resources)

- `docs://portainer-architecture` - Informações sobre a arquitetura do Portainer
- `docs://portainer-best-practices` - Melhores práticas para usar o Portainer

### 💡 Prompts

- `deploy_application` - Prompt que guia na implantação de aplicações usando Portainer
- `troubleshoot_container` - Prompt que ajuda na resolução de problemas com containers

## 🚀 Instalação

### Pré-requisitos

- Python 3.12+
- Portainer instalado e acessível (CE ou BE)
- Acesso à API do Portainer

### Setup

1. Navegue até a pasta do servidor:

```bash
cd portainer-expert
```

2. Instale as dependências:

```bash
pip install -e .
# ou
pip install "mcp[cli]" pydantic requests
```

## ⚙️ Configuração no Cursor

Adicione ao arquivo `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "portainer-expert": {
      "command": "/caminho/para/venv/bin/python",
      "args": ["/caminho/para/portainer-expert/portainer_expert.py"]
    }
  }
}
```

## 📖 Exemplos de Uso

### Autenticação no Portainer

Primeiro, você precisa autenticar para obter o JWT token:

```python
# Exemplo de uso da ferramenta authenticate_portainer
{
  "url": "http://localhost:9000",
  "username": "admin",
  "password": "sua_senha"
}
```

### Listar Containers

Após autenticar, use o token para listar containers:

```python
{
  "portainer_url": "http://localhost:9000",
  "jwt_token": "seu_jwt_token_aqui",
  "endpoint_id": 1
}
```

### Criar uma Stack

Crie uma stack usando Docker Compose:

```python
{
  "portainer_url": "http://localhost:9000",
  "jwt_token": "seu_jwt_token_aqui",
  "endpoint_id": 1,
  "stack_name": "minha-app",
  "compose_file": "version: '3.8'\nservices:\n  web:\n    image: nginx:latest\n    ports:\n      - '80:80'"
}
```

### Executar Ações em Containers

Inicie, pare, reinicie ou remova containers:

```python
{
  "portainer_url": "http://localhost:9000",
  "jwt_token": "seu_jwt_token_aqui",
  "endpoint_id": 1,
  "container_id": "abc123def456",
  "action": "restart"  # start, stop, restart, remove
}
```

## 🔗 Referências

- [Documentação Oficial do Portainer](https://docs.portainer.io/)
- [Portainer API Documentation](https://docs.portainer.io/api/)
- [Portainer Architecture](https://docs.portainer.io/getting-started/introduction/portainer-architecture)

## 🛠️ Tecnologias

- **FastMCP** - Framework para criação de servidores MCP
- **Pydantic** - Validação de dados
- **Requests** - Cliente HTTP para comunicação com a API do Portainer

## 📝 Notas

- Este servidor requer que o Portainer esteja instalado e acessível
- A autenticação retorna um JWT token que deve ser usado em todas as operações subsequentes
- O `endpoint_id` representa o ambiente Docker/Kubernetes configurado no Portainer
- Consulte a [documentação oficial do Portainer](https://docs.portainer.io/) para mais detalhes sobre a API

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📄 Licença

MIT License
