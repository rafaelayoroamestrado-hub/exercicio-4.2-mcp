import httpx
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("tarefas-mcp")
API = "http://localhost:8000"
@mcp.tool()
async def criar_tarefa(titulo: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API}/tarefas", json={"titulo": titulo}, timeout=10)
        resp.raise_for_status()
        return resp.json()
@mcp.tool()
async def listar_tarefas() -> list:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API}/tarefas", timeout=10)
        resp.raise_for_status()
        return resp.json()
if __name__ == "__main__":
    mcp.run(transport="stdio")
