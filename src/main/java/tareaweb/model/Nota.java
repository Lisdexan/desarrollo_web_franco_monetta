package tareaweb.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;

@Entity
public class Nota {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	private Integer valor;

	// El campo 'comentario' ha sido eliminado

	@ManyToOne
	@JoinColumn(name = "aviso_adopcion_id")
	private AvisoAdopcion aviso;

	public Nota() {}
	
	public Nota(AvisoAdopcion aviso, Integer valor) {
		this.aviso = aviso;
		this.valor = valor;
	}


	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public Integer getValor() {
		return valor;
	}

	public void setValor(Integer valor) {
		this.valor = valor;
	}

	public AvisoAdopcion getAviso() {
		return aviso;
	}

	public void setAviso(AvisoAdopcion aviso) {
		this.aviso = aviso;
	}
}