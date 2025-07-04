// === 📤 Función principal para subir el archivo CSV al backend ===
async function subir() {
  // 📌 Referencia al input de archivo
  const fileInput = document.getElementById('csvFile');
  const file = fileInput.files[0];

  // ⚠️ Validación: si no se seleccionó archivo, mostramos alerta
  if (!file) {
    alert("Por favor selecciona un archivo CSV.");
    return;
  }

  // 📦 Creamos un FormData para enviar el archivo como multipart/form-data
  const formData = new FormData();
  formData.append("file", file);

  try {
    // 🚀 Enviamos el archivo al endpoint /upload usando fetch
    const response = await fetch("/upload", {
      method: "POST",
      body: formData
    });

    // 📬 Interpretamos la respuesta como JSON
    const data = await response.json();

    // ✅ Mostramos el mensaje de éxito o error en pantalla
    document.getElementById("mensaje").innerText = data.mensaje || data.error;

  } catch (error) {
    // ❌ Si ocurre un error de red o fetch, lo mostramos
    document.getElementById("mensaje").innerText = "Error al subir el archivo.";
  }
}
