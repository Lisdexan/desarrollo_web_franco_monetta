package tareaweb.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import tareaweb.service.AvisoService;

@Controller
@RequestMapping("/")
public class EvaluacionWebController {

	@Autowired
	private AvisoService avisoService;

	@GetMapping({"/", "/evaluar_avisos"})
	public String listarAvisos(Model model) {
		model.addAttribute("avisos", avisoService.listarTodos());
		return "avisoleaf";
	}

	@GetMapping("/guardarNota")
	public String guardarNota(@RequestParam("avisoId") Long avisoId, @RequestParam("nota") Integer nota) {
		
		// Llamada al servicio sin el parámetro de comentario
		avisoService.asignarNotaYAplicarPromedio(avisoId, nota);
		
		return "redirect:http://127.0.0.1:8080/evaluar_avisos";
	}
}