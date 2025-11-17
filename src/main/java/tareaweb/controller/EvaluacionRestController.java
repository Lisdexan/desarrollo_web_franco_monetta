package tareaweb.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import tareaweb.service.AvisoService;

import java.util.Map;
import java.util.NoSuchElementException;

@RestController
@RequestMapping("/api/evaluacion")
public class EvaluacionRestController {

	@Autowired
	private AvisoService avisoService;

	@PostMapping("/actualizarNota")
	public ResponseEntity<?> actualizarNota(@RequestBody Map<String, Object> payload) {
		
		Long idAviso;
		Integer nota;

		try {
			idAviso = Long.valueOf(payload.get("avisoId").toString());
			nota = Integer.valueOf(payload.get("nota").toString());
			// Se eliminó la variable y extracción del campo 'comentario'
		} catch (Exception e) {
			return new ResponseEntity<>("Datos de entrada inválidos (se requiere avisoId y nota).", HttpStatus.BAD_REQUEST);
		}

		try {
			// Se llama al servicio sin el comentario
			avisoService.asignarNotaYAplicarPromedio(idAviso, nota);
			
			return new ResponseEntity<>("Nota guardada con éxito.", HttpStatus.OK);
			
		} catch (NoSuchElementException e) {
			return new ResponseEntity<>("Error: Aviso no encontrado.", HttpStatus.NOT_FOUND);
		} catch (Exception e) {
			return new ResponseEntity<>("Error interno al actualizar la nota: " + e.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
		}
	}
}