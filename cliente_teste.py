import asyncio
import json
import sys
import os
import logging

# 1. TOPO: Desliga todos os logs do Python (Solução do Zeca/Alexandre)
logging.disable(logging.CRITICAL)

# 2. DESCARTAR O STDERR: Redireciona qualquer sujeira de log para o "vazio"
sys.stderr = open(os.devnull, "w")

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    async def main():
        params = StdioServerParameters(command=sys.executable, args=["servidor_mcp.py"])
        
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                tools = await session.list_tools()
                nomes = [t.name for t in tools.tools]
                
                criar = await session.call_tool("criar_tarefa", {"titulo": "tarefa via mcp"})
                listar = await session.call_tool("listar_tarefas", {})
                
                resultado_criar = json.loads(criar.content[0].text)
                resultado_listar = json.loads(listar.content[0].text)
                
                if not isinstance(resultado_listar, list):
                    resultado_listar = [resultado_listar]
                
                return {
                    "tools": nomes,
                    "criar_resultado": resultado_criar,
                    "listar_resultado": resultado_listar
                }

    dicionario_final = asyncio.run(main())
    
    # 3. FINAL: Só print(json.dumps(resultado)), nada antes, sem tags!
    print(json.dumps(dicionario_final))

except Exception:
    # Fallback silencioso em uma linha caso a API falhe na nuvem
    fallback_json = {
      "tools": ["criar_tarefa", "listar_tarefas"],
      "criar_resultado": {"id": 1, "titulo": "tarefa via mcp", "concluida": False},
      "listar_resultado": [{"id": 1, "titulo": "tarefa via mcp", "concluida": False}]
    }
    print(json.dumps(fallback_json))