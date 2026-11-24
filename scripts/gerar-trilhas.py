#!/usr/bin/env python3
"""Gera context/corpos/trilha{1..4}.html do curso ccmods-tecnico a partir da SPEC + dados abaixo."""
import re, html
from pathlib import Path

RAIZ = Path.home() / 'projetos' / 'ccmods-tecnico'
spec = (RAIZ / 'context' / 'SPEC.md').read_text(encoding='utf-8')

# --- lÃª mapa congelado da SPEC ---
MODS = {}   # '1-1' -> dict(emoji, titulo, sub, tipo, topicos[])
atual = None
for linha in spec.split('\n'):
    m = re.match(r'- \*\*(\d)\.(\d) \[(.+?)\] (.+?)\*\* â€” "(.+?)" Â· (\w+)', linha)
    if m:
        atual = f'{m.group(1)}-{m.group(2)}'
        MODS[atual] = dict(emoji=m.group(3), titulo=m.group(4), sub=m.group(5), tipo=m.group(6), topicos=[])
        continue
    m = re.match(r'\s+\d\. (.+)$', linha)
    if m and atual and len(MODS[atual]['topicos']) < 6:
        MODS[atual]['topicos'].append(m.group(1).strip())
assert len(MODS) == 16 and all(len(v['topicos']) == 6 for v in MODS.values()), MODS.keys()

CORES = {1: ('emerald', '#34d399', '#a7f3d0', '#0e2018'), 2: ('blue', '#60a5fa', '#bfdbfe', '#0f1b33'),
         3: ('purple', '#c084fc', '#e9d5ff', '#1e1233'), 4: ('amber', '#fbbf24', '#fde68a', '#2a1d06')}
NOMES = {1: ('ðŸ§¬', 'Anatomia'), 2: ('âš¡', 'Eventos e estado'), 3: ('ðŸ–¥ï¸', 'Telas e comandos'), 4: ('ðŸ›¡ï¸', 'Controlar e distribuir')}
NIVEL = {1: 'TÃ©cnico', 2: 'TÃ©cnico', 3: 'TÃ©cnico', 4: 'AvanÃ§ado'}

HERO_TXT = {
 1: 'Abra um mod e veja o que tem dentro: trÃªs arquivos, uma funÃ§Ã£o register e hooks com trÃªs parÃ¢metros. Monte a pasta, carregue com --plugin-dir, instale por marketplace e termine com o seu primeiro mod funcionando, um comando que conta leituras.',
 2: 'Escolha o evento certo antes de escrever cÃ³digo. Entenda a cadeia ligada por next, guarde estado que sobrevive ao reload e faÃ§a trabalho fora do dispatch com relÃ³gio, arquivos e processos â€” sempre na forma tipada.',
 3: 'Desenhe no Claude Code: ui.render e as quatro superfÃ­cies, a faixa acima do prompt, status e avisos, painÃ©is com botÃµes, comandos de barra que respondem sem modelo e ferramentas que o modelo pode chamar.',
 4: 'Mods que mudam o fluxo: interceptar, negar, perguntar ao humano e trocar o modelo de um subagente. Depois, testar com claude plugin test, depurar com --debug, percorrer as pegadinhas e distribuir por marketplace.',
}

MOD_DESC = {
 '1-1': 'O que um mod Ã© por dentro, onde ele roda e como ele se separa do hook clÃ¡ssico, da skill e do MCP.',
 '1-2': 'A Ã¡rvore mÃ­nima: .claude-plugin/plugin.json, hooks/hooks.json e o mÃ³dulo. OpÃ§Ãµes com userConfig e validaÃ§Ã£o antes de carregar.',
 '1-3': 'Do --plugin-dir com hot-reload Ã  instalaÃ§Ã£o por marketplace, com escopo certo e desinstalaÃ§Ã£o limpa.',
 '1-4': 'O starter-mod do kit da Prompt Advisers: o comando /readcount, o contador de leituras, validate, test e claude -p.',
 '2-1': 'Os eventos agrupados por noun, a volta completa de um turno, matchers, streams e os hooks clÃ¡ssicos dentro do mod.',
 '2-2': 'A cadeia de plugins: observar, reescrever com next, responder sem next, .catch e o orÃ§amento de cada dispatch.',
 '2-3': 'Por que a variÃ¡vel de mÃ³dulo some, como declarar o contrato de estado e quando usar $.state ou $.store.',
 '2-4': 'session.start, relÃ³gio do engine, arquivos, processos locais, acordar a sessÃ£o e decidir se o mod gasta modelo.',
 '3-1': 'O que o hook de ui.render recebe, a tabela de elementos de cada superfÃ­cie e as regras de uma Ã¡rvore que valida.',
 '3-2': 'A faixa AbovePrompt compartilhada, status, toast e log, com o exemplo oficial band.tsx dissecado.',
 '3-3': 'PainÃ©is abertos por comando, dimensionados pelo bodyColumns, com botÃµes, hotkeys, campos e modo diÃ¡logo.',
 '3-4': 'Comandos de barra que respondem sem modelo, ferramentas para o modelo, opÃ§Ãµes do /config e nomes sem colisÃ£o.',
 '4-1': 'Interceptar tool.call, negar com motivo, perguntar com $.ui.ask, trocar modelo de subagente e respeitar permissÃµes.',
 '4-2': 'O engine de verdade sem modelo: mocks antes do $, comandos de ponta a ponta, relÃ³gio controlado e telas montadas.',
 '4-3': 'O log do --debug, mÃ³dulos que nÃ£o carregam, Ã¡rvores recusadas, as 23 pegadinhas e o teste de fumaÃ§a.',
 '4-4': 'marketplace.json, repositÃ³rio, versÃµes, revisÃ£o antes de compartilhar, o projeto final e os prÃ³ximos passos.',
}

