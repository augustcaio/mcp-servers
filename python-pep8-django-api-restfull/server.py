from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field
import autopep8
import textwrap

# Inicializa o servidor FastMCP
mcp = FastMCP("Python Django Expert")

# --- Constantes de Conhecimento (Baseadas nos Links) ---
PEP8_SUMMARY = """
CRITICAL PEP 8 RULES:
1. Indentation: Use 4 spaces per indentation level.
2. Line Length: Limit all lines to a maximum of 79 characters.
3. Imports: Imports should usually be on separate lines and grouped (Standard -> Third Party -> Local).
4. Naming: 
   - Functions/Variables: snake_case
   - Classes: CapWords
   - Constants: UPPER_CASE
5. Whitespace: Avoid extraneous whitespace.
Ref: https://peps.python.org/pep-0008/
"""

DJANGO_6_BEST_PRACTICES = """
DJANGO MODERN ARCHITECTURE (Targeting 6.0+ readiness):
1. Async Views: Use async def where I/O bound.
2. Project Structure: Decouple business logic from Views using Services/Selectors pattern.
3. Models: Always define __str__, use appropriate field types.
4. Settings: Split settings (base, dev, prod).
Ref: https://docs.djangoproject.com/en/6.0/
"""

DRF_STANDARDS = """
REST FRAMEWORK STANDARDS:
1. ViewSets: Prefer ModelViewSet for CRUD standardisation.
2. Serializers: Use ModelSerializer explicitly defining 'fields'.
3. Routers: Use DefaultRouter to auto-generate URLs.
4. Authentication: Never expose API without Permissions classes.
Ref: https://python-rest-framework.readthedocs.io/en/latest/
"""

# --- Ferramentas (Tools) ---


class CodeInput(BaseModel):
    code: str = Field(...,
                      description="O código Python para analisar ou formatar.")


@mcp.tool()
def enforce_pep8(input_data: CodeInput) -> str:
    """
    Formata o código fornecido estritamente de acordo com a PEP 8 e analisa violações.
    Usa autopep8 para garantir conformidade técnica.
    """
    raw_code = input_data.code

    # Formatação automática
    formatted_code = autopep8.fix_code(
        raw_code,
        options={'aggressive': 1}
    )

    report = "✅ PEP 8 COMPLIANCE REPORT:\n"
    if raw_code != formatted_code:
        report += "⚠️ O código original violava normas da PEP 8. Abaixo está a versão corrigida.\n\n"
        report += "Correções aplicadas: Espaçamento, indentação e quebras de linha.\n"
    else:
        report += "🎉 O código já estava em conformidade com a PEP 8.\n"

    return f"{report}\n--- CODE START ---\n{formatted_code}\n--- CODE END ---"


class DjangoScaffoldInput(BaseModel):
    app_name: str = Field(..., description="Nome do aplicativo Django.")
    models_list: list[str] = Field(...,
                                   description="Lista de nomes de modelos a serem criados.")


@mcp.tool()
def scaffold_django_app(input_data: DjangoScaffoldInput) -> str:
    """
    Gera a estrutura de arquivos para um App Django moderno e robusto.
    Segue a filosofia de 'Fat Models, Skinny Views' ou Service Layer.
    """
    app = input_data.app_name

    # Template para models.py
    models_code = "from django.db import models\n\n"
    for model in input_data.models_list:
        models_code += f"""class {model}(models.Model):
    # TODO: Define fields for {model}
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{model} object ({{self.id}})"

"""

    # Template para apps.py (Configuração moderna)
    apps_code = f"""from django.apps import AppConfig

class {app.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{app}'
"""

    return f"""
    📂 ESTRUTURA SUGERIDA PARA O APP '{app}':
    
    1. {app}/apps.py:
    {apps_code}
    
    2. {app}/models.py:
    {models_code}
    
    3. {app}/services.py (Recomendação Senior):
    # Coloque a lógica de negócios complexa aqui, não nas Views.
    
    4. {app}/selectors.py (Recomendação Senior):
    # Coloque queries complexas aqui.
    """


class DRFGeneratorInput(BaseModel):
    model_name: str = Field(...,
                            description="Nome do modelo Django existente.")
    fields: list[str] = Field(default=["'__all__'"],
                              description="Lista de campos para serializar.")


@mcp.tool()
def generate_drf_api(input_data: DRFGeneratorInput) -> str:
    """
    Gera código para Serializers, ViewSets e Routers seguindo as melhores práticas do DRF.
    Cria uma API RESTful completa para um modelo.
    """
    model = input_data.model_name
    fields_str = ", ".join(input_data.fields) if len(
        input_data.fields) > 1 else "'__all__'"

    # Serializer
    serializer_code = f"""
from rest_framework import serializers
from .models import {model}

class {model}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {model}
        fields = [{fields_str}]
        read_only_fields = ['created_at', 'updated_at']
"""

    # ViewSet
    viewset_code = f"""
from rest_framework import viewsets, permissions
from .models import {model}
from .serializers import {model}Serializer

class {model}ViewSet(viewsets.ModelViewSet):
    \"\"\"
    API endpoint that allows {model} to be viewed or edited.
    \"\"\"
    queryset = {model}.objects.all()
    serializer_class = {model}Serializer
    permission_classes = [permissions.IsAuthenticated] # Security First
"""

    # Router
    router_code = f"""
from rest_framework.routers import DefaultRouter
from .views import {model}ViewSet

router = DefaultRouter()
router.register(r'{model.lower()}s', {model}ViewSet, basename='{model.lower()}')

urlpatterns = router.urls
"""

    return f"""
    🚀 DRF SCAFFOLDING FOR {model}:
    
    📄 serializers.py:
    {serializer_code}
    
    📄 views.py:
    {viewset_code}
    
    📄 urls.py:
    {router_code}
    """

# --- Prompts (Templates de Comportamento) ---


@mcp.prompt()
def review_python_code(code: str) -> str:
    """Retorna um prompt de sistema para que o LLM atue como um revisor de código sênior."""
    return f"""
    Você é um Engenheiro de Software Python Sênior. Sua tarefa é revisar o seguinte código.
    
    Diretrizes Estritas:
    1. Verifique a conformidade com a PEP 8 ({PEP8_SUMMARY}).
    2. Verifique se o código Django segue as práticas modernas da versão 6.0 (ex: async onde possível, types hinting).
    3. Verifique se as APIs REST seguem a arquitetura do DRF (ViewSets, Routers).
    
    Código para revisão:
    ```python
    {code}
    ```
    
    Por favor, liste:
    - Erros de estilo (Linter).
    - Riscos de segurança.
    - Otimizações de desempenho.
    - Código refatorado sugerido.
    """

# --- Recursos (Resources) ---


@mcp.resource("docs://pep8")
def get_pep8_docs() -> str:
    return PEP8_SUMMARY


@mcp.resource("docs://django")
def get_django_docs() -> str:
    return DJANGO_6_BEST_PRACTICES


@mcp.resource("docs://drf")
def get_drf_docs() -> str:
    return DRF_STANDARDS


if __name__ == "__main__":
    mcp.run()
