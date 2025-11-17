import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, extract
from config import Config
from models import db, AvisoAdopcion, Comuna, Region, Foto, Comentario
from datetime import datetime

from validations import validate_aviso_adopcion, validate_comentario
import requests

SPRING_BOOT_API_URL = "http://localhost:8080/evaluar_avisos"

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def index():
    """
    Ruta de la Portada. Muestra un mensaje de bienvenida y los 5 avisos más recientes.
    """

    ultimos_avisos = AvisoAdopcion.query \
        .order_by(AvisoAdopcion.fecha_ingreso.desc()) \
        .limit(5) \
        .all()
        
    return render_template('index.html', ultimos_avisos=ultimos_avisos)


@app.route('/evaluar_avisos')
def evaluar_avisos():
    """
    Ruta para Evaluar Avisos. 
    Redirige directamente al endpoint de Spring Boot para forzar el cambio de puerto
    en el navegador del cliente.
    """
    SPRING_BOOT_URL_CLIENT = "http://localhost:8080/evaluar_avisos"
    return redirect(SPRING_BOOT_URL_CLIENT)

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
        


        errors = validate_aviso_adopcion(request.form, request.files)
        

        if errors:

            region_id_seleccionada = request.form.get('region_id')
            return render_template(
                'agregar_adopcion.html', 
                regiones=regiones, 
                errors=errors,             # Pasamos los mensajes de error
                form_data=request.form,     # Pasamos los datos del formulario para retenerlos
                region_id_seleccionada=region_id_seleccionada
            )
        

        try:

            comuna_id = request.form.get('comuna_id', type=int)
            fecha_entrega_str = request.form.get('fecha_entrega')
            fecha_entrega = datetime.strptime(fecha_entrega_str, '%Y-%m-%dT%H:%M')
            

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


            file = request.files['foto_animal']
            

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
            

            return redirect(url_for('lista_adopciones'))
        
        except Exception as e:

            print(f"Error crítico en la transacción de la BD: {e}")
            db.session.rollback() 
            errors = {'general': 'Ocurrió un error inesperado al guardar el aviso. Intente nuevamente.'}
            return render_template(
                'agregar_adopcion.html', 
                regiones=regiones, 
                errors=errors,
                form_data=request.form
            )
            


    return render_template('agregar_adopcion.html', regiones=regiones, errors={})


@app.route('/estadisticas')
def estadisticas():
    """
    Ruta que despliega la página de estadísticas y carga los gráficos vía AJAX.
    Carga el nuevo archivo estadisticas.html.
    """
    return render_template('estadisticas.html')

@app.route('/api/estadisticas/avisos_por_dia')
def avisos_por_dia_api():
    """API para el Gráfico 1: Avisos agregados por día (Líneas)."""
    
    # Agrupa por fecha (solo el día) y cuenta la cantidad de IDs
    # (Usamos func.date() para agrupar por el día sin la hora)
    data = db.session.query(
        func.date(AvisoAdopcion.fecha_ingreso).label('fecha'),
        func.count(AvisoAdopcion.id).label('cantidad')
    ) \
    .group_by(func.date(AvisoAdopcion.fecha_ingreso)) \
    .order_by('fecha') \
    .all()

    # Formato: [{'fecha': 'YYYY-MM-DD', 'cantidad': X}]
    result = [{'fecha': d.fecha.strftime('%Y-%m-%d'), 'cantidad': d.cantidad} for d in data]
    return jsonify(result)

@app.route('/api/estadisticas/avisos_por_tipo')
def avisos_por_tipo_api():
    """API para el Gráfico 2: Total de avisos por tipo (Torta)."""
    
    # Agrupa por tipo (perro/gato) y suma la cantidad de mascotas
    data = db.session.query(
        AvisoAdopcion.tipo,
        func.sum(AvisoAdopcion.cantidad).label('total')
    ) \
    .group_by(AvisoAdopcion.tipo) \
    .all()

    # Formato para Pie chart: [{'name': 'Gato', 'y': X}, ...]
    result = [{'name': d.tipo.capitalize(), 'y': int(d.total)} for d in data]
    return jsonify(result)

