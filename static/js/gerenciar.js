document.addEventListener('DOMContentLoaded', function () {
    const tabela = document.getElementById('acessosTableBody');
    const campoPesquisa = document.getElementById('campoPesquisa');
  
    function carregarHistorico(filtro = '') {
      fetch(`http://localhost:5000/api/historico?busca=${filtro}`)
        .then(res => res.json())
        .then(data => {
          const tabela = document.getElementById('acessosTableBody');
          tabela.innerHTML = '';
          data.forEach(acesso => {
            const linha = document.createElement('tr');
            linha.innerHTML = `
              <td class="px-4 py-2">${acesso.matricula}</td>
              <td class="px-4 py-2">${acesso.data_acesso}</td>
              <td class="px-4 py-2">${acesso.tipo_usuario}</td>
              <td class="px-4 py-2">${acesso.estado}</td>
              <td class="px-4 py-2">
                <button onclick="removerAcesso(${acesso.id_acesso})" class="bg-red-500 text-white px-2 py-1 rounded">
                  Remover
                </button>
              </td>
            `;
            tabela.appendChild(linha);
          });
        });
    }
  
    
    campoPesquisa.addEventListener('input', () => carregarHistorico(campoPesquisa.value));
    carregarHistorico(); // inicial
  });
  
  function abrirModalAcesso() {
    document.getElementById('modalAcesso').classList.remove('hidden');
  }
  function fecharModalAcesso() {
    document.getElementById('modalAcesso').classList.add('hidden');
  }
  
  function submeterAcesso() {
    const idCarro = document.getElementById('inputIdCarro').value;
    const tipoFrequentador = document.getElementById('inputTipoFrequentador').value;
    const estado = document.getElementById('inputEstado').value;
  
    fetch('http://localhost:5000/api/acessos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id_carro: idCarro, tipo_frequentador: tipoFrequentador, estado })
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'sucesso') {
          fecharModalAcesso();
          alert('Acesso inserido!');
          document.getElementById('campoPesquisa').value = '';
          carregarHistorico();
        } else {
          alert('Erro: ' + data.mensagem);
        }
      });
  }
  
  function removerAcesso(idAcesso) {
    if (!confirm('Deseja remover este acesso?')) return;
  
    fetch(`http://localhost:5000/api/acessos/${idAcesso}`, {
      method: 'DELETE'
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'sucesso') {
          alert('Removido com sucesso!');
          carregarHistorico(); // <-- Agora está acessível
        } else {
          alert('Erro: ' + data.mensagem);
        }
      });
  }