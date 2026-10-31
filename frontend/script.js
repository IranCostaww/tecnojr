// aqui ficam os dados de exemplo do cafe. se precisar trocar telefone, endereco ou horario, e so alterar os valores abaixo:
const CONFIG_CAFE = {
  nome: "Café do Bairro",
  telefone: "11987654321",
  telefoneFormatado: "(11) 98765-4321",
  endereco: "Rua das Acácias, 142 - Bairro das Flores, São Paulo - SP",
  horario: "Terça a Sábado: 07h30 às 18h30\nDomingo: 08h00 às 13h00 (fechado às segundas)",
  apiUrl: "http://127.0.0.1:8000"
};

const campoConsulta = document.getElementById("data-consulta");
const listaConsulta = document.getElementById("lista-consulta");
const btnConsultar = document.getElementById("btn-consultar");
const campoTelefone = document.getElementById("telefone");

// aplica mascara no telefone enquanto o cliente digita, aceitando formato com DDD
campoTelefone.addEventListener("input", (evento) => {
  let digitos = evento.target.value.replace(/\D/g, "");
  if (digitos.length > 11) {
    digitos = digitos.slice(0, 11);
  }

  if (digitos.length <= 2) {
    evento.target.value = digitos.length > 0 ? `(${digitos}` : "";
  } else if (digitos.length <= 6) {
    evento.target.value = `(${digitos.slice(0, 2)}) ${digitos.slice(2)}`;
  } else if (digitos.length <= 10) {
    evento.target.value = `(${digitos.slice(0, 2)}) ${digitos.slice(2, 6)}-${digitos.slice(6)}`;
  } else {
    evento.target.value = `(${digitos.slice(0, 2)}) ${digitos.slice(2, 7)}-${digitos.slice(7, 11)}`;
  }
});

// funcao que busca e renderiza as encomendas de uma data no painel
async function buscarEncomendas(dataEscolhida) {
  if (!dataEscolhida) {
    listaConsulta.innerHTML = '<p class="aviso-vazio">Escolha uma data para pesquisar.</p>';
    return;
  }

  listaConsulta.innerHTML = '<p class="aviso-vazio">Buscando encomendas...</p>';

  try {
    const resposta = await fetch(`${CONFIG_CAFE.apiUrl}/encomendas?data=${dataEscolhida}`);
    const encomendas = await resposta.json();

    if (!resposta.ok) {
      listaConsulta.innerHTML = '<p class="aviso-vazio">Erro ao carregar pedidos.</p>';
      return;
    }

    if (encomendas.length === 0) {
      listaConsulta.innerHTML = `<p class="aviso-vazio">Nenhuma encomenda marcada para o dia ${dataEscolhida}.</p>`;
      return;
    }

    let html = "";
    encomendas.forEach((item) => {
      let classeStatus = "status-recebida";
      if (item.status === "em preparo") classeStatus = "status-em-preparo";
      if (item.status === "entregue") classeStatus = "status-entregue";

      html += `
        <div class="item-encomenda-lista">
          <div><strong>${item.cliente_nome}</strong> - ${item.produto}</div>
          <div>Telefone: ${item.telefone}</div>
          <span class="tag-status ${classeStatus}">${item.status}</span>
        </div>
      `;
    });

    listaConsulta.innerHTML = html;
  } catch (erro) {
    listaConsulta.innerHTML = '<p class="aviso-vazio">Servidor fora do ar ou inacessível.</p>';
  }
}

// preenche as informacoes nos textos da pagina e monta o link do whatsapp
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("texto-horario").innerText = CONFIG_CAFE.horario;
  document.getElementById("texto-endereco").innerText = CONFIG_CAFE.endereco;
  document.getElementById("texto-telefone-rodape").innerText = "Telefone: " + CONFIG_CAFE.telefoneFormatado;

  const linkWhats = document.getElementById("link-whatsapp-destaque");
  const mensagemWhats = encodeURIComponent("Olá Dona Marta! Gostaria de tirar uma dúvida sobre os bolos e encomendas.");
  linkWhats.href = "https://wa.me/55" + CONFIG_CAFE.telefone + "?text=" + mensagemWhats;

  // define a data minima de entrega como hoje para evitar agendar no passado
  const campoData = document.getElementById("data-entrega");
  const hoje = new Date().toISOString().split("T")[0];
  campoData.min = hoje;

  campoConsulta.value = hoje;
});

// envio do formulario de encomenda para o backend
const formEncomenda = document.getElementById("form-encomenda");
const mensagemResposta = document.getElementById("mensagem-resposta");
const btnEnviar = document.getElementById("btn-enviar-encomenda");
let enviandoPedido = false;

formEncomenda.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  // evita cliques duplos ou envios simultaneos
  if (enviandoPedido) {
    return;
  }

  // valida o telefone no formulario e extrai apenas os numeros
  const telefoneLimpo = campoTelefone.value.replace(/\D/g, "");
  if (telefoneLimpo.length < 10 || telefoneLimpo.length > 11) {
    mensagemResposta.className = "mensagem-status erro";
    mensagemResposta.innerText = "Por favor, digite um telefone válido com DDD (10 ou 11 dígitos).";
    return;
  }

  enviandoPedido = true;
  btnEnviar.disabled = true;
  btnEnviar.innerText = "Enviando pedido...";
  mensagemResposta.className = "mensagem-status escondido";

  const dadosFormulario = {
    cliente_nome: document.getElementById("cliente-nome").value.trim(),
    telefone: telefoneLimpo,
    produto: document.getElementById("produto").value,
    data_entrega: document.getElementById("data-entrega").value,
    status: "recebida"
  };

  try {
    const resposta = await fetch(`${CONFIG_CAFE.apiUrl}/encomendas`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(dadosFormulario)
    });

    const resultado = await resposta.json();

    if (resposta.ok) {
      mensagemResposta.className = "mensagem-status sucesso";
      mensagemResposta.innerText = `Encomenda confirmada para ${dadosFormulario.cliente_nome}! Seu pedido de ${dadosFormulario.produto} foi agendado para o dia ${dadosFormulario.data_entrega}.`;
      formEncomenda.reset();

      // atualiza a lista do dia logo apos a criacao sem recarregar a pagina
      campoConsulta.value = dadosFormulario.data_entrega;
      await buscarEncomendas(dadosFormulario.data_entrega);
    } else {
      mensagemResposta.className = "mensagem-status erro";
      // trata mensagem de texto ou lista de erros de validacao sem mostrar [object Object]
      let mensagemErro = "Não foi possível registrar a encomenda. Tente novamente.";
      if (typeof resultado.detail === "string") {
        mensagemErro = resultado.detail;
      } else if (Array.isArray(resultado.detail) && resultado.detail.length > 0) {
        mensagemErro = resultado.detail.map(e => {
          let texto = e.msg || e;
          return typeof texto === "string" ? texto.replace(/^Value error,\s*/i, "") : texto;
        }).join("; ");
      }
      mensagemResposta.innerText = mensagemErro;
    }
  } catch (erro) {
    mensagemResposta.className = "mensagem-status erro";
    mensagemResposta.innerText = "Erro ao conectar com o servidor. Verifique se o backend está rodando.";
  } finally {
    enviandoPedido = false;
    btnEnviar.disabled = false;
    btnEnviar.innerText = "Confirmar Encomenda";
  }
});

// clique do botao de consulta rapida
btnConsultar.addEventListener("click", () => {
  buscarEncomendas(campoConsulta.value);
});
