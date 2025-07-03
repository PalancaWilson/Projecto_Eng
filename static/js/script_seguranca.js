document.addEventListener("DOMContentLoaded", () => {
    // 🔵 Dashboard resumo
    fetch("http://localhost:5000/dashboard-seguranca")
      .then(res => res.json())
      .then(data => {
        document.getElementById("total-autorizados").textContent = data.total_autorizados;
        document.getElementById("tentativas-negadas").textContent = data.tentativas_negadas;
        document.getElementById("acessos-hoje").textContent = data.acessos_hoje;
      });
  
    // 🔵 Tabela de últimos acessos
    fetch("http://localhost:5000/ultimos-acessos")
  .then(res => res.json())
  .then(acessos => {
    const tbody = document.getElementById("tabela-acessos");
    tbody.innerHTML = "";

    acessos.forEach(acesso => {
      const linha = document.createElement("tr");

      linha.innerHTML = `
        <td class="py-2">${acesso.hora}</td>
        <td>${acesso.matricula}</td>
        <td>
          <span class="${acesso.estado === 'Autorizado' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'} text-xs px-2 py-1 rounded">
            ${acesso.estado}
          </span>
        </td>
      `;

      tbody.appendChild(linha);
    });
  })
  .catch(err => {
    console.error("Erro ao carregar últimos acessos:", err);
  });
  
    // 🔵 Gráfico de acessos por hora
    fetch("http://localhost:5000/grafico-acessos")
      .then(res => res.json())
      .then(dados => {
        const ctx = document.getElementById("grafico-acessos").getContext("2d");
        const labels = dados.map(d => `${d.hora}:00`);
        const valores = dados.map(d => d.total);
  
        new Chart(ctx, {
          type: "line",
          data: {
            labels: labels,
            datasets: [{
              label: "Acessos",
              data: valores,
              fill: true,
              borderColor: "#3a5af7",
              backgroundColor: "rgba(58, 90, 247, 0.1)",
              tension: 0.4
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                display: false
              }
            }
          }
        });
      });
  });
  