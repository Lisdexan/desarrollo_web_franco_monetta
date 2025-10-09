import filetype
import os
import re
from datetime import datetime


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

def validate_image_file(file_stream):
    """
    Valida un archivo subido (stream) verificando su extensión y tipo MIME real.
    """
    
    if file_stream.filename == '':
        return False
        

    file_stream.seek(0)
    
    ftype_guess = filetype.guess(file_stream)
    

    file_stream.seek(0) 

    if ftype_guess is None:
        return False
    
    extension = ftype_guess.extension.lower()
    mime = ftype_guess.mime.lower()

    if extension not in ALLOWED_EXTENSIONS or mime not in ALLOWED_MIMETYPES:
        return False

    return True

def validate_aviso_adopcion(form_data, file_data):
    """
    Valida todos los campos del formulario de aviso de adopción y recolecta los errores.

    :param form_data: Diccionario de los datos del formulario (request.form).
    :param file_data: Diccionario de los archivos (request.files).
    :return: Diccionario de errores. Si está vacío, la validación fue exitosa.
    """
    errors = {}
    

    
    comuna_id = form_data.get('comuna_id')
    

    try:
        if not comuna_id or int(comuna_id) <= 0:
            errors['comuna_id'] = 'Debe seleccionar una región y una comuna válida.'
    except (ValueError, TypeError):
        errors['comuna_id'] = 'La comuna seleccionada no es válida.'


    
    nombre = form_data.get('nombre')
    email = form_data.get('email')
    celular = form_data.get('celular')
    

    if not nombre or nombre.strip() == "":
        errors['nombre'] = 'El nombre de contacto es obligatorio.'
    elif not (len(nombre) >= 3 and len(nombre) <= 200):
        errors['nombre'] = 'El nombre debe tener entre 3 y 200 caracteres.'
        

    if not email:
        errors['email'] = 'El correo electrónico es obligatorio.'
    elif not ("@" in email and len(email) <= 100):
        errors['email'] = 'El formato del correo electrónico no es válido (debe tener @ y máx. 100 caracteres).'
        

    if celular:
        cel_regex = r'^\+\d{3}\.\d{8}$'
        if not re.match(cel_regex, celular):
            errors['celular'] = 'El formato del celular debe ser +XXX.XXXXXXXX (Ej: +569.12345678).'
    

    
    tipo = form_data.get('tipo')
    cantidad_str = form_data.get('cantidad')
    edad_str = form_data.get('edad')
    unidad_medida = form_data.get('unidad_medida')
    fecha_entrega_str = form_data.get('fecha_entrega') 
    

    if tipo not in ['gato', 'perro']:
        errors['tipo'] = 'Debe seleccionar el tipo de animal: gato o perro.'
        

    if not cantidad_str:
        errors['cantidad'] = 'La cantidad es obligatoria.'
    elif not cantidad_str.isdigit() or int(cantidad_str) <= 0:
        errors['cantidad'] = 'La cantidad debe ser un número entero positivo.'


    if not edad_str:
        errors['edad'] = 'La edad es obligatoria.'
    elif not edad_str.isdigit() or int(edad_str) <= 0:
        errors['edad'] = 'La edad debe ser un número entero positivo.'
        

    if unidad_medida not in ['a', 'm']:
        errors['unidad_medida'] = 'Debe seleccionar una unidad de medida válida (años o meses).'
    

    if not fecha_entrega_str:
        errors['fecha_entrega'] = 'La fecha máxima de entrega es obligatoria.'
    else:
        try:
            fecha_entrega = datetime.strptime(fecha_entrega_str, '%Y-%m-%dT%H:%M')
            if fecha_entrega < datetime.now():
                 errors['fecha_entrega'] = 'La fecha máxima de entrega no puede ser una fecha pasada.'
        except ValueError:
            errors['fecha_entrega'] = 'El formato de la fecha no es válido.'
            

    

    foto_file = file_data.get('foto_animal')
    
    if not foto_file or foto_file.filename == '':
        errors['foto_animal'] = 'Debe adjuntar una foto para el aviso.'
    else:

        if not validate_image_file(foto_file):
            errors['foto_animal'] = 'El archivo de la foto no es una imagen válida (solo JPG, PNG, GIF).'

    return errors