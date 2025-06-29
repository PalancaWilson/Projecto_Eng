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
          } else if (tipo === "Segurança") {
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

  // CADASTRO DE VEÍCULO
  const formVeiculo = document.getElementById("formVeiculo");
  if (formVeiculo) {
    formVeiculo.addEventListener("submit", function (e) {
      e.preventDefault();

      const dados = {
        matricula: document.getElementById("matricula").value.trim(),
        proprietario: document.getElementById("proprietario").value.trim(),
        tipo_usuario: document.getElementById("tipo").value,
        validade: document.getElementById("validade").value
      };

      if (!dados.matricula || !dados.proprietario || !dados.tipo_usuario || !dados.validade) {
        alert("Todos os campos devem ser preenchidos.");
        return;
      }

      fetch("http://localhost:5000/cadastrar-veiculo", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(dados)
      })
      .then(response => response.json())
      .then(resposta => {
        alert(resposta.mensagem);
        if (resposta.status === "sucesso") {
          document.getElementById("formVeiculo").reset();
        }
      })
      .catch(error => {
        console.error("Erro ao cadastrar:", error);
        alert("Erro ao conectar com o servidor.");
      });
    });
  }

});