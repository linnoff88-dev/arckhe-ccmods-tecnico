# SPEC â€” Mods do Claude Code: curso tÃ©cnico (formato-curso-v2)

Curso ARCKHÉ AI (aberto e gratuito) para **quem programa** e quer escrever, testar e distribuir mods do Claude Code.
TÃ­tulo exato: **Mods do Claude Code â€” o curso tÃ©cnico**. courseId = `ccmt`. Repo `linnoff88-dev/ccmods-tecnico`.
Skill de formato: `~/.claude/skills/formato-curso-v2/` (erros crÃ­ticos #1â€“#31 valem).

## VersÃ£o e autoridade (dizer no curso)

- Tudo foi conferido no **Claude Code 2.1.289**, em **05/10/2026**, nesta mÃ¡quina (Linux ARM64).
- A API de mods estÃ¡ em **acesso antecipado e muda entre versÃµes**. A autoridade Ã© o arquivo de tipos da SUA instalaÃ§Ã£o: `.claude-plugin/types/claude-code/index.d.ts`, que o Claude Code escreve dentro da pasta do mod quando ele carrega por `--plugin-dir`/pasta de mods. O curso ensina a ler esse arquivo; nunca prometer que um nome vale para sempre.

## Fontes da verdade (ler Ã  vontade; NÃƒO editar nenhuma delas)

1. ReferÃªncia oficial (vem com o Claude Code): `/tmp/claude-1000/bundled-skills/2.1.289/4a690ea2f793d25136db54dac3d94b2a/plugin-authoring/reference.md` (182 linhas) e `.../plugin-authoring/examples/{band.tsx,band-state.d.ts,pane.tsx,pane-state.d.ts,tool-call.ts}`.
2. Tipos (20 422 linhas â€” use grep): `.../plugin-authoring/types/claude-code.d.ts`.
3. Kit da Prompt Advisers (MIT, **dar crÃ©dito**): `~/projetos/claude-mods-starter-kit` â€” 10 plugins em `plugins/`, `templates/starter-mod/`, `scripts/{check.sh,try.sh,manage.sh}`, `prompts/`, `.claude-plugin/marketplace.json`.
4. Kit ARCKHÉ: `~/projetos/ARCKHÉ-mods` â€” 18 mods em `mods/`, `docs/COMO-FAZER-UM-MOD.md` (estrutura, verificaÃ§Ã£o e **23 pegadinhas** â€” copiar o sentido, citar a fonte), `scripts/checar-mod.sh`, modelo `mods/recibo-sessao/`.

## PÃºblico e tom

- Programador ou quase: sabe usar terminal, jÃ¡ leu JavaScript/TypeScript, jÃ¡ usou o Claude Code. NÃ£o precisa conhecer a API de mods.
- Mesmo assim, cada termo da API Ã© definido na 1Âª vez (box "ðŸ†• Novo aqui?"): hook, `$`, `e`, `next`, dispatch, surface, noun, matcher, atom, store...
- Tom: direto, frases curtas, parÃ¡grafos de 2â€“4 linhas, sem coachzinho, portuguÃªs correto com acentos.
- NÃ£o citar criadores, canais ou vÃ­deos de terceiros. A Prompt Advisers aparece **sÃ³ como autora do kit** (crÃ©dito, MIT).
- Personagem fixo dos exemplos: **Rafa, 34, dev** de uma agÃªncia pequena, que quer ver o que o Claude toca no repositÃ³rio e nÃ£o perder trabalho entre sessÃµes.

## Forma do cÃ³digo (congelado)

- **Primeiro mod (T1)**: a forma do kit, `hooks/starter.mjs` com `export function register(on) {â€¦}` â€” sem compilaÃ§Ã£o, sem tipos.
- **A partir da T2**: a forma tipada dos exemplos oficiais e do ARCKHÉ-mods: `hooks/register.tsx` (ou `.ts`) com `import type { Register } from 'claude-code'` e `export const register: Register = (on, options) => {â€¦}`; JSX com `h` como fÃ¡brica; tipos de estado em `types/index.d.ts` apontado por `"types"` no `plugin.json`.
- Toda funÃ§Ã£o que recebe `$` Ã© declarada no topo do arquivo (pegadinha 1).

## VocabulÃ¡rio fixo (um nome por conceito)

- **mod** = plugin do Claude Code com *function hooks* (mÃ³dulo que exporta `register`). "Plugin" Ã© o pacote; "mod" Ã© o apelido.
- **hook** = funÃ§Ã£o `($, e, next)` registrada com `on(evento, matcher?, hook)`.
- **hook clÃ¡ssico** = os hooks de `settings.json` (comandos de shell, PreToolUse/PostToolUse...). No mod eles aparecem como eventos `classic.<Nome>`.
- **evento** = nome como `tool.call`; **noun** = a parte antes do ponto (`tool`, `ui`, `session`...).
- **cadeia** = os hooks de todos os plugins + o comportamento do prÃ³prio Claude Code, ligados por `next`.
- **dispatch** = uma passagem de um evento pela cadeia (tem orÃ§amento de tempo).
- **superfÃ­cie** = onde desenha: `terminal`, `desktop`, `mobile`, `vscode`.
- **faixa** = `AbovePrompt` (uma sÃ³, compartilhada); **painel** = `Pane`.

## COMANDOS PERMITIDOS (nenhum outro entra numa pÃ¡gina)

Tier A = rodado aqui em 05/10/2026, saÃ­da real abaixo (pode mostrar como saÃ­da).
Tier B = da referÃªncia oficial ou da documentaÃ§Ã£o dos kits (mostrar o comando; resultado como "esperado", sem inventar saÃ­da de terminal).

| Comando (verbatim) | Fonte | Tier | SaÃ­da / esperado |
|---|---|---|---|
| `claude --version` | â€” | A | `2.1.289 (Claude Code)` |
| `git clone https://github.com/linnoff88-dev/claude-mods-starter-kit` Â· `cd claude-mods-starter-kit` | README do kit | â€” | â€” |
| `git clone https://github.com/linnoff88-dev/ARCKHÉ-mods` Â· `cd ARCKHÉ-mods` | README ARCKHÉ-mods | â€” | â€” |
| `claude plugin validate templates/starter-mod` | kit | A | bloco VALIDATE |
| `claude plugin test templates/starter-mod` | kit | A | bloco TEST |
| `claude plugin validate <pasta-do-mod>` Â· `claude plugin test <pasta-do-mod>` | reference.md | A | `âœ” Validation passed` Â· `N pass` / `0 fail` |
| `bash scripts/check.sh` (kit) | kit | A | ver TABELA DO KIT â€” aqui parou no terminal-pet (teste de desempenho estourou 5 s) |
| `bash scripts/try.sh terminal-pet` | kit START-HERE | B | abre uma sessÃ£o temporÃ¡ria sÃ³ com o mod |
| `bash scripts/manage.sh install user all` Â· `bash scripts/manage.sh disable user all` | kit | B | â€” |
| `claude -p "/readcount" --plugin-dir templates/starter-mod` | kit | A | `read-counter-example: Successful reads observed: 0` |
| `claude -p "/recibo" --plugin-dir mods/recibo-sessao` | ARCKHÉ-mods | A | `recibo-sessao: Nesta sessÃ£o: nenhum arquivo criado ou alterado.` |
| `TSC=<caminho do tsc> scripts/checar-mod.sh mods/recibo-sessao` | ARCKHÉ-mods | A | bloco CHECAR |
| `claude --plugin-dir <pasta>` (repita a flag para vÃ¡rios) | reference.md | B | carrega sÃ³ nesta sessÃ£o; pasta vigiada (hot-reload) |
| `CLAUDE_CODE_PLUGIN_DIRS=<caminho absoluto>` | reference.md | B | igual ao `--plugin-dir`, para desktop/SDK |
| `CLAUDE_CODE_PLUGIN_DIR_WATCH=1` | reference.md | B | vigia tambÃ©m sessÃµes headless longas |
| `claude --debug` | reference.md | B | log com cada hook pulado e o motivo |
| `/reload-plugins` (dentro da sessÃ£o) | reference.md | B | relÃª plugin instalado de marketplace-pasta |
| `claude plugin marketplace add <pasta-ou-dono/repo> --scope user` | kit START-HERE | B | â€” |
| `claude plugin install <plugin>@<marketplace> --scope user` (ou `project`, `local`) | kit START-HERE | B | â€” |
| `claude plugin disable <plugin>@<marketplace> --scope user` | guias do kit | B | â€” |
| `claude plugin update` Â· `claude plugin list` | reference.md | B | `list` mostra `Read from:` |
| `claude plugin init` | reference.md | B | **cria outro tipo de plugin** (command hooks), nÃ£o um mod â€” avisar |
| `ls .claude-plugin/types/` (na pasta do mod carregado) | reference.md | B | `claude-code/`, `claude-code-tools/`, `claude-code-mcp/`, `tsconfig.json` |
| `tsc -p <pasta-do-mod>` | reference.md | B | checa tipos sem passo extra |

Prompts para colar no Claude Code podem ser criados, desde que sÃ³ peÃ§am leitura de arquivos, os comandos acima, ou o uso de um prompt de `prompts/` do kit (ex.: `Leia prompts/01-terminal-pet.txt e construa esse mod numa pasta nova chamada meu-pet. NÃ£o instale nada; teste com claude plugin validate e claude plugin test.`).

### SaÃ­das reais (Tier A)

VALIDATE (`claude plugin validate templates/starter-mod`):
```
Validating plugin manifest: .../templates/starter-mod/.claude-plugin/plugin.json

Validating hooks: .../templates/starter-mod/hooks/hooks.json

  â¯ ./starter.mjs hooks: session.start, tool.call{tool=Read}, command.run{command=readcount}
  â¯ ./starter.mjs calls: $.command.register

âœ” Validation passed
```
TEST (`claude plugin test templates/starter-mod`):
```
tests/starter.test.ts:
(pass) counts successful reads and excludes failed ones [20.64ms]

 1 pass
 0 fail
Ran 1 test across 1 file. [0.13s]
```
CHECAR (`scripts/checar-mod.sh mods/recibo-sessao`):
```
== recibo-sessao
  validate: ok
  tsc: ok
  test: ok (6 linhas de aprovaÃ§Ã£o)
```
TABELA DO KIT (validate + test por plugin, 2.1.289): auto-handoff 15/0 Â· changes-receipt 18/0 Â· context-meter 2/0 Â· coral-skin 9/0 Â· flight-recorder 7/0 Â· model-router 7/0 Â· output-tray 18/0 Â· repo-heatmap 19/0 Â· session-bookmarks 15/0 Â· terminal-pet 12/1 (o teste "whole sprite set stays far under the terminal's color-pair table" estourou o limite de 5 s com a mÃ¡quina carregada) Â· starter-mod 1/0. Total 123 de 124. Todos `validate=ok`.

### Arquivos reais que podem ser mostrados (copiar, nÃ£o reescrever)

- `templates/starter-mod/hooks/hooks.json` = `{"modules":["./starter.mjs"]}`
- `templates/starter-mod/hooks/starter.mjs` e `tests/starter.test.ts` (inteiros â€” sÃ£o curtos).
- `templates/starter-mod/.claude-plugin/plugin.json` (`name: read-counter-example`).
- `.claude-plugin/marketplace.json` do kit (`name: claude-mods-kit`, `plugins[].source: ./plugins/<nome>`).
- `examples/band.tsx` e `examples/pane.tsx` da referÃªncia oficial (trechos).
- `ARCKHÉ-mods/mods/recibo-sessao/` (register.tsx, types, tests/mundo.ts) e `mods/freio-de-mao`, `mods/vigia-api`, `mods/guarda-colisao`, `mods/roteador-subagente` para os exemplos de controle (trechos curtos, sempre com o caminho).

### Nomes de API

Todo `$.<noun>.<mÃ©todo>` e todo `on('<evento>'` citado precisa existir no `claude-code.d.ts` 2.1.289 (o `lint.py` confere). Eventos mais usados: `session.start`, `session.end`, `prompt.submit`, `turn.start`, `turn.step` (stream), `turn.complete`, `tool.call`, `tool.describe`, `command.run`, `ui.render`, `ui.press`, `ui.input`, `ui.select`, `session.append`, `state.set`, `process.spawn` (stream), `classic.<Nome>` (ex.: `classic.PreToolUse`, `classic.Stop`).

## Mapa do curso (CONGELADO â€” tÃ­tulos h2 dos tÃ³picos = tÃ­tulos no Ã­ndice da trilha)

Cada mÃ³dulo: 6 tÃ³picos, `~35 min`. Emoji do card entre colchetes.

### T1 Â· ðŸ§¬ Anatomia (emerald) â€” nav "Anatomia"
- **1.1 [ðŸ§¬] O que Ã© um mod por dentro** â€” "TrÃªs arquivos e uma funÃ§Ã£o" Â· Fundamento
  1. Entenda o que muda quando um mod carrega
  2. Separe mod, hook clÃ¡ssico, skill e MCP
  3. Leia a assinatura register(on, options)
  4. ConheÃ§a os trÃªs parÃ¢metros de todo hook
  5. Saiba onde o mod roda e o que ele nÃ£o tem
  6. Veja o mapa do curso e os dois kits
- **1.2 [ðŸ—‚ï¸] Estrutura de arquivos e manifesto** â€” "plugin.json manda" Â· PrÃ¡tico
  1. Monte a Ã¡rvore mÃ­nima de pastas
  2. Escreva o plugin.json
  3. Aponte o mÃ³dulo no hooks.json
  4. Escolha a extensÃ£o do arquivo
  5. Declare opÃ§Ãµes com userConfig
  6. Valide antes de carregar
- **1.3 [ðŸ”„] Carregar, recarregar e instalar** â€” "Pasta vigiada, mod vivo" Â· PrÃ¡tico
  1. Carregue com --plugin-dir
  2. Veja o hot-reload acontecer
  3. Use CLAUDE_CODE_PLUGIN_DIRS no desktop
  4. Instale por marketplace
  5. Escolha o escopo certo
  6. Desligue e desinstale sem sobras
- **1.4 [ðŸš€] Seu primeiro mod: comando e contador** â€” "readcount funcionando" Â· PrÃ¡tico
  1. Copie o starter-mod
  2. Leia o cÃ³digo linha por linha
  3. Valide e teste
  4. Rode o comando sem gastar modelo
  5. Mude o contador para outra ferramenta
  6. Renomeie para virar seu

### T2 Â· âš¡ Eventos e estado (blue) â€” nav "Eventos e estado"
- **2.1 [ðŸ—ºï¸] O mapa de eventos** â€” "Escolha o evento antes do cÃ³digo" Â· Fundamento
  1. Agrupe os eventos por noun
  2. Siga uma volta completa do turno
  3. Use matchers para filtrar
  4. Trate os eventos que sÃ£o stream
  5. Pendure-se nos hooks clÃ¡ssicos
  6. Ache qualquer evento nos tipos
- **2.2 [â›“ï¸] A cadeia: next, reescrever e responder** â€” "Quem chama next decide" Â· Fundamento
  1. Entenda a cadeia de plugins
  2. Observe e passe adiante
  3. Reescreva o que vem depois
  4. Responda sem chamar next
  5. Use .catch para falhar com seguranÃ§a
  6. Respeite o orÃ§amento e o next.signal
- **2.3 [ðŸ’¾] Estado que sobrevive** â€” "VariÃ¡vel some no reload" Â· PrÃ¡tico
  1. Veja a variÃ¡vel de mÃ³dulo sumir
  2. Declare o contrato em types/index.d.ts
  3. Use atom, read e update
  4. Guarde entre sessÃµes com $.store
  5. Use o relÃ³gio do engine
  6. Escolha onde cada dado mora
- **2.4 [â±ï¸] Trabalho fora do dispatch** â€” "session.start acende, clock mantÃ©m" Â· PrÃ¡tico
  1. Comece no session.start
  2. Agende com clock.every e clock.after
  3. Leia e escreva arquivos com $.fs
  4. Rode processos locais com $.process
  5. Acorde a sessÃ£o com prompt.submit
  6. Decida se o mod pode gastar modelo

### T3 Â· ðŸ–¥ï¸ Telas e comandos (purple) â€” nav "Telas e comandos"
- **3.1 [ðŸŽ¨] ui.render e as superfÃ­cies** â€” "Uma Ã¡rvore por superfÃ­cie" Â· Fundamento
  1. Entenda o que o ui.render recebe
  2. Pegue os elementos com ui.resolve
  3. Respeite as diferenÃ§as entre superfÃ­cies
  4. Desenhe do estado, nunca escreva ao desenhar
  5. Saiba o que acontece quando a Ã¡rvore nÃ£o valida
  6. Use Raster e Image no terminal
- **3.2 [ðŸ“Ÿ] Faixa, status e avisos** â€” "Uma faixa para todos" Â· PrÃ¡tico
  1. Desenhe na faixa acima do prompt
  2. Conviva com os outros mods
  3. Mostre status sem abrir nada
  4. Avise com toast e log
  5. Disseque o exemplo oficial da faixa
  6. Teste a faixa no terminal e no desktop
- **3.3 [ðŸªŸ] PainÃ©is e botÃµes** â€” "Abra por comando" Â· PrÃ¡tico
  1. Abra um painel com ui.open
  2. Dimensione pelo bodyColumns
  3. Ponha botÃµes com hotkey
  4. Trate press, input e select
  5. FaÃ§a um painel virar diÃ¡logo
  6. Feche e libere o painel
- **3.4 [âŒ¨ï¸] Comandos, ferramentas e configuraÃ§Ã£o** â€” "/comando sem modelo" Â· PrÃ¡tico
  1. Registre um comando de barra
  2. Responda o command.run
  3. Desenhe a saÃ­da do comando
  4. DÃª uma ferramenta ao modelo
  5. Leia as opÃ§Ãµes do /config
  6. Evite colisÃ£o de nomes

### T4 Â· ðŸ›¡ï¸ Controlar, testar e distribuir (amber) â€” nav "Controlar e distribuir"
- **4.1 [ðŸ›¡ï¸] Mods que mudam o fluxo** â€” "Pergunte antes de apagar" Â· PrÃ¡tico
  1. Intercepte uma chamada de ferramenta
  2. Negue com motivo claro
  3. Pergunte ao humano com ui.ask
  4. Troque o modelo de um subagente
  5. Preserve as permissÃµes do usuÃ¡rio
  6. Estude a guarda do freio-de-mÃ£o
- **4.2 [ðŸ§ª] Testar com claude plugin test** â€” "O engine de verdade, sem modelo" Â· PrÃ¡tico
  1. Entenda o que o teste simula
  2. Escreva os mocks antes do $
  3. Teste um comando de ponta a ponta
  4. Controle o relÃ³gio
  5. Monte a tela em terminal e desktop
  6. Leia uma falha de teste
- **4.3 [ðŸ”] Depurar e as pegadinhas** â€” "O log diz por quÃª" Â· PrÃ¡tico
  1. Ligue o --debug
  2. Leia a linha de hook pulado
  3. Corrija um mÃ³dulo que nÃ£o carrega
  4. Corrija uma Ã¡rvore recusada
  5. Percorra as pegadinhas do kit ARCKHÉ
  6. FaÃ§a um teste de fumaÃ§a com claude -p
- **4.4 [ðŸ“¦] Distribuir e projeto final** â€” "Seu mod no marketplace" Â· PrÃ¡tico
  1. Monte o marketplace.json
  2. Publique num repositÃ³rio
  3. Atualize sem quebrar quem usa
  4. Revise antes de compartilhar
  5. FaÃ§a o projeto final
  6. Siga para os prÃ³ximos passos

## Projeto final (4.4)

Um mod prÃ³prio do Rafa: comando `/x` + faixa ou painel + estado em `$.state` + teste com `claude plugin test` (mocks antes do `$`) + `claude plugin validate` OK + botÃ£o/comando de desligar + README. Prova: `claude plugin test <pasta>` com `0 fail` e `claude -p "/<comando>" --plugin-dir <pasta>` respondendo sem modelo.

## PrÃ³ximos passos (4.4 tÃ³pico 6, e landing)

- Curso bÃ¡sico de mods (v6) â€” "em breve" (sem link atÃ© existir).
- `https://linnoff88-dev.github.io/ (hooks clÃ¡ssicos), `https://linnoff88-dev.github.io/ (plugins de produÃ§Ã£o), `https://linnoff88-dev.github.io/ (trilha 4: guarda e painel), repos `https://github.com/linnoff88-dev/ARCKHÉ-mods` e `https://github.com/linnoff88-dev/claude-mods-starter-kit`.
