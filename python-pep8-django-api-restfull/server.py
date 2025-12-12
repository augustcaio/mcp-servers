from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import autopep8

# Rebranding para cobrir todo o espectro Backend
mcp = FastMCP("Python Backend Expert")

# --- Bases de Conhecimento (Knowledge Base) ---

PEP8_RULES = """
PEP 8 ESSENTIALS:
- 4 spaces indentation.
- Snake_case for functions/variables, CapWords for classes.
- Imports: Standard -> Third Party -> Local.
- Max line length: 79 chars (soft), 88/100 (hard for modern teams).
"""

DJANGO_BEST_PRACTICES = """
DJANGO ARCHITECTURE (Enterprise Patterns):
- "Fat Models, Skinny Views" is good, but "Service Layer" is better for complexity.
- Selectors: Place complex DB queries in `selectors.py`.
- Services: Place business logic in `services.py`.
- DRF: Use ModelViewSet + DefaultRouter for standard CRUD.
- Auth: Always use Permission Classes.
"""

FASTAPI_BEST_PRACTICES = """
FASTAPI MODERN PATTERNS (2024+):
- Project Structure: `app/api/v1/endpoints`, `app/core`, `app/schemas`.
- Validation: Use Pydantic v2 (`model_config`, `Field`).
- DI: Use `Annotated[Type, Depends(...)]` for cleaner signatures.
- Routers: Never define routes in main.py; use APIRouter.
- Sync vs Async: Use `async def` for I/O bound, `def` for CPU bound.
"""

# --- Ferramentas Compartilhadas ---


class CodeInput(BaseModel):
    code: str = Field(..., description="Código Python para análise.")


@mcp.tool()
def format_python_code(input_data: CodeInput) -> str:
    """Formata código Python seguindo estritamente a PEP 8."""
    formatted = autopep8.fix_code(input_data.code, options={'aggressive': 1})
    return f"✅ Código Formatado (PEP 8):\n\n{formatted}"

# --- Ferramentas Django (Legado Mantido & Melhorado) ---


class DjangoAppInput(BaseModel):
    app_name: str
    models: list[str]


@mcp.tool()
def scaffold_django_feature(input_data: DjangoAppInput) -> str:
    """Gera estrutura Django completa: Model + Service + Selector + DRF ViewSet."""
    app = input_data.app_name

    return f"""
    🏗️ DJANGO STRUCTURE FOR '{app}':
    
    # 1. models.py
    from django.db import models
    class {input_data.models[0]}(models.Model):
        ...
    
    # 2. services.py (Business Logic)
    def create_{input_data.models[0].lower()}(*, data):
        # Implementation here
        pass

    # 3. views.py (DRF)
    from rest_framework import viewsets
    class {input_data.models[0]}ViewSet(viewsets.ModelViewSet):
        permission_classes = [IsAuthenticated]
        ...
    """

# --- NOVAS Ferramentas FastAPI ---


class FastApiEndpointInput(BaseModel):
    resource_name: str = Field(...,
                               description="Nome do recurso (ex: Item, User).")
    http_method: str = Field(..., description="GET, POST, PUT, DELETE")


@mcp.tool()
def generate_fastapi_route(input_data: FastApiEndpointInput) -> str:
    """
    Gera um endpoint FastAPI moderno usando APIRouter, Pydantic v2 e Injeção de Dependência.
    """
    resource = input_data.resource_name
    resource_lower = resource.lower()
    method = input_data.http_method.upper()

    # Schema Pydantic v2
    schema_code = f"""
from pydantic import BaseModel, Field, ConfigDict

class {resource}Schema(BaseModel):
    id: int
    name: str = Field(..., min_length=3)
    
    model_config = ConfigDict(from_attributes=True)
"""

    # Router Code com Annotated (Python 3.10+)
    # Construir o decorator dinamicamente
    decorator_method = method.lower()
    decorator_line = f"@router.{decorator_method}(\"/\", response_model={resource}Schema)"
    router_code = f"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from .schemas import {resource}Schema
from ..db.session import get_db

router = APIRouter(prefix="/{resource_lower}s", tags=["{resource}"])

{decorator_line}
async def {decorator_method}_{resource_lower}(
    payload: {resource}Schema,
    db: Annotated[Session, Depends(get_db)]
):
    \"\"\"
    {method} operation for {resource}.
    Uses Dependency Injection for Database session.
    \"\"\"
    # Call service layer here
    return payload
"""

    return f"""
    🚀 FASTAPI MODERN COMPONENT ({resource}):
    
    📄 schemas.py (Pydantic v2):
    {schema_code}
    
    📄 router.py (Endpoints):
    {router_code}
    
    💡 Dica Sênior: Lembre-se de registrar este router no main.py usando `app.include_router(router)`.
    """


class FastApiStructureInput(BaseModel):
    project_name: str


@mcp.tool()
def scaffold_fastapi_project(input_data: FastApiStructureInput) -> str:
    """Define a estrutura de pastas padrão Sênior para FastAPI."""
    name = input_data.project_name
    return f"""
    📂 ESTRUTURA RECOMENDADA (Clean Architecture para FastAPI):
    
    {name}/
    ├── app/
    │   ├── api/
    │   │   ├── v1/
    │   │   │   ├── endpoints/  <-- Seus routers ficam aqui
    │   │   │   └── api.py      <-- Agrupa routers
    │   │   └── deps.py         <-- Dependências Reutilizáveis (Auth, DB)
    │   ├── core/
    │   │   ├── config.py       <-- Pydantic Settings
    │   │   └── security.py
    │   ├── db/
    │   │   └── session.py      <-- SQLAlchemy/Tortoise setup
    │   ├── models/             <-- Modelos de Banco (ORM)
    │   ├── schemas/            <-- Modelos Pydantic (Input/Output)
    │   └── main.py             <-- Entrypoint limpo
    ├── alembic/                <-- Migrations
    ├── pyproject.toml
    └── Dockerfile
    """

# --- Prompts ---


@mcp.prompt()
def review_code_senior(code: str) -> str:
    """Prompt para revisão de código que distingue entre Django e FastAPI."""
    return f"""
    Atue como um Tech Lead Python (Sênior). Revise o código abaixo.
    
    1. Identifique o Framework (Django ou FastAPI ou Puro).
    2. Se **Django**: Verifique se há lógica nas Views (ruim) ou Services (bom). Verifique padrões DRF.
    3. Se **FastAPI**: 
       - Procure por `Annotated` (Python moderno).
       - Verifique se Pydantic v2 está sendo usado (`model_config`).
       - Garanta que `async` está sendo usado corretamente (não bloqueante).
    4. Se **Geral**: Aplique PEP 8 rigorosa.
    
    Código:
    ```python
    {code}
    ```
    """

# --- Resources ---


@mcp.resource("docs://fastapi")
def get_fastapi_guide() -> str:
    return FASTAPI_BEST_PRACTICES


@mcp.resource("docs://django")
def get_django_guide() -> str:
    return DJANGO_BEST_PRACTICES


if __name__ == "__main__":
    mcp.run()
