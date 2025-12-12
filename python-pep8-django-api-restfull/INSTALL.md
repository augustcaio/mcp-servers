# 📦 Instalação do MCP Server no Cursor

## Pré-requisitos

- Python 3.12+
- Acesso sudo para instalar dependências do sistema

## Passo a Passo

### 1. Instalar dependências do sistema

Execute o script de instalação:

```bash
cd /home/lse/Desktop/Caio/mcp-servers/python-pep8-django-api-restfull
./install.sh
```

Ou execute manualmente:

```bash
# Instalar pip e venv
sudo apt install -y python3-pip python3-venv

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual e instalar dependências
source venv/bin/activate
pip install --upgrade pip
pip install "mcp[cli]" pydantic autopep8
```

### 2. Configuração no Cursor

O arquivo de configuração já foi criado em `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "python-backend-expert": {
      "command": "/home/lse/Desktop/Caio/mcp-servers/python-pep8-django-api-restfull/venv/bin/python3",
      "args": [
        "/home/lse/Desktop/Caio/mcp-servers/python-pep8-django-api-restfull/server.py"
      ]
    }
  }
}
```

### 3. Reiniciar o Cursor

Após instalar as dependências, **reinicie o Cursor** para carregar o servidor MCP.

### 4. Verificar instalação

No Cursor, você deve conseguir ver o servidor MCP `python-backend-expert` disponível com as seguintes ferramentas:

- `format_python_code` - Formata código Python seguindo PEP 8
- `scaffold_django_feature` - Gera estrutura Django completa
- `generate_fastapi_route` - Gera endpoint FastAPI moderno
- `scaffold_fastapi_project` - Define estrutura de pastas FastAPI

## Testando manualmente

Para testar o servidor manualmente:

```bash
cd /home/lse/Desktop/Caio/mcp-servers/python-pep8-django-api-restfull
source venv/bin/activate
python server.py
```

Ou usando o CLI do MCP:

```bash
source venv/bin/activate
mcp dev server.py
```

## Troubleshooting

### Erro: "No module named 'mcp'"

Certifique-se de que:
1. O ambiente virtual foi criado corretamente
2. As dependências foram instaladas no ambiente virtual
3. O caminho no `mcp.json` aponta para o Python correto do venv

### Erro: "python3-venv não encontrado"

Instale o pacote:
```bash
sudo apt install python3.12-venv
```

### O servidor não aparece no Cursor

1. Verifique se o arquivo `~/.cursor/mcp.json` existe e está correto
2. Reinicie o Cursor completamente
3. Verifique os logs do Cursor para erros

