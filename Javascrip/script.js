// script.js

// Lógica da página de login
document.addEventListener("DOMContentLoaded", function () {
    const btnEntrar = document.getElementById("btnEntrar");
    const logoutBtn = document.getElementById("logout");
  
    // Página de login
    if (btnEntrar) {
      btnEntrar.addEventListener("click", function (e) {
        e.preventDefault();
        const email = document.getElementById("email").value.trim();
        const senha = document.getElementById("senha").value.trim();
  
        if (email === "" || senha === "") {
          alert("Por favor, preencha todos os campos.");
          return;
        }
  
        // Simulação de autenticação (em produção, substituir por backend real)
        if (email === "admin@isptec.co.ao" && senha === "1234") {
          alert("Login bem-sucedido!");
          window.location.href = "dasbord.html";
        } else {
          alert("Credenciais inválidas. Tente novamente.");
        }
      });
    }
  
    // Página de dashboard
    if (logoutBtn) {
      logoutBtn.addEventListener("click", function () {
        const confirmar = confirm("Deseja realmente sair?");
        if (confirmar) {
          window.location.href = "index.html";
        }
      });
    }
  });
  