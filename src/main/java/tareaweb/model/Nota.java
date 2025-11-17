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

	// Campo que almacena el valor de la nota (e.g., de 1 a 7)
	private Integer valor;

	// Añadimos un campo para el tercer argumento si es un String
	private String comentario;

	// Este campo 'aviso' es el que es referenciado por el mappedBy="aviso" en AvisoAdopcion.java
	@ManyToOne
	// Se cambia el nombre de la columna a 'aviso_adopcion_id' para que coincida con los scripts SQL (si existen).
	@JoinColumn(name = "aviso_adopcion_id") 
	private AvisoAdopcion aviso;

	public Nota() {}
	
	public Nota(AvisoAdopcion aviso, Integer valor, String comentario) {
		this.aviso = aviso;
		this.valor = valor;
		this.comentario = comentario;
	}


	// --- Getters y Setters ---

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	/**
	 * Este método es usado por AvisoAdopcion.getNotaPromedio() para calcular el promedio.
	 */
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
	
	public String getComentario() {
		return comentario;
	}

	public void setComentario(String comentario) {
		this.comentario = comentario;
	}
}