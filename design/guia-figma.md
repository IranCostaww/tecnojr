# Guia de Montagem do Layout no Figma

Este guia traz todas as especificacoes necessarias para recriar o layout do Cafe do Bairro no Figma, mantendo a identidade simples e a total fidelidade com o codigo do front-end.

## Mini Direcao Visual

Frase de conceito:
Um ambiente acolhedor e simples para um cafe de bairro, combinando tons de cafe com leite e navegacao direta pensada para o celular.

Tipografia (Google Fonts):
- Titulos: Lora (serifada, estilo artesanal de receita caseira).
- Textos e botoes: Nunito (sem serifa, cantos levemente suaves, muito facil de ler no celular).

Paleta de Cores:
- Fundo geral: #FBF8F3 (creme suave, lembra leite morno).
- Superficie e cards: #FFFFFF (branco puro para destaque de conteudo).
- Fundo de apoio: #F4EDE4 (tom de cafe com leite suave para blocos de informacao).
- Titulos e marca: #4A2E1B (marrom escuro profundo, cor de grao de cafe).
- Subtitulos e precos: #8C5336 (terracota suave e canela).
- Botao de acao principal: #C47C48 (tom de caramelo e bolo assado).
- Botao de acao hover: #AA6534 (caramelo escuro).
- Botao de WhatsApp: #2E6B4D (verde folha, sem tom neon).
- Botao de WhatsApp hover: #24543D (verde folha escuro).
- Texto principal: #33261D (marrom escuro para leitura confortavel).
- Texto de apoio: #6B564A (marrom neutro para descricoes e detalhes).
- Bordas e divisores: #E4D8CB (areia claro para linhas suaves).
- Mensagem de sucesso: #2C6B4B sobre fundo #EAF5EE.
- Mensagem de erro de limite: #9E3A3A sobre fundo #FBEAEA.

## Como Usar o Logo de Xicara

O logo segue o desenho simples que o filho da Dona Marta fez:
- Traco: vetor simples com espessura de 3px e cantos arredondados (round cap/join).
- Cor da xicara e do pires: #4A2E1B.
- Cor do vapor: tres pequenas linhas onduladas verticais saindo da xicara na cor #8C5336 com 2.5px de espessura.
- Tamanho no frame: caixa delimitadora de 34 x 34 pixels.
- Posicionamento: no cabecalho, ao lado esquerdo do texto "Cafe do Bairro", com espacamento de 10px entre o icone e o texto.

## Configuracao do Frame no Figma

- Nome do frame: Mobile - Cafe do Bairro
- Dimensoes: 390px de largura por 844px de altura (padrao moderno para testes de celular).
- Estrutura: Auto Layout vertical, alinhamento ao topo, espacamento entre itens de 0px.
- Padding lateral geral do conteudo: 20px a esquerda e a direita.
- Raio de curvatura dos cantos (border radius): 10px para botoes, caixas de formulario e cards.

## Estrutura das Secoes na Ordem

1. Topo fixo (Header)
- Altura aproximada: 60px.
- Fundo: #FFFFFF com borda inferior de 1px em #E4D8CB.
- Conteudo: logo da xicara e texto "Cafe do Bairro" em Lora Semibold 20px a esquerda. Botao pequeno "Encomendar" a direita em Nunito Bold 14px, fundo #F4EDE4 e texto #4A2E1B.

2. Apresentacao principal (Hero)
- Espacamento: padding superior de 36px e inferior de 30px.
- Tag superior: capsula com fundo #F4EDE4, texto "Aberto ha 6 anos" em Nunito Bold 13px, cor #8C5336.
- Titulo principal: "Cafe coado, pao de queijo e bolos caseiros por encomenda" em Lora Regular 28px, entrelinha de 1.25, cor #4A2E1B.
- Texto descritivo: "A Dona Marta prepara bolos caseiros por encomenda e serve cafe fresquinho com pao de queijo quentinho no balcao" em Nunito Regular 16px, cor #6B564A.
- Botoes: dois botoes empilhados verticalmente com 12px de distancia. O primeiro e o botao principal em #C47C48 com texto branco "Fazer encomenda online". O segundo e o botao do WhatsApp em #2E6B4D com texto branco "Pedir pelo WhatsApp". Ambos com altura de 48px e raio de 10px.

3. Secao Cardapio
- Titulo da secao: "Nosso Cardapio" em Lora Semibold 24px, cor #4A2E1B.
- Subtitulo: Nunito Regular 15px, cor #6B564A.
- Cards dos itens: caixas com fundo #FFFFFF, borda de 1px em #E4D8CB, padding interno de 16px e raio de 10px.
- Tipografia do card: nome do item em Lora Semibold 18px e preco em Nunito Bold 16px (#8C5336). Descricao curta em Nunito Regular 14px (#6B564A).
- Destaques visuais: os bolos caseiros possuem uma borda lateral esquerda de 5px em cor caramelo (#C47C48) e a tag "Feito por encomenda". O panetone artesanal possui fundo levemente aquecido (#FAF4EE) e borda esquerda de 5px em #8C5336 com tag "Edicao de fim de ano".

4. Secao Onde Estamos e Horarios
- Titulo da secao: "Onde Estamos e Horarios" em Lora Semibold 24px.
- Cards informativos: duas caixas com fundo #F4EDE4, borda de 1px em #E4D8CB e padding de 16px.
- O primeiro card detalha o horario de funcionamento de terca a sabado (07h30 as 18h30) e domingo (08h00 as 13h00).
- O segundo card detalha o endereco fixo perto da praca central.

5. Secao Formulario de Encomenda
- Container: cartao de destaque com fundo #FFFFFF, borda de 1px em #E4D8CB, padding de 22px e raio de 10px.
- Cabecalho: titulo "Reserve sua Encomenda" e aviso claro sobre o limite de 5 encomendas por dia para a cozinha da Dona Marta.
- Campos de entrada: nome completo, telefone com DDD, selecao de bolo/panetone e data da entrega. Cada campo tem altura de 46px, fundo #FAFAFA, borda de 1px em #E4D8CB e raio de 10px.
- Botao de envio: largura total, cor #C47C48, altura de 48px, texto "Confirmar Encomenda" em Nunito Bold 16px.
- Estado de alerta: card de aviso que surge abaixo do formulario para exibir retorno de confirmacao (verde) ou de limite diario atingido (rosa/vermelho).

6. Secao Painel de Consulta do Dia
- Objetivo: pensada para a Dona Marta abrir no proprio celular da cozinha.
- Caixa com fundo #F6F1EA, borda de 1px em #E4D8CB e padding de 18px.
- Linha de filtro: seletor de data e botao "Ver dia" em #4A2E1B.
- Area de listagem: lista dos pedidos cadastrados com nome do cliente, produto, telefone e etiquetas de status coloridas (recebida em amarelo suave #F7E7CD, em preparo em azul suave #DCE8F7, entregue em verde suave #D6ECD9).

7. Rodape
- Fundo: #4A2E1B.
- Padding: 24px vertical.
- Texto: Nunito Regular 14px na cor #E8DDD4, contendo telefone para contato.
