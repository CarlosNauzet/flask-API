from flask import jsonify, render_template

from . import app
from .models import DBManager


"""
Verbos y formato de endpoints

GET /movimientos ----------->LISTA movimientos
POST /movimientos------------>CREAR un movimiento nuevo

GET /movimientos/1----------->LEER el movimiento con ID=1
POST /movimientos/1---------->ACTUALIZAR el movimiento con ID=1 (sobreescribe todo el objeto
PUT /movimientos/1----------->ACTUALIZAR el movimiento con ID=1 (sobreescribe parcialmente)
DELETE / movimientos/1------->ELIMINAR el movimiento con ID=1

IMPORTANTE!!
Versionar los endpoint (son un contrato)


"""
#TODO: actualizar movimiento por id
#TODO: eliminar movimiento por id

RUTA = app.config.get('RUTA')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/v1/movimientos')
def lista_movimientos():
    try:
        db = DBManager(RUTA)
        sql = 'SELECT * FROM movimientos'
        movimientos = db.consultaSQL(sql)
        if len(movimientos) > 0:
            resultado = {
            "status": "success",
            "results": movimientos
        }
            status_code = 200
        else:
            resultado = {
                'staus': 'error',
                'message': f'No hay movimientos en el sistema'
            }
            status_code = 404
    except Exception as error:
        resultado = {
            "status": "error",
            "message": str(error)
        }
        status_code = 500

    return jsonify(resultado), status_code

@app.route('/api/v1/movimientos/<int:id>')
def get_Movimiento(id):
    try:
        db = DBManager(RUTA)
        mov = db.obtenerMovimiento(id)
        if mov:
            resultado = {
            'status': 'succes',
            'results': mov
            }
            status_code = 200
        else:
            resultado = {
                'status': 'error',
                'message': f'No he encontrado un movimiento con el ID={id}'
            }
            status_code = 404
    except Exception as error:
        resultado = {
        'status': 'error',
        'message': str(error)
    }
        status_code = 500
    return jsonify(resultado), status_code


@app.route('/api/v1/movimientos/<int:id>', methods=['DELETE'])
def eliminar_movimiento(id):
    """
    Instanciar el DB manager
    Comprobar si existe el movimiento con ese ID
    Si existe:
        Preparo la consulta de eliminación
    si se ha birrado:
        resultado = ok
    si no:
        resultado = ko
        mensaje = error al borrar
    si no existe:
        resultado = ko
        mensaje = No existe
    """
    try:
        db= DBManager(RUTA)

        mov = db.obtenerMovimiento(id)
        
        if mov:
            sql = 'DELETE FROM movimientos WHERE id=?'
            esta_borrado = db.consultaConParametros(sql, (id,)) 
            if esta_borrado:
                resultado = {
                'status' : 'success'
            }
                status_code = 200
            else:
                resultado = {
                'status': 'error',
                'message': 'No se ha eliminado el movimiento con )D={id}'
            }
                status_code = 500
        else:
            resultado = {
                'status': 'error',
                'message': f'No existe un movimiento con ID={id} para eliminar'
            }
            status_code = 404
    except:
        resultado = {
            'status': 'error',
            'message': 'Error desconocido en el servidor'
        }
        status_code = 500

    return jsonify(resultado), status_code