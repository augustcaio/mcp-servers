from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("Angular Renaissance Expert")

# --- Knowledge Base (Baseada em angular.dev) ---

SIGNALS_GUIDE = """
ANGULAR SIGNALS CHEATSHEET (v17+):
1. State: `count = signal(0);` -> Read: `count()` -> Update: `count.set(1)` or `count.update(v => v + 1)`.
2. Computed: `double = computed(() => this.count() * 2);`
3. Effects: `effect(() => console.log(this.count()));`
4. Inputs: `name = input.required<string>();` (Replaces @Input)
5. Outputs: `submit = output<void>();` (Replaces @Output + EventEmitter)
6. Model: `checked = model(false);` (Two-way binding signal)
Ref: https://angular.dev/guide/signals
"""

CONTROL_FLOW_GUIDE = """
NEW CONTROL FLOW SYNTAX:
1. If:
   @if (loggedIn()) { <user-profile /> } 
   @else if (loading()) { <spinner /> } 
   @else { <login-form /> }

2. For:
   @for (item of items(); track item.id) {
     <li>{{ item.name }}</li>
   } @empty {
     <li>No items found</li>
   }

3. Switch:
   @switch (status()) {
     @case ('active') { <active-badge /> }
     @default { <unknown-badge /> }
   }
Ref: https://angular.dev/guide/templates/control-flow
"""

STYLE_GUIDE_2025 = """
MODERN ANGULAR STYLE GUIDE:
1. Standalone: Always true. No NgModules unless strictly necessary for legacy.
2. Change Detection: Always `OnPush`. Rely on Signals or AsyncPipe.
3. Lazy Loading: Use `loadComponent` in routes.
4. DI: Use `inject(Service)` instead of constructor injection.
5. Defer: Use `@defer (on viewport)` for heavy components.
"""

# --- Tools ---


class ComponentInput(BaseModel):
    name: str = Field(..., description="Nome do componente (ex: UserProfile).")
    selector: str = Field(...,
                          description="Seletor HTML (ex: app-user-profile).")
    use_signals: bool = Field(
        True, description="Usar inputs/outputs baseados em Signals?")
    include_template: bool = Field(
        True, description="Incluir template HTML inline ou arquivo separado?")


@mcp.tool()
def scaffold_modern_component(input_data: ComponentInput) -> str:
    """
    Gera um Componente Angular seguindo os padrões 'Renaissance' (v18+).
    Standalone, OnPush, inject(), e Signals Inputs.
    """
    class_name = input_data.name.replace(
        "-", " ").title().replace(" ", "") + "Component"
    selector = input_data.selector

    # Imports modernos
    imports = ["Component", "ChangeDetectionStrategy"]
    if input_data.use_signals:
        imports.extend(["input", "output", "signal"])
    else:
        imports.extend(["Input", "Output", "EventEmitter"])  # Legacy fallback

    imports_str = ", ".join(sorted(imports))

    # Template lógico
    template_code = ""
    if input_data.include_template:
        template_code = """
  template: `
    <section class="container">
      @if (loading()) {
        <p>Loading...</p>
      } @else {
        <h1>{{ title() }}</h1>
        <button (click)="handleClick()">Action</button>
      }
    </section>
  `,"""
    else:
        template_code = f"  templateUrl: './{input_data.name.lower()}.component.html',"

    # Corpo da classe
    class_body = ""
    if input_data.use_signals:
        class_body = """
  // Modern Signal Inputs/Outputs
  title = input.required<string>();
  isActive = input(false);
  actionTriggered = output<void>();
  
  // Internal State
  loading = signal(false);

  handleClick() {
    this.loading.set(true);
    this.actionTriggered.emit();
  }
"""
    else:
        class_body = """
  // Legacy Decorators (Avoid if possible)
  @Input({ required: true }) title!: string;
  @Output() actionTriggered = new EventEmitter<void>();
"""

    code = f"""
import {{ {imports_str} }} from '@angular/core';
import {{ CommonModule }} from '@angular/common';

@Component({{
  selector: '{selector}',
  standalone: true,
  imports: [CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush,{template_code}
  styleUrl: './{input_data.name.lower()}.component.scss'
}})
export class {class_name} {{
{class_body}
}}
"""
    return f"🚀 **Modern Angular Component Generated:**\n```typescript\n{code}\n```"


