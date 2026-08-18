#!/bin/sh
# Avisa antes de empurrar uma branch fora do padrão (CONTRIBUTING.md).
# Rodado pelo pre-commit no estágio de pre-push.
# É conveniência, não garantia: --no-verify passa por cima. A garantia é o
# check "nome-da-branch", obrigatório no PR.
# O padrão abaixo é o mesmo de .github/workflows/nome-da-branch.yml.

branch="$(git symbolic-ref --short HEAD 2>/dev/null)" || exit 0

case "$branch" in
main | dev) exit 0 ;;
esac

padrao='^(feat|fix|refactor|perf|test|docs|style|chore|ci|build|hotfix|release)/[a-z0-9]*[0-9][a-z0-9]*-[a-z][a-z0-9]*(-[a-z0-9]+)*$'

if printf '%s' "$branch" | grep -Eq "$padrao"; then
  exit 0
fi

cat >&2 <<AJUDA

Nome de branch fora do padrão: $branch

  Esperado: <slug>/<id-clickup>-<contexto>
  Exemplo:  feat/1-criar-usuarios

  Slugs: feat fix refactor perf test docs style chore ci build hotfix release
  O ID precisa ter pelo menos um dígito; tudo em minúsculas, sem acento.

Renomeie antes de empurrar:

  git branch -m feat/1-criar-usuarios

Detalhes em CONTRIBUTING.md.

AJUDA
exit 1
