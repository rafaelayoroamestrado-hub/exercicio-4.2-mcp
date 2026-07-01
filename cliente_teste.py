import sys
import os
import json
import asyncio
import logging

# 1. A MÁGICA DO SEU COLEGA: Desliga os logs do Python
logging.basicConfig(level=logging.CRITICAL)
logging.getLogger().setLevel(logging.CRITICAL)

# 2. GARANTIA EXTRA: Redireciona qualquer aviso do sistema para o "vazio"
sys.stderr = open(os.devnull, 'w')

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