# 🐍 Python Django Expert MCP Server

Um servidor MCP (Model Context Protocol) especializado em desenvolvimento Python/Django, oferecendo ferramentas para formatação PEP 8, scaffolding de apps Django e geração de APIs REST com Django REST Framework.

## ✨ Funcionalidades

### 🔧 Ferramentas Disponíveis

| Ferramenta | Descrição |
|------------|-----------|
| `enforce_pep8` | Formata código Python seguindo as diretrizes da PEP 8 |
| `scaffold_django_app` | Gera estrutura completa de um app Django moderno |
| `generate_drf_api` | Cria Serializers, ViewSets e Routers para API REST |

### 📚 Recursos (Resources)

- `docs://pep8` - Resumo das regras críticas da PEP 8
- `docs://django` - Melhores práticas do Django 6.0+
- `docs://drf` - Padrões do Django REST Framework

### 💡 Prompts

- `review_python_code` - Template para revisão de código como engenheiro sênior

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

A ferramenta `enforce_pep8` recebe código Python e retorna uma versão formatada:

```python
# Entrada (código com problemas)
def hello(name):return "Hello, "+name

# Saída (código formatado)
def hello(name):
    return "Hello, " + name
```

### Gerando estrutura de App Django

A ferramenta `scaffold_django_app` gera:
- `models.py` com modelos base
- `apps.py` configurado
- Sugestões para `services.py` e `selectors.py`

### Criando API REST

A ferramenta `generate_drf_api` gera código completo para:
- Serializers
- ViewSets
- URL Routers

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
- [MCP Protocol](https://modelcontextprotocol.io/)

