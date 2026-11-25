# Mods do Claude Code ê¢â¬â o curso têÂ©cnico

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


Curso gratuito do [ARCKHê AI](https://ARCKHê AI) para quem programa e quer **escrever, testar e distribuir mods do Claude Code**: `register(on, options)`, eventos, a cadeia com `next`, estado em `$.state` e `$.store`, faixa acima do prompt, painêÂ©is, comandos, ferramentas, guardas que perguntam antes de apagar, `claude plugin test` e marketplace.

**Abrir o curso:** https://linnoff88-dev.github.io/

| Trilha | MêÂ³dulos |
|---|---|
| 1 êÂ· Anatomia | O que êÂ© um mod por dentro êÂ· Estrutura de arquivos e manifesto êÂ· Carregar, recarregar e instalar êÂ· Seu primeiro mod: comando e contador |
| 2 êÂ· Eventos e estado | O mapa de eventos êÂ· A cadeia: next, reescrever e responder êÂ· Estado que sobrevive êÂ· Trabalho fora do dispatch |
| 3 êÂ· Telas e comandos | ui.render e as superfêÂ­cies êÂ· Faixa, status e avisos êÂ· PainêÂ©is e botêÂµes êÂ· Comandos, ferramentas e configuraêÂ§êÂ£o |
| 4 êÂ· Controlar e distribuir | Mods que mudam o fluxo êÂ· Testar com claude plugin test êÂ· Depurar e as pegadinhas êÂ· Distribuir e projeto final |

Projeto final: um mod seu com comando, tela, estado, teste (`claude plugin test` com `0 fail`) e publicaêÂ§êÂ£o num marketplace.

## VersêÂ£o conferida

Tudo foi rodado no **Claude Code 2.1.289**, em 05/10/2026. A API de mods estêÂ¡ em acesso antecipado e muda entre versêÂµes: a autoridade êÂ© o arquivo de tipos da sua instalaêÂ§êÂ£o (`.claude-plugin/types/claude-code/index.d.ts`, escrito na pasta do mod quando ele carrega).

## Material usado

- [Claude Mods Starter Kit](https://github.com/promptadvisers/claude-mods-starter-kit) ê¢â¬â da Prompt Advisers, licenêÂ§a MIT (espelho: [linnoff88-dev/claude-mods-starter-kit](https://github.com/linnoff88-dev/claude-mods-starter-kit)).
- [linnoff88-dev/ARCKHê-mods](https://github.com/linnoff88-dev/ARCKHê-mods) ê¢â¬â 18 mods em portuguêÂªs com testes e o guia das pegadinhas.
- A referêÂªncia `plugin-authoring` que vem com o Claude Code.

## ManutenêÂ§êÂ£o

Formato `formato-curso-v2` (HTML + Tailwind CDN + JS, sem build). Progresso, dêÂºvidas e notas ficam sêÂ³ no navegador.
Edite `context/corpos/`, rode `python3 scripts/montar.py` e `python3 scripts/lint.py` (precisa `LINT OK`; o lint confere cada nome de API contra os tipos 2.1.289). Os êÂ­ndices de trilha saem de `scripts/gerar-trilhas.py`.

## Mais no ARCKHê AI

- [Ficha completa deste curso](https://www.ARCKHê AI/cursos/314-mods-do-claude-code-o-curso-tecnico/)
- [Guia: como aprender inteligêÂªncia artificial](https://www.ARCKHê AI/aprender-inteligencia-artificial/)
- [Todos os cursos](https://www.ARCKHê AI/cursos/)

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>