@app.route('/api/estadisticas/avisos_mensuales_por_tipo')
def avisos_mensuales_por_tipo_api():
    """API para el Gráfico 3: Avisos de perro/gato por mes (Barras)."""
    
    # Agrupa por año, mes y tipo.
    # Usamos extract para obtener mes y año, crucial para un correcto agrupamiento.
    data = db.session.query(
        extract('year', AvisoAdopcion.fecha_ingreso).label('year'),
        extract('month', AvisoAdopcion.fecha_ingreso).label('month'),
        AvisoAdopcion.tipo,
        func.count(AvisoAdopcion.id).label('cantidad')
    ) \
    .group_by('year', 'month', AvisoAdopcion.tipo) \
    .order_by('year', 'month') \
    .all()

    # --- Lógica de formateo para el gráfico de barras agrupadas ---
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    
    # 1. Obtener todas las categorías (ej: "2024-Feb")
    categorias_mes = sorted(list(set(f"{int(d.year)}-{meses[int(d.month)-1]}" for d in data)))
    
    # 2. Inicializar series
    perros = [0] * len(categorias_mes)
    gatos = [0] * len(categorias_mes)
    
    # 3. Llenar las series
    for d in data:
        categoria_str = f"{int(d.year)}-{meses[int(d.month)-1]}"
        try:
            index = categorias_mes.index(categoria_str)
            if d.tipo == 'perro':
                perros[index] = d.cantidad
            elif d.tipo == 'gato':
                gatos[index] = d.cantidad
        except ValueError:
            continue

    result = {
        'categories': categorias_mes,
        'series': [
            {'name': 'Perros', 'data': perros},
            {'name': 'Gatos', 'data': gatos}
        ]
    }
    return jsonify(result)

# app.py (Continuación, después de las rutas de estadísticas)
# ----------------------------------------------------------------------
# RUTAS PARA DETALLE DE AVISO Y COMENTARIOS
# ----------------------------------------------------------------------

@app.route('/adopcion/<int:aviso_id>')
def ver_aviso(aviso_id):
    """
    Ruta para ver la información de un aviso específico. 
    Carga detalle_adopcion.html.
    """
    # Usa get_or_404 para manejar si el ID no existe
    aviso = AvisoAdopcion.query.get_or_404(aviso_id)
    return render_template('detalle_adopcion.html', aviso=aviso)


@app.route('/api/comentarios/<int:aviso_id>', methods=['GET'])
def obtener_comentarios_api(aviso_id):
    """
    API para obtener una lista JSON de comentarios para un aviso dado, 
    ordenados por fecha descendente.
    """
    comentarios = Comentario.query.filter_by(aviso_id=aviso_id).order_by(Comentario.fecha.desc()).all()
    
    # Formatear la lista de comentarios a JSON
    comentarios_json = [
        {
            'nombre': c.nombre, 
            'texto': c.texto, 
            'fecha': c.fecha.isoformat() # Usamos isoformat o strftime para la fecha/hora
        } for c in comentarios
    ]
    return jsonify(comentarios_json)


@app.route('/api/comentarios/<int:aviso_id>', methods=['POST'])
def agregar_comentario_api(aviso_id):
    """
    API para agregar un nuevo comentario a un aviso. Retorna JSON de éxito o error.
    """
    
    # 1. Verificar si el aviso existe
    aviso = AvisoAdopcion.query.get(aviso_id)
    if not aviso:
        return jsonify({'success': False, 'message': 'Aviso de adopción no encontrado.'}), 404

    # 2. Validar datos usando la nueva función
    errors = validate_comentario(request.form)
    if errors:
        # Retorna el diccionario de errores con un código 400 (Bad Request)
        return jsonify({'success': False, 'errors': errors}), 400
    
    # 3. Insertar en BD
    try:
        nuevo_comentario = Comentario(
            nombre=request.form.get('nombre'),
            texto=request.form.get('texto'),
            aviso_id=aviso_id,
            fecha=datetime.utcnow() 
        )
        db.session.add(nuevo_comentario)
        db.session.commit()
        
        # Retornar éxito
        return jsonify({
            'success': True, 
            'message': 'Comentario agregado con éxito.'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error al guardar comentario: {e}")
        return jsonify({'success': False, 'message': 'Error inesperado del servidor al guardar el comentario.'}), 500

if __name__ == '__main__':

    app.run(debug=True)