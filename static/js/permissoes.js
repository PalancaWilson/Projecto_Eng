document.addEventListener('DOMContentLoaded', () => {
  const inputBusca = document.querySelector('input[type="text"]');
  const infoMatricula = document.querySelector('.matricula-info');
  const form = document.querySelector('.formulario');

  let permissaoSelecionada = null;

  // 🔍 Função para buscar permissão pela matrícula
  function buscarPermissaoPorMatricula(matriculaBruta) {
    const valor = matriculaBruta.trim().replace(/\s+/g, '').toUpperCase();

    fetch('http://localhost:5000/api/permissoes')
      .then(res => res.json())
      .then(permissoes => {
        const p = permissoes.find(p =>
          p.matricula.replace(/\s+/g, '').toUpperCase() === valor
        );

        if (!p) {
          alert('Matrícula não encontrada.');
          return;
        }

        permissaoSelecionada = p;

        // Preencher info da matrícula
        infoMatricula.innerHTML = `
          <h2>${p.matricula}</h2>
          <p>${p.proprietario}</p>
        `;

        // Habilitar inputs e preencher dados existentes
        form.querySelectorAll('input, select').forEach(el => el.disabled = false);
        form.querySelector('input[placeholder*="DD"]').value = p.validade;
        form.querySelectorAll('select')[0].value = p.horario_acesso;
        form.querySelectorAll('select')[1].value = p.tipo_usuario;
      })
      .catch(err => {
        console.error('Erro ao buscar permissões:', err);
        alert('Erro ao comunicar com o servidor.');
      });
  }

  // 💾 Submeter alteração de permissão
  document.querySelector('button[type="submit"]').addEventListener('click', e => {
    e.preventDefault();
    if (!permissaoSelecionada) {
      alert("Nenhuma permissão selecionada.");
      return;
    }

    const novaValidade = form.querySelector('input').value;
    const novoHorario = form.querySelectorAll('select')[0].value;
    const novoTipo = form.querySelectorAll('select')[1].value;

    fetch(`http://localhost:5000/api/permissoes/${permissaoSelecionada.id_permissao}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        validade: novaValidade,
        horario_acesso: novoHorario,
        tipo_usuario: novoTipo
      })
    })
    .then(res => res.json())
    .then(resp => {
      alert(resp.mensagem || 'Permissão atualizada!');
    })
    .catch(err => {
      console.error('Erro ao atualizar permissão:', err);
      alert('Erro ao salvar alterações.');
    });
  });

  // 🔎 Evento de clique para buscar a matrícula
  document.querySelector('button.bg-blue-600').addEventListener('click', () => {
    const matricula = inputBusca.value;
    if (matricula) buscarPermissaoPorMatricula(matricula);
  });
});
