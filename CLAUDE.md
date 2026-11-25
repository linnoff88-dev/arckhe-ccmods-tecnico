# CLAUDE.md ê¢â¬â ccmods-tecnico

Curso "Mods do Claude Code ê¢â¬â o curso têÂ©cnico" no formato `formato-curso-v2` (4 trilhas êâ 4 mêÂ³dulos êâ 6 têÂ³picos). courseId `ccmt`.

- Regras, mapa congelado e comandos permitidos: `context/SPEC.md`. Todo comando e todo nome de API do curso tem de existir (Tier A rodado em 05/10/2026 no Claude Code 2.1.289, ou na referêÂªncia oficial / docs dos kits).
- As pêÂ¡ginas sêÂ£o **montadas**: edite `context/corpos/*.html` e rode `python3 scripts/montar.py` e `python3 scripts/lint.py` (precisa `LINT OK`; o lint confere `$.noun.mêÂ©todo`, `on('evento'` e subcomandos `claude` contra o `claude-code.d.ts` 2.1.289). NêÂ£o edite `curso/**/*.html` nem `index.html` êÂ  mêÂ£o.
- Fontes: referêÂªncia `plugin-authoring` do Claude Code, `~/projetos/claude-mods-starter-kit` (Prompt Advisers, MIT ê¢â¬â dar crêÂ©dito) e `~/projetos/ARCKHê-mods`. NêÂ£o editar os kits.
- Sem API externa sem autorizaêÂ§êÂ£o explêÂ­cita.
- Conta git: `linnoff88-dev <linnoff88-dev@gmail.com>`. Publicar = push; GitHub Pages via Actions (raiz).

## Self-learning

When I correct you, or you catch yourself making a mistake: before continuing, add the lesson as a one-line rule under ## Lessons, so it never happens again.

## Lessons

- Agentes paralelos copiam do modelo congelado (`context/corpos/modulo-1-1.html`) por marcador de texto, nunca por nêÂºmero de linha; ninguêÂ©m edita o modelo durante o lote.
