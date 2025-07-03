document.getElementById("btn-ativar-camera").insertAdjacentHTML("afterend", `
    <button id="btn-capturar" class="bg-green-600 text-white px-4 py-1 rounded ml-4 hover:bg-green-700 transition">Reconhecer Matrícula</button>
  `);
  
  document.getElementById("btn-capturar").addEventListener("click", () => {
    const video = document.getElementById("camera-video");
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
  
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
  
    canvas.toBlob((blob) => {
      const formData = new FormData();
      formData.append("imagem", blob, "frame.jpg");
  
      fetch("http://localhost:5000/reconhecer-matricula", {
        method: "POST",
        body: formData
      })
      .then(res => res.json())
      .then(data => {
        if (data.matricula) {
          alert("Matrícula reconhecida: " + data.matricula);
          // Aqui você pode chamar outra rota para verificar acesso na base de dados
        } else {
          alert("Nenhuma matrícula detectada.");
        }
      })
      .catch(err => {
        console.error("Erro no reconhecimento:", err);
      });
    }, "image/jpeg");
  });
  