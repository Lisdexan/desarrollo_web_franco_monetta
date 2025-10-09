import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
# Importar Config, db, y modelos asumiendo que existen y están configurados correctamente
from config import Config
from models import db, AvisoAdopcion, Comuna, Region, Foto
from datetime import datetime
# --- PASO 1: IMPORTAR LA FUNCIÓN DE VALIDACIÓN EXTERNA ---
from validations import validate_aviso_adopcion 

# --- Inicialización de la Aplicación ---
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# CONFIGURACIÓN DE ARCHIVOS
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Rutas de la Aplicación ---

@app.route('/')
def index():
    """
    Ruta de la Portada. Muestra un mensaje de bienvenida y los 5 avisos más recientes.
    """
    # Consulta los 5 avisos más recientes, ordenados por fecha de ingreso
    ultimos_avisos = AvisoAdopcion.query \
        .order_by(AvisoAdopcion.fecha_ingreso.desc()) \
        .limit(5) \
        .all()
        
    return render_template('index.html', ultimos_avisos=ultimos_avisos)


@app.route('/adopciones')
def lista_adopciones():
    """
    Ruta del Listado Completo (con paginación).
    """
    page = request.args.get('page', 1, type=int)
    per_page = 5

    paginador = AvisoAdopcion.query \
        .order_by(AvisoAdopcion.fecha_ingreso.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'lista_adopciones.html', 
        adopciones=paginador.items, 
        paginador=paginador
    )

@app.route('/api/comunas/<int:region_id>')
def obtener_comunas(region_id):
    """Retorna una lista JSON de comunas para una ID de región dada (Ruta API)."""
    
    comunas = Comuna.query.filter_by(region_id=region_id).order_by(Comuna.nombre).all()
    comunas_json = [{'id': c.id, 'nombre': c.nombre} for c in comunas]
    
    return jsonify(comunas_json)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar_adopcion():
    regiones = Region.query.order_by(Region.nombre).all()
    
    if request.method == 'POST':
        
        # --- PASO 2: LLAMAR A LA FUNCIÓN DE VALIDACIÓN ---
        # Pasamos los datos del formulario (request.form) y los archivos (request.files)
        errors = validate_aviso_adopcion(request.form, request.files)
        
        # Si el diccionario 'errors' NO está vacío, hay fallos
        if errors:
            # Si hay errores, recargamos el formulario
            region_id_seleccionada = request.form.get('region_id')
            return render_template(
                'agregar_adopcion.html', 
                regiones=regiones, 
                errors=errors,             # Pasamos los mensajes de error
                form_data=request.form,     # Pasamos los datos del formulario para retenerlos
                region_id_seleccionada=region_id_seleccionada
            )
        
        # Si NO hay errores (errors es un diccionario vacío), procedemos con la inserción en la BD
        try:
            # 2. Recolección de datos
            comuna_id = request.form.get('comuna_id', type=int)
            fecha_entrega_str = request.form.get('fecha_entrega')
            fecha_entrega = datetime.strptime(fecha_entrega_str, '%Y-%m-%dT%H:%M')
            
            # 3. Creación del nuevo objeto AvisoAdopcion
            nuevo_aviso = AvisoAdopcion(
                nombre=request.form.get('nombre'),
                email=request.form.get('email'),
                celular=request.form.get('celular'),
                comuna_id=comuna_id,
                tipo=request.form.get('tipo'),
                cantidad=request.form.get('cantidad', type=int),
                edad=request.form.get('edad', type=int),
                unidad_medida=request.form.get('unidad_medida'),
                fecha_entrega=fecha_entrega,
                descripcion=request.form.get('descripcion'),
                fecha_ingreso=datetime.utcnow()
            )

            db.session.add(nuevo_aviso)
            db.session.commit()

            # 4. PROCESAR Y GUARDAR LA FOTO
            file = request.files['foto_animal']
            
            # El archivo ya ha sido rebobinado y validado por 'validate_aviso_adopcion'
            if file and file.filename != '':
                
                filename_base = secure_filename(file.filename)
                nombre_unico = f"{nuevo_aviso.id}_{filename_base}"
                ruta_guardado = os.path.join(app.config['UPLOAD_FOLDER'], nombre_unico)
                
                file.save(ruta_guardado) 

                nueva_foto = Foto(
                    actividad_id=nuevo_aviso.id,
                    nombre_archivo=nombre_unico,
                    ruta_archivo=f"uploads/{nombre_unico}" 
                )
                db.session.add(nueva_foto)
                db.session.commit()
            
            # 5. Redirigir al listado
            return redirect(url_for('lista_adopciones'))
        
        except Exception as e:
            # Captura errores de base de datos o de proceso crítico
            print(f"Error crítico en la transacción de la BD: {e}")
            db.session.rollback() 
            errors = {'general': 'Ocurrió un error inesperado al guardar el aviso. Intente nuevamente.'}
            return render_template(
                'agregar_adopcion.html', 
                regiones=regiones, 
                errors=errors,
                form_data=request.form
            )
            
    # Mostrar el formulario GET (o después de un error general)
    # Se inicializa errors como diccionario vacío si es GET
    return render_template('agregar_adopcion.html', regiones=regiones, errors={})

if __name__ == '__main__':
    # Ejecutar la aplicación
    app.run(debug=True)