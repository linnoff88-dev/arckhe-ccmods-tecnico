# Estado â€” atualizado 2026-10-05 18:45

## Funciona
- SPEC (context/SPEC.md) com mapa congelado 4Ã—4Ã—6 e comandos Tier A rodados aqui.
- Gerador copiado do curso-agent-runtime (montar/lint/checar-navegador), courseId ccmt; lint com checagem anti-invenÃ§Ã£o de API.
- Modelo context/corpos/modulo-1-1.html â†’ LINT OK.
- 16 mÃ³dulos + 4 Ã­ndices + landing escritos; LINT OK; checar-navegador 42/42; exemplos de cÃ³digo extraÃ­dos e validados (claude plugin validate) â€” os que falham sÃ£o trechos rotulados ou o exemplo propositalmente errado da pegadinha 1.
- Capa (flux, cena temÃ¡tica). Repo linnoff88-dev/ccmods-tecnico publicado (05a9576), Pages via Actions configurado.

## Falta
- Prompts de entrevista (ARCKHÉ-mods + prompts-prontos): ver ~/projetos/output/cursos-mods/CONTINUAR-PROMPTS-ENTREVISTA.md
- Pages no ar (incidente do GitHub Actions: runners nÃ£o alocam; vigia em scratchpad/vigia-pages.sh redispara). Depois: portal (curso em platformsData + trilha ðŸ–¥ï¸ Claude Code + updatesData + enrichment curso:ccmods-tecnico).
- PendÃªncias paralelas desta sessÃ£o:
  - claude-mods-starter-kit: Pages travado no incidente do GitHub Actions; redisparado run 37368206172. Depois: registrar EN/ES em portal/src/data/translated-courses.ts.
  - curso-agent-runtime no portal: patch em /tmp/claude-1000/-home-nmaldaner-projetos-wifi/d9283068-d105-468a-b00a-a8d64c3b4f42/scratchpad/portal-agent-runtime.patch â€” aplicar sÃ³ quando https://linnoff88-dev.github.io/ der 200 (Pages legacy dele tambÃ©m travado). Outra sessÃ£o traduz esse curso (en/, i18n/ nÃ£o commitados) â€” nÃ£o mexer no repo.
  - Curso bÃ¡sico v6: o usuÃ¡rio precisa invocar /formato-curso-v6 sozinho (skill bloqueada para o modelo). Brief: ~/projetos/output/cursos-mods/BRIEF.md.

## Como retomar
```
cd ~/projetos/ccmods-tecnico
python3 scripts/montar.py && python3 scripts/lint.py
```
