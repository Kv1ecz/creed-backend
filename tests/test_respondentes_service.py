"""Testes do service de respondentes.

Demonstra o ganho da separação de camadas do ADR-002: a regra de negócio
é testável sem HTTP e sem banco — exatamente o que permitirá testar o
cálculo dos 5 prismas isoladamente.
"""

from datetime import date

import pytest

from app.domains.respondentes.service import calcular_idade


class TestCalcularIdade:
    def test_retorna_none_sem_data(self) -> None:
        assert calcular_idade(None) is None

    def test_idade_apos_aniversario(self) -> None:
        assert calcular_idade(date(1990, 1, 15), hoje=date(2026, 6, 10)) == 36

    def test_idade_antes_do_aniversario(self) -> None:
        assert calcular_idade(date(1990, 12, 15), hoje=date(2026, 6, 10)) == 35

    def test_idade_no_dia_do_aniversario(self) -> None:
        assert calcular_idade(date(1990, 6, 10), hoje=date(2026, 6, 10)) == 36

    @pytest.mark.parametrize(
        ("nascimento", "hoje", "esperado"),
        [
            (date(2000, 2, 29), date(2026, 2, 28), 25),
            (date(2000, 2, 29), date(2026, 3, 1), 26),
        ],
    )
    def test_ano_bissexto(self, nascimento: date, hoje: date, esperado: int) -> None:
        assert calcular_idade(nascimento, hoje=hoje) == esperado
