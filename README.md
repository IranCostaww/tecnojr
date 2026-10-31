# Projeto Café do Bairro - TecnoJr

Esse projeto foi desenvolvido como solução para o processo seletivo da TecnoJr, atendendo às necessidades da Dona Marta, dona do Café do Bairro. O objetivo principal é organizar os pedidos de bolos e produtos caseiros que antes ficavam anotados no caderno, além de diminuir as mensagens repetitivas de clientes perguntando endereço, horário e cardápio.

O sistema é composto por uma página web simples e acolhedora pensada para celular (mobile first) e uma API em Python para salvar e gerenciar as encomendas no banco de dados SQLite.

## O que tem no projeto

A estrutura de pastas está organizada de forma bem direta:

projeto/
  backend/
    main.py (servidor com FastAPI e conexão SQLite)
    requirements.txt (dependências necessárias)
  frontend/
    index.html (estrutura da página com cardápio e formulário)
    style.css (estilos, cores terrosas e responsividade)
    script.js (lógica de envio do pedido e consulta)
  README.md (este manual)

## Dados de exemplo e onde trocar

O endereço, o horário de funcionamento e o telefone do WhatsApp colocados no site são dados fictícios que eu criei para demonstração.

Para trocar essas informações pelas reais do Café do Bairro:
1. Abra o arquivo frontend/script.js no seu editor de texto.
2. Logo nas primeiras linhas você vai encontrar o objeto CONFIG_CAFE.
3. Basta alterar o telefone, endereço e horário dentro desse bloco.
4. Ao salvar o arquivo e recarregar a página, os textos do site e o link do botão de WhatsApp vão se atualizar automaticamente.

## Como rodar o back-end

Para executar o servidor, você vai precisar do Python 3 instalado no computador. Este passo a passo foi feito para quem está rodando pela primeira vez:

1. Abra o terminal e entre na pasta do backend:
cd backend

2. Crie o ambiente virtual (venv) para manter as bibliotecas isoladas:
python3 -m venv venv

3. Ative o ambiente virtual:
No Linux ou Mac:
source venv/bin/activate

No Windows:
venv\Scripts\activate

4. Com o ambiente ativado e ainda dentro da pasta backend (se tiver saído, execute cd backend), instale as bibliotecas necessárias:
pip install -r requirements.txt

5. Inicie o servidor FastAPI usando o Uvicorn (certifique-se de estar na pasta backend com o comando cd backend):
uvicorn main:app --reload

O servidor vai iniciar no endereço http://127.0.0.1:8000. O parâmetro --reload faz o servidor reiniciar automaticamente sempre que você alterar o código do arquivo main.py.

## Como abrir o front-end

Como o front-end foi feito em HTML, CSS e JavaScript puros sem nenhum framework, abrir a página é direto:

Opção 1: vá até a pasta frontend e dê dois cliques no arquivo index.html para abrir no seu navegador.

Opção 2: se quiser simular um servidor local de arquivos, abra outro terminal na pasta frontend e rode:
python3 -m http.server 3000

Depois acesse http://localhost:3000 no navegador.

Para testar no celular, você pode abrir as ferramentas do desenvolvedor do navegador (F12 ou inspecionar elemento) e ativar a visualização móvel com largura de 390 px.

## Como testar a API

Existem duas maneiras bem práticas de testar o funcionamento da API:

1. Pela documentação automática do Swagger (/docs):
Com o servidor rodando, abra o navegador e vá para:
http://127.0.0.1:8000/docs

Nessa página interativa, você consegue visualizar todos os endpoints (POST, GET, PUT, DELETE), clicar no botão "Try it out" e fazer requisições diretamente pela interface sem precisar de programas externos.

2. Pelo terminal usando comando curl:
Aqui está um exemplo prático para cadastrar uma nova encomenda via terminal:

curl -X POST "http://127.0.0.1:8000/encomendas" \
  -H "Content-Type: application/json" \
  -d '{"cliente_nome": "Carlos Silva", "telefone": "11988887777", "produto": "Bolo de Fuba com Goiabada", "data_entrega": "2026-11-25", "status": "recebida"}'

Para listar as encomendas cadastradas:
curl "http://127.0.0.1:8000/encomendas"

Para filtrar as encomendas de um dia específico:
curl "http://127.0.0.1:8000/encomendas?data=2026-11-25"

## Como funciona a regra das 5 encomendas por dia

A Dona Marta explicou na reunião que só consegue produzir no máximo 5 bolos por dia na cozinha dela, e que na semana anterior acabou marcando pedidos a mais no mesmo dia.

Para resolver isso de forma confiável, a regra foi implementada dentro da rota POST /encomendas no backend:

1. O campo data_entrega é validado como data no formato AAAA-MM-DD pelo Pydantic, garantindo que o valor chegue sempre padronizado.
2. Antes de fazer o INSERT no banco de dados, o sistema roda uma consulta de contagem:
SELECT COUNT(*) FROM encomendas WHERE data_entrega = ?
3. Se o total retornado pelo banco já for igual ou maior que 5, a operação é interrompida imediatamente.
4. O servidor devolve um erro HTTP 400 com a seguinte mensagem: "Limite de 5 encomendas atingido para este dia. Escolha outra data."
5. O JavaScript do front-end captura essa resposta e exibe uma caixa de aviso na tela, explicando o ocorrido e orientando o cliente a escolher outra data disponível.
6. A mesma verificação de contagem também foi colocada na rota PUT caso alguém tente editar a data de uma encomenda existente para um dia que já esteja com 5 pedidos.

## O que eu faria com mais tempo

Se eu tivesse mais tempo de desenvolvimento neste projeto, implementaria duas melhorias principais:

1. Login simples para a Dona Marta:
Hoje a lista de encomendas do dia na página inicial mostra o nome e o telefone dos clientes para qualquer visitante que consultar a data. Com mais tempo, eu criaria uma tela de login simples protegida por senha, para que apenas a Dona Marta e quem trabalha com ela possam acessar os dados de contato dos clientes e atualizar o status dos pedidos.

2. Aviso automático por WhatsApp:
Integrar o sistema para enviar uma confirmação automática no WhatsApp do cliente assim que o pedido for registrado no site, e também mandar um aviso no celular da Dona Marta alertando que entrou uma encomenda nova com o produto e a data escolhida.