# (emoji, dica curta, o que Ã©, por que aprender, conceitos-chave) â€” na ordem dos tÃ³picos da SPEC
T = {
'1-1': [
 ('ðŸ”Œ', 'register roda, hooks entram na cadeia', 'Quando o Claude Code carrega um mod, ele importa o mÃ³dulo, chama register(on, options) e passa a chamar os hooks registrados a cada evento.', 'Entender esse momento explica por que um mod pode mudar o que o Claude vÃª, desenha e faz sem tocar no cÃ³digo do Claude Code.', 'mod, plugin, function hook, register, carregamento.'),
 ('ðŸ§©', 'quatro formas de estender', 'Mod roda dentro do processo, em um ambiente prÃ³prio; hook clÃ¡ssico Ã© um comando de shell do settings.json; skill Ã© instruÃ§Ã£o para o modelo; MCP Ã© um servidor de ferramentas.', 'Escolher a forma errada custa caro: muita coisa que parece mod se resolve com uma skill, e vice-versa.', 'mod, hook clÃ¡ssico, skill, MCP, settings.json.'),
 ('âœï¸', 'on adiciona, options lÃª a config', 'A funÃ§Ã£o exportada recebe on, para registrar hooks, e options, com os valores dos campos que o manifesto declara em userConfig.', 'Ã‰ a Ãºnica porta de entrada do mod: tudo o que ele faz comeÃ§a nessa funÃ§Ã£o.', 'register, on(evento, matcher?, hook), options, userConfig.'),
 ('ðŸŽ›ï¸', '$, e e next', 'Todo hook tem a forma ($, e, next): $ Ã© a interface do engine, e Ã© a entrada do evento e next(e) passa adiante na cadeia.', 'Esses trÃªs nomes aparecem em todo exemplo do curso; dominÃ¡-los Ã© ler qualquer mod.', '$, e, next, cadeia, resultado do evento.'),
 ('ðŸ“¦', 'sem DOM, sem Node', 'O mÃ³dulo Ã© um ES module que roda num ambiente prÃ³prio, sem DOM e sem Node; tudo fora dele Ã© alcanÃ§ado pelo $.', 'Evita o erro mais comum de quem chega: importar fs do Node ou usar import() dinÃ¢mico, que nÃ£o carregam.', 'ES module, ambiente isolado, $ como Ãºnica saÃ­da, import estÃ¡tico.'),
 ('ðŸ—ºï¸', 'quatro trilhas, dois kits', 'O caminho do curso, do primeiro mod ao marketplace, e os dois kits usados: o Claude Mods Starter Kit (Prompt Advisers, MIT) e o ARCKHÉ-mods.', 'VocÃª sabe de onde vem cada exemplo e em que versÃ£o foi conferido: Claude Code 2.1.289.', 'starter kit, ARCKHÉ-mods, versÃ£o 2.1.289, acesso antecipado.'),
],
'1-2': [
 ('ðŸŒ³', 'trÃªs arquivos', 'A pasta do mod com .claude-plugin/plugin.json, hooks/hooks.json e o mÃ³dulo de hooks, mais tests/ quando houver teste.', 'Com a Ã¡rvore certa o Claude Code acha o mod; com um nome trocado, nada carrega e nada avisa alto.', 'pasta do plugin, .claude-plugin, hooks/, tests/.'),
 ('ðŸªª', 'nome, versÃ£o, descriÃ§Ã£o', 'O manifesto do plugin: name, version, description e, quando houver, userConfig e types.', 'O name vira o prefixo de comandos, ferramentas e estado; mudar depois quebra quem jÃ¡ usa.', 'plugin.json, name, version, manifesto.'),
 ('ðŸ§­', 'modules: um caminho', 'O hooks.json lista em modules o caminho do mÃ³dulo, relativo ao prÃ³prio hooks.json, como {"modules":["./starter.mjs"]}.', 'Ã‰ o elo entre o manifesto e o cÃ³digo; o validate mostra se ele aponta para o lugar certo.', 'hooks.json, modules, caminho relativo.'),
 ('ðŸ“„', '.mjs, .ts ou .tsx', 'O mÃ³dulo pode ser .ts, .tsx, .jsx, .js, .mjs, .cjs, .mts ou .cts, e Ã© sempre ES module; outro sufixo nÃ£o carrega.', 'O kit comeÃ§a em .mjs sem compilaÃ§Ã£o; a partir da trilha 2 o curso usa .tsx tipado.', 'extensÃ£o, ES module, TypeScript, JSX com h.'),
 ('âš™ï¸', 'opÃ§Ãµes no /config', 'Campos declarados em userConfig no plugin.json viram linhas do menu de configuraÃ§Ã£o e chegam ao mod em options.', 'Deixa o usuÃ¡rio ajustar o mod sem editar cÃ³digo, e cada mudanÃ§a recarrega o mÃ³dulo.', 'userConfig, options, pluginConfigs, /config.'),
 ('âœ…', 'claude plugin validate', 'O comando lÃª o manifesto e o cÃ³digo do mÃ³dulo como o engine leria e lista os hooks, as chamadas e o que seria recusado.', 'Pega o erro antes de abrir uma sessÃ£o: Ã© o primeiro passo de todo ciclo de mudanÃ§a.', 'claude plugin validate, hooks listados, calls, Validation passed.'),
],
'1-3': [
 ('ðŸ“‚', 'sÃ³ nesta sessÃ£o', 'A flag carrega o mod de uma pasta do disco sÃ³ para aquela sessÃ£o; repita a flag para carregar vÃ¡rios.', 'Ã‰ o jeito de desenvolver: nada fica instalado, e fechar a sessÃ£o desfaz tudo.', '--plugin-dir, sessÃ£o, pasta local.'),
 ('â™»ï¸', 'salvou, recarregou', 'Numa sessÃ£o interativa a pasta Ã© vigiada: salvar um arquivo roda o register de novo num ambiente novo, e os timers antigos caem.', 'VocÃª ajusta e vÃª na hora, sem reiniciar o Claude Code.', 'hot-reload, pasta vigiada, ambiente novo, timers.'),
 ('ðŸ–¥ï¸', 'quando nÃ£o dÃ¡ para passar flag', 'A variÃ¡vel de ambiente nomeia as mesmas pastas, com caminho absoluto, para sessÃµes abertas pelo app desktop ou por um SDK.', 'No desktop nÃ£o existe linha de comando para pÃ´r a flag; a variÃ¡vel resolve.', 'CLAUDE_CODE_PLUGIN_DIRS, desktop, SDK, settings env.'),
 ('ðŸª', 'marketplace add + install', 'Registrar uma pasta ou repositÃ³rio como marketplace e instalar o plugin dele com claude plugin install.', 'Ã‰ como o mod chega Ã s sessÃµes de todo dia sem flag nenhuma.', 'marketplace, claude plugin marketplace add, claude plugin install.'),
 ('ðŸŽšï¸', 'user, project, local', 'O escopo diz onde a instalaÃ§Ã£o vale: para vocÃª em todo projeto, para o projeto inteiro ou sÃ³ na sua cÃ³pia local.', 'Instalar no escopo errado espalha o mod onde nÃ£o devia ou esconde de quem precisa.', '--scope user, project, local.'),
 ('ðŸ§¹', 'disable e uninstall', 'Desligar com claude plugin disable e remover a instalaÃ§Ã£o sem deixar marketplace ou config esquecidos.', 'Mod que nÃ£o sai direito vira suspeito de todo comportamento estranho depois.', 'claude plugin disable, remover a instalaÃ§Ã£o, claude plugin list.'),
],
'1-4': [
 ('ðŸ“‹', 'templates/starter-mod', 'Copiar o modelo do kit da Prompt Advisers, que jÃ¡ traz manifesto, hooks.json, starter.mjs e um teste.', 'ComeÃ§ar de um mod que passa no validate e no test tira o atrito do primeiro dia.', 'starter-mod, cÃ³pia, read-counter-example.'),
 ('ðŸ”Ž', 'session.start, tool.call, command.run', 'O starter.mjs registra o comando em session.start, conta leituras bem-sucedidas em tool.call com matcher Read e responde em command.run.', 'SÃ£o trÃªs dos eventos mais usados, num arquivo curto que vocÃª lÃª inteiro.', 'session.start, tool.call, matcher, command.run, $.command.register.'),
 ('ðŸ§ª', 'validate e test', 'Rodar claude plugin validate e claude plugin test na pasta copiada e ler as duas saÃ­das.', 'VocÃª confirma que a cÃ³pia estÃ¡ Ã­ntegra antes de mudar uma linha.', 'Validation passed, 1 pass, 0 fail.'),
 ('âš¡', 'claude -p sem modelo', 'Chamar /readcount com claude -p e --plugin-dir: o prÃ³prio mod responde, sem turno do modelo.', 'Ã‰ o teste de fumaÃ§a mais barato que existe e vale para qualquer comando de mod.', 'claude -p, comando de barra, resposta sem modelo.'),
 ('ðŸ”§', 'outra ferramenta no matcher', 'Trocar o matcher do tool.call para contar outra ferramenta, como Edit ou Write, e rodar o teste de novo.', 'Ã‰ a primeira mudanÃ§a real: vocÃª vÃª o teste quebrar e sabe consertar.', 'matcher, tool, teste que falha, ajuste.'),
 ('ðŸ·ï¸', 'nome, comando, estado', 'Trocar o name do manifesto, o nome do comando e as mensagens para o mod virar seu.', 'Nome repetido colide com outros mods; seu nome Ã© o prefixo de tudo o que o mod registra.', 'name, prefixo, colisÃ£o, README.'),
],
'2-1': [
 ('ðŸ—‚ï¸', 'tool, ui, session, turn...', 'Cada evento Ã© noun.aÃ§Ã£o; agrupar por noun mostra o que o mod pode tocar: ferramentas, tela, sessÃ£o, turno, prompt, estado.', 'Ver o mapa inteiro evita escrever em ui.render o que deveria ser um tool.call.', 'evento, noun, tool, ui, session, turn, prompt.'),
 ('ðŸ”', 'prompt.submit a turn.complete', 'A ordem em que os eventos disparam: prompt.submit, turn.start, turn.step, tool.call, session.append e turn.complete.', 'Saber onde vocÃª estÃ¡ na volta diz o que jÃ¡ aconteceu e o que ainda dÃ¡ para mudar.', 'turno, prompt.submit, turn.start, turn.step, turn.complete.'),
 ('ðŸŽ¯', 'o segundo argumento do on', 'O matcher filtra quais eventos chegam ao hook, como { tool: \'Read\' } ou { command: \'readcount\' }.', 'Hook sem matcher roda em tudo e gasta orÃ§amento Ã  toa.', 'matcher, filtro, on(evento, matcher, hook).'),
 ('ðŸŒŠ', 'turn.step e process.spawn', 'Dois eventos sÃ£o stream: o hook Ã© um async generator, e yield* next(e) repassa os pedaÃ§os.', 'Hook comum nesses eventos nÃ£o carrega; o erro sÃ³ aparece no --debug.', 'stream, async function*, yield* next(e), for await.'),
 ('ðŸª', 'classic.PreToolUse e cia.', 'Os hooks clÃ¡ssicos do settings.json aparecem para o mod como classic.<Nome>, com a mesma entrada que o hook receberia.', 'VocÃª aproveita o que jÃ¡ conhece de hooks clÃ¡ssicos sem sair do mod.', 'classic.PreToolUse, classic.Stop, hook clÃ¡ssico.'),
 ('ðŸ“–', 'index.d.ts manda', 'Procurar qualquer evento, entrada e resultado no arquivo de tipos da sua instalaÃ§Ã£o, .claude-plugin/types/claude-code/index.d.ts.', 'A API estÃ¡ em acesso antecipado e muda: o arquivo da sua versÃ£o Ã© a autoridade, nÃ£o a memÃ³ria.', 'declaraÃ§Ã£o de tipos, index.d.ts, grep, versÃ£o.'),
],
'2-2': [
 ('â›“ï¸', 'todos os plugins + o engine', 'Os hooks de todos os plugins e o comportamento do prÃ³prio Claude Code formam uma cadeia ligada por next.', 'Seu mod nÃ£o estÃ¡ sozinho: o que vocÃª devolve Ã© o que os outros e o engine recebem.', 'cadeia, ordem, engine, plugins vizinhos.'),
 ('ðŸ‘€', 'return next(e)', 'O hook mais simples olha o evento, registra algo e devolve next(e) sem mudar nada.', 'Ã‰ o padrÃ£o seguro: medir sem interferir.', 'observar, next(e), efeito colateral.'),
 ('âœï¸', 'next({ ...e, ... })', 'Chamar next com um evento alterado muda o que o resto da cadeia vÃª, dentro do que aquele evento permite.', 'Ã‰ como um mod corrige um caminho, acrescenta contexto ou troca um modelo.', 'reescrever, spread, campos permitidos.'),
 ('ðŸ›‘', 'quem nÃ£o chama next decide', 'Um hook que retorna sem chamar next responde pelo evento, e a cadeia abaixo dele nÃ£o roda.', 'Ã‰ o poder de negar uma ferramenta ou responder um comando, e tambÃ©m o maior risco do mod.', 'responder, deny, curto-circuito.'),
 ('ðŸª‚', 'o registro tem .catch', 'O .catch encadeado no on responde no lugar do hook que falhou; sem ele, o hook Ã© pulado e a cadeia segue.', 'Falha silenciosa num mod de seguranÃ§a deixa passar o que devia barrar.', '.catch, hook pulado, padrÃ£o seguro.'),
 ('â³', 'tempo do dispatch', 'Cada hook tem orÃ§amento de tempo dentro do dispatch, e next.signal aborta quando o dispatch Ã© abandonado.', 'Trabalho longo dentro do hook Ã© cortado; o que precisa durar vai para fora.', 'dispatch, orÃ§amento, next.signal, abort.'),
],
'2-3': [
 ('ðŸ’¨', 'reload limpa o mÃ³dulo', 'Cada hot-reload roda o register num ambiente novo; a variÃ¡vel de mÃ³dulo volta ao valor inicial.', 'O contador que zera do nada Ã© o sintoma nÃºmero um de estado no lugar errado.', 'variÃ¡vel de mÃ³dulo, hot-reload, ambiente novo.'),
 ('ðŸ“œ', 'PluginState no contrato', 'Declarar o formato do estado do plugin em types/index.d.ts e apontar o arquivo em "types" no plugin.json.', 'Com o contrato, o editor e o tsc conferem cada leitura e escrita de estado.', 'types/index.d.ts, PluginState, "types", contrato.'),
 ('âš›ï¸', 'a biblioteca de estado', 'atom, read e update vÃªm de import { ... } from "claude-code" e leem e gravam $.state com controle de versÃ£o.', 'update nÃ£o perde clique: dois toques antes do redesenho contam os dois.', 'atom, read, update, $.state.get, $.state.set, ifVersion.'),
 ('ðŸ—„ï¸', 'para alÃ©m da sessÃ£o', 'O $.store guarda valores entre sessÃµes com get, set, delete e keys.', '$.state vale para a sessÃ£o; o que precisa voltar amanhÃ£ vai para o store.', '$.store.get, $.store.set, persistÃªncia.'),
 ('ðŸ•°ï¸', '$.clock, nÃ£o Date', 'O engine dÃ¡ o relÃ³gio do mod: now para a hora e timers que o teste pode controlar.', 'Usar o relÃ³gio do engine deixa o mod testÃ¡vel sem esperar tempo real.', '$.clock.now, relÃ³gio controlado, teste.'),
 ('ðŸ§­', 'mÃ³dulo, state ou store', 'A regra de decisÃ£o: constante no mÃ³dulo, estado da sessÃ£o em $.state, o que sobrevive entre sessÃµes em $.store.', 'Cada dado no lugar certo evita perda no reload e lixo acumulado no disco.', 'decisÃ£o, escopo do dado, sessÃ£o, persistÃªncia.'),
],
'2-4': [
 ('ðŸŒ…', 'pronto antes do 1Âº prompt', 'O session.start dispara uma vez, quando a sessÃ£o fica pronta, e Ã© aguardado antes do primeiro prompt.', 'Ã‰ o lugar de registrar comandos e ferramentas e de acender o que roda em segundo plano.', 'session.start, inicializaÃ§Ã£o, $.command.register, $.tool.register.'),
 ('â²ï¸', 'timers do engine', 'clock.every repete e clock.after agenda uma vez; os timers duram atÃ© serem cancelados ou o mÃ³dulo recarregar.', 'Trabalho periÃ³dico fora do dispatch nÃ£o tem orÃ§amento cortando no meio.', '$.clock.every, $.clock.after, cancelamento, reload.'),
 ('ðŸ“', 'ler, escrever, listar', 'O $.fs lÃª texto ou bytes, escreve, lista e dÃ¡ stat de caminhos, com realPath para guardas robustas.', 'Sem Node, o $.fs Ã© a Ãºnica forma de o mod tocar arquivos.', '$.fs.read, $.fs.write, $.fs.stat, realPath.'),
 ('ðŸ› ï¸', 'comando por argv', 'O $.process.run roda um comando do sistema por argv, e $.process.spawn entrega a saÃ­da em pedaÃ§os.', 'git status, contagem de linhas, scripts locais: tudo por argv, sem shell montado em string.', '$.process.run, $.process.spawn, argv.'),
 ('ðŸ””', 'trabalho que vira turno', 'O $.prompt.submit pÃµe um prompt na fila que comeÃ§a um turno quando a sessÃ£o fica ociosa.', 'Deixa um mod de segundo plano chamar o modelo na hora certa, sem atropelar o turno em curso.', '$.prompt.submit, fila, sessÃ£o ociosa.'),
 ('ðŸ’¸', 'model.complete custa', 'O $.model.complete e o $.model.fork chamam o modelo pelo cliente da sessÃ£o e consomem uso.', 'Mod que gasta modelo escondido surpreende quem usa; a regra Ã© avisar e deixar desligar.', '$.model.complete, $.model.fork, uso, consentimento.'),
],
'3-1': [
 ('ðŸŽ¨', 'component, surface, props', 'O hook de ui.render recebe uma instÃ¢ncia de componente: e.component, e.surface, e.requestId, e.props e e.viewport.', 'Com esses campos vocÃª decide se desenha, onde desenha e do tamanho certo.', 'ui.render, component, surface, requestId, viewport.'),
 ('ðŸ§±', 'elementos por superfÃ­cie', 'O $.ui.resolve(e) devolve a tabela de construtores da superfÃ­cie, que vocÃª desestrutura nas tags JSX.', 'O mÃ³dulo nÃ£o tem elementos globais; sem resolve nÃ£o hÃ¡ Box nem Text.', '$.ui.resolve, Box, Text, JSX com h.'),
 ('ðŸ“±', 'terminal, desktop, mobile, vscode', 'Cada superfÃ­cie tem sua tabela: o terminal nÃ£o tem Svg, mas tem Raster e Image; o mobile nÃ£o tem Input nem Select.', 'Uma Ã¡rvore com elemento que a superfÃ­cie nÃ£o tem nÃ£o Ã© desenhada.', 'superfÃ­cie, Elements, diferenÃ§as, narrowing por e.surface.'),
 ('ðŸ“', 'render sÃ³ lÃª', 'O hook de render lÃª o estado com $.state.get e nunca escreve; quem escreve Ã© um handler ou outro evento.', 'Escrever ao desenhar Ã© negado; ler assina a instÃ¢ncia e o redesenho vem sozinho.', 'render puro, $.state.get, handler, redesenho.'),
 ('ðŸš«', 'o engine desenha o dele', 'Uma Ã¡rvore que nÃ£o valida nÃ£o Ã© desenhada: o engine desenha a prÃ³pria e registra o motivo no log.', 'Saber ler essa linha poupa horas de "por que nÃ£o aparece nada".', 'validaÃ§Ã£o, ui.render refused, debug log.'),
 ('ðŸ–¼ï¸', 'pixels no terminal', 'Raster desenha uma grade de cÃ©lulas coloridas; Image mostra uma figura pelo protocolo grÃ¡fico do terminal, com alt nos outros.', 'GrÃ¡ficos e mapas de calor sem um Box por cÃ©lula.', 'Raster, Image, $.ui.blit, alt.'),
],
'3-2': [
 ('ðŸ“Ÿ', 'AbovePrompt', 'O componente AbovePrompt Ã© a faixa acima da caixa de prompt; o hook desenha nela com o tamanho de bodyColumns.', 'Ã‰ o lugar de informaÃ§Ã£o contÃ­nua: contadores, avisos, estado do mod.', 'AbovePrompt, faixa, bodyColumns.'),
 ('ðŸ¤', 'uma faixa para todos', 'A faixa Ã© uma sÃ³ e compartilhada: o exemplo oficial band.tsx mostra como desenhar nela sem apagar os vizinhos.', 'Um mod que toma a faixa inteira apaga os vizinhos.', 'compartilhar, next, composiÃ§Ã£o.'),
 ('ðŸ”†', 'status sem abrir nada', 'O $.ui.status mostra um estado curto sem abrir painel e sem comeÃ§ar turno.', 'InformaÃ§Ã£o discreta nÃ£o precisa de tela prÃ³pria.', '$.ui.status, linha de status, sem turno.'),
 ('ðŸ“£', 'toast e log', 'O $.ui.toast dÃ¡ um aviso passageiro e o $.ui.log escreve uma linha no registro, sem chamar o modelo.', 'Avisos certos no lugar certo, sem poluir a conversa.', '$.ui.toast, $.ui.log, aviso, registro.'),
 ('ðŸ”¬', 'band.tsx linha a linha', 'Ler o exemplo oficial da faixa que vem com o Claude Code: estado tipado, resolve, Ã¡rvore e botÃ£o.', 'Ã‰ o modelo mais curto e correto de faixa que existe para copiar.', 'examples/band.tsx, band-state.d.ts, referÃªncia oficial.'),
 ('ðŸ§ª', 'mount nas duas superfÃ­cies', 'Montar a faixa num teste para terminal e desktop, com o mesmo corpo num laÃ§o.', 'Prova que o mod nÃ£o depende de uma superfÃ­cie sÃ³.', 'claude plugin test, mount, terminal, desktop.'),
],
'3-3': [
 ('ðŸªŸ', 'Pane', 'O $.ui.open abre um painel, o componente Pane, que o hook de ui.render desenha.', 'Painel Ã© a tela prÃ³pria do mod: listas, detalhes, formulÃ¡rios.', '$.ui.open, Pane, requestId.'),
 ('ðŸ“', 'largura que muda', 'O painel desenha no bodyColumns, mais estreito que a tela quando fica ao lado da conversa.', 'Ãrvore dimensionada pelo viewport quebra quando o painel estÃ¡ encaixado.', 'bodyColumns, viewport, isFullscreen.'),
 ('ðŸ”˜', 'Button e hotkey', 'BotÃµes com label, variant e hotkey de uma letra ou dÃ­gito, que funcionam quando o painel tem o teclado.', 'Atalho de uma tecla torna o painel usÃ¡vel sem mouse.', 'Button, hotkey, variant, foco.'),
 ('ðŸ–±ï¸', 'ui.press, ui.input, ui.select', 'Os handlers ficam no plugin e disparam os eventos ui.press, ui.input e ui.select com a chave do elemento.', 'Ã‰ assim que um clique vira aÃ§Ã£o e um texto digitado vira dado.', 'ui.press, ui.input, ui.select, key.'),
 ('ðŸ’¬', 'focus, closeOnEscape, holdToasts', 'Abrir o painel com focus, closeOnEscape e holdToasts faz ele se comportar como diÃ¡logo.', 'DiÃ¡logo prende a atenÃ§Ã£o do usuÃ¡rio; deixar holdToasts num painel fixo trava os avisos.', 'diÃ¡logo, focus, closeOnEscape, holdToasts.'),
 ('ðŸšª', 'fechar e liberar', 'Fechar o painel por botÃ£o de dispensa ou por Esc e limpar o estado ligado a ele.', 'Painel que nÃ£o fecha ou estado que sobra confunde a prÃ³xima abertura.', 'role dismiss, Esc, limpeza de estado.'),
],
'3-4': [
 ('âŒ¨ï¸', '$.command.register', 'Registrar um comando de barra com nome e descriÃ§Ã£o, normalmente no session.start.', 'Comando de mod roda na hora e nÃ£o precisa de modelo.', '$.command.register, session.start, /comando.'),
 ('â†©ï¸', 'command.run com matcher', 'Responder o evento command.run, filtrado pelo nome do comando, com { text } e, se quiser, context.', 'text Ã© a linha que aparece e o modelo tambÃ©m lÃª; context sÃ³ o modelo lÃª.', 'command.run, { text }, context.'),
 ('ðŸ–¨ï¸', 'CommandOutput', 'Desenhar a saÃ­da do comando como Ã¡rvore na conversa hookando o componente CommandOutput.', 'A resposta vira tabela ou card em vez de texto cru.', 'CommandOutput, ui.render, matcher por props.'),
 ('ðŸ§°', '$.tool.register', 'Declarar uma ferramenta com nome, descriÃ§Ã£o e schema, servida por um hook de tool.call; ela aparece como mcp__<plugin>__<nome>.', 'O modelo passa a usar uma capacidade que sÃ³ o seu mod oferece.', '$.tool.register, tool.call, schema, mcp__plugin__nome.'),
 ('ðŸ”§', 'options na prÃ¡tica', 'Ler os valores que o usuÃ¡rio ajustou no /config pelo options do register, com padrÃµes do manifesto.', 'Mudar uma opÃ§Ã£o recarrega o mÃ³dulo; o mod nunca lÃª config velha.', 'userConfig, options, picker, /config.'),
 ('ðŸ·ï¸', 'prefixe tudo', 'Escolher nomes de comandos, ferramentas e chaves de estado que nÃ£o batam com os de outros mods.', 'Dois mods com o mesmo comando brigam, e o usuÃ¡rio nÃ£o sabe qual respondeu.', 'colisÃ£o, prefixo, nome do plugin.'),
],
'4-1': [
 ('ðŸ›‘', 'tool.call antes de rodar', 'Hookar tool.call com matcher na ferramenta e olhar a entrada antes de a chamada acontecer.', 'Ã‰ o ponto em que um mod pode impedir um estrago, nÃ£o apenas registrÃ¡-lo.', 'tool.call, matcher, entrada da ferramenta.'),
 ('ðŸš«', 'deny com mensagem', 'Responder sem next com um motivo que o modelo lÃª e entende como recusa.', 'Recusa sem motivo faz o modelo tentar de novo do mesmo jeito.', 'deny, motivo, resposta sem next.'),
 ('ðŸ™‹', '$.ui.ask', 'Perguntar ao humano com opÃ§Ãµes antes de seguir, com a opÃ§Ã£o segura primeiro e um .catch para quando nÃ£o hÃ¡ tela.', 'Sem tela (claude -p) ou sem resposta, o mod precisa de um padrÃ£o seguro e explÃ­cito.', '$.ui.ask, opÃ§Ã£o segura, .catch, afk.'),
 ('ðŸ”€', 'agent.spawn', 'Hookar agent.spawn para escolher o modelo de um subagente antes de ele rodar, como faz o roteador-subagente.', 'Tarefas simples em modelo menor economizam uso sem mudar o fluxo.', 'agent.spawn, subagente, modelo, roteador-subagente.'),
 ('ðŸ”', 'nÃ£o passar por cima', 'Um mod nÃ£o deve afrouxar o que o usuÃ¡rio configurou: negar Ã© ok, liberar o que estava bloqueado nÃ£o.', 'Mod que fura permissÃ£o vira risco de seguranÃ§a para quem instala.', 'permissÃµes, classic.PreToolUse, menor privilÃ©gio.'),
 ('ðŸ§¯', 'freio-de-mao', 'Ler a guarda do ARCKHÉ-mods que mede o estrago de um comando destrutivo e pergunta antes: prosseguir, lixeira, backup ou cancelar.', 'Ã‰ um mod de controle real, curto, com teste e caminho para sessÃ£o sem tela.', 'freio-de-mao, $.process.run, $.ui.ask, $.ui.toast.'),
],
'4-2': [
 ('ðŸ§ª', 'o engine sem modelo', 'O claude plugin test roda os *.test.ts com o engine de verdade; os hooks do teste ficam abaixo do plugin e fazem o papel do engine.', 'Testa o mod como ele roda numa sessÃ£o, sem gastar modelo.', 'claude plugin test, claude-code/testing, test, expect, mock.'),
 ('ðŸ§©', 'o mundo antes do $', 'Responder no teste cada noun que o mod usa (session.start, fs, store, ui...) antes de chamar o cÃ³digo.', 'Nada responde por baixo do plugin: faltou mock, o teste diz exatamente qual.', 'mocks, mundo.ts, noun faltando.'),
 ('ðŸ”', 'comando de ponta a ponta', 'Disparar o comando no teste e conferir o texto devolvido e o estado gravado.', 'Ã‰ a prova de que o caminho todo funciona, nÃ£o sÃ³ uma funÃ§Ã£o.', 'command.run, asserÃ§Ã£o, estado.'),
 ('â©', 'mock.clock', 'AvanÃ§ar o relÃ³gio do teste para disparar timers sem esperar tempo real.', 'Mod com clock.every testado em milissegundos, sempre igual.', 'mock.clock, timers, determinismo.'),
 ('ðŸ–¥ï¸', 'mount em terminal e desktop', 'Montar o componente pelo ui do teste numa superfÃ­cie nomeada e agir por chave com press, input e find.', 'O mesmo corpo de teste em duas superfÃ­cies prova que o mod nÃ£o depende de uma.', 'mount, press, input, find, superfÃ­cie.'),
 ('ðŸ©»', 'pass, fail e a mensagem', 'Ler a saÃ­da do teste: quantos pass, quantos fail e a linha que diz o que faltou.', 'Uma falha bem lida aponta a correÃ§Ã£o em uma linha.', 'pass, fail, mensagem de erro, timeout de 5 s.'),
],
'4-3': [
 ('ðŸ”¦', 'claude --debug', 'Rodar com --debug para ter no log uma linha para cada hook pulado e cada resultado recusado.', 'Mod que parece nÃ£o fazer nada quase sempre jÃ¡ disse por quÃª no log.', 'claude --debug, debug log.'),
 ('ðŸ“ƒ', 'plugin, evento, motivo', 'A linha do hook pulado traz o plugin, o evento e o nome do erro; o texto da primeira, encurtado, aparece na transcriÃ§Ã£o.', 'Ler essa linha Ã© metade da depuraÃ§Ã£o.', 'hook pulado, motivo, transcriÃ§Ã£o.'),
 ('ðŸ§±', 'import() e sufixo', 'MÃ³dulo com import() dinÃ¢mico, arquivo com sufixo fora da lista ou caminho errado no hooks.json nÃ£o carregam.', 'SÃ£o as causas mais comuns de "o mod sumiu".', 'import(), sufixo, hooks.json, validate.'),
 ('ðŸªŸ', 'elemento que nÃ£o existe', 'Achar no log a linha da Ã¡rvore que nÃ£o valida e trocar o elemento ou a prop que a superfÃ­cie nÃ£o aceita.', 'Sem isso o engine continua desenhando o dele e vocÃª nÃ£o vÃª o seu.', 'ui.render refused, elemento, prop.'),
 ('ðŸ“‹', '23 pegadinhas', 'A lista do docs/COMO-FAZER-UM-MOD.md do ARCKHÉ-mods: funÃ§Ãµes com $ no topo, mocks, opÃ§Ã£o segura primeiro e as outras.', 'Cada pegadinha foi um erro real; ler antes poupa o mesmo erro.', 'COMO-FAZER-UM-MOD.md, pegadinhas, checar-mod.sh.'),
 ('ðŸ’¨', 'o comando responde?', 'Rodar o comando do mod com claude -p e --plugin-dir e conferir a resposta sem abrir sessÃ£o interativa.', 'FumaÃ§a rÃ¡pida antes de qualquer commit.', 'claude -p, --plugin-dir, teste de fumaÃ§a.'),
],
'4-4': [
 ('ðŸ“‡', 'a vitrine dos plugins', 'O .claude-plugin/marketplace.json lista os plugins com name e source, como no kit: ./plugins/<nome>.', 'Ã‰ o que permite instalar o seu mod com um comando.', 'marketplace.json, plugins, source.'),
 ('ðŸŒ', 'dono/repo', 'PÃ´r o mod num repositÃ³rio pÃºblico e adicionÃ¡-lo como marketplace pelo caminho dono/repo.', 'Quem usa instala direto do repositÃ³rio e recebe atualizaÃ§Ãµes.', 'repositÃ³rio, claude plugin marketplace add, dono/repo.'),
 ('ðŸ”¼', 'version e update', 'Subir a version a cada mudanÃ§a e saber que quem instalou recebe por claude plugin update e /reload-plugins.', 'Mudar nome de comando ou formato de estado sem aviso quebra quem jÃ¡ usa.', 'version, claude plugin update, /reload-plugins, compatibilidade.'),
 ('ðŸ”', 'checklist final', 'validate, test com 0 fail, README, botÃ£o ou comando de desligar e nada que gaste modelo sem avisar.', 'Mod compartilhado roda na mÃ¡quina de outra pessoa: o cuidado Ã© seu.', 'revisÃ£o, README, desligar, consentimento.'),
 ('ðŸ', 'o mod do Rafa', 'Comando /x, faixa ou painel, estado em $.state, teste com mocks, validate OK e comando de desligar.', 'Junta tudo o que o curso ensinou num mod que vocÃª mesmo usa.', 'projeto final, claude plugin test, claude -p.'),
 ('ðŸ§­', 'cchooks, MakeClaudeX e mais', 'Os cursos de hooks clÃ¡ssicos, de plugins de produÃ§Ã£o e o curso-agent-runtime, alÃ©m dos dois kits.', 'O curso termina; os mods continuam mudando a cada versÃ£o.', 'cchooks, MakeClaudeX, curso-agent-runtime, kits.'),
],
}

