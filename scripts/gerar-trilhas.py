#!/usr/bin/env python3
"""Gera context/corpos/trilha{1..4}.html do curso ccmods-tecnico a partir da SPEC + dados abaixo."""
import re, html
from pathlib import Path

RAIZ = Path.home() / 'projetos' / 'ccmods-tecnico'
spec = (RAIZ / 'context' / 'SPEC.md').read_text(encoding='utf-8')

# --- lêÂª mapa congelado da SPEC ---
MODS = {}   # '1-1' -> dict(emoji, titulo, sub, tipo, topicos[])
atual = None
for linha in spec.split('\n'):
    m = re.match(r'- \*\*(\d)\.(\d) \[(.+?)\] (.+?)\*\* ê¢â¬â "(.+?)" êÂ· (\w+)', linha)
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
NOMES = {1: ('ê°Å¸Â§Â¬', 'Anatomia'), 2: ('ê¢Å¡Â¡', 'Eventos e estado'), 3: ('ê°Å¸âÂ¥ê¯Â¸Â', 'Telas e comandos'), 4: ('ê°Å¸âºÂ¡ê¯Â¸Â', 'Controlar e distribuir')}
NIVEL = {1: 'TêÂ©cnico', 2: 'TêÂ©cnico', 3: 'TêÂ©cnico', 4: 'AvanêÂ§ado'}

HERO_TXT = {
 1: 'Abra um mod e veja o que tem dentro: trêÂªs arquivos, uma funêÂ§êÂ£o register e hooks com trêÂªs parêÂ¢metros. Monte a pasta, carregue com --plugin-dir, instale por marketplace e termine com o seu primeiro mod funcionando, um comando que conta leituras.',
 2: 'Escolha o evento certo antes de escrever cêÂ³digo. Entenda a cadeia ligada por next, guarde estado que sobrevive ao reload e faêÂ§a trabalho fora do dispatch com relêÂ³gio, arquivos e processos ê¢â¬â sempre na forma tipada.',
 3: 'Desenhe no Claude Code: ui.render e as quatro superfêÂ­cies, a faixa acima do prompt, status e avisos, painêÂ©is com botêÂµes, comandos de barra que respondem sem modelo e ferramentas que o modelo pode chamar.',
 4: 'Mods que mudam o fluxo: interceptar, negar, perguntar ao humano e trocar o modelo de um subagente. Depois, testar com claude plugin test, depurar com --debug, percorrer as pegadinhas e distribuir por marketplace.',
}

MOD_DESC = {
 '1-1': 'O que um mod êÂ© por dentro, onde ele roda e como ele se separa do hook clêÂ¡ssico, da skill e do MCP.',
 '1-2': 'A êÂ¡rvore mêÂ­nima: .claude-plugin/plugin.json, hooks/hooks.json e o mêÂ³dulo. OpêÂ§êÂµes com userConfig e validaêÂ§êÂ£o antes de carregar.',
 '1-3': 'Do --plugin-dir com hot-reload êÂ  instalaêÂ§êÂ£o por marketplace, com escopo certo e desinstalaêÂ§êÂ£o limpa.',
 '1-4': 'O starter-mod do kit da Prompt Advisers: o comando /readcount, o contador de leituras, validate, test e claude -p.',
 '2-1': 'Os eventos agrupados por noun, a volta completa de um turno, matchers, streams e os hooks clêÂ¡ssicos dentro do mod.',
 '2-2': 'A cadeia de plugins: observar, reescrever com next, responder sem next, .catch e o orêÂ§amento de cada dispatch.',
 '2-3': 'Por que a variêÂ¡vel de mêÂ³dulo some, como declarar o contrato de estado e quando usar $.state ou $.store.',
 '2-4': 'session.start, relêÂ³gio do engine, arquivos, processos locais, acordar a sessêÂ£o e decidir se o mod gasta modelo.',
 '3-1': 'O que o hook de ui.render recebe, a tabela de elementos de cada superfêÂ­cie e as regras de uma êÂ¡rvore que valida.',
 '3-2': 'A faixa AbovePrompt compartilhada, status, toast e log, com o exemplo oficial band.tsx dissecado.',
 '3-3': 'PainêÂ©is abertos por comando, dimensionados pelo bodyColumns, com botêÂµes, hotkeys, campos e modo diêÂ¡logo.',
 '3-4': 'Comandos de barra que respondem sem modelo, ferramentas para o modelo, opêÂ§êÂµes do /config e nomes sem colisêÂ£o.',
 '4-1': 'Interceptar tool.call, negar com motivo, perguntar com $.ui.ask, trocar modelo de subagente e respeitar permissêÂµes.',
 '4-2': 'O engine de verdade sem modelo: mocks antes do $, comandos de ponta a ponta, relêÂ³gio controlado e telas montadas.',
 '4-3': 'O log do --debug, mêÂ³dulos que nêÂ£o carregam, êÂ¡rvores recusadas, as 23 pegadinhas e o teste de fumaêÂ§a.',
 '4-4': 'marketplace.json, repositêÂ³rio, versêÂµes, revisêÂ£o antes de compartilhar, o projeto final e os prêÂ³ximos passos.',
}

