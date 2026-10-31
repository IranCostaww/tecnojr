# Relatorio de Testes do Projeto Cafe do Bairro

Este documento registra a execucao real de todos os testes solicitados para o backend, o frontend e a estrutura geral do projeto, com o resultado de cada verificacao.

## Testes do Backend

- Criar uma encomenda valida e conferir retorno 201 com id: PASSOU (criou com id 1 e salvou todos os campos).
- Criar com campo faltando (sem nome, sem telefone, sem produto, sem data): PASSOU (FastAPI devolveu erro 422 em todas as tentativas).
- Criar com data em formato errado (31/10/26, 2026-13-45, texto): PASSOU (Pydantic barrou com erro 422).
- Criar com data no passado: PASSOU (bloqueado com erro 400 e mensagem clara).
- Criar com status invalido (ex: "pronto"): PASSOU (bloqueado com erro 400 informando os status permitidos).
- Criar 5 encomendas na mesma data e tentar a sexta: PASSOU (a sexta tentativa devolveu erro 400 com mensagem sobre o limite diario).
- Apos a sexta bloqueada, criar uma na data seguinte: PASSOU (cadastrou normalmente com status 201).
- Remover uma encomenda de uma data cheia e criar outra: PASSOU (apos deletar, a vaga foi liberada e aceitou nova encomenda).
- Atualizar status da encomenda (recebida, em preparo, entregue): PASSOU (atualizou e persistiu a alteracao).
- Atualizar data para dia que ja tem 5 encomendas: PASSOU (backend bloqueou a alteracao com erro 400 respeitando a regra).
- Atualizar e remover id inexistente: PASSOU (retornou erro 404 em ambos os casos, sem erro 500).
- Listar sem filtro e com filtro por data, inclusive data vazia: PASSOU (listou todas, filtrou pelo dia e retornou array vazio quando nao ha pedidos).
- Telefone com letras, muito curto ou nao numerico: PASSOU (bloqueado pelo Pydantic com erro 422 e mensagem clara exigindo apenas digitos e entre 10 e 11 caracteres).
- Nome com aspas, acento e caracteres especiais: PASSOU (salvou e retornou corretamente caracteres como acentos e apostrofos).

## Testes do Frontend

- Enviar formulario com dados validos: PASSOU (exibiu mensagem de confirmacao e limpou todos os campos do formulario).
- Enviar com campos vazios: PASSOU (o navegador bloqueou o envio pelo atributo required sem quebrar a pagina).
- Mascara de telefone no formulario: PASSOU (aplica automaticamente formato com DDD como (73) 98861-4159 enquanto o cliente digita).
- Validacao de telefone no formulario: PASSOU (mostra aviso em tela se o telefone tiver menos de 10 digitos ou formato incorreto).
- Envio de telefone com digitos puros: PASSOU (o formulario aceita a mascara visual mas envia somente os digitos numericos para a API).
- Enviar para data cheia: PASSOU (a mensagem de erro 400 devolvida pela API foi exibida no alerta da tela).
- Enviar com API desligada: PASSOU (exibiu a mensagem amigavel informando que o servidor nao respondeu).
- Clicar em "Ver dia" com data sem encomendas: PASSOU (exibiu o texto informando que nao ha pedidos para a data).
- Dados do formulario aparecem na listagem do dia logo apos envio sem recarregar: PASSOU (a listagem do dia e atualizada automaticamente ao confirmar a encomenda).
- Botao de WhatsApp abre o link correto: PASSOU (link gerado com o numero de exemplo e texto inicial preenchido).
- Links internos e imagens: PASSOU (todos os links ancoras apontam para secoes existentes e o icone em SVG carregou perfeitamente).
- Layout em 390 px, 768 px e 1280 px: PASSOU (testado em navegador real sem rolagem horizontal nem quebra de texto).
- Clique duplo rapido no botao de confirmar: PASSOU (trava booleana impede disparar requisicoes duplicadas).

## Testes Gerais

- Seguir o README do zero em pasta limpa com novo venv: PASSOU (todos os comandos executaram sem erros).
- Dependencias no requirements.txt: PASSOU (contem fastapi e uvicorn, suficientes para executar o projeto).
- Variaveis e funcoes nao utilizadas: PASSOU (revisao realizada no backend e frontend, apenas itens em uso mantidos).
- Apagar o banco, reiniciar o servidor e conferir recriacao da tabela: PASSOU (o arquivo encomendas.db foi recriado vazio com a tabela de encomendas pronta).
