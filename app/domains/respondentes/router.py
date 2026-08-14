"""Endpoints HTTP do domínio respondentes (ADR-002, secao 2.2).

Esta camada é fina de propósito: recebe, valida via Pydantic, delega ao
service e devolve. Nenhuma regra de negócio aqui.
"""

import uuid

from fastapi import APIRouter, HTTPException, Query, status

from app.domains.respondentes.dependencies import ServiceDep
from app.domains.respondentes.models import Respondente
from app.domains.respondentes.schemas import (
    RespondenteCreate,
    RespondenteListResponse,
    RespondenteResponse,
    RespondenteUpdate,
)
from app.domains.respondentes.service import calcular_idade
from app.shared.exceptions import ConflictError, NotFoundError

router = APIRouter(prefix="/respondentes", tags=["respondentes"])


def _to_response(respondente: Respondente) -> RespondenteResponse:
    resposta = RespondenteResponse.model_validate(respondente)
    resposta.idade = calcular_idade(respondente.data_nascimento)
    return resposta


@router.get("", response_model=RespondenteListResponse)
async def listar_respondentes(
    service: ServiceDep,
    pagina: int = Query(default=1, ge=1),
    tamanho_pagina: int = Query(default=50, ge=1, le=200),
    pais: str | None = Query(default=None, min_length=2, max_length=2),
    regiao: str | None = Query(default=None),
) -> RespondenteListResponse:
    itens, total = await service.listar(
        pagina=pagina, tamanho_pagina=tamanho_pagina, pais=pais, regiao=regiao
    )
    return RespondenteListResponse(
        itens=[_to_response(item) for item in itens],
        total=total,
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
    )


@router.get("/{respondente_id}", response_model=RespondenteResponse)
async def obter_respondente(
    respondente_id: uuid.UUID, service: ServiceDep
) -> RespondenteResponse:
    try:
        return _to_response(await service.obter(respondente_id))
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, exc.message) from exc


@router.post("", response_model=RespondenteResponse, status_code=status.HTTP_201_CREATED)
async def criar_respondente(
    dados: RespondenteCreate, service: ServiceDep
) -> RespondenteResponse:
    try:
        return _to_response(await service.criar(dados))
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, exc.message) from exc


@router.patch("/{respondente_id}", response_model=RespondenteResponse)
async def atualizar_respondente(
    respondente_id: uuid.UUID, dados: RespondenteUpdate, service: ServiceDep
) -> RespondenteResponse:
    try:
        return _to_response(await service.atualizar(respondente_id, dados))
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, exc.message) from exc
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, exc.message) from exc


@router.delete("/{respondente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_respondente(respondente_id: uuid.UUID, service: ServiceDep) -> None:
    try:
        await service.remover(respondente_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, exc.message) from exc
