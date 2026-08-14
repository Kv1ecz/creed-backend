"""Acesso a dados do domínio respondentes (ADR-002, secao 2.2).

Esta camada NÃO contém regra de negócio: só queries e agregações.
Agregação pesada é empurrada para o Postgres, nunca feita em memória.
"""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.respondentes.models import Respondente


class RespondenteRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, respondente_id: uuid.UUID) -> Respondente | None:
        result = await self.db.execute(
            select(Respondente).where(Respondente.id == respondente_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Respondente | None:
        result = await self.db.execute(
            select(Respondente).where(Respondente.email == email)
        )
        return result.scalar_one_or_none()

    async def list_paginated(
        self,
        *,
        offset: int = 0,
        limit: int = 50,
        pais: str | None = None,
        regiao: str | None = None,
    ) -> tuple[list[Respondente], int]:
        """Lista com filtros de recorte usados nas análises comparativas."""
        stmt = select(Respondente)
        count_stmt = select(func.count()).select_from(Respondente)

        if pais:
            stmt = stmt.where(Respondente.pais == pais)
            count_stmt = count_stmt.where(Respondente.pais == pais)
        if regiao:
            stmt = stmt.where(Respondente.regiao == regiao)
            count_stmt = count_stmt.where(Respondente.regiao == regiao)

        stmt = stmt.order_by(Respondente.criado_em.desc()).offset(offset).limit(limit)

        result = await self.db.execute(stmt)
        total = (await self.db.execute(count_stmt)).scalar_one()
        return list(result.scalars().all()), total

    async def create(self, respondente: Respondente) -> Respondente:
        self.db.add(respondente)
        await self.db.flush()
        await self.db.refresh(respondente)
        return respondente

    async def delete(self, respondente: Respondente) -> None:
        await self.db.delete(respondente)
        await self.db.flush()
