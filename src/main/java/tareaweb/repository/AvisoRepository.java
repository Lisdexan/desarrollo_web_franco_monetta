package tareaweb.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import tareaweb.model.AvisoAdopcion;

@Repository
public interface AvisoRepository extends JpaRepository<AvisoAdopcion, Long> {

}