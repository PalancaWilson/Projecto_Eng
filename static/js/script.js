

// Executa quando o DOM é carregado
document.addEventListener('DOMContentLoaded', () => {
  // --- LOGIN ---
  const btnEntrar = document.getElementById('btnEntrar');
  if (btnEntrar) {
    btnEntrar.addEventListener('click', async () => {
      const email = document.getElementById('email')?.value.trim();
      const senha = document.getElementById('senha')?.value.trim();
      const tipoRadio = document.querySelector('input[name="tipo"]:checked');

      if (!email || !senha || !tipoRadio) {
        alert("Preencha todos os campos.");
        return;
      }

      const tipo = tipoRadio.value;

      try {
        const res = await fetch('http://127.0.0.1:5000/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, senha, tipo })
        });

        const result = await res.json();

        if (res.ok && result.status === "sucesso") {
          sessionStorage.setItem("usuario", JSON.stringify(result.usuario));

          if (tipo === "Administrador") {
            window.location.href = "dasbord.html";
          } else if (tipo.toLowerCase() === "seguranca" || tipo.toLowerCase() === "segurança") {
            window.location.href = "dashboard_seguranca.html";
          } else {
            alert("Tipo de usuário inválido.");
          }
        } else {
          alert(result.mensagem || "Credenciais inválidas.");
        }

      } catch (error) {
        console.error(error);
        alert("Erro ao conectar com o servidor.");
      }
    });
  }

  // --- LOGOUT ---
  const logoutBtn = document.getElementById("logout");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      if (confirm("Deseja realmente sair?")) {
        sessionStorage.clear();
        window.location.href = "../template/index.html";
      }
    });
  }

  // --- HISTÓRICO DE ACESSOS ---
  const tbody = document.getElementById("acessosTableBody");
  if (tbody) carregarAcessos();

  function carregarAcessos(filtro = "") {
    let url = "http://127.0.0.1:5000/api/historico";
    if (filtro) url += "?" + filtro;

    fetch(url)
      .then(res => res.json())
      .then(dados => {
        tbody.innerHTML = "";

        if (!Array.isArray(dados) || dados.length === 0) {
          tbody.innerHTML = '<tr><td colspan="6" class="text-center text-gray-500 py-4">Nenhum acesso encontrado.</td></tr>';
          return;
        }

        dados.forEach(acesso => {
          const tr = document.createElement("tr");
          tr.classList.add("bg-gray-50");

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
            </td>`;

          tbody.appendChild(tr);
        });
      })
      .catch(err => {
        console.error("Erro ao carregar acessos:", err);
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-red-500 py-4">Erro ao carregar acessos.</td></tr>';
      });
  }

  // Busca dinâmica
  const campoBusca = document.querySelector("input[placeholder*='matrícula']");
  if (campoBusca) {
    campoBusca.addEventListener("input", () => {
      const valor = campoBusca.value.trim();
      carregarAcessos(valor ? "busca=" + encodeURIComponent(valor) : "");
    });
  }

  // --- DASHBOARD ---
  if (document.getElementById("totalVeiculos")) {
    fetch("http://127.0.0.1:5000/dashboard-data")
      .then(r => r.json())
      .then(d => {
        document.getElementById("totalVeiculos").textContent = d.total_veiculos;
        document.getElementById("tentativasNegadas").textContent = d.recusados;
        document.getElementById("acessosDia").textContent = d.acessos_dia;
        document.getElementById("pendencias").textContent = d.pendentes;
      });

    fetch("http://localhost:5000/ultimos-acessos")
      .then(res => res.json())
      .then(acessos => {
        const tbody = document.getElementById("tabela-acessos");
        tbody.innerHTML = "";

        acessos.forEach(acesso => {
          const tr = document.createElement("tr");
          tr.innerHTML = `
            <td class="py-2">${acesso.hora}</td>
            <td>${acesso.matricula}</td>
            <td><span class="${acesso.estado === 'Autorizado' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'} text-xs px-2 py-1 rounded">${acesso.estado}</span></td>`;
          tbody.appendChild(tr);
        });
      });

    fetch("http://localhost:5000/grafico-acessos")
      .then(res => res.json())
      .then(dados => {
        const ctx = document.getElementById("grafico-acessos").getContext("2d");
        const labels = dados.map(d => `${d.hora}:00`);
        const valores = dados.map(d => d.total);

        new Chart(ctx, {
          type: "line",
          data: {
            labels,
            datasets: [{
              label: "Acessos",
              data: valores,
              fill: true,
              borderColor: "#3a5af7",
              backgroundColor: "rgba(58, 90, 247, 0.1)",
              tension: 0.4
            }]
          },
          options: { responsive: true, plugins: { legend: { display: false } } }
        });
      });
  }

  // --- CADASTRO VEÍCULO ---
  const formVeiculo = document.getElementById("formCadastroVeiculo");
  const selectTipoUsuario = document.getElementById("tipo_usuario");

  if (selectTipoUsuario) {
    fetch("http://localhost:5000/frequentadores")
      .then(res => res.json())
      .then(data => {
        data.forEach(f => {
          const opt = document.createElement("option");
          opt.value = f.id_frequentador;
          opt.textContent = `${f.nome} (${f.tipo})`;
          selectTipoUsuario.appendChild(opt);
        });
      });
  }

  if (formVeiculo) {
    formVeiculo.addEventListener("submit", e => {
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
        .then(r => r.json())
        .then(res => {
          alert(res.mensagem);
          if (res.status === "sucesso") {
            formVeiculo.reset();
          }
        });
    });
  }
});
