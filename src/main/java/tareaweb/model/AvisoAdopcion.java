package tareaweb.model;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import java.util.ArrayList;
import java.util.List;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;

@Entity
public class AvisoAdopcion {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	private LocalDate fechaPublicacion;
	private String sector;
	private Integer cantidad;
	private String tipo;
	private String edad;
	private String comuna;
	
	@OneToMany(mappedBy = "aviso", cascade = CascadeType.ALL, orphanRemoval = true)
	private List<Nota> notas = new ArrayList<>();
	
	private Double promedioNota;


	public AvisoAdopcion() {
		this.promedioNota = 0.0;
	}
	
	public AvisoAdopcion(Long id, LocalDate fechaPublicacion, String sector, Integer cantidad, String tipo, String edad, String comuna) {
		this.id = id;
		this.fechaPublicacion = fechaPublicacion;
		this.sector = sector;
		this.cantidad = cantidad;
		this.tipo = tipo;
		this.edad = edad;
		this.comuna = comuna;
		this.promedioNota = 0.0;
	}
	
	public Double calcularYActualizarPromedio() {
		if (notas == null || notas.isEmpty()) {
			this.promedioNota = 0.0;
			return 0.0;
		}

		double sumaValores = notas.stream()
			.mapToInt(Nota::getValor)
			.sum();
		
		long cantidadNotas = notas.size();
		
		if (cantidadNotas > 0) {
			BigDecimal promedioBD = BigDecimal.valueOf(sumaValores)
											.divide(BigDecimal.valueOf(cantidadNotas), 2, RoundingMode.HALF_UP);
			this.promedioNota = promedioBD.doubleValue();
		} else {
			this.promedioNota = 0.0;
		}
		
		return this.promedioNota;
	}


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

	public Integer getCantidad() {
		return cantidad;
	}

	public void setCantidad(Integer cantidad) {
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

	public Double getPromedioNota() {
		return promedioNota;
	}

	public void setPromedioNota(Double promedioNota) {
		this.promedioNota = promedioNota;
	}
}