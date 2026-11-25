# Goal ê¢â¬â curso-v2 (ccmods-tecnico)

- **InêÂ­cio:** 2026-10-05 17:09 êÂ· **Agente:** Claude (sessêÂ£o interativa) + 5 subagentes
- **Tetos:** tempo 4 h êÂ· sem API paga êÂ· Codex sêÂ³ pela assinatura (traduêÂ§êÂ£o, se fizer)

## Resultado
Curso v2 "Mods do Claude Code ê¢â¬â o curso têÂ©cnico" publicado em linnoff88-dev.github.io/ e cadastrado no portal (trilha ê°Å¸âÂ¥ê¯Â¸Â Claude Code).

## CritêÂ©rios de pronto
**FunêÂ§êÂ£o**
- [ ] `python3 scripts/montar.py && python3 scripts/lint.py` ê¢â â `LINT OK` (16 mêÂ³dulos êâ 6 têÂ³picos, 4 êÂ­ndices com 24 têÂ³picos, landing; checagem de API contra o d.ts 2.1.289)
- [ ] `node scripts/checar-navegador.cjs http://127.0.0.1:<porta> pt` (NODE_PATH=~/projetos/agent-browser/node_modules) ê¢â â 0 erros de pêÂ¡gina, 0 overflow em 360 px
- [ ] `curl -s -o /dev/null -w '%{http_code}' https://linnoff88-dev.github.io/ ê¢â â `200`
**RegressêÂ£o**
- [ ] `context/corpos/modulo-1-1.html` sem mudanêÂ§a depois do lote (modelo congelado): `git diff --stat <commit-modelo> -- context/corpos/modulo-1-1.html` ê¢â â vazio
**Limite**
- [ ] nada editado em ~/projetos/ARCKHê-mods nem ~/projetos/claude-mods-starter-kit (`git -C ê¢â¬Â¦ status --short` igual ao inêÂ­cio)
- [ ] portal: sêÂ³ as linhas do curso (courses.ts, Portal.tsx trilha Claude Code, courses.data.json)

**Teste rêÂ¡pido por ciclo**: `LINT_SEM_LINKS=1 python3 scripts/lint.py <arquivo>`
**Teste completo no final**: lint completo + checar-navegador
