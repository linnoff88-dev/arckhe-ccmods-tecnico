# CLAUDE.md â€” ccmods-tecnico

Curso "Mods do Claude Code â€” o curso tÃ©cnico" no formato `formato-curso-v2` (4 trilhas Ã— 4 mÃ³dulos Ã— 6 tÃ³picos). courseId `ccmt`.

- Regras, mapa congelado e comandos permitidos: `context/SPEC.md`. Todo comando e todo nome de API do curso tem de existir (Tier A rodado em 05/10/2026 no Claude Code 2.1.289, ou na referÃªncia oficial / docs dos kits).
- As pÃ¡ginas sÃ£o **montadas**: edite `context/corpos/*.html` e rode `python3 scripts/montar.py` e `python3 scripts/lint.py` (precisa `LINT OK`; o lint confere `$.noun.mÃ©todo`, `on('evento'` e subcomandos `claude` contra o `claude-code.d.ts` 2.1.289). NÃ£o edite `curso/**/*.html` nem `index.html` Ã  mÃ£o.
- Fontes: referÃªncia `plugin-authoring` do Claude Code, `~/projetos/claude-mods-starter-kit` (Prompt Advisers, MIT â€” dar crÃ©dito) e `~/projetos/ARCKHÉ-mods`. NÃ£o editar os kits.
- Sem API externa sem autorizaÃ§Ã£o explÃ­cita.
- Conta git: `linnoff88-dev <linnoff88-dev@gmail.com>`. Publicar = push; GitHub Pages via Actions (raiz).

## Self-learning

When I correct you, or you catch yourself making a mistake: before continuing, add the lesson as a one-line rule under ## Lessons, so it never happens again.

## Lessons

- Agentes paralelos copiam do modelo congelado (`context/corpos/modulo-1-1.html`) por marcador de texto, nunca por nÃºmero de linha; ninguÃ©m edita o modelo durante o lote.
