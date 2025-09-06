const avisos = [
  {
    fechaPublicacion: "2025-09-01",
    fechaEntrega: "2025-09-10",
    comuna: "Providencia",
    sector: "Centro",
    cantidad: 1,
    tipo: "Perro",
    edad: "2 años",
    nombre: "Julian",
    contacto: "Whatsapp +56912345678",
    fotos: [
      "../fof/firulais1.jpg",
      "../fof/firulais2.jpg"
    ]
  },
  {
    fechaPublicacion: "2025-08-25",
    fechaEntrega: "2025-09-05",
    comuna: "Ñuñoa",
    sector: "Parque",
    cantidad: 2,
    tipo: "Gato",
    edad: "6 meses",
    nombre: "Lucas",
    contacto: "Telegram @michiluna",
    fotos: [
      "../fof/michi1.jpg",
      "../fof/michi2.jpg"
    ]
  },
  {
    fechaPublicacion: "2025-08-30",
    fechaEntrega: "2025-09-15",
    comuna: "Las Condes",
    sector: "Valle",
    cantidad: 1,
    tipo: "Perro",
    edad: "4 años",
    nombre: "Anna",
    contacto: "Instagram @rex_adopcion",
    fotos: [
      "../fof/perrobroken.jpg"
    ]
  },
  {
    fechaPublicacion: "2025-09-02",
    fechaEntrega: "2025-09-12",
    comuna: "Santiago Centro",
    sector: "Bellas Artes",
    cantidad: 1,
    tipo: "Gato",
    edad: "1 año",
    nombre: "Nala",
    contacto: "X @nala_gato",
    fotos: [
      "../fof/larry.jpg",
      "../fof/gatobroken.jpg"
    ]
  },
  {
    fechaPublicacion: "2025-09-03",
    fechaEntrega: "2025-09-20",
    comuna: "Maipú",
    sector: "Villa",
    cantidad: 3,
    tipo: "Perro",
    edad: "3 meses",
    nombre: "Bruno",
    contacto: "Whatsapp +56998765432",
    fotos: [
      "../fof/3perritous.jpg",
    ]
  }
];

// Generar tabla
const tbody = document.querySelector("#tabla-avisos tbody");

avisos.forEach((aviso, i) => {
  const tr = document.createElement("tr");
  tr.innerHTML = `
    <td>${aviso.fechaPublicacion}</td>
    <td>${aviso.fechaEntrega}</td>
    <td>${aviso.comuna}</td>
    <td>${aviso.sector}</td>
    <td>${aviso.cantidad}</td>
    <td>${aviso.tipo}</td>
    <td>${aviso.edad}</td>
    <td>${aviso.nombre}</td>
    <td>${aviso.contacto}</td>
    <td>${aviso.fotos.length}</td>
  `;
  tr.addEventListener("click", () => mostrarDetalle(i));
  tbody.appendChild(tr);
});

// Mostrar detalle
function mostrarDetalle(index) {
  const aviso = avisos[index];
  document.getElementById("listado-container").style.display = "none";
  const detalle = document.getElementById("detalle-container");
  detalle.style.display = "block";

  document.getElementById("detalle-nombre").innerText = aviso.nombre;
  document.getElementById("detalle-tipo").innerText = aviso.tipo;
  document.getElementById("detalle-edad").innerText = aviso.edad;
  document.getElementById("detalle-comuna").innerText = aviso.comuna;
  document.getElementById("detalle-sector").innerText = aviso.sector;
  document.getElementById("detalle-cantidad").innerText = aviso.cantidad;
  document.getElementById("detalle-contacto").innerText = aviso.contacto;
  document.getElementById("detalle-fechapub").innerText = aviso.fechaPublicacion;
  document.getElementById("detalle-fechaent").innerText = aviso.fechaEntrega;

  const fotosDiv = document.getElementById("detalle-fotos");
  fotosDiv.innerHTML = "";
  aviso.fotos.forEach(url => {
    const img = document.createElement("img");
    img.src = url;
    img.addEventListener("click", () => mostrarFotoGrande(url));
    fotosDiv.appendChild(img);
  });
}

// Volver al listado
document.getElementById("volver-listado").addEventListener("click", () => {
  document.getElementById("detalle-container").style.display = "none";
  document.getElementById("listado-container").style.display = "block";
});

// Volver a portada
document.getElementById("volver-portada").addEventListener("click", () => {
  window.location.href = "../html/main.html";
});

// Fotos grandes
function mostrarFotoGrande(url) {
  document.getElementById("img-grande").src = url;
  document.getElementById("foto-grande").style.display = "block";
}

document.getElementById("cerrar-foto").addEventListener("click", () => {
  document.getElementById("foto-grande").style.display = "none";
});
