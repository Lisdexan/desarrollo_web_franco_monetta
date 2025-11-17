package tareaweb.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import tareaweb.model.Nota;

@Repository
public interface NotaRepository extends JpaRepository<Nota, Long> {

}