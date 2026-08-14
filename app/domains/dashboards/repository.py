"""Acesso a dados do domínio dashboards — o entregável focal (ADR-001, secao 4.1).

REGRA DE OURO: agregação no banco, cálculo no service, renderização no front.
As análises comparativas (indivíduo / organização / região / país sobre os
5 prismas) devem usar GROUP BY, GROUPING SETS e window functions — NUNCA
trazer linhas cruas para agregar em memória.

Exemplo do padrão esperado:

    stmt = (
        select(
            Avaliacao.pais,
            Prisma.codigo,
            func.avg(Avaliacao.score).label("media"),
            func.count().label("n"),
        )
        .join(Prisma)
        .group_by(Avaliacao.pais, Prisma.codigo)
    )
"""
