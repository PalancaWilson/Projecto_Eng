
document.addEventListener("DOMContentLoaded", () => {
  const tabela = document.getElementById("tabelaUsuarios");
  const formUsuario = document.getElementById("formUsuario");
  const usuarioForm = document.getElementById("usuarioForm");
  const feedback = document.getElementById("feedback");
  const btnAdicionar = document.querySelector("button.bg-blue-600");
  const btnCancelar = formUsuario.querySelector("button.bg-gray-200");

  let modoEdicao = false;
  let usuarioEditandoId = null;

  const usuariosExemplo = [
    { id: 1, nome: "João Silva", email: "joao@email.com", tipo: "Administrador", estado: "Autorizado" },
    { id: 2, nome: "Maria Santos", email: "maria@email.com", tipo: "Segurança", estado: "Autorizado" }
  ];

  function renderTabela(usuarios) {
    tabela.innerHTML = "";
    usuarios.forEach(usuario => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="p-3">${usuario.nome}</td>
        <td class="p-3">${usuario.email}</td>
        <td class="p-3">${usuario.tipo}</td>
        <td class="p-3"><span class="bg-green-100 text-green-700 px-2 py-1 rounded">${usuario.estado}</span></td>
        <td class="p-3 flex gap-2">
          <button class="editar text-blue-600" data-id="${usuario.id}">✏️</button>
          <button class="remover text-red-600" data-id="${usuario.id}">🗑️</button>
        </td>
      `;
      tabela.appendChild(tr);
    });
  }

  function resetFormulario() {
    usuarioForm.reset();
    formUsuario.classList.add("hidden");
    modoEdicao = false;
    usuarioEditandoId = null;
  }

  btnAdicionar.addEventListener("click", () => {
    formUsuario.classList.remove("hidden");
    usuarioForm.reset();
  });

  btnCancelar.addEventListener("click", () => resetFormulario());

  usuarioForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const campos = usuarioForm.querySelectorAll("input, select");
    const novoUsuario = {
      id: modoEdicao ? usuarioEditandoId : Date.now(),
      nome: campos[0].value,
      email: campos[0].value.toLowerCase().replace(/\s+/g, '') + "@isp.com",
      tipo: campos[2].value,
      estado: "Autorizado"
    };

    if (modoEdicao) {
      const index = usuariosExemplo.findIndex(u => u.id === usuarioEditandoId);
      usuariosExemplo[index] = novoUsuario;
    } else {
      usuariosExemplo.push(novoUsuario);
    }

    renderTabela(usuariosExemplo);
    resetFormulario();
    feedback.classList.remove("hidden");
  });

  tabela.addEventListener("click", (e) => {
    if (e.target.classList.contains("editar")) {
      const id = parseInt(e.target.dataset.id);
      const usuario = usuariosExemplo.find(u => u.id === id);
      const campos = usuarioForm.querySelectorAll("input, select");
      campos[0].value = usuario.nome;
      campos[1].value = usuario.tipo;
      campos[2].value = "********"; // senha fictícia
      campos[3].value = usuario.tipo;
      formUsuario.classList.remove("hidden");
      modoEdicao = true;
      usuarioEditandoId = id;
    }

    if (e.target.classList.contains("remover")) {
      const id = parseInt(e.target.dataset.id);
      const i = usuariosExemplo.findIndex(u => u.id === id);
      if (i !== -1) {
        usuariosExemplo.splice(i, 1);
        renderTabela(usuariosExemplo);
      }
    }
  });

  renderTabela(usuariosExemplo);
});