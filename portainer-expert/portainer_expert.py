from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
import requests
from requests.auth import HTTPBasicAuth

# Inicialização do Servidor
mcp = FastMCP("Portainer Expert")

# --- Knowledge Base (Baseada em docs.portainer.io) ---

PORTAINER_ARCHITECTURE = """
PORTAINER ARCHITECTURE (docs.portainer.io):
- Portainer CE: Community Edition - open source, Docker/Swarm/Kubernetes/Azure ACI
- Portainer BE: Business Edition - comercial, adiciona RBAC, registry management, suporte dedicado
- Suporta múltiplos ambientes: Docker, Docker Swarm, Kubernetes, Podman, Azure ACI, Nomad
- Interface web para gerenciar containers sem CLI
- API REST completa para automação
"""

PORTAINER_BEST_PRACTICES = """
PORTAINER BEST PRACTICES:
1. Autenticação: Use JWT tokens para API calls (obtido via /api/auth)
2. Ambientes: Adicione ambientes Docker/Kubernetes via UI ou API
3. Stacks: Use Docker Compose para definir aplicações multi-container
4. Volumes: Use named volumes para persistência de dados
5. Networks: Crie networks isoladas para diferentes aplicações
6. Segurança: Configure RBAC (Business Edition) para controle de acesso
7. Edge Agents: Use Edge Agents para ambientes remotos
"""

# --- Models ---


class PortainerAuthInput(BaseModel):
    url: str = Field(..., description="URL do Portainer (ex: http://localhost:9000)")
    username: str = Field(..., description="Usuário do Portainer")
    password: str = Field(..., description="Senha do Portainer")


class PortainerContainerInput(BaseModel):
    portainer_url: str = Field(..., description="URL do Portainer")
    jwt_token: str = Field(..., description="JWT token de autenticação")
    endpoint_id: int = Field(..., description="ID do ambiente Docker")
    container_id: Optional[str] = Field(None, description="ID do container (opcional)")


class PortainerStackInput(BaseModel):
    portainer_url: str = Field(..., description="URL do Portainer")
    jwt_token: str = Field(..., description="JWT token de autenticação")
    endpoint_id: int = Field(..., description="ID do ambiente Docker")
    stack_name: str = Field(..., description="Nome da stack")
    compose_file: str = Field(..., description="Conteúdo do docker-compose.yml")


class PortainerVolumeInput(BaseModel):
    portainer_url: str = Field(..., description="URL do Portainer")
    jwt_token: str = Field(..., description="JWT token de autenticação")
    endpoint_id: int = Field(..., description="ID do ambiente Docker")
    volume_name: Optional[str] = Field(None, description="Nome do volume")


class PortainerImageInput(BaseModel):
    portainer_url: str = Field(..., description="URL do Portainer")
    jwt_token: str = Field(..., description="JWT token de autenticação")
    endpoint_id: int = Field(..., description="ID do ambiente Docker")
    image_name: Optional[str] = Field(None, description="Nome da imagem (opcional)")


class PortainerNetworkInput(BaseModel):
    portainer_url: str = Field(..., description="URL do Portainer")
    jwt_token: str = Field(..., description="JWT token de autenticação")
    endpoint_id: int = Field(..., description="ID do ambiente Docker")
    network_name: Optional[str] = Field(None, description="Nome da network")


class PortainerContainerActionInput(BaseModel):
    portainer_url: str = Field(..., description="URL do Portainer")
    jwt_token: str = Field(..., description="JWT token de autenticação")
    endpoint_id: int = Field(..., description="ID do ambiente Docker")
    container_id: str = Field(..., description="ID do container")
    action: Literal["start", "stop", "restart", "remove"] = Field(
        ..., description="Ação a executar"
    )


# --- Tools (Ferramentas) ---


@mcp.tool()
def authenticate_portainer(input_data: PortainerAuthInput) -> str:
    """
    Autentica no Portainer e retorna o JWT token para uso em outras operações.
    Baseado na documentação oficial: https://docs.portainer.io/api/authentication
    """
    url = f"{input_data.url.rstrip('/')}/api/auth"
    
    try:
        response = requests.post(
            url,
            json={"Username": input_data.username, "Password": input_data.password},
            timeout=10
        )
        
        if response.status_code == 200:
            token = response.json().get("jwt")
            return f"✅ Autenticação bem-sucedida!\n\nToken JWT: {token}\n\n⚠️ Guarde este token para usar nas outras operações."
        else:
            return f"❌ Erro na autenticação: {response.status_code}\n{response.text}"
    except Exception as e:
        return f"❌ Erro ao conectar ao Portainer: {str(e)}"


