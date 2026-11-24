# Goal â€” curso-v2 (ccmods-tecnico)

- **InÃ­cio:** 2026-10-05 17:09 Â· **Agente:** Claude (sessÃ£o interativa) + 5 subagentes
- **Tetos:** tempo 4 h Â· sem API paga Â· Codex sÃ³ pela assinatura (traduÃ§Ã£o, se fizer)

## Resultado
Curso v2 "Mods do Claude Code â€” o curso tÃ©cnico" publicado em linnoff88-dev.github.io/ e cadastrado no portal (trilha ðŸ–¥ï¸ Claude Code).

## CritÃ©rios de pronto
**FunÃ§Ã£o**
- [ ] `python3 scripts/montar.py && python3 scripts/lint.py` â†’ `LINT OK` (16 mÃ³dulos Ã— 6 tÃ³picos, 4 Ã­ndices com 24 tÃ³picos, landing; checagem de API contra o d.ts 2.1.289)
- [ ] `node scripts/checar-navegador.cjs http://127.0.0.1:<porta> pt` (NODE_PATH=~/projetos/agent-browser/node_modules) â†’ 0 erros de pÃ¡gina, 0 overflow em 360 px
- [ ] `curl -s -o /dev/null -w '%{http_code}' https://linnoff88-dev.github.io/ â†’ `200`
**RegressÃ£o**
- [ ] `context/corpos/modulo-1-1.html` sem mudanÃ§a depois do lote (modelo congelado): `git diff --stat <commit-modelo> -- context/corpos/modulo-1-1.html` â†’ vazio
**Limite**
- [ ] nada editado em ~/projetos/ARCKHÉ-mods nem ~/projetos/claude-mods-starter-kit (`git -C â€¦ status --short` igual ao inÃ­cio)
- [ ] portal: sÃ³ as linhas do curso (courses.ts, Portal.tsx trilha Claude Code, courses.data.json)

**Teste rÃ¡pido por ciclo**: `LINT_SEM_LINKS=1 python3 scripts/lint.py <arquivo>`
**Teste completo no final**: lint completo + checar-navegador
