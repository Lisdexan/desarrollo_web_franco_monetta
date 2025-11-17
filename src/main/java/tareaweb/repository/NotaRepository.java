package tareaweb.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import jakarta.transaction.Transactional;
import tareaweb.model.Nota;

@Repository
public interface NotaRepository extends JpaRepository<Nota, Long> {

	/**
	 * Método para eliminar todas las notas asociadas a un AvisoAdopcion específico.
	 * * Se utiliza @Query y JPQL explícito para evitar el error de validación
	 * causado por la convención automática de Spring Data JPA. El campo
	 * de relación en la entidad Nota se llama 'aviso', no 'avisoAdopcion'.
	 * * @param avisoId El ID del AvisoAdopcion cuyas notas se eliminarán.
	 */
	@Modifying
	@Transactional
	@Query("DELETE FROM Nota n WHERE n.aviso.id = :avisoId")
	void eliminarNotasPorAvisoId(@Param("avisoId") Long avisoId);
}