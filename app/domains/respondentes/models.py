"""Models SQLAlchemy do domínio respondentes.

Coleta de dados demográficos (Termo de Abertura: densidade demográfica,
gênero, idade, região).
"""

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Respondente(Base):
    __tablename__ = "respondentes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    data_nascimento: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Recortes usados nas análises comparativas (ADR-001, secao 4.1)
    genero: Mapped[str | None] = mapped_column(String(50), nullable=True)
    regiao: Mapped[str | None] = mapped_column(String(100), nullable=True)
    pais: Mapped[str | None] = mapped_column(String(2), nullable=True)  # ISO 3166-1

    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
