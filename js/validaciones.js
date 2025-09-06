const validateSelect = (select) => {
  if(!select) return false;
  return true
}

const validateExistence = (string) => {  //me acabo de fijar que es igual a validateSelect pero se ve bonito
  if (!string) return false;
  return true
}

const validateLenght = (string, min, max) => {
  if (!string) return false;
  let lengthValid = string.length >= min && string.length <= max;

  return lengthValid;
}

const validateInt = (int, min) => {
  if (!int) return false;
  if (int > min){
    return true;
  }
}

const validateEmail = (email) => {
  if (!email) return false;
  let lengthValid = email.length <= 100;

  // validamos el formato
  let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
  let formatValid = re.test(email);

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && formatValid;
};

const validatePhoneNumber = (phoneNumber) => {
  if (!phoneNumber) return false;
  // validación de longitud
  let lengthValid = phoneNumber.length >= 8;

  // validación de formato
  let re = /^\+\d{3}\.\d{8}$/;
  let formatValid = re.test(phoneNumber);

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && formatValid;
};

const ValidateContactInput = (contactInput, contacttype) => { //el input de contacto solo es obligatorio si se selecciona un tipo de contacto
    if (validateSelect(contacttype)){
        return validateExistence(contactInput) && validateLenght(contactInput,4,50);
    }
    else{ //si no se selecciona nada, no es obligatorio llenar el input
        return true;
    }
}

const validateDate = (dateString) => {
  if (!dateString) return false;              // no hay valor
  const fechaIngresada = new Date(dateString);
  const ahora = new Date();

  // Redondear segundos y milisegundos para evitar falsos negativos
  fechaIngresada.setSeconds(0, 0);
  ahora.setSeconds(0, 0);

  return fechaIngresada > ahora;              // true si fecha futura, false si igual o pasada
}

const validateFiles = (files) => {
  if (!files) return false;

  // validación del número de archivos
  let lengthValid = 1 <= files.length && files.length <= 5;

  // validación del tipo de archivo
  let typeValid = true;

  for (const file of files) {
    // el tipo de archivo debe ser "image/<foo>" o "application/pdf"
    let fileFamily = file.type.split("/")[0];
    typeValid &&= fileFamily == "image" || file.type == "application/pdf";
  }

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && typeValid;
};




const validateForm = () => {
  // obtener elementos del DOM usando el nombre del formulario.
  let myForm = document.forms["myForm"];
  let email = myForm["email"].value;
  let phoneNumber = myForm["tel"].value;
  let name = myForm["nombre"].value;
  let files = myForm["files"].files;
  let department = myForm["select-department"].value;
  let curso = myForm["select-course"].value;
  let sector = myForm["sector"].value;
  let contacttype = myForm["select-contacto"].value;
  let contactInput = myForm["contactInput"].value;
  let mascotaType = myForm["tipo-mascota"].value;
  let mascotaQuantity = myForm["cantidad"].value;
  let mascotaAge = myForm["edad"].value;
  let mascotaAgeType = myForm["tipo-edad"].value;
  let fecha = myForm["fecha"].value;

  let newInput = document.createElement("input");
  newInput.type = "file";
  newInput.name = "files";
  newInput.required = false;
  // variables auxiliares de validación y función.
  let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
  };

  // lógica de validación
  if (!validateExistence(name)) {
    setInvalidInput("Nombre");
  }
  if (!validateLenght(name,3,200)){
    setInvalidInput("Nombre");
  }
  if (!validateEmail(email)) {
    setInvalidInput("Email");
  }
  if (!validatePhoneNumber(phoneNumber)) {
    setInvalidInput("Número");
  }
  if (!validateFiles(files)) {
    setInvalidInput("Fotos");
  }
  if (!validateSelect(department)) {
    setInvalidInput("Region");
  }
  if (!validateSelect(curso)) {
    setInvalidInput("Comuna");
  }
  if (!validateExistence(sector)){
    setInvalidInput("Sector");
  }
  if (!validateLenght(sector,0,100)){
    setInvalidInput("Sector");
  }
  if (!ValidateContactInput(contactInput, contacttype)){
    setInvalidInput("Contacto");
  }
  if (!validateSelect(mascotaType)){
    setInvalidInput("Tipo de Mascota");
  }
  if (!validateInt(mascotaQuantity,0)){
    setInvalidInput("Cantidad de Mascotas");
  }
  if (!validateInt(mascotaAge,0)){
    setInvalidInput("Edad de Mascotas");
  }
  if (!validateSelect(mascotaAgeType)){
    setInvalidInput("Tipo de Edad");
  }
  if (!validateDate(fecha)){
    setInvalidInput("Fecha");
  }   


  // finalmente mostrar la validación
  let validationBox = document.getElementById("val-box");
  let validationMessageElem = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");
  let formContainer = document.querySelector(".main-container");

  if (!isValid) {
    validationListElem.textContent = "";
    // agregar elementos inválidos al elemento val-list.
    for (input of invalidInputs) {
      let listElement = document.createElement("li");
      listElement.innerText = input;
      validationListElem.append(listElement);
    }
    // establecer val-msg
    validationMessageElem.innerText = "Los siguientes campos son inválidos:";

    // aplicar estilos de error
    validationBox.style.backgroundColor = "#ffdddd";
    validationBox.style.borderLeftColor = "#f44336";

    // hacer visible el mensaje de validación
    validationBox.hidden = false;
  } else {
    // Ocultar el formulario
    myForm.style.display = "none";

    // establecer mensaje de éxito
    validationMessageElem.innerText = "¡Formulario válido! ¿Deseas enviarlo o volver?";
    validationListElem.textContent = "";

    // aplicar estilos de éxito
    validationBox.style.backgroundColor = "#ddffdd";
    validationBox.style.borderLeftColor = "#4CAF50";

    let submitButton = document.createElement("button");
    submitButton.innerText = "Enviar";
    submitButton.style.marginRight = "10px";

    submitButton.addEventListener("click", () => {
    const confirmSend = confirm("¿Estás seguro de enviar el formulario?");
    if (confirmSend) {
        validationMessageElem.innerText = "Hemos recibido la info, ¡muchas gracias! 🎉";
        validationListElem.textContent = "";

        let backToMenuBtn = document.createElement("button");
        backToMenuBtn.innerText = "Volver al menú";
        backToMenuBtn.style.marginTop = "10px";
        backToMenuBtn.addEventListener("click", () => {
            window.location.href = "../html/main.html";
        });

        validationListElem.appendChild(backToMenuBtn);

        submitButton.style.display = "none";
        backButton.style.display = "none";
    }
});


    let backButton = document.createElement("button");
    backButton.innerText = "Volver";
    backButton.addEventListener("click", () => {
      // Mostrar el formulario nuevamente
      myForm.style.display = "block";
      validationBox.hidden = true;
    });

    validationListElem.appendChild(submitButton);
    validationListElem.appendChild(backButton);

    // hacer visible el mensaje de validación
    validationBox.hidden = false;
  }
};

let submitBtn = document.getElementById("submit-btn");
submitBtn.addEventListener("click", validateForm);