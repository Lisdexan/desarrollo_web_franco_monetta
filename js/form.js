const contacttypes = ["Whatsapp", "Telegram", "X","Instagram","TikTok", "Otra"];

const volver = () => {
    window.location.href = "../html/main.html";
} 

document.getElementById("backtomain").addEventListener("click", volver);


const poblarDepartamentos = () => {
  let departmentSelect = document.getElementById("select-department");
  for (const department in data) {
      let option = document.createElement("option");
      option.value = department;
      option.text = department;
      departmentSelect.appendChild(option);
  }
};

const updateCursos = () => {
  let departmentSelect = document.getElementById("select-department");
  let courseSelect = document.getElementById("select-course");
  let selectedDepartment = departmentSelect.value;
  
  courseSelect.innerHTML = '<option value="">Seleccione un ramo</option>';
  
  if (data[selectedDepartment]) {
      data[selectedDepartment].forEach(course => {
          let option = document.createElement("option");
          option.value = course;
          option.text = course;
          courseSelect.appendChild(option);
      });
  }
};


const updateContacto = () => {
    let contactSelect = document.getElementById("select-contacto");
    for (const contact of contacttypes) {
        let option = document.createElement("option");
        option.value = contact;
        option.text = contact;
        contactSelect.appendChild(option);
    }

}


function showTextbox() {
    const contactoselect = document.getElementById("select-contacto");
    let contactInput = document.getElementById("contactInput");
    if (contactoselect.value !== "") {
        contactInput.style.display = "block";
    } else {
        contactInput.style.display = "none";
    }
}

const inputFecha = document.getElementById('fecha');
const fechaActual = new Date();

const fechaPrellenada = new Date();
fechaPrellenada.setHours(fechaPrellenada.getHours() + 3);

function formatearFecha(date) {
  const yyyy = date.getFullYear();
  const mm = String(date.getMonth() + 1).padStart(2, '0');
  const dd = String(date.getDate()).padStart(2, '0');
  const hh = String(date.getHours()).padStart(2, '0');
  const min = String(date.getMinutes()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd}T${hh}:${min}`;
}
inputFecha.min = formatearFecha(fechaActual);
inputFecha.value = formatearFecha(fechaPrellenada);

document.addEventListener("DOMContentLoaded", () => {
  const fileContainer = document.getElementById("file-container");
  const addPhotoBtn = document.getElementById("add-photo-btn");

  addPhotoBtn.addEventListener("click", () => {
    const fileInputs = fileContainer.querySelectorAll(".file-input");

    if (fileInputs.length >= 5) {
      alert("No puedes subir más de 5 fotos.");
      return;
    }

    // Crear un nuevo input file
    const newInput = document.createElement("input");
    newInput.type = "file";
    newInput.name = "files";
    newInput.classList.add("file-input");
    newInput.accept = "image/*,.pdf";
    

    // Añadir al contenedor
    fileContainer.appendChild(newInput);
  });
});






document.getElementById("select-contacto").addEventListener("change", showTextbox);
document.getElementById("select-department").addEventListener("change", updateCursos);




window.onload = () => {
  poblarDepartamentos();
  updateContacto();
  showTextbox();
};