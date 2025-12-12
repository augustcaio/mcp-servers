#!/bin/bash
# Script de instalação do MCP Server para Cursor

set -e

echo "🚀 Instalando dependências do sistema..."
sudo apt install -y python3-pip python3-venv

echo "📦 Criando ambiente virtual..."
cd "$(dirname "$0")"
python3 -m venv venv

echo "🔧 Instalando dependências Python..."
source venv/bin/activate
pip install --upgrade pip
pip install "mcp[cli]" pydantic autopep8

echo "✅ Instalação concluída!"
echo ""
echo "📝 Configuração do MCP já foi criada em ~/.cursor/mcp.json"
echo "🔄 Reinicie o Cursor para carregar o servidor MCP"
echo ""
echo "🧪 Para testar, execute:"
echo "   source venv/bin/activate"
echo "   python server.py"

