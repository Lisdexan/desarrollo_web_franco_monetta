package tareaweb.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tareaweb.model.AvisoAdopcion;
import tareaweb.model.Nota;
import tareaweb.repository.AvisoAdopcionRepository;
import tareaweb.repository.NotaRepository; 

import java.util.List;
import java.util.NoSuchElementException;

@Service
public class AvisoService {

    @Autowired
    private AvisoAdopcionRepository avisoRepository; 
    
    @Autowired
    private NotaRepository notaRepository; 

    @Transactional(readOnly = true)
    public List<AvisoAdopcion> listarTodos() {
        return avisoRepository.findAll();
    }
    
    @Transactional(readOnly = true)
    public AvisoAdopcion obtenerAvisoPorId(Long id) {
        return avisoRepository.findById(id)
                .orElseThrow(() -> new NoSuchElementException("Aviso no encontrado con ID: " + id));
    }

    @Transactional
    public void guardarYRecalcularNota(Long idAviso, Integer valorNota) {
        AvisoAdopcion aviso = obtenerAvisoPorId(idAviso);
        
        // 1. ELIMINAR TODAS LAS NOTAS PREVIAS usando el nuevo método explícito
        notaRepository.eliminarNotasPorAvisoId(idAviso);
        
        // 2. Crear y guardar la nueva nota (será la única)
        Nota nuevaNota = new Nota(aviso, valorNota, "Evaluador_Web"); 
        notaRepository.save(nuevaNota);
    }
}