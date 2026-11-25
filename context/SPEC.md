# SPEC ê¢â¬â Mods do Claude Code: curso têÂ©cnico (formato-curso-v2)

Curso ARCKHê AI (aberto e gratuito) para **quem programa** e quer escrever, testar e distribuir mods do Claude Code.
TêÂ­tulo exato: **Mods do Claude Code ê¢â¬â o curso têÂ©cnico**. courseId = `ccmt`. Repo `linnoff88-dev/ccmods-tecnico`.
Skill de formato: `~/.claude/skills/formato-curso-v2/` (erros crêÂ­ticos #1ê¢â¬â#31 valem).

## VersêÂ£o e autoridade (dizer no curso)

- Tudo foi conferido no **Claude Code 2.1.289**, em **05/10/2026**, nesta mêÂ¡quina (Linux ARM64).
- A API de mods estêÂ¡ em **acesso antecipado e muda entre versêÂµes**. A autoridade êÂ© o arquivo de tipos da SUA instalaêÂ§êÂ£o: `.claude-plugin/types/claude-code/index.d.ts`, que o Claude Code escreve dentro da pasta do mod quando ele carrega por `--plugin-dir`/pasta de mods. O curso ensina a ler esse arquivo; nunca prometer que um nome vale para sempre.

## Fontes da verdade (ler êÂ  vontade; NêÆO editar nenhuma delas)

1. ReferêÂªncia oficial (vem com o Claude Code): `/tmp/claude-1000/bundled-skills/2.1.289/4a690ea2f793d25136db54dac3d94b2a/plugin-authoring/reference.md` (182 linhas) e `.../plugin-authoring/examples/{band.tsx,band-state.d.ts,pane.tsx,pane-state.d.ts,tool-call.ts}`.
2. Tipos (20 422 linhas ê¢â¬â use grep): `.../plugin-authoring/types/claude-code.d.ts`.
3. Kit da Prompt Advisers (MIT, **dar crêÂ©dito**): `~/projetos/claude-mods-starter-kit` ê¢â¬â 10 plugins em `plugins/`, `templates/starter-mod/`, `scripts/{check.sh,try.sh,manage.sh}`, `prompts/`, `.claude-plugin/marketplace.json`.
4. Kit ARCKHê: `~/projetos/ARCKHê-mods` ê¢â¬â 18 mods em `mods/`, `docs/COMO-FAZER-UM-MOD.md` (estrutura, verificaêÂ§êÂ£o e **23 pegadinhas** ê¢â¬â copiar o sentido, citar a fonte), `scripts/checar-mod.sh`, modelo `mods/recibo-sessao/`.

## PêÂºblico e tom

- Programador ou quase: sabe usar terminal, jêÂ¡ leu JavaScript/TypeScript, jêÂ¡ usou o Claude Code. NêÂ£o precisa conhecer a API de mods.
- Mesmo assim, cada termo da API êÂ© definido na 1êÂª vez (box "ê°Å¸â â¢ Novo aqui?"): hook, `$`, `e`, `next`, dispatch, surface, noun, matcher, atom, store...
- Tom: direto, frases curtas, parêÂ¡grafos de 2ê¢â¬â4 linhas, sem coachzinho, portuguêÂªs correto com acentos.
- NêÂ£o citar criadores, canais ou vêÂ­deos de terceiros. A Prompt Advisers aparece **sêÂ³ como autora do kit** (crêÂ©dito, MIT).
- Personagem fixo dos exemplos: **Rafa, 34, dev** de uma agêÂªncia pequena, que quer ver o que o Claude toca no repositêÂ³rio e nêÂ£o perder trabalho entre sessêÂµes.

## Forma do cêÂ³digo (congelado)

- **Primeiro mod (T1)**: a forma do kit, `hooks/starter.mjs` com `export function register(on) {ê¢â¬Â¦}` ê¢â¬â sem compilaêÂ§êÂ£o, sem tipos.
- **A partir da T2**: a forma tipada dos exemplos oficiais e do ARCKHê-mods: `hooks/register.tsx` (ou `.ts`) com `import type { Register } from 'claude-code'` e `export const register: Register = (on, options) => {ê¢â¬Â¦}`; JSX com `h` como fêÂ¡brica; tipos de estado em `types/index.d.ts` apontado por `"types"` no `plugin.json`.
- Toda funêÂ§êÂ£o que recebe `$` êÂ© declarada no topo do arquivo (pegadinha 1).

## VocabulêÂ¡rio fixo (um nome por conceito)

- **mod** = plugin do Claude Code com *function hooks* (mêÂ³dulo que exporta `register`). "Plugin" êÂ© o pacote; "mod" êÂ© o apelido.
- **hook** = funêÂ§êÂ£o `($, e, next)` registrada com `on(evento, matcher?, hook)`.
- **hook clêÂ¡ssico** = os hooks de `settings.json` (comandos de shell, PreToolUse/PostToolUse...). No mod eles aparecem como eventos `classic.<Nome>`.
- **evento** = nome como `tool.call`; **noun** = a parte antes do ponto (`tool`, `ui`, `session`...).
- **cadeia** = os hooks de todos os plugins + o comportamento do prêÂ³prio Claude Code, ligados por `next`.
- **dispatch** = uma passagem de um evento pela cadeia (tem orêÂ§amento de tempo).
- **superfêÂ­cie** = onde desenha: `terminal`, `desktop`, `mobile`, `vscode`.
- **faixa** = `AbovePrompt` (uma sêÂ³, compartilhada); **painel** = `Pane`.

## COMANDOS PERMITIDOS (nenhum outro entra numa pêÂ¡gina)

Tier A = rodado aqui em 05/10/2026, saêÂ­da real abaixo (pode mostrar como saêÂ­da).
Tier B = da referêÂªncia oficial ou da documentaêÂ§êÂ£o dos kits (mostrar o comando; resultado como "esperado", sem inventar saêÂ­da de terminal).

| Comando (verbatim) | Fonte | Tier | SaêÂ­da / esperado |
|---|---|---|---|
| `claude --version` | ê¢â¬â | A | `2.1.289 (Claude Code)` |
| `git clone https://github.com/linnoff88-dev/claude-mods-starter-kit` êÂ· `cd claude-mods-starter-kit` | README do kit | ê¢â¬â | ê¢â¬â |
| `git clone https://github.com/linnoff88-dev/ARCKHê-mods` êÂ· `cd ARCKHê-mods` | README ARCKHê-mods | ê¢â¬â | ê¢â¬â |
| `claude plugin validate templates/starter-mod` | kit | A | bloco VALIDATE |
| `claude plugin test templates/starter-mod` | kit | A | bloco TEST |
| `claude plugin validate <pasta-do-mod>` êÂ· `claude plugin test <pasta-do-mod>` | reference.md | A | `ê¢Åâ Validation passed` êÂ· `N pass` / `0 fail` |
| `bash scripts/check.sh` (kit) | kit | A | ver TABELA DO KIT ê¢â¬â aqui parou no terminal-pet (teste de desempenho estourou 5 s) |
| `bash scripts/try.sh terminal-pet` | kit START-HERE | B | abre uma sessêÂ£o temporêÂ¡ria sêÂ³ com o mod |
| `bash scripts/manage.sh install user all` êÂ· `bash scripts/manage.sh disable user all` | kit | B | ê¢â¬â |
| `claude -p "/readcount" --plugin-dir templates/starter-mod` | kit | A | `read-counter-example: Successful reads observed: 0` |
| `claude -p "/recibo" --plugin-dir mods/recibo-sessao` | ARCKHê-mods | A | `recibo-sessao: Nesta sessêÂ£o: nenhum arquivo criado ou alterado.` |
| `TSC=<caminho do tsc> scripts/checar-mod.sh mods/recibo-sessao` | ARCKHê-mods | A | bloco CHECAR |
| `claude --plugin-dir <pasta>` (repita a flag para vêÂ¡rios) | reference.md | B | carrega sêÂ³ nesta sessêÂ£o; pasta vigiada (hot-reload) |
| `CLAUDE_CODE_PLUGIN_DIRS=<caminho absoluto>` | reference.md | B | igual ao `--plugin-dir`, para desktop/SDK |
| `CLAUDE_CODE_PLUGIN_DIR_WATCH=1` | reference.md | B | vigia tambêÂ©m sessêÂµes headless longas |
| `claude --debug` | reference.md | B | log com cada hook pulado e o motivo |
| `/reload-plugins` (dentro da sessêÂ£o) | reference.md | B | relêÂª plugin instalado de marketplace-pasta |
| `claude plugin marketplace add <pasta-ou-dono/repo> --scope user` | kit START-HERE | B | ê¢â¬â |
| `claude plugin install <plugin>@<marketplace> --scope user` (ou `project`, `local`) | kit START-HERE | B | ê¢â¬â |
| `claude plugin disable <plugin>@<marketplace> --scope user` | guias do kit | B | ê¢â¬â |
| `claude plugin update` êÂ· `claude plugin list` | reference.md | B | `list` mostra `Read from:` |
| `claude plugin init` | reference.md | B | **cria outro tipo de plugin** (command hooks), nêÂ£o um mod ê¢â¬â avisar |
| `ls .claude-plugin/types/` (na pasta do mod carregado) | reference.md | B | `claude-code/`, `claude-code-tools/`, `claude-code-mcp/`, `tsconfig.json` |
| `tsc -p <pasta-do-mod>` | reference.md | B | checa tipos sem passo extra |

Prompts para colar no Claude Code podem ser criados, desde que sêÂ³ peêÂ§am leitura de arquivos, os comandos acima, ou o uso de um prompt de `prompts/` do kit (ex.: `Leia prompts/01-terminal-pet.txt e construa esse mod numa pasta nova chamada meu-pet. NêÂ£o instale nada; teste com claude plugin validate e claude plugin test.`).

### SaêÂ­das reais (Tier A)

VALIDATE (`claude plugin validate templates/starter-mod`):
```
Validating plugin manifest: .../templates/starter-mod/.claude-plugin/plugin.json

Validating hooks: .../templates/starter-mod/hooks/hooks.json

  ê¢ÂÂ¯ ./starter.mjs hooks: session.start, tool.call{tool=Read}, command.run{command=readcount}
  ê¢ÂÂ¯ ./starter.mjs calls: $.command.register

ê¢Åâ Validation passed
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
  test: ok (6 linhas de aprovaêÂ§êÂ£o)
```
TABELA DO KIT (validate + test por plugin, 2.1.289): auto-handoff 15/0 êÂ· changes-receipt 18/0 êÂ· context-meter 2/0 êÂ· coral-skin 9/0 êÂ· flight-recorder 7/0 êÂ· model-router 7/0 êÂ· output-tray 18/0 êÂ· repo-heatmap 19/0 êÂ· session-bookmarks 15/0 êÂ· terminal-pet 12/1 (o teste "whole sprite set stays far under the terminal's color-pair table" estourou o limite de 5 s com a mêÂ¡quina carregada) êÂ· starter-mod 1/0. Total 123 de 124. Todos `validate=ok`.

### Arquivos reais que podem ser mostrados (copiar, nêÂ£o reescrever)

- `templates/starter-mod/hooks/hooks.json` = `{"modules":["./starter.mjs"]}`
- `templates/starter-mod/hooks/starter.mjs` e `tests/starter.test.ts` (inteiros ê¢â¬â sêÂ£o curtos).
- `templates/starter-mod/.claude-plugin/plugin.json` (`name: read-counter-example`).
- `.claude-plugin/marketplace.json` do kit (`name: claude-mods-kit`, `plugins[].source: ./plugins/<nome>`).
- `examples/band.tsx` e `examples/pane.tsx` da referêÂªncia oficial (trechos).
- `ARCKHê-mods/mods/recibo-sessao/` (register.tsx, types, tests/mundo.ts) e `mods/freio-de-mao`, `mods/vigia-api`, `mods/guarda-colisao`, `mods/roteador-subagente` para os exemplos de controle (trechos curtos, sempre com o caminho).

### Nomes de API

Todo `$.<noun>.<mêÂ©todo>` e todo `on('<evento>'` citado precisa existir no `claude-code.d.ts` 2.1.289 (o `lint.py` confere). Eventos mais usados: `session.start`, `session.end`, `prompt.submit`, `turn.start`, `turn.step` (stream), `turn.complete`, `tool.call`, `tool.describe`, `command.run`, `ui.render`, `ui.press`, `ui.input`, `ui.select`, `session.append`, `state.set`, `process.spawn` (stream), `classic.<Nome>` (ex.: `classic.PreToolUse`, `classic.Stop`).

## Mapa do curso (CONGELADO ê¢â¬â têÂ­tulos h2 dos têÂ³picos = têÂ­tulos no êÂ­ndice da trilha)

Cada mêÂ³dulo: 6 têÂ³picos, `~35 min`. Emoji do card entre colchetes.

### T1 êÂ· ê°Å¸Â§Â¬ Anatomia (emerald) ê¢â¬â nav "Anatomia"
- **1.1 [ê°Å¸Â§Â¬] O que êÂ© um mod por dentro** ê¢â¬â "TrêÂªs arquivos e uma funêÂ§êÂ£o" êÂ· Fundamento
  1. Entenda o que muda quando um mod carrega
  2. Separe mod, hook clêÂ¡ssico, skill e MCP
  3. Leia a assinatura register(on, options)
  4. ConheêÂ§a os trêÂªs parêÂ¢metros de todo hook
  5. Saiba onde o mod roda e o que ele nêÂ£o tem
  6. Veja o mapa do curso e os dois kits
- **1.2 [ê°Å¸ââê¯Â¸Â] Estrutura de arquivos e manifesto** ê¢â¬â "plugin.json manda" êÂ· PrêÂ¡tico
  1. Monte a êÂ¡rvore mêÂ­nima de pastas
  2. Escreva o plugin.json
  3. Aponte o mêÂ³dulo no hooks.json
  4. Escolha a extensêÂ£o do arquivo
  5. Declare opêÂ§êÂµes com userConfig
  6. Valide antes de carregar
- **1.3 [ê°Å¸ââ] Carregar, recarregar e instalar** ê¢â¬â "Pasta vigiada, mod vivo" êÂ· PrêÂ¡tico
  1. Carregue com --plugin-dir
  2. Veja o hot-reload acontecer
  3. Use CLAUDE_CODE_PLUGIN_DIRS no desktop
  4. Instale por marketplace
  5. Escolha o escopo certo
  6. Desligue e desinstale sem sobras
- **1.4 [ê°Å¸Å¡â¬] Seu primeiro mod: comando e contador** ê¢â¬â "readcount funcionando" êÂ· PrêÂ¡tico
  1. Copie o starter-mod
  2. Leia o cêÂ³digo linha por linha
  3. Valide e teste
  4. Rode o comando sem gastar modelo
  5. Mude o contador para outra ferramenta
  6. Renomeie para virar seu

### T2 êÂ· ê¢Å¡Â¡ Eventos e estado (blue) ê¢â¬â nav "Eventos e estado"
- **2.1 [ê°Å¸âÂºê¯Â¸Â] O mapa de eventos** ê¢â¬â "Escolha o evento antes do cêÂ³digo" êÂ· Fundamento
  1. Agrupe os eventos por noun
  2. Siga uma volta completa do turno
  3. Use matchers para filtrar
  4. Trate os eventos que sêÂ£o stream
  5. Pendure-se nos hooks clêÂ¡ssicos
  6. Ache qualquer evento nos tipos
- **2.2 [ê¢âºâê¯Â¸Â] A cadeia: next, reescrever e responder** ê¢â¬â "Quem chama next decide" êÂ· Fundamento
  1. Entenda a cadeia de plugins
  2. Observe e passe adiante
  3. Reescreva o que vem depois
  4. Responda sem chamar next
  5. Use .catch para falhar com seguranêÂ§a
  6. Respeite o orêÂ§amento e o next.signal
- **2.3 [ê°Å¸âÂ¾] Estado que sobrevive** ê¢â¬â "VariêÂ¡vel some no reload" êÂ· PrêÂ¡tico
  1. Veja a variêÂ¡vel de mêÂ³dulo sumir
  2. Declare o contrato em types/index.d.ts
  3. Use atom, read e update
  4. Guarde entre sessêÂµes com $.store
  5. Use o relêÂ³gio do engine
  6. Escolha onde cada dado mora
- **2.4 [ê¢ÂÂ±ê¯Â¸Â] Trabalho fora do dispatch** ê¢â¬â "session.start acende, clock mantêÂ©m" êÂ· PrêÂ¡tico
  1. Comece no session.start
  2. Agende com clock.every e clock.after
  3. Leia e escreva arquivos com $.fs
  4. Rode processos locais com $.process
  5. Acorde a sessêÂ£o com prompt.submit
  6. Decida se o mod pode gastar modelo

### T3 êÂ· ê°Å¸âÂ¥ê¯Â¸Â Telas e comandos (purple) ê¢â¬â nav "Telas e comandos"
- **3.1 [ê°Å¸Å½Â¨] ui.render e as superfêÂ­cies** ê¢â¬â "Uma êÂ¡rvore por superfêÂ­cie" êÂ· Fundamento
  1. Entenda o que o ui.render recebe
  2. Pegue os elementos com ui.resolve
  3. Respeite as diferenêÂ§as entre superfêÂ­cies
  4. Desenhe do estado, nunca escreva ao desenhar
  5. Saiba o que acontece quando a êÂ¡rvore nêÂ£o valida
  6. Use Raster e Image no terminal
- **3.2 [ê°Å¸âÅ¸] Faixa, status e avisos** ê¢â¬â "Uma faixa para todos" êÂ· PrêÂ¡tico
  1. Desenhe na faixa acima do prompt
  2. Conviva com os outros mods
  3. Mostre status sem abrir nada
  4. Avise com toast e log
  5. Disseque o exemplo oficial da faixa
  6. Teste a faixa no terminal e no desktop
- **3.3 [ê°Å¸ÂªÅ¸] PainêÂ©is e botêÂµes** ê¢â¬â "Abra por comando" êÂ· PrêÂ¡tico
  1. Abra um painel com ui.open
  2. Dimensione pelo bodyColumns
  3. Ponha botêÂµes com hotkey
  4. Trate press, input e select
  5. FaêÂ§a um painel virar diêÂ¡logo
  6. Feche e libere o painel
- **3.4 [ê¢ÅÂ¨ê¯Â¸Â] Comandos, ferramentas e configuraêÂ§êÂ£o** ê¢â¬â "/comando sem modelo" êÂ· PrêÂ¡tico
  1. Registre um comando de barra
  2. Responda o command.run
  3. Desenhe a saêÂ­da do comando
  4. DêÂª uma ferramenta ao modelo
  5. Leia as opêÂ§êÂµes do /config
  6. Evite colisêÂ£o de nomes

### T4 êÂ· ê°Å¸âºÂ¡ê¯Â¸Â Controlar, testar e distribuir (amber) ê¢â¬â nav "Controlar e distribuir"
- **4.1 [ê°Å¸âºÂ¡ê¯Â¸Â] Mods que mudam o fluxo** ê¢â¬â "Pergunte antes de apagar" êÂ· PrêÂ¡tico
  1. Intercepte uma chamada de ferramenta
  2. Negue com motivo claro
  3. Pergunte ao humano com ui.ask
  4. Troque o modelo de um subagente
  5. Preserve as permissêÂµes do usuêÂ¡rio
  6. Estude a guarda do freio-de-mêÂ£o
- **4.2 [ê°Å¸Â§Âª] Testar com claude plugin test** ê¢â¬â "O engine de verdade, sem modelo" êÂ· PrêÂ¡tico
  1. Entenda o que o teste simula
  2. Escreva os mocks antes do $
  3. Teste um comando de ponta a ponta
  4. Controle o relêÂ³gio
  5. Monte a tela em terminal e desktop
  6. Leia uma falha de teste
- **4.3 [ê°Å¸âÂ] Depurar e as pegadinhas** ê¢â¬â "O log diz por quêÂª" êÂ· PrêÂ¡tico
  1. Ligue o --debug
  2. Leia a linha de hook pulado
  3. Corrija um mêÂ³dulo que nêÂ£o carrega
  4. Corrija uma êÂ¡rvore recusada
  5. Percorra as pegadinhas do kit ARCKHê
  6. FaêÂ§a um teste de fumaêÂ§a com claude -p
- **4.4 [ê°Å¸âÂ¦] Distribuir e projeto final** ê¢â¬â "Seu mod no marketplace" êÂ· PrêÂ¡tico
  1. Monte o marketplace.json
  2. Publique num repositêÂ³rio
  3. Atualize sem quebrar quem usa
  4. Revise antes de compartilhar
  5. FaêÂ§a o projeto final
  6. Siga para os prêÂ³ximos passos

## Projeto final (4.4)

Um mod prêÂ³prio do Rafa: comando `/x` + faixa ou painel + estado em `$.state` + teste com `claude plugin test` (mocks antes do `$`) + `claude plugin validate` OK + botêÂ£o/comando de desligar + README. Prova: `claude plugin test <pasta>` com `0 fail` e `claude -p "/<comando>" --plugin-dir <pasta>` respondendo sem modelo.

## PrêÂ³ximos passos (4.4 têÂ³pico 6, e landing)

- Curso bêÂ¡sico de mods (v6) ê¢â¬â "em breve" (sem link atêÂ© existir).
- `https://linnoff88-dev.github.io/ (hooks clêÂ¡ssicos), `https://linnoff88-dev.github.io/ (plugins de produêÂ§êÂ£o), `https://linnoff88-dev.github.io/ (trilha 4: guarda e painel), repos `https://github.com/linnoff88-dev/ARCKHê-mods` e `https://github.com/linnoff88-dev/claude-mods-starter-kit`.
