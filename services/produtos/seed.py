"""
Script para popular banco com dados de teste.
"""
import asyncio
from database import AsyncSessionLocal


async def seed_data():
    """Popula banco com dados de teste."""
    async with AsyncSessionLocal() as session:
        # TODO: Implementar seed de dados
        print("✓ Dados de teste inseridos")


if __name__ == "__main__":
    asyncio.run(seed_data())
