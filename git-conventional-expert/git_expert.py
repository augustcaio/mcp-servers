from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import re
from typing import Optional

# Inicialização do Servidor
mcp = FastMCP("Git Conventional Expert")

# --- Knowledge Base (Constantes) ---

CONVENTIONAL_TYPES = {
    "feat": "A new feature (correlates with MINOR in Semantic Versioning)",
    "fix": "A bug fix (correlates with PATCH in Semantic Versioning)",
    "docs": "Documentation only changes",
    "style": "Changes that do not affect the meaning of the code (white-space, formatting, etc)",
    "refactor": "A code change that neither fixes a bug nor adds a feature",
    "perf": "A code change that improves performance",
    "test": "Adding missing tests or correcting existing tests",
    "build": "Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)",
    "ci": "Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)",
    "chore": "Other changes that don't modify src or test files",
    "revert": "Reverts a previous commit"
}

REGEX_HEADER = r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9-._]+\))?(!)?: .{1,72}$"

# --- Tools (Ferramentas) ---


class CommitMessageInput(BaseModel):
    message: str = Field(...,
                         description="A mensagem de commit completa para validar.")


@mcp.tool()
def validate_commit(input_data: CommitMessageInput) -> str:
    """
    Valida se uma mensagem de commit segue estritamente a especificação Conventional Commits v1.0.0.
    Verifica: Estrutura, Tipos permitidos, Comprimento do cabeçalho e Breaking Changes.
    """
    msg = input_data.message.strip()
    lines = msg.split('\n')
    header = lines[0]

    # 1. Validação de Estrutura do Header
    if not re.match(REGEX_HEADER, header):
        return (
            "❌ **COMMIT INVÁLIDO**\n"
            f"O cabeçalho '{header}' não segue o padrão.\n"
            "Formato esperado: `<type>(<scope>): <description>`\n"
            f"Tipos permitidos: {', '.join(CONVENTIONAL_TYPES.keys())}\n"
            "Exemplo: `feat(auth): add login by google`"
        )

    # 2. Análise de Semântica
    type_found = header.split(':')[0].split('(')[0].replace('!', '')

    report = "✅ **COMMIT VÁLIDO**\n"
    report += f"- **Tipo**: `{type_found}` ({CONVENTIONAL_TYPES.get(type_found, 'Unknown')})\n"

    # 3. Validação de Corpo e Rodapé (separação) - Aviso não bloqueia
    warnings = []
    if len(lines) > 1 and lines[1] != "":
        warnings.append(
            "⚠️ Deve haver uma linha em branco entre o cabeçalho e o corpo do commit.")

    # 4. Verificação de Breaking Changes
    if "!" in header.split(':')[0] or (len(lines) > 1 and "BREAKING CHANGE:" in msg):
        report += "- **⚠️ BREAKING CHANGE**: Este commit irá disparar uma versão MAJOR.\n"

    # Adicionar avisos ao relatório se houver
    if warnings:
        report += "\n**Avisos de Formato:**\n"
        for warning in warnings:
            report += f"- {warning}\n"

    return report


class CommitBuilderInput(BaseModel):
    type: str = Field(...,
                      description="Tipo do commit (feat, fix, chore, etc).")
    scope: Optional[str] = Field(
        None, description="Escopo da mudança (ex: api, db, ui).")
    description: str = Field(...,
                             description="Descrição curta e imperativa (max 50 chars).")
    body: Optional[str] = Field(
        None, description="Explicação detalhada do 'porquê' e 'como'.")
    is_breaking: bool = Field(
        False, description="Se introduz uma mudança que quebra compatibilidade.")
    footer: Optional[str] = Field(
        None, description="Rodapé (ex: Closes #123).")


@mcp.tool()
def construct_commit(input_data: CommitBuilderInput) -> str:
    """
    Constrói programaticamente uma string de commit perfeitamente formatada.
    Útil para garantir que a IA não erre espaços ou parênteses.
    """
    # Validação do tipo
    if input_data.type not in CONVENTIONAL_TYPES:
        valid_types = ", ".join(CONVENTIONAL_TYPES.keys())
        return f"Erro: Tipo '{input_data.type}' inválido. Use: {valid_types}"

    # Validação do escopo (se fornecido)
    if input_data.scope:
        scope_pattern = r"^[a-z0-9-._]+$"
        if not re.match(scope_pattern, input_data.scope):
            return (
                f"Erro: Escopo '{input_data.scope}' inválido. "
                "Use apenas letras minúsculas, números, hífens, pontos ou underscores."
            )

    # Validação do comprimento da descrição
    if len(input_data.description) > 50:
        return (
            f"Erro: Descrição muito longa ({len(input_data.description)} caracteres). "
            "Máximo recomendado: 50 caracteres."
        )

    # Montagem do Header
    scope_part = f"({input_data.scope})" if input_data.scope else ""
    breaking_mark = "!" if input_data.is_breaking else ""

    header = f"{input_data.type}{scope_part}{breaking_mark}: {input_data.description}"

    # Montagem completa
    full_message = header

    if input_data.body:
        full_message += f"\n\n{input_data.body}"

    if input_data.is_breaking and "BREAKING CHANGE" not in (input_data.body or ""):
        # Se marcou breaking mas não escreveu no corpo, adicionamos no footer automaticamente
        footer_text = f"BREAKING CHANGE: {input_data.description}"
        if input_data.footer:
            full_message += f"\n\n{footer_text}\n{input_data.footer}"
        else:
            full_message += f"\n\n{footer_text}"
    elif input_data.footer:
        full_message += f"\n\n{input_data.footer}"

    return full_message

# --- Resources (Documentação Viva) ---


@mcp.resource("docs://conventional-types")
def get_conventional_types() -> str:
    """Retorna a lista oficial de tipos e suas descrições."""
    docs = "# Conventional Commits Types (v1.0.0)\n\n"
    for type_key, desc in CONVENTIONAL_TYPES.items():
        docs += f"- **{type_key}**: {desc}\n"
    return docs

# --- Prompts (Templates de Raciocínio) ---


@mcp.prompt()
def generate_commit_from_diff(diff_content: str) -> str:
    """
    Prompt avançado que instrui o LLM a analisar um diff e sugerir o commit perfeito.
    """
    return f"""
    Aja como um Tech Lead Sênior revisando código para merge.
    Sua tarefa é criar uma mensagem de commit baseada no `git diff` fornecido abaixo.
    
    REGRAS ESTRITAS (Conventional Commits v1.0.0):
    1. Formato: `<tipo>(<escopo opcional>): <descrição>`
    2. Tipos permitidos: {', '.join(CONVENTIONAL_TYPES.keys())}.
    3. Use o modo imperativo na descrição ("add" e não "added").
    4. Se houver mudanças que quebram compatibilidade, use `!` após o tipo ou adicione `BREAKING CHANGE:` no rodapé.
    5. Identifique o escopo com base nos arquivos alterados (ex: se mudou `user_service.py`, escopo é `user`).

    Conteúdo do Diff:
    ```
    {diff_content}
    ```

    Saída esperada:
    Apenas o bloco de código com a mensagem sugerida, e uma breve explicação do porquê escolheu esse tipo.
    """


if __name__ == "__main__":
    mcp.run()
