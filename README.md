# 🔌 MCP Servers Collection

Coleção de servidores MCP (Model Context Protocol) desenvolvidos para estender as capacidades de assistentes de IA como Claude e Cursor.

## 📦 Servidores Disponíveis

| Servidor | Descrição | Status |
|----------|-----------|--------|
| [python-pep8-django-api-restfull](./python-pep8-django-api-restfull/) | Ferramentas para PEP 8, Django e Django REST Framework | ✅ Ativo |

## 🚀 Como Usar

Cada servidor possui seu próprio `README.md` com instruções específicas de instalação e configuração.

### Configuração Geral no Cursor

Adicione os servidores desejados ao arquivo `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "nome-do-servidor": {
      "command": "python",
      "args": ["/caminho/para/server.py"]
    }
  }
}
```

## 🛠️ Tecnologias

- **Python 3.12+**
- **FastMCP** - Framework para criação de servidores MCP
- **Pydantic** - Validação de dados

## 📁 Estrutura do Repositório

```
mcp-servers/
├── README.md                              # Este arquivo
├── .gitignore                             # Arquivos ignorados
└── python-pep8-django-api-restfull/       # Servidor Python/Django
    ├── server.py
    ├── pyproject.toml
    └── README.md
```

## 🤝 Contribuindo

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feat/novo-servidor`)
3. Commit suas mudanças (`git commit -m 'feat: add novo servidor MCP'`)
4. Push para a branch (`git push origin feat/novo-servidor`)
5. Abra um Pull Request

## 📝 Licença

MIT License

## 👤 Autor

**Caio Augusto** - [@augustcaio](https://github.com/augustcaio)

---

⭐ Se este repositório foi útil, considere dar uma estrela!

