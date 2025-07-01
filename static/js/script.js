
document.addEventListener('DOMContentLoaded', () => {

  // LOGIN DE USUÁRIO
  const btnEntrar = document.getElementById('btnEntrar');
  if (btnEntrar) {
    btnEntrar.addEventListener('click', async () => {
      const email = document.getElementById('email').value.trim();
      const senha = document.getElementById('senha').value.trim();
      const tipoRadio = document.querySelector('input[name="tipo"]:checked');

      if (!email || !senha || !tipoRadio) {
        alert("Preencha todos os campos.");
        return;
      }

      const tipo = tipoRadio.parentElement.textContent.trim();

      try {
        const response = await fetch('http://127.0.0.1:5000/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, senha, tipo })
        });

        const result = await response.json();

        if (response.ok && result.status === "sucesso") {
          alert("Login bem-sucedido!");

          sessionStorage.setItem("usuario", JSON.stringify(result.usuario));

          if (tipo === "Administrador") {
            window.location.href = "dasbord.html";
          } else if (tipo === "Seguranca") {
            window.location.href = "dashboard_seguranca.html";
          } else {
            alert("Tipo de usuário inválido.");
          }
        } else {
          alert(result.mensagem || "Credenciais inválidas.");
        }

      } catch (error) {
        alert("Erro ao conectar com o servidor.");
        console.error(error);
      }
    });
  }
  

  document.addEventListener("DOMContentLoaded", () => {
    const selectTipoUsuario = document.getElementById("tipo_usuario");
  
    // Verifica se o elemento existe antes de continuar
    if (!selectTipoUsuario) return;
  
    fetch("http://localhost:5000/frequentadores")
      .then(response => {
        if (!response.ok) {
          throw new Error("Erro ao buscar frequentadores.");
        }
        return response.json();
      })
      .then(data => {
        data.forEach(f => {
          const option = document.createElement("option");
          option.value = f.id_frequentador; // Envia o ID na submissão
          option.textContent = `${f.nome} (${f.tipo})`;
          selectTipoUsuario.appendChild(option);
        });
      })
      .catch(error => {
        console.error("Erro ao carregar frequentadores:", error);
        alert("Erro ao carregar os frequentadores. Tente novamente.");
      });
  });
  
  

  // CADASTRO DE VEÍCULO
  const formVeiculo = document.getElementById("formCadastroVeiculo");
  if (formCadastroVeiculo) {
    formCadastroVeiculo.addEventListener("submit", function (e) {
      e.preventDefault();

      const dados = {
        matricula: document.getElementById("matricula").value.trim(),
        proprietario: document.getElementById("proprietario").value.trim(),
        tipo_usuario: document.getElementById("tipo_usuario").value,
        marca: document.getElementById("marca").value.trim(),
        modelo : document.getElementById("modelo").value.trim(),
        estado : document.getElementById("estado").value,
        imagem : document.getElementById("imagem").files[0]
      };

      if (!matricula || !proprietario || !tipo_usuario || !marca || !modelo || !estado || !imagem) {
        alert("Por favor, preencha todos os campos e selecione uma imagem.");
        return;
      }

      const formData = new FormData(formVeiculo);
    formData.append("matricula", matricula);
    formData.append("proprietario", proprietario);
    formData.append("tipo_usuario", tipo_usuario);
    formData.append("marca", marca);
    formData.append("modelo", modelo);
    formData.append("estado", estado);
    formData.append("imagem", imagem);
    formData.append("cadastrado_por", 1); // Substituir pelo ID do usuário autenticado, se aplicável

      fetch("http://localhost:5000/cadastrar-veiculo", {
        method: "POST",
        body: formData,
      })
      .then(response => response.json())
      .then(resposta => {
        alert(resposta.mensagem);
        if (resposta.status === "sucesso") {
          formVeiculo.reset();
        }
      })
      .catch(error => {
        console.error("Erro ao cadastrar:", error);
        alert("Erro ao conectar com o servidor.");
      });
    });
  }

});





// Dasbord 

document.addEventListener("DOMContentLoaded", () => {
  fetch("http://127.0.0.1:5000/dashboard-data")
    .then(response => response.json())
    .then(data => {
      document.getElementById("totalVeiculos").textContent = data.total_veiculos;
      document.getElementById("tentativasNegadas").textContent = data.recusados;
      document.getElementById("acessosDia").textContent = data.acessos_dia;
      document.getElementById("pendencias").textContent = data.pendentes;
    })
    .catch(error => {
      console.error("Erro ao buscar dados do dashboard:", error);
      alert("Não foi possível carregar as informações do painel.");
    });
});




// Historico de acesso
document.addEventListener("DOMContentLoaded", () => {
  fetch("http://127.0.0.1:5000/api/historico")
    .then(response => response.json())
    .then(dados => {
      const tbody = document.getElementById("acessosTableBody");
      tbody.innerHTML = ""; // limpar

      if (dados.length === 0) {
        tbody.innerHTML = `
          <tr><td colspan="6" class="text-center text-gray-500 py-4">Nenhum acesso encontrado.</td></tr>`;
        return;
      }

      dados.forEach(acesso => {
        const tr = document.createElement("tr");
        tr.classList.add("bg-gray-50", "rounded-lg");

        tr.innerHTML = `
          <td class="px-4 py-2">${acesso.data_acesso}</td>
          <td class="px-4 py-2">${acesso.hora_acesso}</td>
          <td class="px-4 py-2">${acesso.tipo_usuario}</td>
          <td class="px-4 py-2">${acesso.matricula}</td>
          <td class="px-4 py-2">
            <span class="${acesso.estado === 'Autorizado' ? 'text-green-600' : 'text-red-600'} font-semibold">
              ${acesso.estado}
            </span>
          </td>
          <td class="px-4 py-2 text-center">
            <span class="material-symbols-outlined cursor-pointer text-gray-600 hover:text-gray-900">download</span>
          </td>
        `;
        tbody.appendChild(tr);
      });
    })
    .catch(error => {
      console.error("Erro ao carregar acessos:", error);
      const tbody = document.getElementById("acessosTableBody");
      tbody.innerHTML = `
        <tr><td colspan="6" class="text-center text-red-500 py-4">Erro ao carregar acessos.</td></tr>`;
    });
});
