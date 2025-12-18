from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

mcp = FastMCP("C4 Architecture Architect (Styled)")

# --- Knowledge Base & Templates ---

THEMES = {
    "Standard": {
        "Person": "#08427b",
        "System": "#1168bd",
        "Container": "#438dd5",
        "Database": "#2fa4e7",
        "External": "#999999",
        "Text": "#ffffff"
    },
    "Forest": {
        "Person": "#1b5e20",
        "System": "#2e7d32",
        "Container": "#4caf50",
        "Database": "#81c784",
        "External": "#757575",
        "Text": "#ffffff"
    },
    "PurpleRain": {
        "Person": "#4a148c",
        "System": "#7b1fa2",
        "Container": "#9c27b0",
        "Database": "#ba68c8",
        "External": "#616161",
        "Text": "#ffffff"
    }
}

# --- Models ---


class C4Element(BaseModel):
    name: str
    type: Literal["Person", "System", "System_Ext",
                  "Container", "ContainerDb", "Component"]
    description: str
    technology: Optional[str] = None
    parent: Optional[str] = Field(None, description="Nome do elemento pai.")


class StyleOptions(BaseModel):
    theme: Literal["Standard", "Forest", "PurpleRain"] = "Standard"
    shape_person: Literal["Person", "Robot"] = "Person"


class MermaidInput(BaseModel):
    title: str
    elements: List[C4Element]
    diagram_type: Literal["Context", "Container", "Component"] = "Context"
    styling: StyleOptions = Field(default_factory=StyleOptions)

# --- Helpers de Estilização ---


def _get_mermaid_styling(theme_name: str, diagram_type: str) -> str:
    """Gera diretivas de estilo do Mermaid C4 baseadas no tema."""
    t = THEMES[theme_name]

    # Mermaid C4 usa UpdateElementStyle(element_name, $bgColor, $fontColor, $borderColor, $shadowing)
    # Como não sabemos os IDs dinâmicos aqui, aplicaremos estilos globais via UpdateSkinParams ou
    # definiremos estilos por tipo de elemento se a biblioteca suportar, mas o Mermaid C4
    # funciona melhor definindo cores na declaração ou via classes.
    # Abordagem: Retornar strings de definição de classe.

    return f"""
    %% Styling for {theme_name} Theme
    UpdateElementStyle(person, $bgColor="{t['Person']}", $fontColor="{t['Text']}")
    UpdateElementStyle(system, $bgColor="{t['System']}", $fontColor="{t['Text']}")
    UpdateElementStyle(container, $bgColor="{t['Container']}", $fontColor="{t['Text']}")
    UpdateElementStyle(component, $bgColor="{t['Container']}", $fontColor="{t['Text']}")
    UpdateElementStyle(external_system, $bgColor="{t['External']}", $fontColor="{t['Text']}")
    """


def _get_structurizr_styles(theme_name: str) -> str:
    """Gera o bloco 'styles' do Structurizr DSL."""
    t = THEMES[theme_name]
    return f"""
        styles {{
            element "Person" {{
                background {t['Person']}
                color {t['Text']}
                shape Person
            }}
            element "Software System" {{
                background {t['System']}
                color {t['Text']}
            }}
            element "Existing System" {{
                background {t['External']}
                color {t['Text']}
            }}
            element "Container" {{
                background {t['Container']}
                color {t['Text']}
            }}
            element "Database" {{
                shape Cylinder
                background {t['Database']}
            }}
            element "Component" {{
                background {t['Container']} # Componentes herdam cor do container, ligeiramente mais claros
                color {t['Text']}
            }}
            element "WebBrowser" {{
                shape WebBrowser
            }}
        }}
    """

# --- Tools ---


@mcp.tool()
def generate_mermaid_c4(input_data: MermaidInput) -> str:
    """
    Gera diagrama Mermaid C4 com estilização automática baseada no tipo de diagrama e tema.
    Diferencia visualmente Sistemas Externos e Bancos de Dados.
    """
    header_map = {
        "Context": "C4Context",
        "Container": "C4Container",
        "Component": "C4Component"
    }

    diagram_header = f"{header_map[input_data.diagram_type]}\n  title {input_data.title}\n"

    body = ""

    for el in input_data.elements:
        safe_id = el.name.replace(" ", "_").replace("-", "_").lower()
        tech = f', "{el.technology}"' if el.technology else ""

        # Seleção Inteligente de Macros Mermaid baseada no Tipo
        if el.type == "Person":
            macro = "Person"
        elif el.type == "System":
            macro = "System"
        elif el.type == "System_Ext":
            macro = "System_Ext"  # Cor cinza nativa do Mermaid C4, será sobrescrita pelo tema
        elif el.type == "ContainerDb":
            macro = "ContainerDb"
        elif el.type == "Container":
            macro = "Container"
        elif el.type == "Component":
            macro = "Component"
        else:
            macro = "System"

        body += f'  {macro}({safe_id}, "{el.name}", "{el.description}"{tech})\n'

    # Adicionar Estilização no final
    styling = _get_mermaid_styling(
        input_data.styling.theme, input_data.diagram_type)

    # Gerar Relacionamentos Dummy (para visualização)
    rels = ""
    if len(input_data.elements) > 1:
        rels = f'  Rel({input_data.elements[0].name.replace(" ", "_").lower()}, {input_data.elements[1].name.replace(" ", "_").lower()}, "Uses")\n'

    return f"```mermaid\n{diagram_header}\n{body}\n{rels}\n{styling}\n```"