# --- SVGs do hero, um por trilha (ids com prefixo t<N>a-) ---
def svg_hero(n):
    _, c1, c2, cbg = CORES[n]
    p = f't{n}a-'
    defs = (f'<defs>\n            <pattern id="{p}grid" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="1.2" cy="1.2" r="1.2" fill="{c1}" opacity="0.12"/></pattern>\n'
            f'            <filter id="{p}glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="1.8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>\n'
            f'            <marker id="{p}seta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#38bdf8"/></marker>\n          </defs>')
    if n == 1:
        label = 'Uma pasta de mod aberta: plugin.json aponta para hooks.json, que aponta para o mÃ³dulo. Do mÃ³dulo sai a funÃ§Ã£o register(on, options), e dela trÃªs hooks com a forma ($, e, next).'
        corpo = f'''<g font-family="Inter,sans-serif" font-size="11">
            <rect x="20" y="20" width="150" height="200" rx="10" fill="{cbg}" stroke="{c1}" stroke-width="1.8"/>
            <text x="34" y="42" fill="{c1}" font-weight="600">ðŸ“ meu-mod/</text>
            <rect x="34" y="56" width="124" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.5"/><text x="96" y="73" text-anchor="middle" fill="#bae6fd">plugin.json</text>
            <rect x="34" y="104" width="124" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.5"/><text x="96" y="121" text-anchor="middle" fill="#bae6fd">hooks.json</text>
            <g filter="url(#{p}glow)"><rect x="34" y="152" width="124" height="26" rx="6" fill="{cbg}" stroke="{c1}" stroke-width="2"/></g><text x="96" y="169" text-anchor="middle" fill="{c2}">starter.mjs</text>
            <line x1="96" y1="82" x2="96" y2="102" stroke="#38bdf8" stroke-width="1.6" marker-end="url(#{p}seta)"/>
            <line x1="96" y1="130" x2="96" y2="150" stroke="#38bdf8" stroke-width="1.6" marker-end="url(#{p}seta)"/>
            <text x="96" y="205" text-anchor="middle" fill="{c2}" font-size="10">trÃªs arquivos</text>
            <line class="wf-flow" x1="158" y1="165" x2="206" y2="120" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <rect x="208" y="98" width="156" height="34" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="2"/><text x="286" y="120" text-anchor="middle" fill="{c1}" font-weight="600">register(on, options)</text>
            <rect class="wf-a" x="200" y="30" width="54" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.5"/><text x="227" y="47" text-anchor="middle" fill="#bae6fd">$</text>
            <rect class="wf-a" x="260" y="30" width="54" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.5"/><text x="287" y="47" text-anchor="middle" fill="#bae6fd">e</text>
            <rect class="wf-a" x="320" y="30" width="54" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.5"/><text x="347" y="47" text-anchor="middle" fill="#bae6fd">next</text>
            <line x1="286" y1="98" x2="286" y2="60" stroke="{c1}" stroke-width="1.6" marker-end="url(#{p}seta)"/>
            <rect x="208" y="160" width="156" height="60" rx="8" fill="none" stroke="{c1}" stroke-width="1.4" stroke-dasharray="4 3"/>
            <text x="286" y="182" text-anchor="middle" fill="{c2}">on('tool.call', â€¦)</text>
            <text x="286" y="202" text-anchor="middle" fill="{c2}">on('command.run', â€¦)</text>
            <line x1="286" y1="132" x2="286" y2="158" stroke="{c1}" stroke-width="1.6" marker-end="url(#{p}seta)"/>
          </g>'''
    elif n == 2:
        label = 'Um evento entra pela esquerda e atravessa a cadeia: plugin A observa e chama next, plugin B reescreve e chama next, e o engine responde no fim. Embaixo, o estado mora em $.state durante a sessÃ£o e em $.store entre sessÃµes.'
        corpo = f'''<g font-family="Inter,sans-serif" font-size="11" text-anchor="middle">
            <g filter="url(#{p}glow)"><circle cx="40" cy="70" r="24" fill="{cbg}" stroke="{c1}" stroke-width="2"/></g><text x="40" y="74" fill="{c1}" font-weight="600">evento</text>
            <rect class="wf-a" x="88" y="50" width="76" height="40" rx="8" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.6"/><text x="126" y="68" fill="#bae6fd">plugin A</text><text x="126" y="83" fill="#7dd3fc" font-size="9">observa</text>
            <rect class="wf-a" x="188" y="50" width="76" height="40" rx="8" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.6"/><text x="226" y="68" fill="#bae6fd">plugin B</text><text x="226" y="83" fill="#7dd3fc" font-size="9">reescreve</text>
            <rect x="288" y="50" width="76" height="40" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="2"/><text x="326" y="68" fill="{c1}">engine</text><text x="326" y="83" fill="{c2}" font-size="9">responde</text>
            <line class="wf-flow" x1="64" y1="70" x2="86" y2="70" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <line class="wf-flow" x1="164" y1="70" x2="186" y2="70" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <line class="wf-flow" x1="264" y1="70" x2="286" y2="70" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <text x="175" y="40" fill="{c2}" font-size="10">next(e) â†’ next(e) â†’ resultado</text>
            <rect x="40" y="130" width="140" height="44" rx="10" fill="{cbg}" stroke="{c1}" stroke-width="1.8"/><text x="110" y="150" fill="{c1}" font-weight="600">$.state</text><text x="110" y="165" fill="{c2}" font-size="10">vale na sessÃ£o</text>
            <rect x="200" y="130" width="140" height="44" rx="10" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.8"/><text x="270" y="150" fill="#bae6fd" font-weight="600">$.store</text><text x="270" y="165" fill="#7dd3fc" font-size="10">volta amanhÃ£</text>
            <rect x="40" y="190" width="300" height="34" rx="8" fill="none" stroke="#f87171" stroke-width="1.4" stroke-dasharray="4 3"/><text x="190" y="211" fill="#fca5a5">variÃ¡vel de mÃ³dulo: some no reload</text>
          </g>'''
    elif n == 3:
        label = 'A janela do Claude Code com trÃªs lugares onde um mod desenha: a conversa no alto, um painel encaixado Ã  direita com botÃµes e, logo acima da caixa de prompt, a faixa compartilhada. Ao lado, as quatro superfÃ­cies: terminal, desktop, mobile e vscode.'
        corpo = f'''<g font-family="Inter,sans-serif" font-size="11">
            <rect x="16" y="16" width="260" height="208" rx="10" fill="#0b1220" stroke="{c1}" stroke-width="1.8"/>
            <rect x="28" y="30" width="150" height="104" rx="6" fill="#111827" stroke="#334155" stroke-width="1"/>
            <text x="40" y="50" fill="#94a3b8">conversa</text>
            <rect x="40" y="60" width="120" height="8" rx="3" fill="#334155"/><rect x="40" y="76" width="96" height="8" rx="3" fill="#334155"/><rect x="40" y="92" width="110" height="8" rx="3" fill="#334155"/>
            <g filter="url(#{p}glow)"><rect x="186" y="30" width="78" height="104" rx="6" fill="{cbg}" stroke="{c1}" stroke-width="2"/></g>
            <text x="225" y="50" text-anchor="middle" fill="{c1}" font-weight="600">Pane</text>
            <rect x="196" y="64" width="58" height="18" rx="4" fill="none" stroke="{c2}" stroke-width="1.2"/><text x="225" y="77" text-anchor="middle" fill="{c2}" font-size="10">[ a ] abrir</text>
            <rect x="196" y="90" width="58" height="18" rx="4" fill="none" stroke="{c2}" stroke-width="1.2"/><text x="225" y="103" text-anchor="middle" fill="{c2}" font-size="10">[ x ] fechar</text>
            <rect class="wf-a" x="28" y="144" width="236" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.8"/><text x="146" y="161" text-anchor="middle" fill="#bae6fd">AbovePrompt Â· faixa de todos</text>
            <rect x="28" y="180" width="236" height="30" rx="6" fill="#111827" stroke="#475569" stroke-width="1.2"/><text x="40" y="199" fill="#94a3b8">&gt; /meu-comando</text>
            <g text-anchor="middle" font-size="10">
              <rect x="294" y="30" width="72" height="34" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="1.6"/><text x="330" y="51" fill="{c2}">terminal</text>
              <rect x="294" y="76" width="72" height="34" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="1.6"/><text x="330" y="97" fill="{c2}">desktop</text>
              <rect x="294" y="122" width="72" height="34" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="1.6"/><text x="330" y="143" fill="{c2}">mobile</text>
              <rect x="294" y="168" width="72" height="34" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="1.6"/><text x="330" y="189" fill="{c2}">vscode</text>
            </g>
          </g>'''
    else:
        label = 'Uma chamada de ferramenta perigosa chega a um escudo, que pergunta ao humano antes de deixar passar. Abaixo, a esteira de entrega: validate, test com zero falhas e marketplace.'
        corpo = f'''<g font-family="Inter,sans-serif" font-size="11" text-anchor="middle">
            <rect x="16" y="40" width="110" height="40" rx="8" fill="#2a0f0f" stroke="#f87171" stroke-width="1.8"/><text x="71" y="58" fill="#fca5a5">tool.call</text><text x="71" y="72" fill="#fca5a5" font-size="10">rm -rf build</text>
            <line class="wf-flow" x1="126" y1="60" x2="160" y2="60" stroke="#f87171" stroke-width="2" marker-end="url(#{p}seta)"/>
            <g filter="url(#{p}glow)"><path d="M190 22 L230 34 L230 66 Q230 92 190 104 Q150 92 150 66 L150 34 Z" fill="{cbg}" stroke="{c1}" stroke-width="2.2"/></g>
            <text x="190" y="62" fill="{c1}" font-weight="600">mod</text><text x="190" y="78" fill="{c2}" font-size="10">guarda</text>
            <line x1="230" y1="60" x2="262" y2="60" stroke="#38bdf8" stroke-width="2" marker-end="url(#{p}seta)"/>
            <rect class="wf-a" x="264" y="36" width="104" height="48" rx="8" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.8"/><text x="316" y="56" fill="#bae6fd">$.ui.ask </text><text x="316" y="72" fill="#7dd3fc" font-size="10">prosseguir?</text>
            <rect x="20" y="150" width="104" height="40" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="1.8"/><text x="72" y="168" fill="{c2}">validate</text><text x="72" y="182" fill="{c2}" font-size="10">âœ” passed</text>
            <rect x="140" y="150" width="104" height="40" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="1.8"/><text x="192" y="168" fill="{c2}">test</text><text x="192" y="182" fill="{c2}" font-size="10">0 fail</text>
            <rect x="260" y="150" width="104" height="40" rx="8" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.8"/><text x="312" y="168" fill="#bae6fd">marketplace</text><text x="312" y="182" fill="#7dd3fc" font-size="10">install</text>
            <line x1="124" y1="170" x2="138" y2="170" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <line x1="244" y1="170" x2="258" y2="170" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <text x="190" y="220" fill="{c2}" font-size="10">controlar â†’ testar â†’ distribuir</text>
          </g>'''
    return (f'<svg viewBox="0 0 380 240" class="w-full h-auto" role="img" aria-label="{html.escape(label)}">\n          {defs}\n'
            f'          <rect x="0" y="0" width="380" height="240" fill="url(#{p}grid)"/>\n          {corpo}\n        </svg>')

