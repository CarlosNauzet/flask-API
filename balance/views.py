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
#TODO: obtener un movimiento por id
#TODO: actualizar movimiento por id
#TODO: eliminar movimiento por id

RUTA = app.config.get('RUTA')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/v1/movimientos')
def listat_movimientos():
    try:
        db = DBManager(RUTA)
        sql = 'SELECT * FROM movimientos'
        movimientos = db.consultaSQL(sql)
        resultado = {
            "status": "success",
            "results": movimientos
        }
    except Exception as error:
        resultado = {
            "status": "error",
            "message": str(error)
        }
    return jsonify(resultado)

