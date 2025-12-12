# 🐍 Python Backend Expert MCP Server

Um servidor MCP (Model Context Protocol) especializado em desenvolvimento Python Backend, oferecendo ferramentas para formatação PEP 8, scaffolding de apps Django e FastAPI, e geração de APIs REST modernas.

## ✨ Funcionalidades

### 🔧 Ferramentas Disponíveis

| Ferramenta | Descrição |
|------------|-----------|
| `format_python_code` | Formata código Python seguindo estritamente as diretrizes da PEP 8 |
| `scaffold_django_feature` | Gera estrutura Django completa: Model + Service + Selector + DRF ViewSet |
| `generate_fastapi_route` | Gera endpoint FastAPI moderno usando APIRouter, Pydantic v2 e Injeção de Dependência |
| `scaffold_fastapi_project` | Define estrutura de pastas padrão Sênior para FastAPI (Clean Architecture) |

### 📚 Recursos (Resources)

- `docs://django` - Melhores práticas do Django (Enterprise Patterns)
- `docs://fastapi` - Padrões modernos do FastAPI (2024+)

### 💡 Prompts

- `review_code_senior` - Prompt para revisão de código que distingue entre Django e FastAPI

## 🚀 Instalação

### Pré-requisitos

- Python 3.12+
- pip

### Setup

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/python-django-expert-mcp.git
cd python-django-expert-mcp
```

2. Crie um ambiente virtual:
```bash
python3 -m venv ven
source ven/bin/activate  # Linux/Mac
# ou
ven\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -e .
# ou
pip install "mcp[cli]" pydantic autopep8
```

## ⚙️ Configuração no Cursor

Adicione ao arquivo `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "python-django-expert": {
      "command": "/caminho/para/seu/ven/bin/python",
      "args": ["/caminho/para/server.py"]
    }
  }
}
```

## 🧪 Testando o Servidor

### Modo Desenvolvimento (Interface Web)
```bash
mcp dev server.py
```

### Modo Produção (stdio)
```bash
mcp run server.py
```

## 📖 Exemplos de Uso

### Formatando código com PEP 8

A ferramenta `format_python_code` recebe código Python e retorna uma versão formatada seguindo PEP 8:

```python
# Entrada (código com problemas)
def hello(name):return "Hello, "+name

# Saída (código formatado)
def hello(name):
    return "Hello, " + name
```

### Gerando estrutura de App Django

A ferramenta `scaffold_django_feature` gera estrutura completa:
- `models.py` com modelos base
- `services.py` para lógica de negócio
- `selectors.py` para queries complexas
- ViewSets DRF com permissões configuradas

### Gerando endpoint FastAPI moderno

A ferramenta `generate_fastapi_route` gera código completo para:
- Schemas Pydantic v2 com `model_config`
- Routers usando `APIRouter`
- Injeção de dependência com `Annotated`
- Imports corretos de SQLAlchemy

### Estruturando projeto FastAPI

A ferramenta `scaffold_fastapi_project` define estrutura Clean Architecture:
- Separação de camadas (api, core, db, models, schemas)
- Versionamento de API (v1)
- Configuração de migrations (Alembic)

## 📁 Estrutura do Projeto

```
python-pep8-django-api-restfull/
├── server.py          # Servidor MCP principal
├── pyproject.toml     # Configuração do projeto
├── README.md          # Este arquivo
└── .gitignore         # Arquivos ignorados pelo Git
```

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT.

## 🔗 Links Úteis

- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MCP Protocol](https://modelcontextprotocol.io/)

