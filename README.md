# Mods do Claude Code â€” o curso tÃ©cnico

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


Curso gratuito do [INEMA.CLUB](https://inema.club) para quem programa e quer **escrever, testar e distribuir mods do Claude Code**: `register(on, options)`, eventos, a cadeia com `next`, estado em `$.state` e `$.store`, faixa acima do prompt, painÃ©is, comandos, ferramentas, guardas que perguntam antes de apagar, `claude plugin test` e marketplace.

**Abrir o curso:** https://inematds.github.io/ccmods-tecnico/

| Trilha | MÃ³dulos |
|---|---|
| 1 Â· Anatomia | O que Ã© um mod por dentro Â· Estrutura de arquivos e manifesto Â· Carregar, recarregar e instalar Â· Seu primeiro mod: comando e contador |
| 2 Â· Eventos e estado | O mapa de eventos Â· A cadeia: next, reescrever e responder Â· Estado que sobrevive Â· Trabalho fora do dispatch |
| 3 Â· Telas e comandos | ui.render e as superfÃ­cies Â· Faixa, status e avisos Â· PainÃ©is e botÃµes Â· Comandos, ferramentas e configuraÃ§Ã£o |
| 4 Â· Controlar e distribuir | Mods que mudam o fluxo Â· Testar com claude plugin test Â· Depurar e as pegadinhas Â· Distribuir e projeto final |

Projeto final: um mod seu com comando, tela, estado, teste (`claude plugin test` com `0 fail`) e publicaÃ§Ã£o num marketplace.

## VersÃ£o conferida

Tudo foi rodado no **Claude Code 2.1.289**, em 05/10/2026. A API de mods estÃ¡ em acesso antecipado e muda entre versÃµes: a autoridade Ã© o arquivo de tipos da sua instalaÃ§Ã£o (`.claude-plugin/types/claude-code/index.d.ts`, escrito na pasta do mod quando ele carrega).

## Material usado

- [Claude Mods Starter Kit](https://github.com/promptadvisers/claude-mods-starter-kit) â€” da Prompt Advisers, licenÃ§a MIT (espelho: [inematds/claude-mods-starter-kit](https://github.com/inematds/claude-mods-starter-kit)).
- [inematds/inema-mods](https://github.com/inematds/inema-mods) â€” 18 mods em portuguÃªs com testes e o guia das pegadinhas.
- A referÃªncia `plugin-authoring` que vem com o Claude Code.

## ManutenÃ§Ã£o

Formato `formato-curso-v2` (HTML + Tailwind CDN + JS, sem build). Progresso, dÃºvidas e notas ficam sÃ³ no navegador.
Edite `context/corpos/`, rode `python3 scripts/montar.py` e `python3 scripts/lint.py` (precisa `LINT OK`; o lint confere cada nome de API contra os tipos 2.1.289). Os Ã­ndices de trilha saem de `scripts/gerar-trilhas.py`.

## Mais no INEMA.CLUB

- [Ficha completa deste curso](https://www.inema.club/cursos/314-mods-do-claude-code-o-curso-tecnico/)
- [Guia: como aprender inteligÃªncia artificial](https://www.inema.club/aprender-inteligencia-artificial/)
- [Todos os cursos](https://www.inema.club/cursos/)

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>