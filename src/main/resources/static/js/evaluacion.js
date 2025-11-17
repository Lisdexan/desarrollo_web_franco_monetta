/**
 * evalucion.js: Función para manejar el clic en el botón "evaluar".
 * Envía la nota ingresada al EvaluacionRestController a través de una solicitud POST JSON.
 */
function cambiarNota(idAviso) {
	// 1. Mostrar un diálogo para que el usuario ingrese la nota.
	const nuevaNotaString = prompt(`Introduce la nueva nota (1 a 7) para el Aviso ID: ${idAviso}`);

	if (nuevaNotaString === null || nuevaNotaString.trim() === "") {
		console.log("Evaluación cancelada.");
		return;
	}
	
	// 2. Validar y convertir la nota a número.
	const nuevaNota = parseInt(nuevaNotaString, 10);

	if (isNaN(nuevaNota) || nuevaNota < 1 || nuevaNota > 7) {
		alert("Por favor, introduce un número válido entre 1 y 7.");
		return;
	}
	
	// 3. Realiza la llamada FETCH al controlador REST, enviando el JSON esperado
	fetch('/api/evaluacion/actualizarNota', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json' 
		},
		// Enviar el cuerpo de la solicitud como JSON (compatible con @RequestBody en Java)
		body: JSON.stringify({
			avisoId: idAviso, 
			nota: nuevaNota   
		})
	})
	.then(response => {
		if (response.ok) {
			// Éxito: El servidor respondió con 200 OK
			alert(`Nota ${nuevaNota} actualizada para el Aviso ID ${idAviso} con éxito.`);
			// Recargar la página para ver la nota actualizada en la tabla
			window.location.reload(); 
		} else {
			// Error en el servidor (4xx o 5xx)
			alert("Error al actualizar la nota. Revisa la consola del navegador y la consola del servidor.");
		}
	})
	.catch(error => {
		console.error('Error de red o al procesar la solicitud:', error);
		alert("Error de conexión al servidor. Asegúrate de que el backend esté corriendo.");
	});
}