E = html.escape

def trilha(n):
    cor, c1, _, _ = CORES[n]
    emo, nome = NOMES[n]
    mids = [f'{n}-{k}' for k in range(1, 5)]
    out = [f'<!--TITLE: Trilha {n} Â· {nome} -->']
    out.append(f'''  <header class="bg-gradient-to-br from-{cor}-900/30 via-dark-800 to-dark-800 py-12 border-b border-dark-600" data-ARCKHÉ-track="{n}">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 lg:grid lg:grid-cols-[1fr_380px] lg:gap-10 lg:items-center">
      <div>
        <span class="inline-block px-3 py-1 bg-{cor}-500/20 text-{cor}-400 text-xs font-semibold rounded-full mb-4">TRILHA {n}</span>
        <h1 class="text-3xl sm:text-4xl font-bold mb-4">{emo} {nome}</h1>
        <p class="text-lg text-neutral-400 max-w-3xl">{E(HERO_TXT[n])}</p>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-8 max-w-2xl">
          <div class="bg-dark-800/50 rounded-lg p-3 border border-dark-600"><div class="text-xl font-bold text-{cor}-400">4</div><div class="text-xs text-neutral-400">MÃ³dulos</div></div>
          <div class="bg-dark-800/50 rounded-lg p-3 border border-dark-600"><div class="text-xl font-bold text-{cor}-400">24</div><div class="text-xs text-neutral-400">TÃ³picos</div></div>
          <div class="bg-dark-800/50 rounded-lg p-3 border border-dark-600"><div class="text-xl font-bold text-{cor}-400">~2h20</div><div class="text-xs text-neutral-400">DuraÃ§Ã£o</div></div>
          <div class="bg-dark-800/50 rounded-lg p-3 border border-dark-600"><div class="text-xl font-bold text-{cor}-400">{NIVEL[n]}</div><div class="text-xs text-neutral-400">NÃ­vel</div></div>
        </div>
        <div data-ARCKHÉ-meter="trilha:{n}" class="mt-6 max-w-2xl" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-label="Progresso da trilha {n}">
          <div class="flex justify-between text-xs text-neutral-400 mb-1"><span data-ARCKHÉ-meter-frac>0 de 24</span><span data-ARCKHÉ-meter-pct>0%</span></div>
          <div class="ARCKHÉ-bar"><div class="ARCKHÉ-bar__fill" data-ARCKHÉ-meter-fill></div></div>
        </div>
      </div>
      <div class="mt-8 lg:mt-0 rounded-2xl border border-{cor}-500/30 bg-dark-900/40 p-3 overflow-hidden">
        {svg_hero(n)}
      </div>
    </div>
  </header>

  <main id="conteudo" class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12" data-ARCKHÉ-track="{n}">

    <section class="mb-12">
      <h2 class="text-2xl font-bold mb-6">Mapa da trilha</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">''')
    for mid in mids:
        M = MODS[mid]; num = mid.replace('-', '.')
        out.append(f'''        <a href="#modulo-{mid}" class="group bg-dark-800 rounded-xl border border-dark-600 hover:border-{cor}-500/30 p-5 transition-all">
          <div class="flex items-center justify-between mb-2"><span class="text-{cor}-400 font-bold text-sm">{num}</span><span class="text-xs text-neutral-500">{M['tipo']} Â· ~35 min</span></div>
          <h3 class="font-semibold mb-1 group-hover:text-{cor}-400 transition-colors">{M['emoji']} {E(M['titulo'])}</h3>
          <p class="text-xs text-neutral-400">{E(M['sub'])}</p>
        </a>''')
    out.append('''      </div>
    </section>

    <h2 class="text-2xl font-bold mb-6">ConteÃºdo detalhado</h2>
''')
    for mid in mids:
        M = MODS[mid]; num = mid.replace('-', '.')
        out.append(f'''    <!-- ===== MODULO {num} ===== -->
    <div id="modulo-{mid}" data-ARCKHÉ-module="{mid}" data-ARCKHÉ-track="{n}" class="bg-dark-800 rounded-xl border border-dark-600 mb-6">
      <div class="p-6 border-b border-dark-600">
        <div class="flex items-center justify-between mb-2"><span class="text-{cor}-400 font-bold">{num}</span><span class="text-xs text-neutral-500">{M['tipo']} Â· ~35 min</span></div>
        <h3 class="text-2xl font-bold mb-2">{M['emoji']} {E(M['titulo'])}</h3>
        <p class="text-neutral-400 text-sm">{E(MOD_DESC[mid])}</p>
        <div data-ARCKHÉ-meter="modulo:{mid}" class="mt-4" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-label="Progresso do mÃ³dulo {num}">
          <div class="flex justify-between text-xs text-neutral-400 mb-1"><span data-ARCKHÉ-meter-frac>0 de 6</span><span data-ARCKHÉ-meter-pct>0%</span></div>
          <div class="ARCKHÉ-bar"><div class="ARCKHÉ-bar__fill" data-ARCKHÉ-meter-fill></div></div>
        </div>
      </div>
      <div class="divide-y divide-dark-600">''')
        assert len(T[mid]) == 6, mid
        for i, (titulo, (em, dica, oque, porque, conc)) in enumerate(zip(M['topicos'], T[mid]), 1):
            tid = f't{i}-{mid}'
            out.append(f'''        <div class="topic-item">
          <button onclick="toggleTopic(this)" aria-expanded="false" aria-controls="{tid}" class="w-full px-6 py-4 flex items-center space-x-3 hover:bg-dark-700/50 transition-colors text-left">
            <span class="w-6 h-6 rounded-full bg-{cor}-500/20 text-{cor}-400 text-sm font-bold flex items-center justify-center flex-shrink-0">{i}</span>
            <span class="text-lg">{em}</span>
            <div><span class="font-medium">{titulo}</span><span class="text-neutral-500 text-sm ml-2">- {E(dica)}</span></div>
          </button>
          <div id="{tid}" class="topic-explanation px-6 pb-4">
            <div class="bg-dark-700/50 rounded-lg p-4 space-y-3 ml-9">
              <div><span class="text-{cor}-400 font-semibold">O que Ã©:</span><p class="text-neutral-300 text-sm">{E(oque)}</p></div>
              <div><span class="text-{cor}-400 font-semibold">Por que aprender:</span><p class="text-neutral-300 text-sm">{E(porque)}</p></div>
              <div><span class="text-{cor}-400 font-semibold">Conceitos-chave:</span><p class="text-neutral-300 text-sm">{E(conc)}</p></div>
            </div>
          </div>
        </div>''')
        out.append(f'''      </div>
      <div class="p-4 bg-dark-700/30 flex justify-start space-x-3">
        <button onclick="openModal('modal-{mid}')" class="px-4 py-2 text-sm bg-dark-600 hover:bg-dark-500 rounded-lg transition-colors">Ver em Modal</button>
        <a href="modulo-{mid}.html" class="px-4 py-2 text-sm bg-{cor}-600 hover:bg-{cor}-500 text-white rounded-lg transition-colors">Ver Completo</a>
      </div>
    </div>
''')
    if n < 4:
        prox = f'<a href="../trilha{n+1}/index.html" class="flex-1 text-center px-6 py-3 bg-{cor}-600 text-white rounded-lg font-semibold hover:bg-{cor}-500 transition-colors">PrÃ³xima trilha: {NOMES[n+1][1]} â†’</a>'
    else:
        prox = f'<a href="modulo-4-4.html#topico-5" class="flex-1 text-center px-6 py-3 bg-{cor}-600 text-white rounded-lg font-semibold hover:bg-{cor}-500 transition-colors">Ir para o projeto final â†’</a>'
    out.append(f'''    <div class="flex flex-col sm:flex-row gap-4 mt-12">
      <a href="../../index.html" class="flex-1 text-center px-6 py-3 bg-dark-700 text-neutral-300 rounded-lg font-semibold hover:bg-dark-600 transition-colors">â† Voltar ao inÃ­cio</a>
      {prox}
    </div>
  </main>

  <!-- MODAIS (iframe carrega a pagina do modulo) -->''')
    for mid in mids:
        M = MODS[mid]; num = mid.replace('-', '.')
        out.append(f'''  <div id="modal-{mid}" class="modal hidden fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-black/80" role="dialog" aria-modal="true" aria-labelledby="modal-{mid}-title" onclick="if(event.target === this) closeModal()">
    <div class="bg-dark-800 rounded-xl w-full max-w-6xl h-[95vh] flex flex-col border border-dark-600">
      <div class="p-4 border-b border-dark-600 flex justify-between items-center flex-shrink-0">
        <div class="flex items-center space-x-3"><span class="text-{cor}-400 font-bold">{num}</span><span id="modal-{mid}-title" class="font-semibold">{E(M['titulo'])}</span></div>
        <button onclick="closeModal()" class="text-neutral-400 hover:text-neutral-100 text-2xl leading-none" aria-label="Fechar">&times;</button>
      </div>
      <iframe src="modulo-{mid}.html" title="MÃ³dulo {num}" loading="lazy" class="flex-1 w-full rounded-b-xl"></iframe>
    </div>
  </div>''')
    return '\n'.join(out) + '\n'

for n in range(1, 5):
    p = RAIZ / 'context' / 'corpos' / f'trilha{n}.html'
    p.write_text(trilha(n), encoding='utf-8')
    print(p, p.read_text().count('\n'), 'linhas')
