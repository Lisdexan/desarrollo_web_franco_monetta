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

    // Cuando el navegador accede a la lista, lo redirigimos a la URL completa para asegurarnos de que el puerto sea 8080
    @GetMapping({"/", "/evaluar_avisos"})
    public String listarAvisos(Model model) {
        model.addAttribute("avisos", avisoService.listarTodos());
        return "avisoleaf";
    }

    @GetMapping("/guardarNota")
    public String guardarNota(@RequestParam("avisoId") Long avisoId, @RequestParam("nota") Integer nota) {
        
        avisoService.guardarYRecalcularNota(avisoId, nota);
        
        // Redirección ABSOLUTA para que, después de guardar, siempre regrese a 8080.
        return "redirect:http://127.0.0.1:8080/evaluar_avisos";
    }
}