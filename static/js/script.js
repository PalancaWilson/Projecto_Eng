
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
          } else if (tipo === "Segurança" || tipo === "Seguranca") {
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

  // DASHBOARD
  if (document.getElementById("totalVeiculos")) {
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
  }

  // HISTÓRICO DE ACESSOS
  if (document.getElementById("acessosTableBody")) {
    fetch("http://127.0.0.1:5000/api/historico")
      .then(response => response.json())
      .then(dados => {
        const tbody = document.getElementById("acessosTableBody");
        tbody.innerHTML = "";

        if (dados.length === 0) {
          tbody.innerHTML = '<tr><td colspan="6" class="text-center text-gray-500 py-4">Nenhum acesso encontrado.</td></tr>';
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
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-red-500 py-4">Erro ao carregar acessos.</td></tr>';
      });
  }

  // FORMULÁRIO DE CADASTRO DE VEÍCULO
  const formVeiculo = document.getElementById("formCadastroVeiculo");
  const selectTipoUsuario = document.getElementById("tipo_usuario");

  if (selectTipoUsuario) {
    fetch("http://localhost:5000/frequentadores")
      .then(res => res.json())
      .then(data => {
        data.forEach(f => {
          const option = document.createElement("option");
          option.value = f.id_frequentador;  // Corrigido para enviar ID inteiro
          option.textContent = `${f.nome} (${f.tipo})`;
          selectTipoUsuario.appendChild(option);
        });
      })
      .catch(err => {
        console.error("Erro ao carregar frequentadores:", err);
        alert("Não foi possível carregar os tipos de usuário.");
      });
  }

  if (formVeiculo) {
    formVeiculo.addEventListener("submit", function (e) {
      e.preventDefault();

      const formData = new FormData(formVeiculo);
      const matricula = formData.get("matricula");
      const proprietario = formData.get("proprietario");
      const tipo_usuario = formData.get("tipo_usuario");

      if (!matricula || !proprietario || !tipo_usuario) {
        alert("Preencha todos os campos obrigatórios.");
        return;
      }

      fetch("http://localhost:5000/cadastrar-veiculo", {
        method: "POST",
        body: formData
      })
        .then(response => response.json())
        .then(res => {
          alert(res.mensagem);
          if (res.status === "sucesso") {
            formVeiculo.reset();
          }
        })
        .catch(error => {
          console.error("Erro ao enviar dados:", error);
          alert("Erro ao cadastrar veículo.");
        });
    });
  }
});