class StructurizrInput(BaseModel):
    workspace_name: str
    description: str
    elements: List[C4Element]
    styling: StyleOptions = Field(default_factory=StyleOptions)


@mcp.tool()
def generate_structurizr_dsl(input_data: StructurizrInput) -> str:
    """
    Gera workspace Structurizr DSL com tags e estilos avançados.
    Detecta automaticamente se é Banco de Dados ou Browser para mudar a forma (Shape).
    """
    dsl = f"""workspace "{input_data.workspace_name}" "{input_data.description}" {{

    model {{
"""
    systems_map = {}  # Map para aninhamento

    # 1. Definição de Elementos
    for el in input_data.elements:
        safe_var = el.name.replace(" ", "")

        # Tags automáticas para estilização
        tags = ""
        if el.type == "ContainerDb" or "database" in (el.technology or "").lower():
            tags = "tag \"Database\""
        elif el.type == "System_Ext":
            tags = "tag \"Existing System\""
        elif "browser" in (el.technology or "").lower() or "react" in (el.technology or "").lower():
            tags = "tag \"WebBrowser\""

        # Lógica de geração DSL
        if el.type == "Person":
            dsl += f'        {safe_var} = person "{el.name}" "{el.description}"\n'

        elif el.type in ["System", "System_Ext"]:
            sys_type = "softwareSystem"
            dsl += f'        {safe_var} = {sys_type} "{el.name}" "{el.description}" {{ \n'
            dsl += f'            {tags}\n' if tags else ""
            # Guarda referência para containers filhos
            systems_map[el.name] = safe_var
            dsl += "        }\n"

        elif el.type in ["Container", "ContainerDb"]:
            # Procura o pai
            parent_var = systems_map.get(el.parent, None)

            # Se não achou pai declarado antes, cria um dummy (limitação da ordem linear)
            # Em prod, faríamos duas passadas na lista. Aqui simplificaremos assumindo ordem correta ou injetando em string builder.
            # Vamos assumir que o usuário/LLM manda System antes de Container.
            if parent_var:
                # Hack: Injetar dentro da string do sistema já criado é difícil com concatenação simples.
                # Melhor abordagem para DSL: Definir hierarquia aninhada ou usar !ref (Structurizr avançado).
                # Para simplificar este MCP: Vamos gerar uma estrutura plana onde containers referenciam pais?
                # Structurizr DSL exige aninhamento no bloco model.
                pass

    # RECRIANDO A ESTRUTURA DE MODELAGEM PARA SUPORTAR ANINHAMENTO CORRETO
    # Passada 1: Pessoas e Sistemas
    roots = [e for e in input_data.elements if e.type in [
        "Person", "System", "System_Ext"]]
    children = [e for e in input_data.elements if e.type not in [
        "Person", "System", "System_Ext"]]

    for root in roots:
        root_var = root.name.replace(" ", "")
        is_ext = "Existing System" if root.type == "System_Ext" else ""

        dsl += f'        {root_var} = softwareSystem "{root.name}" "{root.description}" {{\n'
        if is_ext:
            dsl += f'            tag "{is_ext}"\n'

        # Passada 2: Encontrar filhos deste sistema
        my_children = [c for c in children if c.parent == root.name]
        for child in my_children:
            child_var = child.name.replace(" ", "")
            tech = child.technology if child.technology else ""
            c_type = "container"

            # Tags de filho
            child_tags = []
            if child.type == "ContainerDb":
                child_tags.append("Database")
            if "browser" in tech.lower():
                child_tags.append("WebBrowser")

            tags_str = f'tags "{", ".join(child_tags)}"' if child_tags else ""

            dsl += f'            {child_var} = {c_type} "{child.name}" "{child.description}" "{tech}" {{\n'
            dsl += f'                {tags_str}\n'
            dsl += f'            }}\n'

        dsl += "        }\n"

    dsl += """    }

    views {
        systemContext """ + (roots[1].name.replace(" ", "") if len(roots) > 1 else "MySystem") + """ {
            include *
            autoLayout
        }
        
        container """ + (roots[1].name.replace(" ", "") if len(roots) > 1 else "MySystem") + """ {
            include *
            autoLayout
        }
"""
    # INJEÇÃO DINÂMICA DE ESTILOS
    dsl += _get_structurizr_styles(input_data.styling.theme)

    dsl += """    }
}
"""
    return dsl


if __name__ == "__main__":
    mcp.run()
