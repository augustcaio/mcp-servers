from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

mcp = FastMCP("C4 Ultimate Architect")

# --- Knowledge Base & Styles ---

THEMES = {
    "Standard": {"Person": "#08427b", "System": "#1168bd", "Container": "#438dd5", "Component": "#85bbf0", "Node": "#ffffff"},
    "Dark": {"Person": "#1e88e5", "System": "#1565c0", "Container": "#42a5f5", "Component": "#90caf9", "Node": "#424242"}
}

DOCS_C4_FULL = """
C4 MODEL FULL SPECIFICATION:
1. Context: Big picture (System + Users).
2. Container: Deployable units (API, DB, SPA).
3. Component: Internal building blocks (Controllers, Services).
4. Code: Class diagrams (UML).
+ Deployment: Mapping Containers to Infrastructure Nodes (AWS, Docker).
+ Dynamic: Runtime communication steps for a specific feature.
"""

# --- Models Unificados ---


class C4Element(BaseModel):
    id: str = Field(...,
                    description="Identificador único (sem espaços, ex: 'web_app').")
    name: str
    type: Literal[
        "Person", "System", "System_Ext",
        "Container", "ContainerDb",
        "Component",
        "DeploymentNode", "InfrastructureNode"
    ]
    description: str
    technology: Optional[str] = None
    parent_id: Optional[str] = Field(
        None, description="ID do elemento pai (ex: Componente pertence a Container).")


class Relationship(BaseModel):
    source_id: str
    target_id: str
    label: str
    technology: Optional[str] = None
    order: Optional[str] = Field(
        None, description="Para diagramas dinâmicos: '1', '2', '2.1'")


class StyleOptions(BaseModel):
    theme: Literal["Standard", "Dark"] = "Standard"

# --- Tool 1: Gerador de Diagramas Estruturais (Context, Container, Component, Deployment) ---


class StructuralDiagramInput(BaseModel):
    title: str
    view_type: Literal["Context", "Container", "Component", "Deployment"]
    elements: List[C4Element]
    relationships: List[Relationship] = []
    styling: StyleOptions = Field(default_factory=StyleOptions)


@mcp.tool()
def generate_c4_structural(input_data: StructuralDiagramInput) -> str:
    """
    Gera diagramas C4 estruturais (Níveis 1, 2, 3 e Implantação) usando Mermaid.js.
    Suporta aninhamento profundo (Boundary) para Components e Deployment Nodes.
    """
    t = input_data.view_type

    # Header Mapping
    if t == "Context": header = "C4Context"
    elif t == "Container": header = "C4Container"
    elif t == "Component": header = "C4Component"
    # Mermaid usa C4Context base com Nodes
    elif t == "Deployment": header = "C4Context"
    else: header = "C4Context"

    mermaid_code = f"```mermaid\n{header}\n  title {input_data.title}\n"

    # Mapeamento de Elementos por ID para facilitar hierarquia
    elements_map = {e.id: e for e in input_data.elements}
    children_map = {e.id: [] for e in input_data.elements}
    roots = []

    # Construir árvore
    for e in input_data.elements:
        if e.parent_id and e.parent_id in elements_map:
            children_map[e.parent_id].append(e)
        else:
            roots.append(e)

    # Função recursiva para desenhar (necessária para Componentes dentro de Containers dentro de Sistemas)
    def draw_node(element):
        code = ""
        children = children_map.get(element.id, [])

        # Definição de macros Mermaid
        tech = f', "{element.technology}"' if element.technology else ""

        # Se tem filhos, é um Boundary (Subgrafo)
        if children:
            boundary_type = "System_Boundary"
            if element.type == "Container": boundary_type = "Container_Boundary"
            if element.type == "DeploymentNode": boundary_type = "Node"

            code += f'  {boundary_type}({element.id}, "{element.name}") {{\n'
            for child in children:
                code += draw_node(child)
            code += "  }\n"
        else:
            # Elemento Folha
            macro_map = {
                "Person": "Person", "System": "System", "System_Ext": "System_Ext",
                "Container": "Container", "ContainerDb": "ContainerDb",
                "Component": "Component",
                "DeploymentNode": "Node", "InfrastructureNode": "Node"  # Fallback
            }
            macro = macro_map.get(element.type, "System")
            code += f'  {macro}({element.id}, "{element.name}", "{element.description}"{tech})\n'

        return code

    # Renderizar Elementos
    for root in roots:
        mermaid_code += draw_node(root)

    # Renderizar Relacionamentos
    for rel in input_data.relationships:
        tech_rel = f', "{rel.technology}"' if rel.technology else ""
        mermaid_code += f'  Rel({rel.source_id}, {rel.target_id}, "{rel.label}"{tech_rel})\n'

    # Estilização básica
    mermaid_code += _apply_theme(input_data.styling.theme)
    mermaid_code += "\n```"
    return mermaid_code

