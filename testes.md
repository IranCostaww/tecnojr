# Relatório de Testes do Projeto Café do Bairro

Este documento registra a execução real de todos os testes solicitados para o backend, o frontend e a estrutura geral do projeto, com o resultado de cada verificação.

## Testes do Backend

- Criar uma encomenda válida e conferir retorno 201 com id: PASSOU (criou com id 1 e salvou todos os campos).
- Criar com campo faltando (sem nome, sem telefone, sem produto, sem data): PASSOU (FastAPI devolveu erro 422 em todas as tentativas).
- Criar com data em formato errado (31/10/26, 2026-13-45, texto): PASSOU (Pydantic barrou com erro 422).
- Criar com data no passado: PASSOU (bloqueado com erro 400 e mensagem clara).
- Criar com status inválido (ex: "pronto"): PASSOU (bloqueado com erro 400 informando os status permitidos).
- Criar 5 encomendas na mesma data e tentar a sexta: PASSOU (a sexta tentativa devolveu erro 400 com mensagem sobre o limite diário).
- Após a sexta bloqueada, criar uma na data seguinte: PASSOU (cadastrou normalmente com status 201).
- Remover uma encomenda de uma data cheia e criar outra: PASSOU (após deletar, a vaga foi liberada e aceitou nova encomenda).
- Atualizar status da encomenda (recebida, em preparo, entregue): PASSOU (atualizou e persistiu a alteração).
- Atualizar data para dia que já tem 5 encomendas: PASSOU (backend bloqueou a alteração com erro 400 respeitando a regra).
- Atualizar e remover id inexistente: PASSOU (retornou erro 404 em ambos os casos, sem erro 500).
- Listar sem filtro e com filtro por data, inclusive data vazia: PASSOU (listou todas, filtrou pelo dia e retornou array vazio quando não há pedidos).
- Telefone com letras, muito curto ou não numérico: PASSOU (bloqueado pelo Pydantic com erro 422 e mensagem clara exigindo apenas dígitos e entre 10 e 11 caracteres).
- Nome com aspas, acento e caracteres especiais: PASSOU (salvou e retornou corretamente caracteres como acentos e apóstrofos).

## Testes do Frontend

- Enviar formulário com dados válidos: PASSOU (exibiu mensagem de confirmação e limpou todos os campos do formulário).
- Enviar com campos vazios: PASSOU (o navegador bloqueou o envio pelo atributo required sem quebrar a página).
- Máscara de telefone no formulário: PASSOU (aplica automaticamente formato com DDD como (73) 98861-4159 enquanto o cliente digita).
- Validação de telefone no formulário: PASSOU (mostra aviso em tela se o telefone tiver menos de 10 dígitos ou formato incorreto).
- Envio de telefone com dígitos puros: PASSOU (o formulário aceita a máscara visual mas envia somente os dígitos numéricos para a API).
- Enviar para data cheia: PASSOU (a mensagem de erro 400 devolvida pela API foi exibida no alerta da tela).
- Enviar com API desligada: PASSOU (exibiu a mensagem amigável informando que o servidor não respondeu).
- Clicar em "Ver dia" com data sem encomendas: PASSOU (exibiu o texto informando que não há pedidos para a data).
- Dados do formulário aparecem na listagem do dia logo após envio sem recarregar: PASSOU (a listagem do dia é atualizada automaticamente ao confirmar a encomenda).
- Botão de WhatsApp abre o link correto: PASSOU (link gerado com o número de exemplo e texto inicial preenchido).
- Links internos e imagens: PASSOU (todos os links âncoras apontam para seções existentes e o ícone em SVG carregou perfeitamente).
- Layout em 390 px, 768 px e 1280 px: PASSOU (testado em navegador real sem rolagem horizontal nem quebra de texto).
- Clique duplo rápido no botão de confirmar: PASSOU (trava booleana impede disparar requisições duplicadas).

## Testes Gerais

- Seguir o README do zero em pasta limpa com novo venv: PASSOU (todos os comandos executaram sem erros).
- Dependências no requirements.txt: PASSOU (contém fastapi e uvicorn, suficientes para executar o projeto).
- Variáveis e funções não utilizadas: PASSOU (revisão realizada no backend e frontend, apenas itens em uso mantidos).
- Apagar o banco, reiniciar o servidor e conferir recriação da tabela: PASSOU (o arquivo encomendas.db foi recriado vazio com a tabela de encomendas pronta).