class MigrationInput(BaseModel):
    legacy_template: str = Field(...,
                                 description="Snippet de template usando *ngIf ou *ngFor.")


@mcp.tool()
def convert_to_control_flow(input_data: MigrationInput) -> str:
    """
    Converte templates Angular antigos (Diretivas Estruturais) para a nova sintaxe de Control Flow (@if, @for).
    """
    content = input_data.legacy_template

    # Lógica simples de substituição (em um cenário real, usaria AST, mas para LLM + Regex funciona bem como hint)
    # Convertendo *ngIf
    # *ngIf="cond" -> @if (cond) { ... }
    # Nota: Esta é uma simplificação ilustrativa. A IA é melhor lendo e reescrevendo do que regex puro.
    explanation = """
    🔄 **MIGRATION PLAN:**
    
    1. `*ngIf="condition"`  ➡️  `@if (condition) { ... }`
    2. `*ngFor="let item of list"` ➡️ `@for (item of list; track item.id) { ... }`
       ⚠️ *Nota: O novo @for EXIGE uma expressão 'track'. Certifique-se de adicionar `track item.id` ou `track $index`.*
    3. `*ngSwitch` ➡️ `@switch`
    """

    prompt_reinforcement = f"""
    Eu (o servidor) detectei que você quer migrar este código. 
    Use o seu conhecimento de LLM para reescrever o seguinte bloco aplicando a sintaxe explicada acima:
    
    ```html
    {content}
    ```
    """

    return f"{explanation}\n\n{prompt_reinforcement}"


class RouteInput(BaseModel):
    path: str
    component_name: str


@mcp.tool()
def generate_lazy_route(input_data: RouteInput) -> str:
    """
    Gera configuração de rota usando Lazy Loading moderno (loadComponent).
    """
    return f"""
    🛣️ **Modern Route Configuration:**
    
    {{
      path: '{input_data.path}',
      loadComponent: () => import('./{input_data.path}/{input_data.component_name}.component')
        .then(m => m.{input_data.component_name}Component),
      title: '{input_data.component_name}' 
    }}
    
    *Dica Sênior: Se estiver usando default export (menos comum em Angular, mas possível), o .then pode ser omitido dependendo da config.*
    """

# --- Prompts ---


@mcp.prompt()
def review_angular_pr(code: str) -> str:
    """
    Prompt Sênior para Code Review focado em Angular v17/18+.
    Critica uso de NgModules, *ngIf e falta de tipagem estrita.
    """
    return f"""
    Atue como um Google Developer Expert (GDE) em Angular. Revise o código abaixo.
    
    Regras de Ouro (Angular Renaissance):
    1. **Signals**: O código usa `signal()`, `input()`, `computed()`? Se usar RxJS `BehaviorSubject` para estado síncrono, sugira refatoração.
    2. **Control Flow**: Se houver `*ngIf` ou `*ngFor`, marque como "Depreciado/Legado" e sugira `@if`/`@for`.
    3. **Standalone**: Verifique se o componente é `standalone: true`. Se houver `NgModule`, questione a necessidade.
    4. **Change Detection**: Se não houver `changeDetection: ChangeDetectionStrategy.OnPush`, aponte como problema de performance.
    5. **Injection**: O uso de `inject(MyService)` é preferido sobre construtores.
    
    Código para revisão:
    ```typescript
    {code}
    ```
    """


@mcp.prompt()
def angular_architect_design(feature_description: str) -> str:
    """
    Ajuda a desenhar a estrutura de pastas e serviços para uma feature.
    """
    return f"""
    Com base na documentação oficial (angular.dev), proponha uma arquitetura para a feature: "{feature_description}".
    
    Estrutura Esperada:
    - Feature-sliced ou Nx-style folders.
    - Componentes "Smart" (Container) vs "Dumb" (UI).
    - Uso de Services para lógica de negócios (State Management com Signals).
    - Definição de rotas com Lazy Loading.
    """

# --- Resources ---


@mcp.resource("docs://angular-signals")
def get_signals_docs() -> str:
    return SIGNALS_GUIDE


@mcp.resource("docs://angular-control-flow")
def get_control_flow_docs() -> str:
    return CONTROL_FLOW_GUIDE


@mcp.resource("docs://angular-style-guide")
def get_style_guide() -> str:
    return STYLE_GUIDE_2025


if __name__ == "__main__":
    mcp.run()
