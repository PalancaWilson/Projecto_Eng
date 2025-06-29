document.addEventListener('DOMContentLoaded', function () {
  const btnEntrar = document.getElementById('btnEntrar');

  btnEntrar.addEventListener('click', function () {
    const email = document.getElementById('email').value.trim();
    const senha = document.getElementById('senha').value.trim();
    const tipoSelecionado = document.querySelector('input[name="tipo"]:checked');

    // Validação básica
    if (!email || !senha || !tipoSelecionado) {
      alert('Por favor, preencha todos os campos e selecione o tipo de usuário.');
      return;
    }

    const tipo = tipoSelecionado.parentElement.textContent.trim(); // Pega "Administrador" ou "Segurança"

    const dados = {
      email: email,
      senha: senha,
      tipo: tipo
    };

    // Chamada à API Python (Flask)
    fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dados)
    })
    .then(response => response.json())
    .then(resposta => {
      if (resposta.status === 'sucesso') {
        alert('Login bem-sucedido! Redirecionando...');

        // Redireciona com base no tipo de usuário
        if (tipo === 'Administrador') {
          window.location.href = '../template/dasboard.html';
        } else if (tipo === 'Seguranca') {
          window.location.href = '../template/dashboard_seguranca.html';
        } else {
          alert('Tipo de usuário inválido!');
        }
      } else {
        alert('Erro: ' + resposta.mensagem);
      }
    })
    .catch(error => {
      console.error('Erro ao conectar com o servidor:', error);
      alert('Erro de conexão com o servidor. Verifique se o backend está em execução.');
    });
  });
});





  // Dasbord 

  document.addEventListener('DOMContentLoaded', () => {
    // FUNÇÃO DE LOGOUT
    const logoutBtn = document.getElementById('logout');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', () => {
        const confirmar = confirm("Deseja realmente encerrar a sessão?");
        if (confirmar) {
          window.location.href = "index.html"; // Redireciona para tela de login
        }
      });
    }
  
    // SIMULAÇÃO DE VALORES DOS CARDS
    const valores = document.querySelectorAll('.card .valor');
    if (valores.length === 4) {
      valores[0].textContent = Math.floor(Math.random() * 500 + 200);  // Veículos autorizados
      valores[1].textContent = Math.floor(Math.random() * 50);         // Tentativas negadas
      valores[2].textContent = Math.floor(Math.random() * 200 + 50);   // Acessos do dia
      valores[3].textContent = Math.floor(Math.random() * 30);         // Sincronizações pendentes
    }
  });
  