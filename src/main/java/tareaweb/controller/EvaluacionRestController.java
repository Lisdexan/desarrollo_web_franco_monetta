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

    // Este endpoint es solo un ejemplo. 
    // Si estás usando el flujo del WebController que redirige con /guardarNota, 
    // este archivo REST puede no ser necesario para tu funcionalidad actual.
    
    // Si necesitas un endpoint REST para actualizar la nota sin refrescar la página, usa este:
    @PostMapping("/actualizarNota")
    public ResponseEntity<?> actualizarNota(@RequestBody Map<String, Object> payload) {
        
        Long idAviso;
        Integer nota;
        
        try {
            idAviso = Long.valueOf(payload.get("avisoId").toString());
            nota = Integer.valueOf(payload.get("nota").toString());
        } catch (Exception e) {
            return new ResponseEntity<>("Datos de entrada inválidos.", HttpStatus.BAD_REQUEST);
        }

        try {
            // Llama al método VOID del servicio. Ya NO espera un valor double de retorno.
            avisoService.guardarYRecalcularNota(idAviso, nota);
            
            // Retorna una respuesta de éxito (HTTP 200 OK)
            return new ResponseEntity<>("Nota actualizada con éxito.", HttpStatus.OK);
            
        } catch (NoSuchElementException e) {
            return new ResponseEntity<>(e.getMessage(), HttpStatus.NOT_FOUND);
        } catch (Exception e) {
            return new ResponseEntity<>("Error al actualizar la nota: " + e.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}