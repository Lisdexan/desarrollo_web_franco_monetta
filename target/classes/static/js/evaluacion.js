function cambiarNota(idAviso) {
	const nuevaNotaString = prompt(`Introduce la nueva nota (1 a 7) para el Aviso ID: ${idAviso}`);

	if (nuevaNotaString === null || nuevaNotaString.trim() === "") {
		return;
	}
	
	const nuevaNota = parseInt(nuevaNotaString, 10);

	if (isNaN(nuevaNota) || nuevaNota < 1 || nuevaNota > 7) {
		alert("Por favor, introduce un número válido entre 1 y 7.");
		return;
	}
	

	fetch('/api/evaluacion/actualizarNota', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json' 
		},
		body: JSON.stringify({
			avisoId: idAviso,
			nota: nuevaNota
			// Se eliminó el envío del campo 'comentario'
		})
	})
	.then(response => {
		if (response.ok) {
			alert(`Nota ${nuevaNota} actualizada para el Aviso ID ${idAviso} con éxito.`);
			window.location.reload(); 
		} else {
			alert("Error al actualizar la nota. Revisa la consola del navegador y la consola del servidor.");
		}
	})
	.catch(error => {
		console.error('Error de red o al procesar la solicitud:', error);
		alert("Error de conexión al servidor. Asegúrate de que el backend esté corriendo.");
	});
}