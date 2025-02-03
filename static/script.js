document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("gastoForm").addEventListener("submit", function (event) {
        event.preventDefault();

        const mes = document.getElementById("mes").value;
        const categoria = document.getElementById("categoria").value;
        const descripcion = document.getElementById("descripcion").value;
        const valor_euros = document.getElementById("valor").value;

        if (!descripcion || !valor_euros) {
            mostrarMensaje("Por favor completa todos los campos.", "danger");
            return;
        }

        fetch("/agregar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mes, categoria, descripcion, valor_euros })
        })
        .then(response => response.json())
        .then(data => {
            mostrarMensaje(data.mensaje, "success");
            document.getElementById("gastoForm").reset();
        })
        .catch(error => {
            mostrarMensaje("Error al registrar gasto.", "danger");
        });
    });
});

function mostrarMensaje(mensaje, tipo) {
    const mensajeDiv = document.getElementById("mensaje");
    mensajeDiv.innerHTML = `<div class="alert alert-${tipo}">${mensaje}</div>`;
    setTimeout(() => { mensajeDiv.innerHTML = ""; }, 3000);
}