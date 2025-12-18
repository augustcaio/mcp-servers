from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# Inicializa o servidor
mcp = FastMCP("C4 Architecture Architect")

# --- Knowledge Base ---

C4_LEVELS_INFO = """
THE C4 MODEL HIERARCHY:
1. System Context: High-level view. Shows your Software System + Users + External Systems.
   - Focus: Scope and relationships.
2. Container: Zoom into your System. Shows Applications (Web, Mobile), APIs, Databases.
   - Focus: Technology choices and high-level responsibilities.
   - NOT Docker containers (necessarily), but deployable units.
3. Component: Zoom into a Container. Shows internal modules/classes/layers.
   - Focus: Implementation details and structural organization.
4. Code: UML Class diagrams (usually too detailed for high-level architecture).
Ref: https://c4model.com/
"""

MERMAID_TEMPLATE = """
C4Context
  title System Context diagram for {system_name}
  
  Person(user, "{user_role}", "A user of the system")
  System(system, "{system_name}", "The core system")
  
  Rel(user, system, "Uses")
"""

# --- Tools ---


class C4Element(BaseModel):
    name: str
    type: Literal["Person", "System", "Container", "Component", "Database"]
    description: str
    technology: Optional[str] = None
    parent: Optional[str] = Field(
        None, description="Nome do elemento pai (ex: Container pertence a um System).")


class MermaidInput(BaseModel):
    title: str
    elements: List[C4Element]
    diagram_type: Literal["Context", "Container", "Component"] = "Context"


@mcp.tool()
def generate_mermaid_c4(input_data: MermaidInput) -> str:
    """
    Gera código Mermaid.js compatível com o diagrama C4 solicitado.
    Suporta C4Context, C4Container e C4Component.
    """
    # Mapeamento de Tipos C4 para Macros Mermaid
    type_map = {
        "Person": "Person",
        "System": "System",
        "Container": "Container",
        "Database": "ContainerDb",
        "Component": "Component"
    }

    diagram_header = f"C4{input_data.diagram_type}\n  title {input_data.title}\n"

    body = ""
    relationships = ""

    # Gerar definições de elementos
    for el in input_data.elements:
        safe_id = el.name.replace(" ", "_").lower()
        macro = type_map.get(el.type, "System")

        # Parâmetros extras para Container/Component (Tecnologia)
        tech_str = f', "{el.technology}"' if el.technology and el.type in [
            "Container", "Database", "Component"] else ""

        # Se tem pai, usamos Boundary (Subgrafos no Mermaid)
        if el.parent:
            # Nota: Mermaid C4 lida com Boundaries de forma diferente, simplificaremos aqui para geração plana
            # ou usaríamos Container_Boundary para aninhamento visual avançado.
            pass

        body += f'  {macro}({safe_id}, "{el.name}", "{el.description}"{tech_str})\n'

    # Gerar relacionamentos genéricos (Exemplo: Todos conectam ao primeiro System encontrado)
    # Numa aplicação real, o input deveria ter uma lista de "Relationships" explícita.
    # Aqui inferimos uma conexão básica para não gerar diagrama vazio.
    if len(input_data.elements) > 1:
        first_id = input_data.elements[0].name.replace(" ", "_").lower()
        for i in range(1, len(input_data.elements)):
            curr_id = input_data.elements[i].name.replace(" ", "_").lower()
            relationships += f'  Rel({first_id}, {curr_id}, "Uses", "HTTPS/JSON")\n'

    return f"```mermaid\n{diagram_header}\n{body}\n{relationships}\n```"


class StructurizrInput(BaseModel):
    workspace_name: str
    description: str
    elements: List[C4Element]


