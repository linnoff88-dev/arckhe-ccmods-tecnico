# Brief para os agentes que escrevem pêÂ¡ginas (curso ccmods-tecnico)

VocêÂª escreve CORPOS em `~/projetos/ccmods-tecnico/context/corpos/`. Nunca edite `curso/**` nem `index.html` (sêÂ£o gerados), nem o modelo `context/corpos/modulo-1-1.html`, nem a SPEC, nem os scripts.

## Leia antes de escrever
1. `context/SPEC.md` ê¢â¬â pêÂºblico, tom, vocabulêÂ¡rio, **mapa congelado** (têÂ­tulos dos 6 têÂ³picos de cada mêÂ³dulo = os h2, verbatim), COMANDOS PERMITIDOS e saêÂ­das reais.
2. `context/corpos/modulo-1-1.html` ê¢â¬â o MODELO. Copie a estrutura por marcador de texto (header, `<main>`, cada `<section id="topico-N">`, boxes, resumo, `<aside>` com TOC, `<!--CHECKS-->`), nunca por nêÂºmero de linha.
3. As fontes têÂ©cnicas da SPEC (reference.md, claude-code.d.ts, kits). Use `grep` no d.ts (20 mil linhas) para confirmar cada nome de evento, noun, mêÂ©todo e campo ANTES de escrever. NêÂ£o invente API: o lint rejeita `$.x.y` e `on('evento'` que nêÂ£o existam no d.ts.

## Regras de cada mêÂ³dulo (o lint confere)
- Primeira linha: `<!--TITLE: <têÂ­tulo do mêÂ³dulo> -->`.
- Cor da trilha: T1 emerald, T2 blue, T3 purple, T4 amber (troque todas as classes `emerald` do modelo; ciano `#38bdf8` continua secundêÂ¡rio nos SVG). Cores SVG da trilha: emerald #34d399/#a7f3d0/#0e2018 êÂ· blue #60a5fa/#bfdbfe/#0f1b33 êÂ· purple #c084fc/#e9d5ff/#1e1233 êÂ· amber #fbbf24/#fde68a/#2a1d06.
- Exatamente 6 `<section id="topico-N" data-ARCKHê-topic="modulo-X-Y#topico-N">`, com `<h2 class="text-2xl font-bold flex-1">` = têÂ­tulo da SPEC, verbatim.
- `data-ARCKHê-module="X-Y"` e `data-ARCKHê-track="X"` no header e no main; `data-ARCKHê-block="mX-Y-tN-pM"` êÂºnicos nos parêÂ¡grafos; botêÂ£o "Tenho dêÂºvida" e "Marcar como lido" em cada têÂ³pico (copiar do modelo).
- **ê¢â°Â¥2 SVG** `role="img"` com `aria-label` que ensina, cada um seguido de "Como ler o desenho". IDs de `pattern/filter/marker/gradient` êÂºnicos na pêÂ¡gina: prefixo `m<XY><letra>-` (ex.: `m23a-grid`, `m23b-glow`).
- Cada mêÂ³dulo **PrêÂ¡tico** tem ê¢â°Â¥1 bloco copia-e-cola no formato do modelo 1.2 do agent-runtime: cabeêÂ§alho "ê°Å¸Å½Â¯ Objetivo: ê¢â¬Â¦", `<pre>` com o cêÂ³digo/comando, rodapêÂ© `<strong>Como verificar:</strong> ê¢â¬Â¦`. SêÂ³ comandos da tabela COMANDOS PERMITIDOS; saêÂ­da mostrada sêÂ³ se for Tier A (verbatim da SPEC); senêÂ£o "resultado esperado".
- CêÂ³digo de mod mostrado: copie de arquivos reais (com o caminho no cabeêÂ§alho do bloco) ou escreva exemplos curtos que usem Sêâ nomes confirmados no d.ts. A partir da T2, forma tipada (`import type { Register } from 'claude-code'`, `export const register: Register = (on, options) => {ê¢â¬Â¦}`), funêÂ§êÂµes que recebem `$` declaradas no topo do arquivo.
- Escape HTML dentro de `<pre>`: `&lt;` `&gt;` `&amp;`.
- Box "ê°Å¸â â¢ Novo aqui?" para cada termo novo da API na primeira apariêÂ§êÂ£o.
- Variedade: ê¢â°Â¥2 grids ê¢Åâ/ê¢Åâ, ê¢â°Â¥1 sequêÂªncia numerada (timeline), ê¢â°Â¥2 boxes (ê°Å¸âÂ¡ dica, ê¢Å¡Â ê¯Â¸Â alerta), tabelas quando comparar.
- 1 teste rêÂ¡pido (`data-ARCKHê-check="modulo-X-Y#q1"`, 3 opêÂ§êÂµes, feedback no bloco `<!--CHECKS-->` com `ARCKHê.registerCheck`).
- Resumo com 5 ê¢Åâ, "PrêÂ³ximo mêÂ³dulo" e botêÂµes ê¢â Â trilha / MêÂ³dulo seguinte ê¢â â (no êÂºltimo mêÂ³dulo da trilha, aponte para `../trilhaN+1/index.html`; no 4.4, para `../../index.html`).
- `<aside>` com TOC de 6 itens curtos.
- Tamanho do corpo: 420ê¢â¬â560 linhas (a pêÂ¡gina montada fica entre 500 e 850).
- PortuguêÂªs correto com acentos, frases curtas, sem emoji em excesso no texto corrido. Exemplos com o Rafa quando couber.
- CrêÂ©dito: o Claude Mods Starter Kit êÂ© da Prompt Advisers (MIT).

## VerificaêÂ§êÂ£o (obrigatêÂ³ria antes de terminar)
```
cd ~/projetos/ccmods-tecnico && python3 scripts/montar.py && LINT_SEM_LINKS=1 python3 scripts/lint.py curso/trilhaX/modulo-X-Y.html
```
Precisa terminar em `LINT OK` para cada arquivo seu. Corrija atêÂ© passar. Responda sêÂ³ com as linhas de resultado do lint dos seus arquivos e, se houver, o que vocêÂª nêÂ£o conseguiu confirmar no d.ts.