# --- Tool 2: Diagrama Dinâmico (Fluxos) ---


class DynamicDiagramInput(BaseModel):
    title: str
    elements: List[C4Element]
    steps: List[Relationship]
    styling: StyleOptions = Field(default_factory=StyleOptions)


@mcp.tool()
def generate_c4_dynamic(input_data: DynamicDiagramInput) -> str:
    """
    Gera um diagrama C4 Dinâmico.
    Foca na sequência de interações para uma funcionalidade específica.
    """
    mermaid_code = f"```mermaid\nC4Dynamic\n  title {input_data.title}\n"

    # Apenas declara os elementos envolvidos (sem hierarquia complexa visualmente)
    for e in input_data.elements:
        macro = "Container"  # Default para dynamic costuma ser Container ou Component
        if e.type == "Component": macro = "Component"
        elif e.type == "Person": macro = "Person"

        tech = f', "{e.technology}"' if e.technology else ""
        mermaid_code += f'  {macro}({e.id}, "{e.name}", "{e.technology or ""}", "{e.description}")\n'

    # Relacionamentos com índices
    for step in input_data.steps:
        idx = f'{step.order}: ' if step.order else ""
        mermaid_code += f'  Rel({step.source_id}, {step.target_id}, "{idx}{step.label}")\n'

    mermaid_code += _apply_theme(input_data.styling.theme)
    mermaid_code += "\n```"
    return mermaid_code

# --- Tool 3: Nível 4 - Código (Classes) ---


class ClassDiagramInput(BaseModel):
    title: str
    classes_code: str = Field(...,
                              description="Definição simplificada das classes/interfaces.")


@mcp.tool()
def generate_code_diagram(input_data: ClassDiagramInput) -> str:
    """
    Gera o Nível 4 (Code) usando Mermaid Class Diagram.
    Embora o C4 evite isso, às vezes é necessário para detalhes de Componentes.
    """
    return f"""```mermaid
classDiagram
    note "C4 Level 4: Code Diagram for {input_data.title}"
    {input_data.classes_code}
```"""


# --- Helper de Estilização ---

def _apply_theme(theme_name: str) -> str:
    """Aplica tema de cores ao diagrama Mermaid C4."""
    t = THEMES.get(theme_name, THEMES["Standard"])
    return f"""
    UpdateElementStyle(person, $bgColor="{t['Person']}", $fontColor="#ffffff")
    UpdateElementStyle(system, $bgColor="{t['System']}", $fontColor="#ffffff")
    UpdateElementStyle(container, $bgColor="{t['Container']}", $fontColor="#ffffff")
    UpdateElementStyle(component, $bgColor="{t['Component']}", $fontColor="#000000")
"""


# --- Resources ---

@mcp.resource("docs://c4-model")
def get_c4_docs() -> str:
    return DOCS_C4_FULL


if __name__ == "__main__":
    mcp.run()