@mcp.tool()
def generate_structurizr_dsl(input_data: StructurizrInput) -> str:
    """
    Gera um workspace completo em Structurizr DSL.
    Ideal para estruturas complexas e versionamento 'Diagrams as Code'.
    """
    dsl = f"""workspace "{input_data.workspace_name}" "{input_data.description}" {{

    model {{
"""
    # Dicionários para organizar hierarquia
    people = []
    systems = {}  # SystemName -> {description, containers: []}

    for el in input_data.elements:
        if el.type == "Person":
            people.append(
                f'        {el.name.replace(" ", "")} = person "{el.name}" "{el.description}"')
        elif el.type == "System":
            systems[el.name] = {"desc": el.description, "containers": []}
        elif el.type in ["Container", "Database"]:
            if el.parent and el.parent in systems:
                systems[el.parent]["containers"].append(el)
            else:
                # Fallback se pai não definido: cria sistema dummy
                if "GenericSystem" not in systems:
                    systems["GenericSystem"] = {
                        "desc": "Holder for orphans", "containers": []}
                systems["GenericSystem"]["containers"].append(el)

    # Escrever People
    for p in people:
        dsl += p + "\n"

    # Escrever Systems e Containers
    for sys_name, data in systems.items():
        sys_var = sys_name.replace(" ", "")
        dsl += f'        {sys_var} = softwareSystem "{sys_name}" "{data["desc"]}" {{\n'

        for cont in data["containers"]:
            cont_var = cont.name.replace(" ", "")
            tech = cont.technology if cont.technology else "Unspecified"
            type_decl = "container"
            dsl += f'            {cont_var} = {type_decl} "{cont.name}" "{cont.description}" "{tech}"\n'

        dsl += "        }\n"

    dsl += """    }

    views {
        systemContext softwareSystem {
            include *
            autoLayout
        }
        
        # Adicione container views aqui se houver containers
        
        styles {
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "Person" {
                shape Person
                background #08427b
                color #ffffff
            }
            element "Container" {
                background #438dd5
                color #ffffff
            }
            element "Database" {
                shape Cylinder
            }
        }
    }
}
"""
    return dsl


class ValidationInput(BaseModel):
    hierarchy: dict = Field(
        ..., description="Dict representando a árvore: {System: {Container: [Components]}}")


@mcp.tool()
def validate_c4_hierarchy(input_data: ValidationInput) -> str:
    """
    Valida logicamente se a estrutura respeita as regras de abstração do C4.
    Ex: Componente fora de Container é inválido.
    """
    errors = []
    structure = input_data.hierarchy

    # Regra 1: Raiz deve ser Software System ou Contexto
    for system, containers in structure.items():
        if not isinstance(containers, dict):
            # Se for apenas uma lista ou string, assume-se que parou no nível System (OK)
            continue

        # Regra 2: Containers contém Componentes
        for container, components in containers.items():
            if not isinstance(components, list):
                errors.append(
                    f"❌ Estrutura inválida em '{container}': Containers devem conter uma lista de Componentes.")

            # Regra 3: Componentes são folhas (neste validador simples)
            # Se tentarem aninhar mais coisas dentro de components, avisar que é nível Code
            for comp in components:
                if isinstance(comp, dict):
                    errors.append(
                        f"⚠️ Aviso em '{comp}': C4 para no nível Componente. Detalhes internos pertencem ao nível Code (Classes).")

    if not errors:
        return "✅ Estrutura C4 Válida! A hierarquia System -> Container -> Component está correta."

    return "\n".join(errors)

# --- Prompts ---


@mcp.prompt()
def design_system_architecture(requirements: str) -> str:
    """
    Prompt Sistêmico: Guia o LLM para atuar como Arquiteto C4.
    """
    return f"""
    Você é um Arquiteto de Software Especialista no Modelo C4 (Simon Brown).
    Analise os requisitos abaixo e proponha uma arquitetura seguindo os 4 níveis.
    
    Requisitos do Usuário:
    "{requirements}"
    
    Sua tarefa:
    1. **Nível Contexto**: Identifique o Sistema, Usuários e Sistemas Externos.
    2. **Nível Container**: Exploda o sistema principal em Containers (Web App, API, DB, Mobile, Microservices). Defina tecnologias.
    3. **Nível Componente**: Escolha UM Container complexo e liste seus componentes principais (Controllers, Services, Repositories).
    
    Saída Obrigatória:
    - Explicação textual da decisão arquitetural.
    - Chamada sugerida para a ferramenta `generate_structurizr_dsl` ou `generate_mermaid_c4` com os dados identificados.
    """

# --- Resources ---


@mcp.resource("docs://c4-levels")
def get_c4_guide() -> str:
    return C4_LEVELS_INFO


@mcp.resource("docs://mermaid-syntax")
def get_mermaid_c4_syntax() -> str:
    return """
    Mermaid C4 Syntax Guide:
    - Person(alias, label, desc)
    - System(alias, label, desc)
    - Container(alias, label, desc, tech)
    - Component(alias, label, desc, tech)
    - Rel(from, to, label, tech)
    
    Use 'C4Context', 'C4Container', 'C4Component' as diagram types.
    """


if __name__ == "__main__":
    mcp.run()