# (emoji, dica curta, o que êÂ©, por que aprender, conceitos-chave) ê¢â¬â na ordem dos têÂ³picos da SPEC
T = {
'1-1': [
 ('ê°Å¸âÅ', 'register roda, hooks entram na cadeia', 'Quando o Claude Code carrega um mod, ele importa o mêÂ³dulo, chama register(on, options) e passa a chamar os hooks registrados a cada evento.', 'Entender esse momento explica por que um mod pode mudar o que o Claude vêÂª, desenha e faz sem tocar no cêÂ³digo do Claude Code.', 'mod, plugin, function hook, register, carregamento.'),
 ('ê°Å¸Â§Â©', 'quatro formas de estender', 'Mod roda dentro do processo, em um ambiente prêÂ³prio; hook clêÂ¡ssico êÂ© um comando de shell do settings.json; skill êÂ© instruêÂ§êÂ£o para o modelo; MCP êÂ© um servidor de ferramentas.', 'Escolher a forma errada custa caro: muita coisa que parece mod se resolve com uma skill, e vice-versa.', 'mod, hook clêÂ¡ssico, skill, MCP, settings.json.'),
 ('ê¢ÅÂê¯Â¸Â', 'on adiciona, options lêÂª a config', 'A funêÂ§êÂ£o exportada recebe on, para registrar hooks, e options, com os valores dos campos que o manifesto declara em userConfig.', 'êâ° a êÂºnica porta de entrada do mod: tudo o que ele faz comeêÂ§a nessa funêÂ§êÂ£o.', 'register, on(evento, matcher?, hook), options, userConfig.'),
 ('ê°Å¸Å½âºê¯Â¸Â', '$, e e next', 'Todo hook tem a forma ($, e, next): $ êÂ© a interface do engine, e êÂ© a entrada do evento e next(e) passa adiante na cadeia.', 'Esses trêÂªs nomes aparecem em todo exemplo do curso; dominêÂ¡-los êÂ© ler qualquer mod.', '$, e, next, cadeia, resultado do evento.'),
 ('ê°Å¸âÂ¦', 'sem DOM, sem Node', 'O mêÂ³dulo êÂ© um ES module que roda num ambiente prêÂ³prio, sem DOM e sem Node; tudo fora dele êÂ© alcanêÂ§ado pelo $.', 'Evita o erro mais comum de quem chega: importar fs do Node ou usar import() dinêÂ¢mico, que nêÂ£o carregam.', 'ES module, ambiente isolado, $ como êÂºnica saêÂ­da, import estêÂ¡tico.'),
 ('ê°Å¸âÂºê¯Â¸Â', 'quatro trilhas, dois kits', 'O caminho do curso, do primeiro mod ao marketplace, e os dois kits usados: o Claude Mods Starter Kit (Prompt Advisers, MIT) e o ARCKHê-mods.', 'VocêÂª sabe de onde vem cada exemplo e em que versêÂ£o foi conferido: Claude Code 2.1.289.', 'starter kit, ARCKHê-mods, versêÂ£o 2.1.289, acesso antecipado.'),
],
'1-2': [
 ('ê°Å¸ÅÂ³', 'trêÂªs arquivos', 'A pasta do mod com .claude-plugin/plugin.json, hooks/hooks.json e o mêÂ³dulo de hooks, mais tests/ quando houver teste.', 'Com a êÂ¡rvore certa o Claude Code acha o mod; com um nome trocado, nada carrega e nada avisa alto.', 'pasta do plugin, .claude-plugin, hooks/, tests/.'),
 ('ê°Å¸ÂªÂª', 'nome, versêÂ£o, descriêÂ§êÂ£o', 'O manifesto do plugin: name, version, description e, quando houver, userConfig e types.', 'O name vira o prefixo de comandos, ferramentas e estado; mudar depois quebra quem jêÂ¡ usa.', 'plugin.json, name, version, manifesto.'),
 ('ê°Å¸Â§Â­', 'modules: um caminho', 'O hooks.json lista em modules o caminho do mêÂ³dulo, relativo ao prêÂ³prio hooks.json, como {"modules":["./starter.mjs"]}.', 'êâ° o elo entre o manifesto e o cêÂ³digo; o validate mostra se ele aponta para o lugar certo.', 'hooks.json, modules, caminho relativo.'),
 ('ê°Å¸ââ', '.mjs, .ts ou .tsx', 'O mêÂ³dulo pode ser .ts, .tsx, .jsx, .js, .mjs, .cjs, .mts ou .cts, e êÂ© sempre ES module; outro sufixo nêÂ£o carrega.', 'O kit comeêÂ§a em .mjs sem compilaêÂ§êÂ£o; a partir da trilha 2 o curso usa .tsx tipado.', 'extensêÂ£o, ES module, TypeScript, JSX com h.'),
 ('ê¢Å¡â¢ê¯Â¸Â', 'opêÂ§êÂµes no /config', 'Campos declarados em userConfig no plugin.json viram linhas do menu de configuraêÂ§êÂ£o e chegam ao mod em options.', 'Deixa o usuêÂ¡rio ajustar o mod sem editar cêÂ³digo, e cada mudanêÂ§a recarrega o mêÂ³dulo.', 'userConfig, options, pluginConfigs, /config.'),
 ('ê¢Åâ¦', 'claude plugin validate', 'O comando lêÂª o manifesto e o cêÂ³digo do mêÂ³dulo como o engine leria e lista os hooks, as chamadas e o que seria recusado.', 'Pega o erro antes de abrir uma sessêÂ£o: êÂ© o primeiro passo de todo ciclo de mudanêÂ§a.', 'claude plugin validate, hooks listados, calls, Validation passed.'),
],
'1-3': [
 ('ê°Å¸ââ', 'sêÂ³ nesta sessêÂ£o', 'A flag carrega o mod de uma pasta do disco sêÂ³ para aquela sessêÂ£o; repita a flag para carregar vêÂ¡rios.', 'êâ° o jeito de desenvolver: nada fica instalado, e fechar a sessêÂ£o desfaz tudo.', '--plugin-dir, sessêÂ£o, pasta local.'),
 ('ê¢â¢Â»ê¯Â¸Â', 'salvou, recarregou', 'Numa sessêÂ£o interativa a pasta êÂ© vigiada: salvar um arquivo roda o register de novo num ambiente novo, e os timers antigos caem.', 'VocêÂª ajusta e vêÂª na hora, sem reiniciar o Claude Code.', 'hot-reload, pasta vigiada, ambiente novo, timers.'),
 ('ê°Å¸âÂ¥ê¯Â¸Â', 'quando nêÂ£o dêÂ¡ para passar flag', 'A variêÂ¡vel de ambiente nomeia as mesmas pastas, com caminho absoluto, para sessêÂµes abertas pelo app desktop ou por um SDK.', 'No desktop nêÂ£o existe linha de comando para pêÂ´r a flag; a variêÂ¡vel resolve.', 'CLAUDE_CODE_PLUGIN_DIRS, desktop, SDK, settings env.'),
 ('ê°Å¸ÂÂª', 'marketplace add + install', 'Registrar uma pasta ou repositêÂ³rio como marketplace e instalar o plugin dele com claude plugin install.', 'êâ° como o mod chega êÂ s sessêÂµes de todo dia sem flag nenhuma.', 'marketplace, claude plugin marketplace add, claude plugin install.'),
 ('ê°Å¸Å½Å¡ê¯Â¸Â', 'user, project, local', 'O escopo diz onde a instalaêÂ§êÂ£o vale: para vocêÂª em todo projeto, para o projeto inteiro ou sêÂ³ na sua cêÂ³pia local.', 'Instalar no escopo errado espalha o mod onde nêÂ£o devia ou esconde de quem precisa.', '--scope user, project, local.'),
 ('ê°Å¸Â§Â¹', 'disable e uninstall', 'Desligar com claude plugin disable e remover a instalaêÂ§êÂ£o sem deixar marketplace ou config esquecidos.', 'Mod que nêÂ£o sai direito vira suspeito de todo comportamento estranho depois.', 'claude plugin disable, remover a instalaêÂ§êÂ£o, claude plugin list.'),
],
'1-4': [
 ('ê°Å¸ââ¹', 'templates/starter-mod', 'Copiar o modelo do kit da Prompt Advisers, que jêÂ¡ traz manifesto, hooks.json, starter.mjs e um teste.', 'ComeêÂ§ar de um mod que passa no validate e no test tira o atrito do primeiro dia.', 'starter-mod, cêÂ³pia, read-counter-example.'),
 ('ê°Å¸âÅ½', 'session.start, tool.call, command.run', 'O starter.mjs registra o comando em session.start, conta leituras bem-sucedidas em tool.call com matcher Read e responde em command.run.', 'SêÂ£o trêÂªs dos eventos mais usados, num arquivo curto que vocêÂª lêÂª inteiro.', 'session.start, tool.call, matcher, command.run, $.command.register.'),
 ('ê°Å¸Â§Âª', 'validate e test', 'Rodar claude plugin validate e claude plugin test na pasta copiada e ler as duas saêÂ­das.', 'VocêÂª confirma que a cêÂ³pia estêÂ¡ êÂ­ntegra antes de mudar uma linha.', 'Validation passed, 1 pass, 0 fail.'),
 ('ê¢Å¡Â¡', 'claude -p sem modelo', 'Chamar /readcount com claude -p e --plugin-dir: o prêÂ³prio mod responde, sem turno do modelo.', 'êâ° o teste de fumaêÂ§a mais barato que existe e vale para qualquer comando de mod.', 'claude -p, comando de barra, resposta sem modelo.'),
 ('ê°Å¸âÂ§', 'outra ferramenta no matcher', 'Trocar o matcher do tool.call para contar outra ferramenta, como Edit ou Write, e rodar o teste de novo.', 'êâ° a primeira mudanêÂ§a real: vocêÂª vêÂª o teste quebrar e sabe consertar.', 'matcher, tool, teste que falha, ajuste.'),
 ('ê°Å¸ÂÂ·ê¯Â¸Â', 'nome, comando, estado', 'Trocar o name do manifesto, o nome do comando e as mensagens para o mod virar seu.', 'Nome repetido colide com outros mods; seu nome êÂ© o prefixo de tudo o que o mod registra.', 'name, prefixo, colisêÂ£o, README.'),
],
'2-1': [
 ('ê°Å¸ââê¯Â¸Â', 'tool, ui, session, turn...', 'Cada evento êÂ© noun.aêÂ§êÂ£o; agrupar por noun mostra o que o mod pode tocar: ferramentas, tela, sessêÂ£o, turno, prompt, estado.', 'Ver o mapa inteiro evita escrever em ui.render o que deveria ser um tool.call.', 'evento, noun, tool, ui, session, turn, prompt.'),
 ('ê°Å¸âÂ', 'prompt.submit a turn.complete', 'A ordem em que os eventos disparam: prompt.submit, turn.start, turn.step, tool.call, session.append e turn.complete.', 'Saber onde vocêÂª estêÂ¡ na volta diz o que jêÂ¡ aconteceu e o que ainda dêÂ¡ para mudar.', 'turno, prompt.submit, turn.start, turn.step, turn.complete.'),
 ('ê°Å¸Å½Â¯', 'o segundo argumento do on', 'O matcher filtra quais eventos chegam ao hook, como { tool: \'Read\' } ou { command: \'readcount\' }.', 'Hook sem matcher roda em tudo e gasta orêÂ§amento êÂ  toa.', 'matcher, filtro, on(evento, matcher, hook).'),
 ('ê°Å¸ÅÅ ', 'turn.step e process.spawn', 'Dois eventos sêÂ£o stream: o hook êÂ© um async generator, e yield* next(e) repassa os pedaêÂ§os.', 'Hook comum nesses eventos nêÂ£o carrega; o erro sêÂ³ aparece no --debug.', 'stream, async function*, yield* next(e), for await.'),
 ('ê°Å¸ÂªÂ', 'classic.PreToolUse e cia.', 'Os hooks clêÂ¡ssicos do settings.json aparecem para o mod como classic.<Nome>, com a mesma entrada que o hook receberia.', 'VocêÂª aproveita o que jêÂ¡ conhece de hooks clêÂ¡ssicos sem sair do mod.', 'classic.PreToolUse, classic.Stop, hook clêÂ¡ssico.'),
 ('ê°Å¸ââ', 'index.d.ts manda', 'Procurar qualquer evento, entrada e resultado no arquivo de tipos da sua instalaêÂ§êÂ£o, .claude-plugin/types/claude-code/index.d.ts.', 'A API estêÂ¡ em acesso antecipado e muda: o arquivo da sua versêÂ£o êÂ© a autoridade, nêÂ£o a memêÂ³ria.', 'declaraêÂ§êÂ£o de tipos, index.d.ts, grep, versêÂ£o.'),
],
'2-2': [
 ('ê¢âºâê¯Â¸Â', 'todos os plugins + o engine', 'Os hooks de todos os plugins e o comportamento do prêÂ³prio Claude Code formam uma cadeia ligada por next.', 'Seu mod nêÂ£o estêÂ¡ sozinho: o que vocêÂª devolve êÂ© o que os outros e o engine recebem.', 'cadeia, ordem, engine, plugins vizinhos.'),
 ('ê°Å¸ââ¬', 'return next(e)', 'O hook mais simples olha o evento, registra algo e devolve next(e) sem mudar nada.', 'êâ° o padrêÂ£o seguro: medir sem interferir.', 'observar, next(e), efeito colateral.'),
 ('ê¢ÅÂê¯Â¸Â', 'next({ ...e, ... })', 'Chamar next com um evento alterado muda o que o resto da cadeia vêÂª, dentro do que aquele evento permite.', 'êâ° como um mod corrige um caminho, acrescenta contexto ou troca um modelo.', 'reescrever, spread, campos permitidos.'),
 ('ê°Å¸âºâ', 'quem nêÂ£o chama next decide', 'Um hook que retorna sem chamar next responde pelo evento, e a cadeia abaixo dele nêÂ£o roda.', 'êâ° o poder de negar uma ferramenta ou responder um comando, e tambêÂ©m o maior risco do mod.', 'responder, deny, curto-circuito.'),
 ('ê°Å¸Âªâ', 'o registro tem .catch', 'O .catch encadeado no on responde no lugar do hook que falhou; sem ele, o hook êÂ© pulado e a cadeia segue.', 'Falha silenciosa num mod de seguranêÂ§a deixa passar o que devia barrar.', '.catch, hook pulado, padrêÂ£o seguro.'),
 ('ê¢ÂÂ³', 'tempo do dispatch', 'Cada hook tem orêÂ§amento de tempo dentro do dispatch, e next.signal aborta quando o dispatch êÂ© abandonado.', 'Trabalho longo dentro do hook êÂ© cortado; o que precisa durar vai para fora.', 'dispatch, orêÂ§amento, next.signal, abort.'),
],
'2-3': [
 ('ê°Å¸âÂ¨', 'reload limpa o mêÂ³dulo', 'Cada hot-reload roda o register num ambiente novo; a variêÂ¡vel de mêÂ³dulo volta ao valor inicial.', 'O contador que zera do nada êÂ© o sintoma nêÂºmero um de estado no lugar errado.', 'variêÂ¡vel de mêÂ³dulo, hot-reload, ambiente novo.'),
 ('ê°Å¸âÅ', 'PluginState no contrato', 'Declarar o formato do estado do plugin em types/index.d.ts e apontar o arquivo em "types" no plugin.json.', 'Com o contrato, o editor e o tsc conferem cada leitura e escrita de estado.', 'types/index.d.ts, PluginState, "types", contrato.'),
 ('ê¢Å¡âºê¯Â¸Â', 'a biblioteca de estado', 'atom, read e update vêÂªm de import { ... } from "claude-code" e leem e gravam $.state com controle de versêÂ£o.', 'update nêÂ£o perde clique: dois toques antes do redesenho contam os dois.', 'atom, read, update, $.state.get, $.state.set, ifVersion.'),
 ('ê°Å¸ââê¯Â¸Â', 'para alêÂ©m da sessêÂ£o', 'O $.store guarda valores entre sessêÂµes com get, set, delete e keys.', '$.state vale para a sessêÂ£o; o que precisa voltar amanhêÂ£ vai para o store.', '$.store.get, $.store.set, persistêÂªncia.'),
 ('ê°Å¸â¢Â°ê¯Â¸Â', '$.clock, nêÂ£o Date', 'O engine dêÂ¡ o relêÂ³gio do mod: now para a hora e timers que o teste pode controlar.', 'Usar o relêÂ³gio do engine deixa o mod testêÂ¡vel sem esperar tempo real.', '$.clock.now, relêÂ³gio controlado, teste.'),
 ('ê°Å¸Â§Â­', 'mêÂ³dulo, state ou store', 'A regra de decisêÂ£o: constante no mêÂ³dulo, estado da sessêÂ£o em $.state, o que sobrevive entre sessêÂµes em $.store.', 'Cada dado no lugar certo evita perda no reload e lixo acumulado no disco.', 'decisêÂ£o, escopo do dado, sessêÂ£o, persistêÂªncia.'),
],
'2-4': [
 ('ê°Å¸Åâ¦', 'pronto antes do 1êÂº prompt', 'O session.start dispara uma vez, quando a sessêÂ£o fica pronta, e êÂ© aguardado antes do primeiro prompt.', 'êâ° o lugar de registrar comandos e ferramentas e de acender o que roda em segundo plano.', 'session.start, inicializaêÂ§êÂ£o, $.command.register, $.tool.register.'),
 ('ê¢ÂÂ²ê¯Â¸Â', 'timers do engine', 'clock.every repete e clock.after agenda uma vez; os timers duram atêÂ© serem cancelados ou o mêÂ³dulo recarregar.', 'Trabalho periêÂ³dico fora do dispatch nêÂ£o tem orêÂ§amento cortando no meio.', '$.clock.every, $.clock.after, cancelamento, reload.'),
 ('ê°Å¸âÂ', 'ler, escrever, listar', 'O $.fs lêÂª texto ou bytes, escreve, lista e dêÂ¡ stat de caminhos, com realPath para guardas robustas.', 'Sem Node, o $.fs êÂ© a êÂºnica forma de o mod tocar arquivos.', '$.fs.read, $.fs.write, $.fs.stat, realPath.'),
 ('ê°Å¸âºÂ ê¯Â¸Â', 'comando por argv', 'O $.process.run roda um comando do sistema por argv, e $.process.spawn entrega a saêÂ­da em pedaêÂ§os.', 'git status, contagem de linhas, scripts locais: tudo por argv, sem shell montado em string.', '$.process.run, $.process.spawn, argv.'),
 ('ê°Å¸ââ', 'trabalho que vira turno', 'O $.prompt.submit pêÂµe um prompt na fila que comeêÂ§a um turno quando a sessêÂ£o fica ociosa.', 'Deixa um mod de segundo plano chamar o modelo na hora certa, sem atropelar o turno em curso.', '$.prompt.submit, fila, sessêÂ£o ociosa.'),
 ('ê°Å¸âÂ¸', 'model.complete custa', 'O $.model.complete e o $.model.fork chamam o modelo pelo cliente da sessêÂ£o e consomem uso.', 'Mod que gasta modelo escondido surpreende quem usa; a regra êÂ© avisar e deixar desligar.', '$.model.complete, $.model.fork, uso, consentimento.'),
],
'3-1': [
 ('ê°Å¸Å½Â¨', 'component, surface, props', 'O hook de ui.render recebe uma instêÂ¢ncia de componente: e.component, e.surface, e.requestId, e.props e e.viewport.', 'Com esses campos vocêÂª decide se desenha, onde desenha e do tamanho certo.', 'ui.render, component, surface, requestId, viewport.'),
 ('ê°Å¸Â§Â±', 'elementos por superfêÂ­cie', 'O $.ui.resolve(e) devolve a tabela de construtores da superfêÂ­cie, que vocêÂª desestrutura nas tags JSX.', 'O mêÂ³dulo nêÂ£o tem elementos globais; sem resolve nêÂ£o hêÂ¡ Box nem Text.', '$.ui.resolve, Box, Text, JSX com h.'),
 ('ê°Å¸âÂ±', 'terminal, desktop, mobile, vscode', 'Cada superfêÂ­cie tem sua tabela: o terminal nêÂ£o tem Svg, mas tem Raster e Image; o mobile nêÂ£o tem Input nem Select.', 'Uma êÂ¡rvore com elemento que a superfêÂ­cie nêÂ£o tem nêÂ£o êÂ© desenhada.', 'superfêÂ­cie, Elements, diferenêÂ§as, narrowing por e.surface.'),
 ('ê°Å¸âÂ', 'render sêÂ³ lêÂª', 'O hook de render lêÂª o estado com $.state.get e nunca escreve; quem escreve êÂ© um handler ou outro evento.', 'Escrever ao desenhar êÂ© negado; ler assina a instêÂ¢ncia e o redesenho vem sozinho.', 'render puro, $.state.get, handler, redesenho.'),
 ('ê°Å¸Å¡Â«', 'o engine desenha o dele', 'Uma êÂ¡rvore que nêÂ£o valida nêÂ£o êÂ© desenhada: o engine desenha a prêÂ³pria e registra o motivo no log.', 'Saber ler essa linha poupa horas de "por que nêÂ£o aparece nada".', 'validaêÂ§êÂ£o, ui.render refused, debug log.'),
 ('ê°Å¸âÂ¼ê¯Â¸Â', 'pixels no terminal', 'Raster desenha uma grade de cêÂ©lulas coloridas; Image mostra uma figura pelo protocolo grêÂ¡fico do terminal, com alt nos outros.', 'GrêÂ¡ficos e mapas de calor sem um Box por cêÂ©lula.', 'Raster, Image, $.ui.blit, alt.'),
],
'3-2': [
 ('ê°Å¸âÅ¸', 'AbovePrompt', 'O componente AbovePrompt êÂ© a faixa acima da caixa de prompt; o hook desenha nela com o tamanho de bodyColumns.', 'êâ° o lugar de informaêÂ§êÂ£o contêÂ­nua: contadores, avisos, estado do mod.', 'AbovePrompt, faixa, bodyColumns.'),
 ('ê°Å¸Â¤Â', 'uma faixa para todos', 'A faixa êÂ© uma sêÂ³ e compartilhada: o exemplo oficial band.tsx mostra como desenhar nela sem apagar os vizinhos.', 'Um mod que toma a faixa inteira apaga os vizinhos.', 'compartilhar, next, composiêÂ§êÂ£o.'),
 ('ê°Å¸ââ ', 'status sem abrir nada', 'O $.ui.status mostra um estado curto sem abrir painel e sem comeêÂ§ar turno.', 'InformaêÂ§êÂ£o discreta nêÂ£o precisa de tela prêÂ³pria.', '$.ui.status, linha de status, sem turno.'),
 ('ê°Å¸âÂ£', 'toast e log', 'O $.ui.toast dêÂ¡ um aviso passageiro e o $.ui.log escreve uma linha no registro, sem chamar o modelo.', 'Avisos certos no lugar certo, sem poluir a conversa.', '$.ui.toast, $.ui.log, aviso, registro.'),
 ('ê°Å¸âÂ¬', 'band.tsx linha a linha', 'Ler o exemplo oficial da faixa que vem com o Claude Code: estado tipado, resolve, êÂ¡rvore e botêÂ£o.', 'êâ° o modelo mais curto e correto de faixa que existe para copiar.', 'examples/band.tsx, band-state.d.ts, referêÂªncia oficial.'),
 ('ê°Å¸Â§Âª', 'mount nas duas superfêÂ­cies', 'Montar a faixa num teste para terminal e desktop, com o mesmo corpo num laêÂ§o.', 'Prova que o mod nêÂ£o depende de uma superfêÂ­cie sêÂ³.', 'claude plugin test, mount, terminal, desktop.'),
],
'3-3': [
 ('ê°Å¸ÂªÅ¸', 'Pane', 'O $.ui.open abre um painel, o componente Pane, que o hook de ui.render desenha.', 'Painel êÂ© a tela prêÂ³pria do mod: listas, detalhes, formulêÂ¡rios.', '$.ui.open, Pane, requestId.'),
 ('ê°Å¸âÂ', 'largura que muda', 'O painel desenha no bodyColumns, mais estreito que a tela quando fica ao lado da conversa.', 'êÂrvore dimensionada pelo viewport quebra quando o painel estêÂ¡ encaixado.', 'bodyColumns, viewport, isFullscreen.'),
 ('ê°Å¸âË', 'Button e hotkey', 'BotêÂµes com label, variant e hotkey de uma letra ou dêÂ­gito, que funcionam quando o painel tem o teclado.', 'Atalho de uma tecla torna o painel usêÂ¡vel sem mouse.', 'Button, hotkey, variant, foco.'),
 ('ê°Å¸âÂ±ê¯Â¸Â', 'ui.press, ui.input, ui.select', 'Os handlers ficam no plugin e disparam os eventos ui.press, ui.input e ui.select com a chave do elemento.', 'êâ° assim que um clique vira aêÂ§êÂ£o e um texto digitado vira dado.', 'ui.press, ui.input, ui.select, key.'),
 ('ê°Å¸âÂ¬', 'focus, closeOnEscape, holdToasts', 'Abrir o painel com focus, closeOnEscape e holdToasts faz ele se comportar como diêÂ¡logo.', 'DiêÂ¡logo prende a atenêÂ§êÂ£o do usuêÂ¡rio; deixar holdToasts num painel fixo trava os avisos.', 'diêÂ¡logo, focus, closeOnEscape, holdToasts.'),
 ('ê°Å¸Å¡Âª', 'fechar e liberar', 'Fechar o painel por botêÂ£o de dispensa ou por Esc e limpar o estado ligado a ele.', 'Painel que nêÂ£o fecha ou estado que sobra confunde a prêÂ³xima abertura.', 'role dismiss, Esc, limpeza de estado.'),
],
'3-4': [
 ('ê¢ÅÂ¨ê¯Â¸Â', '$.command.register', 'Registrar um comando de barra com nome e descriêÂ§êÂ£o, normalmente no session.start.', 'Comando de mod roda na hora e nêÂ£o precisa de modelo.', '$.command.register, session.start, /comando.'),
 ('ê¢â Â©ê¯Â¸Â', 'command.run com matcher', 'Responder o evento command.run, filtrado pelo nome do comando, com { text } e, se quiser, context.', 'text êÂ© a linha que aparece e o modelo tambêÂ©m lêÂª; context sêÂ³ o modelo lêÂª.', 'command.run, { text }, context.'),
 ('ê°Å¸âÂ¨ê¯Â¸Â', 'CommandOutput', 'Desenhar a saêÂ­da do comando como êÂ¡rvore na conversa hookando o componente CommandOutput.', 'A resposta vira tabela ou card em vez de texto cru.', 'CommandOutput, ui.render, matcher por props.'),
 ('ê°Å¸Â§Â°', '$.tool.register', 'Declarar uma ferramenta com nome, descriêÂ§êÂ£o e schema, servida por um hook de tool.call; ela aparece como mcp__<plugin>__<nome>.', 'O modelo passa a usar uma capacidade que sêÂ³ o seu mod oferece.', '$.tool.register, tool.call, schema, mcp__plugin__nome.'),
 ('ê°Å¸âÂ§', 'options na prêÂ¡tica', 'Ler os valores que o usuêÂ¡rio ajustou no /config pelo options do register, com padrêÂµes do manifesto.', 'Mudar uma opêÂ§êÂ£o recarrega o mêÂ³dulo; o mod nunca lêÂª config velha.', 'userConfig, options, picker, /config.'),
 ('ê°Å¸ÂÂ·ê¯Â¸Â', 'prefixe tudo', 'Escolher nomes de comandos, ferramentas e chaves de estado que nêÂ£o batam com os de outros mods.', 'Dois mods com o mesmo comando brigam, e o usuêÂ¡rio nêÂ£o sabe qual respondeu.', 'colisêÂ£o, prefixo, nome do plugin.'),
],
'4-1': [
 ('ê°Å¸âºâ', 'tool.call antes de rodar', 'Hookar tool.call com matcher na ferramenta e olhar a entrada antes de a chamada acontecer.', 'êâ° o ponto em que um mod pode impedir um estrago, nêÂ£o apenas registrêÂ¡-lo.', 'tool.call, matcher, entrada da ferramenta.'),
 ('ê°Å¸Å¡Â«', 'deny com mensagem', 'Responder sem next com um motivo que o modelo lêÂª e entende como recusa.', 'Recusa sem motivo faz o modelo tentar de novo do mesmo jeito.', 'deny, motivo, resposta sem next.'),
 ('ê°Å¸â¢â¹', '$.ui.ask', 'Perguntar ao humano com opêÂ§êÂµes antes de seguir, com a opêÂ§êÂ£o segura primeiro e um .catch para quando nêÂ£o hêÂ¡ tela.', 'Sem tela (claude -p) ou sem resposta, o mod precisa de um padrêÂ£o seguro e explêÂ­cito.', '$.ui.ask, opêÂ§êÂ£o segura, .catch, afk.'),
 ('ê°Å¸ââ¬', 'agent.spawn', 'Hookar agent.spawn para escolher o modelo de um subagente antes de ele rodar, como faz o roteador-subagente.', 'Tarefas simples em modelo menor economizam uso sem mudar o fluxo.', 'agent.spawn, subagente, modelo, roteador-subagente.'),
 ('ê°Å¸âÂ', 'nêÂ£o passar por cima', 'Um mod nêÂ£o deve afrouxar o que o usuêÂ¡rio configurou: negar êÂ© ok, liberar o que estava bloqueado nêÂ£o.', 'Mod que fura permissêÂ£o vira risco de seguranêÂ§a para quem instala.', 'permissêÂµes, classic.PreToolUse, menor privilêÂ©gio.'),
 ('ê°Å¸Â§Â¯', 'freio-de-mao', 'Ler a guarda do ARCKHê-mods que mede o estrago de um comando destrutivo e pergunta antes: prosseguir, lixeira, backup ou cancelar.', 'êâ° um mod de controle real, curto, com teste e caminho para sessêÂ£o sem tela.', 'freio-de-mao, $.process.run, $.ui.ask, $.ui.toast.'),
],
'4-2': [
 ('ê°Å¸Â§Âª', 'o engine sem modelo', 'O claude plugin test roda os *.test.ts com o engine de verdade; os hooks do teste ficam abaixo do plugin e fazem o papel do engine.', 'Testa o mod como ele roda numa sessêÂ£o, sem gastar modelo.', 'claude plugin test, claude-code/testing, test, expect, mock.'),
 ('ê°Å¸Â§Â©', 'o mundo antes do $', 'Responder no teste cada noun que o mod usa (session.start, fs, store, ui...) antes de chamar o cêÂ³digo.', 'Nada responde por baixo do plugin: faltou mock, o teste diz exatamente qual.', 'mocks, mundo.ts, noun faltando.'),
 ('ê°Å¸âÂ', 'comando de ponta a ponta', 'Disparar o comando no teste e conferir o texto devolvido e o estado gravado.', 'êâ° a prova de que o caminho todo funciona, nêÂ£o sêÂ³ uma funêÂ§êÂ£o.', 'command.run, asserêÂ§êÂ£o, estado.'),
 ('ê¢ÂÂ©', 'mock.clock', 'AvanêÂ§ar o relêÂ³gio do teste para disparar timers sem esperar tempo real.', 'Mod com clock.every testado em milissegundos, sempre igual.', 'mock.clock, timers, determinismo.'),
 ('ê°Å¸âÂ¥ê¯Â¸Â', 'mount em terminal e desktop', 'Montar o componente pelo ui do teste numa superfêÂ­cie nomeada e agir por chave com press, input e find.', 'O mesmo corpo de teste em duas superfêÂ­cies prova que o mod nêÂ£o depende de uma.', 'mount, press, input, find, superfêÂ­cie.'),
 ('ê°Å¸Â©Â»', 'pass, fail e a mensagem', 'Ler a saêÂ­da do teste: quantos pass, quantos fail e a linha que diz o que faltou.', 'Uma falha bem lida aponta a correêÂ§êÂ£o em uma linha.', 'pass, fail, mensagem de erro, timeout de 5 s.'),
],
'4-3': [
 ('ê°Å¸âÂ¦', 'claude --debug', 'Rodar com --debug para ter no log uma linha para cada hook pulado e cada resultado recusado.', 'Mod que parece nêÂ£o fazer nada quase sempre jêÂ¡ disse por quêÂª no log.', 'claude --debug, debug log.'),
 ('ê°Å¸âÆ', 'plugin, evento, motivo', 'A linha do hook pulado traz o plugin, o evento e o nome do erro; o texto da primeira, encurtado, aparece na transcriêÂ§êÂ£o.', 'Ler essa linha êÂ© metade da depuraêÂ§êÂ£o.', 'hook pulado, motivo, transcriêÂ§êÂ£o.'),
 ('ê°Å¸Â§Â±', 'import() e sufixo', 'MêÂ³dulo com import() dinêÂ¢mico, arquivo com sufixo fora da lista ou caminho errado no hooks.json nêÂ£o carregam.', 'SêÂ£o as causas mais comuns de "o mod sumiu".', 'import(), sufixo, hooks.json, validate.'),
 ('ê°Å¸ÂªÅ¸', 'elemento que nêÂ£o existe', 'Achar no log a linha da êÂ¡rvore que nêÂ£o valida e trocar o elemento ou a prop que a superfêÂ­cie nêÂ£o aceita.', 'Sem isso o engine continua desenhando o dele e vocêÂª nêÂ£o vêÂª o seu.', 'ui.render refused, elemento, prop.'),
 ('ê°Å¸ââ¹', '23 pegadinhas', 'A lista do docs/COMO-FAZER-UM-MOD.md do ARCKHê-mods: funêÂ§êÂµes com $ no topo, mocks, opêÂ§êÂ£o segura primeiro e as outras.', 'Cada pegadinha foi um erro real; ler antes poupa o mesmo erro.', 'COMO-FAZER-UM-MOD.md, pegadinhas, checar-mod.sh.'),
 ('ê°Å¸âÂ¨', 'o comando responde?', 'Rodar o comando do mod com claude -p e --plugin-dir e conferir a resposta sem abrir sessêÂ£o interativa.', 'FumaêÂ§a rêÂ¡pida antes de qualquer commit.', 'claude -p, --plugin-dir, teste de fumaêÂ§a.'),
],
'4-4': [
 ('ê°Å¸ââ¡', 'a vitrine dos plugins', 'O .claude-plugin/marketplace.json lista os plugins com name e source, como no kit: ./plugins/<nome>.', 'êâ° o que permite instalar o seu mod com um comando.', 'marketplace.json, plugins, source.'),
 ('ê°Å¸ÅÂ', 'dono/repo', 'PêÂ´r o mod num repositêÂ³rio pêÂºblico e adicionêÂ¡-lo como marketplace pelo caminho dono/repo.', 'Quem usa instala direto do repositêÂ³rio e recebe atualizaêÂ§êÂµes.', 'repositêÂ³rio, claude plugin marketplace add, dono/repo.'),
 ('ê°Å¸âÂ¼', 'version e update', 'Subir a version a cada mudanêÂ§a e saber que quem instalou recebe por claude plugin update e /reload-plugins.', 'Mudar nome de comando ou formato de estado sem aviso quebra quem jêÂ¡ usa.', 'version, claude plugin update, /reload-plugins, compatibilidade.'),
 ('ê°Å¸âÂ', 'checklist final', 'validate, test com 0 fail, README, botêÂ£o ou comando de desligar e nada que gaste modelo sem avisar.', 'Mod compartilhado roda na mêÂ¡quina de outra pessoa: o cuidado êÂ© seu.', 'revisêÂ£o, README, desligar, consentimento.'),
 ('ê°Å¸ÂÂ', 'o mod do Rafa', 'Comando /x, faixa ou painel, estado em $.state, teste com mocks, validate OK e comando de desligar.', 'Junta tudo o que o curso ensinou num mod que vocêÂª mesmo usa.', 'projeto final, claude plugin test, claude -p.'),
 ('ê°Å¸Â§Â­', 'cchooks, MakeClaudeX e mais', 'Os cursos de hooks clêÂ¡ssicos, de plugins de produêÂ§êÂ£o e o curso-agent-runtime, alêÂ©m dos dois kits.', 'O curso termina; os mods continuam mudando a cada versêÂ£o.', 'cchooks, MakeClaudeX, curso-agent-runtime, kits.'),
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
        label = 'Uma pasta de mod aberta: plugin.json aponta para hooks.json, que aponta para o mêÂ³dulo. Do mêÂ³dulo sai a funêÂ§êÂ£o register(on, options), e dela trêÂªs hooks com a forma ($, e, next).'
        corpo = f'''<g font-family="Inter,sans-serif" font-size="11">
            <rect x="20" y="20" width="150" height="200" rx="10" fill="{cbg}" stroke="{c1}" stroke-width="1.8"/>
            <text x="34" y="42" fill="{c1}" font-weight="600">ê°Å¸âÂ meu-mod/</text>
            <rect x="34" y="56" width="124" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.5"/><text x="96" y="73" text-anchor="middle" fill="#bae6fd">plugin.json</text>
            <rect x="34" y="104" width="124" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.5"/><text x="96" y="121" text-anchor="middle" fill="#bae6fd">hooks.json</text>
            <g filter="url(#{p}glow)"><rect x="34" y="152" width="124" height="26" rx="6" fill="{cbg}" stroke="{c1}" stroke-width="2"/></g><text x="96" y="169" text-anchor="middle" fill="{c2}">starter.mjs</text>
            <line x1="96" y1="82" x2="96" y2="102" stroke="#38bdf8" stroke-width="1.6" marker-end="url(#{p}seta)"/>
            <line x1="96" y1="130" x2="96" y2="150" stroke="#38bdf8" stroke-width="1.6" marker-end="url(#{p}seta)"/>
            <text x="96" y="205" text-anchor="middle" fill="{c2}" font-size="10">trêÂªs arquivos</text>
            <line class="wf-flow" x1="158" y1="165" x2="206" y2="120" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <rect x="208" y="98" width="156" height="34" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="2"/><text x="286" y="120" text-anchor="middle" fill="{c1}" font-weight="600">register(on, options)</text>
            <rect class="wf-a" x="200" y="30" width="54" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.5"/><text x="227" y="47" text-anchor="middle" fill="#bae6fd">$</text>
            <rect class="wf-a" x="260" y="30" width="54" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.5"/><text x="287" y="47" text-anchor="middle" fill="#bae6fd">e</text>
            <rect class="wf-a" x="320" y="30" width="54" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.5"/><text x="347" y="47" text-anchor="middle" fill="#bae6fd">next</text>
            <line x1="286" y1="98" x2="286" y2="60" stroke="{c1}" stroke-width="1.6" marker-end="url(#{p}seta)"/>
            <rect x="208" y="160" width="156" height="60" rx="8" fill="none" stroke="{c1}" stroke-width="1.4" stroke-dasharray="4 3"/>
            <text x="286" y="182" text-anchor="middle" fill="{c2}">on('tool.call', ê¢â¬Â¦)</text>
            <text x="286" y="202" text-anchor="middle" fill="{c2}">on('command.run', ê¢â¬Â¦)</text>
            <line x1="286" y1="132" x2="286" y2="158" stroke="{c1}" stroke-width="1.6" marker-end="url(#{p}seta)"/>
          </g>'''
    elif n == 2:
        label = 'Um evento entra pela esquerda e atravessa a cadeia: plugin A observa e chama next, plugin B reescreve e chama next, e o engine responde no fim. Embaixo, o estado mora em $.state durante a sessêÂ£o e em $.store entre sessêÂµes.'
        corpo = f'''<g font-family="Inter,sans-serif" font-size="11" text-anchor="middle">
            <g filter="url(#{p}glow)"><circle cx="40" cy="70" r="24" fill="{cbg}" stroke="{c1}" stroke-width="2"/></g><text x="40" y="74" fill="{c1}" font-weight="600">evento</text>
            <rect class="wf-a" x="88" y="50" width="76" height="40" rx="8" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.6"/><text x="126" y="68" fill="#bae6fd">plugin A</text><text x="126" y="83" fill="#7dd3fc" font-size="9">observa</text>
            <rect class="wf-a" x="188" y="50" width="76" height="40" rx="8" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.6"/><text x="226" y="68" fill="#bae6fd">plugin B</text><text x="226" y="83" fill="#7dd3fc" font-size="9">reescreve</text>
            <rect x="288" y="50" width="76" height="40" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="2"/><text x="326" y="68" fill="{c1}">engine</text><text x="326" y="83" fill="{c2}" font-size="9">responde</text>
            <line class="wf-flow" x1="64" y1="70" x2="86" y2="70" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <line class="wf-flow" x1="164" y1="70" x2="186" y2="70" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <line class="wf-flow" x1="264" y1="70" x2="286" y2="70" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <text x="175" y="40" fill="{c2}" font-size="10">next(e) ê¢â â next(e) ê¢â â resultado</text>
            <rect x="40" y="130" width="140" height="44" rx="10" fill="{cbg}" stroke="{c1}" stroke-width="1.8"/><text x="110" y="150" fill="{c1}" font-weight="600">$.state</text><text x="110" y="165" fill="{c2}" font-size="10">vale na sessêÂ£o</text>
            <rect x="200" y="130" width="140" height="44" rx="10" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.8"/><text x="270" y="150" fill="#bae6fd" font-weight="600">$.store</text><text x="270" y="165" fill="#7dd3fc" font-size="10">volta amanhêÂ£</text>
            <rect x="40" y="190" width="300" height="34" rx="8" fill="none" stroke="#f87171" stroke-width="1.4" stroke-dasharray="4 3"/><text x="190" y="211" fill="#fca5a5">variêÂ¡vel de mêÂ³dulo: some no reload</text>
          </g>'''
    elif n == 3:
        label = 'A janela do Claude Code com trêÂªs lugares onde um mod desenha: a conversa no alto, um painel encaixado êÂ  direita com botêÂµes e, logo acima da caixa de prompt, a faixa compartilhada. Ao lado, as quatro superfêÂ­cies: terminal, desktop, mobile e vscode.'
        corpo = f'''<g font-family="Inter,sans-serif" font-size="11">
            <rect x="16" y="16" width="260" height="208" rx="10" fill="#0b1220" stroke="{c1}" stroke-width="1.8"/>
            <rect x="28" y="30" width="150" height="104" rx="6" fill="#111827" stroke="#334155" stroke-width="1"/>
            <text x="40" y="50" fill="#94a3b8">conversa</text>
            <rect x="40" y="60" width="120" height="8" rx="3" fill="#334155"/><rect x="40" y="76" width="96" height="8" rx="3" fill="#334155"/><rect x="40" y="92" width="110" height="8" rx="3" fill="#334155"/>
            <g filter="url(#{p}glow)"><rect x="186" y="30" width="78" height="104" rx="6" fill="{cbg}" stroke="{c1}" stroke-width="2"/></g>
            <text x="225" y="50" text-anchor="middle" fill="{c1}" font-weight="600">Pane</text>
            <rect x="196" y="64" width="58" height="18" rx="4" fill="none" stroke="{c2}" stroke-width="1.2"/><text x="225" y="77" text-anchor="middle" fill="{c2}" font-size="10">[ a ] abrir</text>
            <rect x="196" y="90" width="58" height="18" rx="4" fill="none" stroke="{c2}" stroke-width="1.2"/><text x="225" y="103" text-anchor="middle" fill="{c2}" font-size="10">[ x ] fechar</text>
            <rect class="wf-a" x="28" y="144" width="236" height="26" rx="6" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.8"/><text x="146" y="161" text-anchor="middle" fill="#bae6fd">AbovePrompt êÂ· faixa de todos</text>
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
            <rect x="20" y="150" width="104" height="40" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="1.8"/><text x="72" y="168" fill="{c2}">validate</text><text x="72" y="182" fill="{c2}" font-size="10">ê¢Åâ passed</text>
            <rect x="140" y="150" width="104" height="40" rx="8" fill="{cbg}" stroke="{c1}" stroke-width="1.8"/><text x="192" y="168" fill="{c2}">test</text><text x="192" y="182" fill="{c2}" font-size="10">0 fail</text>
            <rect x="260" y="150" width="104" height="40" rx="8" fill="#0b1f2e" stroke="#38bdf8" stroke-width="1.8"/><text x="312" y="168" fill="#bae6fd">marketplace</text><text x="312" y="182" fill="#7dd3fc" font-size="10">install</text>
            <line x1="124" y1="170" x2="138" y2="170" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <line x1="244" y1="170" x2="258" y2="170" stroke="{c1}" stroke-width="2" marker-end="url(#{p}seta)"/>
            <text x="190" y="220" fill="{c2}" font-size="10">controlar ê¢â â testar ê¢â â distribuir</text>
          </g>'''
    return (f'<svg viewBox="0 0 380 240" class="w-full h-auto" role="img" aria-label="{html.escape(label)}">\n          {defs}\n'
            f'          <rect x="0" y="0" width="380" height="240" fill="url(#{p}grid)"/>\n          {corpo}\n        </svg>')

E = html.escape

def trilha(n):
    cor, c1, _, _ = CORES[n]
    emo, nome = NOMES[n]
    mids = [f'{n}-{k}' for k in range(1, 5)]
    out = [f'<!--TITLE: Trilha {n} êÂ· {nome} -->']
    out.append(f'''  <header class="bg-gradient-to-br from-{cor}-900/30 via-dark-800 to-dark-800 py-12 border-b border-dark-600" data-ARCKHê-track="{n}">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 lg:grid lg:grid-cols-[1fr_380px] lg:gap-10 lg:items-center">
      <div>
        <span class="inline-block px-3 py-1 bg-{cor}-500/20 text-{cor}-400 text-xs font-semibold rounded-full mb-4">TRILHA {n}</span>
        <h1 class="text-3xl sm:text-4xl font-bold mb-4">{emo} {nome}</h1>
        <p class="text-lg text-neutral-400 max-w-3xl">{E(HERO_TXT[n])}</p>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-8 max-w-2xl">
          <div class="bg-dark-800/50 rounded-lg p-3 border border-dark-600"><div class="text-xl font-bold text-{cor}-400">4</div><div class="text-xs text-neutral-400">MêÂ³dulos</div></div>
          <div class="bg-dark-800/50 rounded-lg p-3 border border-dark-600"><div class="text-xl font-bold text-{cor}-400">24</div><div class="text-xs text-neutral-400">TêÂ³picos</div></div>
          <div class="bg-dark-800/50 rounded-lg p-3 border border-dark-600"><div class="text-xl font-bold text-{cor}-400">~2h20</div><div class="text-xs text-neutral-400">DuraêÂ§êÂ£o</div></div>
          <div class="bg-dark-800/50 rounded-lg p-3 border border-dark-600"><div class="text-xl font-bold text-{cor}-400">{NIVEL[n]}</div><div class="text-xs text-neutral-400">NêÂ­vel</div></div>
        </div>
        <div data-ARCKHê-meter="trilha:{n}" class="mt-6 max-w-2xl" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-label="Progresso da trilha {n}">
          <div class="flex justify-between text-xs text-neutral-400 mb-1"><span data-ARCKHê-meter-frac>0 de 24</span><span data-ARCKHê-meter-pct>0%</span></div>
          <div class="ARCKHê-bar"><div class="ARCKHê-bar__fill" data-ARCKHê-meter-fill></div></div>
        </div>
      </div>
      <div class="mt-8 lg:mt-0 rounded-2xl border border-{cor}-500/30 bg-dark-900/40 p-3 overflow-hidden">
        {svg_hero(n)}
      </div>
    </div>
  </header>

  <main id="conteudo" class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12" data-ARCKHê-track="{n}">

    <section class="mb-12">
      <h2 class="text-2xl font-bold mb-6">Mapa da trilha</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">''')
    for mid in mids:
        M = MODS[mid]; num = mid.replace('-', '.')
        out.append(f'''        <a href="#modulo-{mid}" class="group bg-dark-800 rounded-xl border border-dark-600 hover:border-{cor}-500/30 p-5 transition-all">
          <div class="flex items-center justify-between mb-2"><span class="text-{cor}-400 font-bold text-sm">{num}</span><span class="text-xs text-neutral-500">{M['tipo']} êÂ· ~35 min</span></div>
          <h3 class="font-semibold mb-1 group-hover:text-{cor}-400 transition-colors">{M['emoji']} {E(M['titulo'])}</h3>
          <p class="text-xs text-neutral-400">{E(M['sub'])}</p>
        </a>''')
    out.append('''      </div>
    </section>

    <h2 class="text-2xl font-bold mb-6">ConteêÂºdo detalhado</h2>
''')
    for mid in mids:
        M = MODS[mid]; num = mid.replace('-', '.')
        out.append(f'''    <!-- ===== MODULO {num} ===== -->
    <div id="modulo-{mid}" data-ARCKHê-module="{mid}" data-ARCKHê-track="{n}" class="bg-dark-800 rounded-xl border border-dark-600 mb-6">
      <div class="p-6 border-b border-dark-600">
        <div class="flex items-center justify-between mb-2"><span class="text-{cor}-400 font-bold">{num}</span><span class="text-xs text-neutral-500">{M['tipo']} êÂ· ~35 min</span></div>
        <h3 class="text-2xl font-bold mb-2">{M['emoji']} {E(M['titulo'])}</h3>
        <p class="text-neutral-400 text-sm">{E(MOD_DESC[mid])}</p>
        <div data-ARCKHê-meter="modulo:{mid}" class="mt-4" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-label="Progresso do mêÂ³dulo {num}">
          <div class="flex justify-between text-xs text-neutral-400 mb-1"><span data-ARCKHê-meter-frac>0 de 6</span><span data-ARCKHê-meter-pct>0%</span></div>
          <div class="ARCKHê-bar"><div class="ARCKHê-bar__fill" data-ARCKHê-meter-fill></div></div>
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
              <div><span class="text-{cor}-400 font-semibold">O que êÂ©:</span><p class="text-neutral-300 text-sm">{E(oque)}</p></div>
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
        prox = f'<a href="../trilha{n+1}/index.html" class="flex-1 text-center px-6 py-3 bg-{cor}-600 text-white rounded-lg font-semibold hover:bg-{cor}-500 transition-colors">PrêÂ³xima trilha: {NOMES[n+1][1]} ê¢â â</a>'
    else:
        prox = f'<a href="modulo-4-4.html#topico-5" class="flex-1 text-center px-6 py-3 bg-{cor}-600 text-white rounded-lg font-semibold hover:bg-{cor}-500 transition-colors">Ir para o projeto final ê¢â â</a>'
    out.append(f'''    <div class="flex flex-col sm:flex-row gap-4 mt-12">
      <a href="../../index.html" class="flex-1 text-center px-6 py-3 bg-dark-700 text-neutral-300 rounded-lg font-semibold hover:bg-dark-600 transition-colors">ê¢â Â Voltar ao inêÂ­cio</a>
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
      <iframe src="modulo-{mid}.html" title="MêÂ³dulo {num}" loading="lazy" class="flex-1 w-full rounded-b-xl"></iframe>
    </div>
  </div>''')
    return '\n'.join(out) + '\n'

for n in range(1, 5):
    p = RAIZ / 'context' / 'corpos' / f'trilha{n}.html'
    p.write_text(trilha(n), encoding='utf-8')
    print(p, p.read_text().count('\n'), 'linhas')
