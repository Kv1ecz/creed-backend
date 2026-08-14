"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

CHECKLIST DE REVISÃO (ADR-002, secao 2.4):
  [ ] Autogenerate foi lido linha a linha?
  [ ] Renomeação virou drop+create? (perde dados — corrigir para op.alter_column)
  [ ] Mudança destrutiva foi dividida em passos (adicionar -> migrar -> remover)?
  [ ] `alembic heads` conferido antes de abrir o PR?
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

revision: str = ${repr(up_revision)}
down_revision: str | None = ${repr(down_revision)}
branch_labels: str | Sequence[str] | None = ${repr(branch_labels)}
depends_on: str | Sequence[str] | None = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
