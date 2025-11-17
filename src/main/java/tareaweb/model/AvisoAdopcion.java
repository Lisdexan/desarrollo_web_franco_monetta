package tareaweb.model; 

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Transient;
import java.time.LocalDate;
import java.util.List;

@Entity
public class AvisoAdopcion {

	@Id
	private Long id;

	@Column(name = "fecha_publicacion")
	private LocalDate fechaPublicacion;

	private String sector;

	private int cantidad;

	private String tipo;

	private String edad; 

	private String comuna;
	
	// ******* CAMBIO CLAVE 1: RELACIÓN CON NOTAS *******
	@OneToMany(mappedBy = "aviso") 
	private List<Nota> notas;

	public AvisoAdopcion() {}
	
	// ******* CAMBIO CLAVE 2: MÉTODO getNotaPromedio() *******
	/**
	 * Calcula la nota promedio basada en las notas relacionadas.
	 * Este método es llamado por Thymeleaf como ${aviso.notaPromedio}.
	 */
	@Transient
	public Double getNotaPromedio() {
		if (this.notas == null || this.notas.isEmpty()) {
			return null;
		}
		
		double suma = 0.0;
		// Asume que la entidad Nota tiene un método getValor() que retorna la nota (int/double)
		for (Nota nota : this.notas) { 
			suma += nota.getValor(); 
		}
		
		return suma / this.notas.size();
	}


	// --- Getters and Setters existentes (se mantienen) ---

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public LocalDate getFechaPublicacion() {
		return fechaPublicacion;
	}

	public void setFechaPublicacion(LocalDate fechaPublicacion) {
		this.fechaPublicacion = fechaPublicacion;
	}

	public String getSector() {
		return sector;
	}

	public void setSector(String sector) {
		this.sector = sector;
	}

	public int getCantidad() {
		return cantidad;
	}

	public void setCantidad(int cantidad) {
		this.cantidad = cantidad;
	}

	public String getTipo() {
		return tipo;
	}

	public void setTipo(String tipo) {
		this.tipo = tipo;
	}

	public String getEdad() {
		return edad;
	}

	public void setEdad(String edad) {
		this.edad = edad;
	}

	public String getComuna() {
		return comuna;
	}

	public void setComuna(String comuna) {
		this.comuna = comuna;
	}
	
	public List<Nota> getNotas() {
		return notas;
	}

	public void setNotas(List<Nota> notas) {
		this.notas = notas;
	}
}