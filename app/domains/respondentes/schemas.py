"""Schemas Pydantic do domínio respondentes.

Separados por direção (ADR-002, secao 2.3): entrada e saída não se contaminam.
"""

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RespondenteBase(BaseModel):
    nome: str = Field(min_length=2, max_length=200)
    email: EmailStr
    data_nascimento: date | None = None
    genero: str | None = Field(default=None, max_length=50)
    regiao: str | None = Field(default=None, max_length=100)
    pais: str | None = Field(default=None, min_length=2, max_length=2)


class RespondenteCreate(RespondenteBase):
    """Payload de criação."""


class RespondenteUpdate(BaseModel):
    """Payload de atualização parcial — todos os campos opcionais."""

    nome: str | None = Field(default=None, min_length=2, max_length=200)
    email: EmailStr | None = None
    data_nascimento: date | None = None
    genero: str | None = Field(default=None, max_length=50)
    regiao: str | None = Field(default=None, max_length=100)
    pais: str | None = Field(default=None, min_length=2, max_length=2)


class RespondenteResponse(RespondenteBase):
    """Representação de saída."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    idade: int | None = None
    criado_em: datetime


class RespondenteListResponse(BaseModel):
    itens: list[RespondenteResponse]
    total: int
    pagina: int
    tamanho_pagina: int
