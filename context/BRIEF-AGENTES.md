# Brief para os agentes que escrevem pÃ¡ginas (curso ccmods-tecnico)

VocÃª escreve CORPOS em `~/projetos/ccmods-tecnico/context/corpos/`. Nunca edite `curso/**` nem `index.html` (sÃ£o gerados), nem o modelo `context/corpos/modulo-1-1.html`, nem a SPEC, nem os scripts.

## Leia antes de escrever
1. `context/SPEC.md` â€” pÃºblico, tom, vocabulÃ¡rio, **mapa congelado** (tÃ­tulos dos 6 tÃ³picos de cada mÃ³dulo = os h2, verbatim), COMANDOS PERMITIDOS e saÃ­das reais.
2. `context/corpos/modulo-1-1.html` â€” o MODELO. Copie a estrutura por marcador de texto (header, `<main>`, cada `<section id="topico-N">`, boxes, resumo, `<aside>` com TOC, `<!--CHECKS-->`), nunca por nÃºmero de linha.
3. As fontes tÃ©cnicas da SPEC (reference.md, claude-code.d.ts, kits). Use `grep` no d.ts (20 mil linhas) para confirmar cada nome de evento, noun, mÃ©todo e campo ANTES de escrever. NÃ£o invente API: o lint rejeita `$.x.y` e `on('evento'` que nÃ£o existam no d.ts.

## Regras de cada mÃ³dulo (o lint confere)
- Primeira linha: `<!--TITLE: <tÃ­tulo do mÃ³dulo> -->`.
- Cor da trilha: T1 emerald, T2 blue, T3 purple, T4 amber (troque todas as classes `emerald` do modelo; ciano `#38bdf8` continua secundÃ¡rio nos SVG). Cores SVG da trilha: emerald #34d399/#a7f3d0/#0e2018 Â· blue #60a5fa/#bfdbfe/#0f1b33 Â· purple #c084fc/#e9d5ff/#1e1233 Â· amber #fbbf24/#fde68a/#2a1d06.
- Exatamente 6 `<section id="topico-N" data-ARCKHÉ-topic="modulo-X-Y#topico-N">`, com `<h2 class="text-2xl font-bold flex-1">` = tÃ­tulo da SPEC, verbatim.
- `data-ARCKHÉ-module="X-Y"` e `data-ARCKHÉ-track="X"` no header e no main; `data-ARCKHÉ-block="mX-Y-tN-pM"` Ãºnicos nos parÃ¡grafos; botÃ£o "Tenho dÃºvida" e "Marcar como lido" em cada tÃ³pico (copiar do modelo).
- **â‰¥2 SVG** `role="img"` com `aria-label` que ensina, cada um seguido de "Como ler o desenho". IDs de `pattern/filter/marker/gradient` Ãºnicos na pÃ¡gina: prefixo `m<XY><letra>-` (ex.: `m23a-grid`, `m23b-glow`).
- Cada mÃ³dulo **PrÃ¡tico** tem â‰¥1 bloco copia-e-cola no formato do modelo 1.2 do agent-runtime: cabeÃ§alho "ðŸŽ¯ Objetivo: â€¦", `<pre>` com o cÃ³digo/comando, rodapÃ© `<strong>Como verificar:</strong> â€¦`. SÃ³ comandos da tabela COMANDOS PERMITIDOS; saÃ­da mostrada sÃ³ se for Tier A (verbatim da SPEC); senÃ£o "resultado esperado".
- CÃ³digo de mod mostrado: copie de arquivos reais (com o caminho no cabeÃ§alho do bloco) ou escreva exemplos curtos que usem SÃ“ nomes confirmados no d.ts. A partir da T2, forma tipada (`import type { Register } from 'claude-code'`, `export const register: Register = (on, options) => {â€¦}`), funÃ§Ãµes que recebem `$` declaradas no topo do arquivo.
- Escape HTML dentro de `<pre>`: `&lt;` `&gt;` `&amp;`.
- Box "ðŸ†• Novo aqui?" para cada termo novo da API na primeira apariÃ§Ã£o.
- Variedade: â‰¥2 grids âœ“/âœ—, â‰¥1 sequÃªncia numerada (timeline), â‰¥2 boxes (ðŸ’¡ dica, âš ï¸ alerta), tabelas quando comparar.
- 1 teste rÃ¡pido (`data-ARCKHÉ-check="modulo-X-Y#q1"`, 3 opÃ§Ãµes, feedback no bloco `<!--CHECKS-->` com `ARCKHÉ.registerCheck`).
- Resumo com 5 âœ“, "PrÃ³ximo mÃ³dulo" e botÃµes â† trilha / MÃ³dulo seguinte â†’ (no Ãºltimo mÃ³dulo da trilha, aponte para `../trilhaN+1/index.html`; no 4.4, para `../../index.html`).
- `<aside>` com TOC de 6 itens curtos.
- Tamanho do corpo: 420â€“560 linhas (a pÃ¡gina montada fica entre 500 e 850).
- PortuguÃªs correto com acentos, frases curtas, sem emoji em excesso no texto corrido. Exemplos com o Rafa quando couber.
- CrÃ©dito: o Claude Mods Starter Kit Ã© da Prompt Advisers (MIT).

## VerificaÃ§Ã£o (obrigatÃ³ria antes de terminar)
```
cd ~/projetos/ccmods-tecnico && python3 scripts/montar.py && LINT_SEM_LINKS=1 python3 scripts/lint.py curso/trilhaX/modulo-X-Y.html
```
Precisa terminar em `LINT OK` para cada arquivo seu. Corrija atÃ© passar. Responda sÃ³ com as linhas de resultado do lint dos seus arquivos e, se houver, o que vocÃª nÃ£o conseguiu confirmar no d.ts.
