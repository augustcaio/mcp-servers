# ⚡ Angular Renaissance Expert MCP Server

Um servidor MCP (Model Context Protocol) especializado em **Angular Renaissance** (v17+), oferecendo ferramentas para desenvolvimento moderno com Signals, Control Flow, Standalone Components e melhores práticas do Angular.

## ✨ Funcionalidades

### 🔧 Ferramentas Disponíveis

| Ferramenta | Descrição |
|------------|-----------|
| `scaffold_modern_component` | Gera componente Angular moderno seguindo padrões Renaissance (Standalone, OnPush, Signals) |
| `convert_to_control_flow` | Converte templates antigos (*ngIf, *ngFor) para nova sintaxe de Control Flow (@if, @for) |
| `generate_lazy_route` | Gera configuração de rota usando Lazy Loading moderno (loadComponent) |

### 📚 Recursos (Resources)

- `docs://angular-signals` - Guia completo de Signals (signal, computed, effect, input, output, model)
- `docs://angular-control-flow` - Sintaxe moderna de Control Flow (@if, @for, @switch)
- `docs://angular-style-guide` - Guia de estilo moderno Angular 2025

### 💡 Prompts

- `review_angular_pr` - Code Review focado em Angular v17/18+ com padrões Renaissance
- `angular_architect_design` - Ajuda a desenhar arquitetura de features seguindo padrões modernos

## 🚀 Instalação

### Pré-requisitos

- Python 3.12+
- pip

### Setup

1. Clone o repositório ou navegue até a pasta:
```bash
cd angular-renaissance-expert
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
    "angular-renaissance-expert": {
      "command": "/caminho/para/venv/bin/python3",
      "args": [
        "/caminho/para/angular-renaissance-expert/angular_expert.py"
      ]
    }
  }
}
```

## 🧪 Testando o Servidor

### Modo Desenvolvimento (Interface Web)
```bash
mcp dev angular_expert.py
```

### Modo Produção (stdio)
```bash
mcp run angular_expert.py
```

## 📖 Exemplos de Uso

### Gerando um Componente Moderno

A ferramenta `scaffold_modern_component` gera componentes seguindo padrões Renaissance:

**Input:**
- name: `UserProfile`
- selector: `app-user-profile`
- use_signals: `true`
- include_template: `true`

**Saída:**
```typescript
import { Component, ChangeDetectionStrategy, input, output, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user-profile',
  standalone: true,
  imports: [CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <section class="container">
      @if (loading()) {
        <p>Loading...</p>
      } @else {
        <h1>{{ title() }}</h1>
        <button (click)="handleClick()">Action</button>
      }
    </section>
  `,
  styleUrl: './userprofile.component.scss'
})
export class UserProfileComponent {
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
}
```

### Convertendo Control Flow

A ferramenta `convert_to_control_flow` ajuda a migrar templates antigos:

**Input:**
```html
<div *ngIf="user()">
  <ul>
    <li *ngFor="let item of items()">{{ item.name }}</li>
  </ul>
</div>
```

**Saída sugerida:**
```html
@if (user()) {
  <ul>
    @for (item of items(); track item.id) {
      <li>{{ item.name }}</li>
    } @empty {
      <li>No items found</li>
    }
  </ul>
}
```

### Gerando Rotas com Lazy Loading

A ferramenta `generate_lazy_route` gera configuração moderna:

**Input:**
- path: `users`
- component_name: `UserList`

**Saída:**
```typescript
{
  path: 'users',
  loadComponent: () => import('./users/user-list.component')
    .then(m => m.UserListComponent),
  title: 'UserList' 
}
```

## 🎯 Padrões Angular Renaissance

### Signals
- `signal()` para estado reativo
- `computed()` para valores derivados
- `effect()` para side effects
- `input()` e `output()` para comunicação entre componentes
- `model()` para two-way binding

### Control Flow
- `@if` / `@else` / `@else if` substitui `*ngIf`
- `@for` substitui `*ngFor` (requer `track`)
- `@switch` / `@case` / `@default` substitui `*ngSwitch`

### Standalone Components
- Sempre use `standalone: true`
- Evite NgModules a menos que necessário para legado
- Use `imports` diretamente no decorator `@Component`

### Change Detection
- Sempre use `ChangeDetectionStrategy.OnPush`
- Rely em Signals ou AsyncPipe para reatividade

### Dependency Injection
- Prefira `inject(Service)` sobre constructor injection
- Mais limpo e funcional

## 📁 Estrutura do Projeto

```
angular-renaissance-expert/
├── angular_expert.py      # Servidor MCP principal
├── pyproject.toml         # Configuração do projeto
├── README.md              # Este arquivo
└── .gitignore             # Arquivos ignorados pelo Git
```

## 🧠 Benefícios

### Desenvolvimento Moderno
- Gera código seguindo padrões mais recentes do Angular
- Evita padrões legados e depreciados
- Promove performance com OnPush e Signals

### Migração Facilitada
- Ajuda a migrar código legado para padrões modernos
- Converte diretivas estruturais para Control Flow
- Sugere refatorações baseadas em melhores práticas

### Code Review Inteligente
- Identifica uso de padrões legados
- Sugere melhorias de performance
- Valida arquitetura seguindo Angular Style Guide

## 🔗 Links Úteis

- [Angular.dev - Official Documentation](https://angular.dev/)
- [Angular Signals Guide](https://angular.dev/guide/signals)
- [Angular Control Flow](https://angular.dev/guide/templates/control-flow)
- [MCP Protocol](https://modelcontextprotocol.io/)

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feat/nova-feature`)
3. Commit suas mudanças usando Conventional Commits (`git commit -m 'feat: add nova feature'`)
4. Push para a branch (`git push origin feat/nova-feature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT.