@mcp.tool()
def list_containers(input_data: PortainerContainerInput) -> str:
    """
    Lista todos os containers no ambiente Docker especificado.
    Baseado em: https://docs.portainer.io/api/containers
    """
    url = f"{input_data.portainer_url.rstrip('/')}/api/endpoints/{input_data.endpoint_id}/docker/containers/json"
    headers = {"Authorization": f"Bearer {input_data.jwt_token}"}
    
    try:
        response = requests.get(url, headers=headers, params={"all": True}, timeout=10)
        
        if response.status_code == 200:
            containers = response.json()
            if not containers:
                return "📦 Nenhum container encontrado neste ambiente."
            
            result = f"📦 **Containers encontrados ({len(containers)}):**\n\n"
            for container in containers:
                names = ", ".join([name.lstrip("/") for name in container.get("Names", [])])
                status = container.get("Status", "Unknown")
                image = container.get("Image", "Unknown")
                container_id = container.get("Id", "")[:12]
                
                result += f"- **{names}**\n"
                result += f"  - ID: `{container_id}`\n"
                result += f"  - Status: {status}\n"
                result += f"  - Imagem: {image}\n\n"
            
            return result
        else:
            return f"❌ Erro ao listar containers: {response.status_code}\n{response.text}"
    except Exception as e:
        return f"❌ Erro ao conectar ao Portainer: {str(e)}"


@mcp.tool()
def container_action(input_data: PortainerContainerActionInput) -> str:
    """
    Executa ações em containers: start, stop, restart ou remove.
    Baseado em: https://docs.portainer.io/api/containers
    """
    action_map = {
        "start": "start",
        "stop": "stop",
        "restart": "restart",
        "remove": "remove"
    }
    
    action_endpoint = action_map[input_data.action]
    url = f"{input_data.portainer_url.rstrip('/')}/api/endpoints/{input_data.endpoint_id}/docker/containers/{input_data.container_id}/{action_endpoint}"
    headers = {"Authorization": f"Bearer {input_data.jwt_token}"}
    
    try:
        if input_data.action == "remove":
            response = requests.delete(url, headers=headers, params={"force": True}, timeout=10)
        else:
            response = requests.post(url, headers=headers, timeout=10)
        
        if response.status_code in [200, 204, 304]:
            return f"✅ Container {input_data.container_id[:12]} {input_data.action} executado com sucesso!"
        else:
            return f"❌ Erro ao executar ação: {response.status_code}\n{response.text}"
    except Exception as e:
        return f"❌ Erro ao conectar ao Portainer: {str(e)}"


@mcp.tool()
def list_stacks(input_data: PortainerStackInput) -> str:
    """
    Lista todas as stacks (Docker Compose) no ambiente especificado.
    Baseado em: https://docs.portainer.io/api/stacks
    """
    url = f"{input_data.portainer_url.rstrip('/')}/api/stacks"
    headers = {"Authorization": f"Bearer {input_data.jwt_token}"}
    
    try:
        response = requests.get(url, headers=headers, params={"filters": f'{{"EndpointID":{input_data.endpoint_id}}}'}, timeout=10)
        
        if response.status_code == 200:
            stacks = response.json()
            if not stacks:
                return "📚 Nenhuma stack encontrada neste ambiente."
            
            result = f"📚 **Stacks encontradas ({len(stacks)}):**\n\n"
            for stack in stacks:
                name = stack.get("Name", "Unknown")
                status = stack.get("Status", "Unknown")
                stack_id = stack.get("Id", "Unknown")
                
                result += f"- **{name}**\n"
                result += f"  - ID: {stack_id}\n"
                result += f"  - Status: {status}\n\n"
            
            return result
        else:
            return f"❌ Erro ao listar stacks: {response.status_code}\n{response.text}"
    except Exception as e:
        return f"❌ Erro ao conectar ao Portainer: {str(e)}"


