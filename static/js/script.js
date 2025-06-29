document.getElementById('btnEntrar').addEventListener('click', async () => {
  const email = document.getElementById('email').value;
  const senha = document.getElementById('senha').value;
  const tipo = document.querySelector('input[name="tipo"]:checked')?.nextSibling.textContent.trim();

  if (!email || !senha || !tipo) {
    alert("Preencha todos os campos.");
    return;
  }

  try {
    const response = await fetch('http://http://127.0.0.1:8000/ispsecurity/template/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, senha, tipo })
    });

    const result = await response.json();

    if (response.ok) {
      alert("Login bem-sucedido!");
      // Salvar dados do usuário no sessionStorage/localStorage, se desejar
      window.location.href = "dasboard.html";
    } else {
      alert(result.mensagem);
    }

  } catch (error) {
    alert("Erro ao conectar com o servidor.");
    console.error(error);
  }
});