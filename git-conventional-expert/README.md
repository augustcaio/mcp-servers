# 🔀 Git Conventional Expert MCP Server

Um servidor MCP (Model Context Protocol) especializado em **Conventional Commits v1.0.0**, oferecendo ferramentas para validação, construção e geração automática de mensagens de commit semânticas.

## ✨ Funcionalidades

### 🔧 Ferramentas Disponíveis

| Ferramenta | Descrição |
|------------|-----------|
| `validate_commit` | Valida se uma mensagem de commit segue estritamente a especificação Conventional Commits v1.0.0 |
| `construct_commit` | Constrói programaticamente uma string de commit perfeitamente formatada a partir de inputs isolados |

### 📚 Recursos (Resources)

- `docs://conventional-types` - Lista oficial de tipos Conventional Commits com descrições detalhadas

### 💡 Prompts

- `generate_commit_from_diff` - Prompt avançado que analisa um `git diff` e sugere o commit perfeito

## 🚀 Instalação

### Pré-requisitos

- Python 3.12+
- pip

### Setup

1. Clone o repositório ou navegue até a pasta:
```bash
cd git-conventional-expert
```

2. Crie um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -e .
# ou
pip install "mcp[cli]" pydantic
```

## ⚙️ Configuração no Cursor

Adicione ao arquivo `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "git-conventional-expert": {
      "command": "/caminho/para/venv/bin/python3",
      "args": [
        "/caminho/para/git-conventional-expert/git_expert.py"
      ]
    }
  }
}
```

## 🧪 Testando o Servidor

### Modo Desenvolvimento (Interface Web)
```bash
mcp dev git_expert.py
```

### Modo Produção (stdio)
```bash
mcp run git_expert.py
```

## 📖 Exemplos de Uso

### Validando um commit

A ferramenta `validate_commit` valida mensagens de commit:

**Entrada:**
```
feat(auth): add login by google
```

**Saída:**
```
✅ **COMMIT VÁLIDO**
- **Tipo**: `feat` (A new feature (correlates with MINOR in Semantic Versioning))
```

**Entrada inválida:**
```
fix: bug
```

**Saída:**
```
❌ **COMMIT INVÁLIDO**
O cabeçalho 'fix: bug' não segue o padrão.
Formato esperado: `<type>(<scope>): <description>`
Tipos permitidos: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
Exemplo: `feat(auth): add login by google`
```

### Construindo um commit

A ferramenta `construct_commit` constrói commits formatados:

**Input:**
- type: `feat`
- scope: `auth`
- description: `add OAuth2 support`
- body: `Implemented OAuth2 authentication flow with Google and GitHub providers`
- is_breaking: `false`

**Saída:**
```
feat(auth): add OAuth2 support

Implemented OAuth2 authentication flow with Google and GitHub providers
```

### Gerando commit a partir de diff

Use o prompt `generate_commit_from_diff` para analisar um `git diff` e gerar automaticamente a mensagem de commit apropriada.

## 🎯 Tipos de Commit (Conventional Commits v1.0.0)

- **feat**: A new feature (correlates with MINOR in Semantic Versioning)
- **fix**: A bug fix (correlates with PATCH in Semantic Versioning)
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to our CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

## 🔍 Validações Implementadas

- ✅ Estrutura do header (tipo, escopo opcional, breaking change marker)
- ✅ Tipos permitidos conforme spec v1.0.0
- ✅ Comprimento do header (máximo 72 caracteres)
- ✅ Formato do escopo (apenas letras minúsculas, números, hífens, pontos, underscores)
- ✅ Comprimento da descrição (recomendado máximo 50 caracteres)
- ✅ Separação entre header e body (linha em branco)
- ✅ Detecção de Breaking Changes

## 📁 Estrutura do Projeto

```
git-conventional-expert/
├── git_expert.py      # Servidor MCP principal
├── pyproject.toml     # Configuração do projeto
├── README.md          # Este arquivo
└── .gitignore         # Arquivos ignorados pelo Git
```

## 🧠 Benefícios

### Impede "Commits Preguiçosos"
O validador `validate_commit` rejeita descrições vagas como `fix: bug` ou `wip`, garantindo commits descritivos.

### Automação de Breaking Changes
A ferramenta `construct_commit` garante que breaking changes sejam marcados corretamente (com `!` ou `BREAKING CHANGE:`), essencial para ferramentas de versionamento automático como Semantic Release.

### Análise de Contexto Inteligente
O prompt `generate_commit_from_diff` analisa o contexto das mudanças e sugere automaticamente o tipo, escopo e descrição apropriados.

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças usando Conventional Commits (`git commit -m 'feat: add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT.

## 🔗 Links Úteis

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [MCP Protocol](https://modelcontextprotocol.io/)

