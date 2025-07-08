document.addEventListener("DOMContentLoaded", () => {
  const btnAtivarCamera = document.getElementById("btn-ativar-camera");
  const btnCapturarFoto = document.getElementById("btn-capturar-foto");
  const video = document.getElementById("camera-video");
  const canvas = document.getElementById("canvas-preview");
  const ctx = canvas.getContext("2d");
  const resultado = document.getElementById("resultado-analise");
  const matriculaSpan = document.getElementById("matricula-analisada");
  const estadoSpan = document.getElementById("estado-analisado");
  const imagemCapturada = document.getElementById("imagem-capturada");

  let stream;

  btnAtivarCamera.addEventListener("click", async () => {
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: true });
      video.srcObject = stream;

      video.addEventListener("loadedmetadata", () => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
      });

      btnAtivarCamera.disabled = true;
      btnCapturarFoto.disabled = false;
      btnAtivarCamera.textContent = "Câmera Ativada";
    } catch (err) {
      alert("Erro ao acessar a câmera: " + err.message);
    }
  });

  btnCapturarFoto.addEventListener("click", () => {
    if (!stream) {
      alert("Câmera não ativada.");
      return;
    }

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.classList.remove("hidden");

    canvas.toBlob((blob) => {
      if (!blob) {
        alert("Erro ao capturar imagem.");
        return;
      }
      console.log("Blob gerado:", blob); // <-- Adicione isso
      const formData = new FormData();
      formData.append("imagem", blob, "captura.jpg");

      fetch("http://127.0.0.1:5000/reconhecer-matricula", {
        method: "POST",
        body: formData,
      })
        .then(async (res) => {
          const contentType = res.headers.get("Content-Type");

          if (!res.ok) {
            const erroTexto = await res.text();
            console.error("Erro do servidor:", erroTexto);
            throw new Error("Erro ao processar imagem");
          }

          if (contentType && contentType.includes("application/json")) {
            return res.json();
          } else {
            throw new Error("Resposta do servidor não é JSON.");
          }
        })
        .then((data) => {
          console.log("Resposta do servidor:", data);

          if (data.status && data.matricula) {
            resultado.classList.remove("hidden");
            matriculaSpan.textContent = data.matricula;
            estadoSpan.textContent = data.status;

            estadoSpan.classList.remove("text-green-700", "text-red-700");
            estadoSpan.classList.add(
              data.status === "Autorizado" ? "text-green-700" : "text-red-700"
            );

            imagemCapturada.src = canvas.toDataURL("image/jpeg");
          } else {
            alert("Nenhuma matrícula detectada.");
          }
        })
        .catch((err) => {
          console.error("Erro ao enviar imagem:", err);
          alert("Erro ao enviar imagem para o servidor.");
        });
    }, "image/jpeg");
  });

  const logoutBtn = document.getElementById("logout");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      if (confirm("Deseja realmente sair?")) {
        window.location.href = "../template/index.html";
      }
    });
  }
});
