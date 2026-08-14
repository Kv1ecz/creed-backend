"""Wiring de injeção de dependência do domínio (ADR-002, secao 2.3).

Usa o sistema Depends nativo do FastAPI para montar a cadeia
repository -> service, mantendo o router livre de construção de objetos.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.respondentes.repository import RespondenteRepository
from app.domains.respondentes.service import RespondenteService


def get_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RespondenteRepository:
    return RespondenteRepository(db)


def get_service(
    repository: Annotated[RespondenteRepository, Depends(get_repository)],
) -> RespondenteService:
    return RespondenteService(repository)


ServiceDep = Annotated[RespondenteService, Depends(get_service)]
