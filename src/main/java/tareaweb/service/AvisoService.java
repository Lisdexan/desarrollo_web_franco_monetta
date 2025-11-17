package tareaweb.service;

import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import jakarta.transaction.Transactional;

import tareaweb.model.AvisoAdopcion;
import tareaweb.model.Nota;
import tareaweb.repository.AvisoRepository;
import tareaweb.repository.NotaRepository;

@Service
public class AvisoService {

	@Autowired
	private AvisoRepository avisoRepository;
	
	@Autowired
	private NotaRepository notaRepository;
	
	public List<AvisoAdopcion> listarTodos() {
		return avisoRepository.findAll();
	}

	@Transactional
	
	public AvisoAdopcion asignarNotaYAplicarPromedio(Long avisoId, Integer valorNota) {
		Optional<AvisoAdopcion> avisoOpt = avisoRepository.findById(avisoId);
		
		if (avisoOpt.isEmpty()) {
			throw new RuntimeException("AvisoAdopcion con ID " + avisoId + " no encontrado.");
		}
		
		AvisoAdopcion aviso = avisoOpt.get();
		
		
		Nota nuevaNota = new Nota(aviso, valorNota);
		
		notaRepository.save(nuevaNota);
		
        if (!aviso.getNotas().contains(nuevaNota)) {
            aviso.getNotas().add(nuevaNota);
        }
		
		aviso.calcularYActualizarPromedio();
		
		return avisoRepository.save(aviso);
	}
}