@mcp.tool()
def create_stack(input_data: PortainerStackInput) -> str:
    """
    Cria uma nova stack usando Docker Compose.
    Baseado em: https://docs.portainer.io/api/stacks
    """
    url = f"{input_data.portainer_url.rstrip('/')}/api/stacks"
    headers = {
        "Authorization": f"Bearer {input_data.jwt_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "Name": input_data.stack_name,
        "StackFileContent": input_data.compose_file,
        "EndpointID": input_data.endpoint_id,
        "Type": 1  # 1 = Docker Compose, 2 = Docker Swarm
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code in [200, 201]:
            stack_data = response.json()
            return f"✅ Stack '{input_data.stack_name}' criada com sucesso!\n\nID: {stack_data.get('Id')}"
        else:
            return f"❌ Erro ao criar stack: {response.status_code}\n{response.text}"
    except Exception as e:
        return f"❌ Erro ao conectar ao Portainer: {str(e)}"


@mcp.tool()
def list_volumes(input_data: PortainerVolumeInput) -> str:
    """
    Lista todos os volumes Docker no ambiente especificado.
    Baseado em: https://docs.portainer.io/api/volumes
    """
    url = f"{input_data.portainer_url.rstrip('/')}/api/endpoints/{input_data.endpoint_id}/docker/volumes"
    headers = {"Authorization": f"Bearer {input_data.jwt_token}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            volumes_data = response.json()
            volumes = volumes_data.get("Volumes", [])
            
            if not volumes:
                return "💾 Nenhum volume encontrado neste ambiente."
            
            result = f"💾 **Volumes encontrados ({len(volumes)}):**\n\n"
            for volume in volumes:
                name = volume.get("Name", "Unknown")
                driver = volume.get("Driver", "local")
                mountpoint = volume.get("Mountpoint", "Unknown")
                
                result += f"- **{name}**\n"
                result += f"  - Driver: {driver}\n"
                result += f"  - Mountpoint: {mountpoint}\n\n"
            
            return result
        else:
            return f"❌ Erro ao listar volumes: {response.status_code}\n{response.text}"
    except Exception as e:
        return f"❌ Erro ao conectar ao Portainer: {str(e)}"


@mcp.tool()
def list_images(input_data: PortainerImageInput) -> str:
    """
    Lista todas as imagens Docker no ambiente especificado.
    Baseado em: https://docs.portainer.io/api/images
    """
    url = f"{input_data.portainer_url.rstrip('/')}/api/endpoints/{input_data.endpoint_id}/docker/images/json"
    headers = {"Authorization": f"Bearer {input_data.jwt_token}"}
    
    try:
        response = requests.get(url, headers=headers, params={"all": True}, timeout=10)
        
        if response.status_code == 200:
            images = response.json()
            if not images:
                return "🖼️ Nenhuma imagem encontrada neste ambiente."
            
            result = f"🖼️ **Imagens encontradas ({len(images)}):**\n\n"
            for image in images:
                repo_tags = image.get("RepoTags", ["<none>:<none>"])
                image_id = image.get("Id", "")[:12]
                size = image.get("Size", 0)
                size_mb = size / (1024 * 1024)
                
                result += f"- **{repo_tags[0]}**\n"
                result += f"  - ID: `{image_id}`\n"
                result += f"  - Tamanho: {size_mb:.2f} MB\n\n"
            
            return result
        else:
            return f"❌ Erro ao listar imagens: {response.status_code}\n{response.text}"
    except Exception as e:
        return f"❌ Erro ao conectar ao Portainer: {str(e)}"


@mcp.tool()
def list_networks(input_data: PortainerNetworkInput) -> str:
    """
    Lista todas as networks Docker no ambiente especificado.
    Baseado em: https://docs.portainer.io/api/networks
    """
    url = f"{input_data.portainer_url.rstrip('/')}/api/endpoints/{input_data.endpoint_id}/docker/networks"
    headers = {"Authorization": f"Bearer {input_data.jwt_token}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            networks = response.json()
            if not networks:
                return "🌐 Nenhuma network encontrada neste ambiente."
            
            result = f"🌐 **Networks encontradas ({len(networks)}):**\n\n"
            for network in networks:
                name = network.get("Name", "Unknown")
                driver = network.get("Driver", "bridge")
                scope = network.get("Scope", "local")
                
                result += f"- **{name}**\n"
                result += f"  - Driver: {driver}\n"
                result += f"  - Scope: {scope}\n\n"
            
            return result
        else:
            return f"❌ Erro ao listar networks: {response.status_code}\n{response.text}"
    except Exception as e:
        return f"❌ Erro ao conectar ao Portainer: {str(e)}"


# --- Resources (Documentação) ---


@mcp.resource("docs://portainer-architecture")
def get_portainer_architecture() -> str:
    """Retorna informações sobre a arquitetura do Portainer."""
    return PORTAINER_ARCHITECTURE


@mcp.resource("docs://portainer-best-practices")
def get_portainer_best_practices() -> str:
    """Retorna melhores práticas para usar o Portainer."""
    return PORTAINER_BEST_PRACTICES


# --- Prompts (Templates de Raciocínio) ---


@mcp.prompt()
def deploy_application(compose_content: str) -> str:
    """
    Prompt que guia o LLM a ajudar na implantação de uma aplicação usando Portainer.
    """
    return f"""
    Você é um especialista em Portainer (docs.portainer.io).
    Sua tarefa é ajudar a implantar uma aplicação usando Docker Compose no Portainer.
    
    REGRAS IMPORTANTES:
    1. Primeiro, autentique no Portainer usando `authenticate_portainer` para obter o JWT token
    2. Identifique o endpoint_id do ambiente Docker onde deseja implantar
    3. Use `create_stack` para criar a stack com o conteúdo do docker-compose.yml
    4. Monitore o status usando `list_stacks` e `list_containers`
    
    Conteúdo do docker-compose.yml:
    ```
    {compose_content}
    ```
    
    Forneça instruções passo a passo para implantar esta aplicação no Portainer.
    """


@mcp.prompt()
def troubleshoot_container(container_id: str, issue_description: str) -> str:
    """
    Prompt que guia o LLM a ajudar na resolução de problemas com containers.
    """
    return f"""
    Você é um especialista em Portainer e Docker.
    Sua tarefa é ajudar a resolver problemas com um container.
    
    Container ID: {container_id}
    Descrição do Problema: {issue_description}
    
    SUGESTÕES DE DIAGNÓSTICO:
    1. Liste os containers para verificar o status: `list_containers`
    2. Verifique os logs do container (use a API do Portainer)
    3. Verifique recursos: CPU, memória, disco
    4. Verifique networks e volumes associados
    5. Considere reiniciar o container: `container_action` com action="restart"
    
    Forneça um plano de ação para diagnosticar e resolver o problema.
    """


if __name__ == "__main__":
    mcp.run()
