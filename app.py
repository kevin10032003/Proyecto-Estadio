from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Cambia si tienes contraseña configurada
app.config['MYSQL_DB'] = 'flaskcontacts'
app.secret_key = '1234'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mysql = MySQL(app)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# ----------------------- LOCALIDADES -----------------------
@app.route('/localidades')
def localidades():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, precio, descripcion, created_at FROM localidades")
    data = cur.fetchall()
    # Convertir a una lista de diccionarios
    localidades = [{'id': row[0], 'nombre': row[1], 'precio': row[2], 'descripcion': row[3], 'created_at': row[4]} for row in data]
    cur.close()
    return render_template('tabla_localidades.html', localidades=localidades)

@app.route('/localidades/add', methods=['POST'])
def add_localidad():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        descripcion = request.form['descripcion']
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO localidades (nombre, precio, descripcion) 
            VALUES (%s, %s, %s)
""", (nombre, precio, descripcion))

        mysql.connection.commit()
        flash('Localidad agregada correctamente')
        return redirect(url_for('localidades'))
    
@app.route('/editar_localidad/<int:id>', methods=['GET', 'POST'])
def editar_localidad(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM localidades WHERE id = %s", [id])
    localidad = cur.fetchone()
    cur.close()

    if not localidad:
        return redirect(url_for('localidades'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        descripcion = request.form['descripcion']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE localidades 
            SET nombre = %s, precio = %s, descripcion = %s 
            WHERE id = %s
        """, (nombre, precio, descripcion, id))
        mysql.connection.commit()
        cur.close()

        flash('Localidad actualizada correctamente')
        return redirect(url_for('localidades'))

    return render_template('editar_localidad.html', localidad=localidad)

@app.route('/eliminar_localidad/<int:id>', methods=['POST'])
def eliminar_localidad(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM localidades WHERE id = %s', (id,))
    mysql.connection.commit()  # Confirmar la eliminación
    flash('Localidad eliminada correctamente')
    return redirect(url_for('localidades'))

# ----------------------- CLIENTES -----------------------
@app.route('/clientes')
def clientes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, fullname, email, telephone FROM clientes')
    data = cur.fetchall()
    clientes = [{'id': row[0], 'fullname': row[1], 'email': row[2], 'telephone': row[3]} for row in data]
    cur.close()
    return render_template('tabla_clientes.html', clientes=clientes)


@app.route('/clientes/add', methods=['POST'])
def add_cliente():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        telephone = request.form['telephone']
        created_at = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO clientes (fullname, email, telephone, created_at) VALUES (%s, %s, %s, %s)", (fullname, email, telephone, created_at))
        mysql.connection.commit()
        flash('Cliente agregado correctamente')
        return redirect(url_for('clientes'))
    
@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM clientes WHERE id = %s", [id])
    cliente = cur.fetchone()
    cur.close()

    if not cliente:
        return redirect(url_for('clientes'))

    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        telephone = request.form['telephone']
        

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE clientes 
            SET fullname = %s, email = %s, telephone = %s
            WHERE id = %s
        """, (fullname, email, telephone, id))
        mysql.connection.commit()
        cur.close()

        flash('Cliente actualizado correctamente')
        return redirect(url_for('clientes'))

    return render_template('editar_cliente.html', cliente=cliente)    
    

@app.route('/eliminar_cliente/<int:id>', methods=['POST'])
def eliminar_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM clientes WHERE id = %s', (id,))
    mysql.connection.commit()  # Confirmar la eliminación
    flash('Cliente eliminado correctamente')
    return redirect(url_for('clientes'))

# ----------------------- EVENTOS -----------------------
@app.route('/eventos')
def eventos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre_evento, fecha_evento, descripcion FROM eventos')
    data = cur.fetchall()
    eventos = [{'id': row[0], 'nombre_evento': row[1], 'fecha_evento': row[2], 'descripcion': row[3]} for row in data]
    cur.close()
    return render_template('tabla_eventos.html', eventos=eventos)


@app.route('/eventos/add', methods=['POST'])
def add_evento():
    if request.method == 'POST':
        nombre_evento = request.form['nombre_evento']
        fecha_evento = request.form['fecha_evento']
        descripcion = request.form['descripcion']
        created_at = datetime.now()  # Si quieres agregar la fecha y hora actual
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO eventos (nombre_evento, fecha_evento, descripcion, created_at) 
            VALUES (%s, %s, %s, %s)
""", (nombre_evento, fecha_evento, descripcion, created_at))

        mysql.connection.commit()
        flash('Evento agregado correctamente')
        return redirect(url_for('eventos'))
    
@app.route('/editar_evento/<int:id>', methods=['GET', 'POST'])
def editar_evento(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM eventos WHERE id = %s", [id])
    evento = cur.fetchone()
    cur.close()

    if not evento:
        return redirect(url_for('eventos'))

    if request.method == 'POST':
        nombre_evento = request.form['nombre_evento']
        fecha_evento = request.form['fecha_evento']
        descripcion = request.form['descripcion']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE eventos 
            SET nombre_evento = %s, fecha_evento = %s, descripcion = %s 
            WHERE id = %s
        """, (nombre_evento, fecha_evento, descripcion, id))
        mysql.connection.commit()
        cur.close()

        flash('Evento actualizado correctamente')
        return redirect(url_for('eventos'))

    return render_template('editar_evento.html', evento=evento)

@app.route('/eliminar_evento/<int:id>', methods=['POST'])
def eliminar_evento(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM eventos WHERE id = %s', (id,))
    mysql.connection.commit()  # Confirmar la eliminación
    flash('Evento eliminado correctamente')
    return redirect(url_for('eventos'))

# ----------------------- PAGOS -----------------------
@app.route('/pagos')
def pagos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, id_reserva, monto, fecha_pago, estado_pago FROM pagos')
    data = cur.fetchall()
    pagos = [{'id': row[0], 'id_reserva': row[1], 'monto': row[2], 'fecha_pago': row[3], 'estado_pago': row[4]} for row in data]
    cur.close()
    return render_template('tabla_pagos.html', pagos=pagos)


@app.route('/pagos/add', methods=['POST'])
def add_pago():
    if request.method == 'POST':
        try:
            id_reserva = request.form['id_reserva']
            monto = request.form['monto']
            fecha_pago = request.form['fecha_pago']
            estado_pago = request.form['estado_pago']
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO pagos (id_reserva, monto, fecha_pago, estado_pago) 
                VALUES (%s, %s, %s, %s)
            """, (id_reserva, monto, fecha_pago, estado_pago))

            mysql.connection.commit()
            flash('Pago registrado correctamente')
        except Exception as e:
            flash('Error al agregar el pago: verifica que el ID de la reserva sea válido.', 'error')
    return redirect(url_for('pagos'))
    
@app.route('/editar_pago/<int:id>', methods=['GET', 'POST'])
def editar_pago(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pagos WHERE id = %s", [id])
    pago = cur.fetchone()
    cur.close()

    if not pago:
        return redirect(url_for('pagos'))

    if request.method == 'POST':
        id_reserva = request.form['id_reserva']
        monto = request.form['monto']
        fecha_pago = request.form['fecha_pago']
        estado_pago = request.form['estado_pago']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE pagos 
            SET id_reserva = %s, monto = %s, fecha_pago = %s, estado_pago = %s 
            WHERE id = %s
        """, (id_reserva, monto, fecha_pago, estado_pago, id))
        mysql.connection.commit()
        cur.close()

        flash('Pago registrado correctamente')
        return redirect(url_for('pagos'))

    return render_template('editar_pago.html', pago=pago)

@app.route('/eliminar_pago/<int:id>', methods=['POST'])
def eliminar_pago(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM pagos WHERE id = %s', (id,))
    mysql.connection.commit()  # Confirmar la eliminación
    flash('Pago eliminado correctamente')
    return redirect(url_for('pagos'))

# ----------------------- RESERVAS -----------------------
@app.route('/reservas')
def reservas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, id_cliente, id_localidad, fecha_reserva FROM reservas")
    data = cur.fetchall()
    # Convertir a una lista de diccionarios
    reservas = [{'id': row[0], 'id_cliente': row[1], 'id_localidad': row[2], 'fecha_reserva': row[3]} for row in data]
    cur.close()
    return render_template('tabla_reservas.html', reservas=reservas)

@app.route('/reservas/add', methods=['POST'])
def add_reserva():
    if request.method == 'POST':
        try:
            id_cliente = request.form['id_cliente']
            id_localidad = request.form['id_localidad']
            fecha_reserva = request.form['fecha_reserva']
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO reservas (id_cliente, id_localidad, fecha_reserva) 
                VALUES (%s, %s, %s)
            """, (id_cliente, id_localidad, fecha_reserva))

            mysql.connection.commit()
            flash('Reserva registrada correctamente')
        except Exception as e:
            flash('Error al agregar la reserva: verifica que el ID del cliente y de la localidad sea válido.', 'error')
    return redirect(url_for('reservas'))
    
@app.route('/editar_reserva/<int:id>', methods=['GET', 'POST'])
def editar_reserva(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reservas WHERE id = %s", [id])
    reserva = cur.fetchone()
    cur.close()

    if not reserva:
        return redirect(url_for('reservas'))

    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        id_localidad = request.form['id_localidad']
        fecha_reserva = request.form['fecha_reserva']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE reservas 
            SET id_cliente = %s, id_localidad = %s, fecha_reserva = %s 
            WHERE id = %s
        """, (id_cliente, id_localidad, fecha_reserva, id))
        mysql.connection.commit()
        cur.close()

        flash('Reserva actualizada correctamente')
        return redirect(url_for('reservas'))

    return render_template('editar_reserva.html', reserva=reserva)

@app.route('/eliminar_reserva/<int:id>', methods=['POST'])
def eliminar_reserva(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM reservas WHERE id = %s', (id,))
    mysql.connection.commit()  # Confirmar la eliminación
    flash('Reserva eliminada correctamente')
    return redirect(url_for('reservas'))

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3000)

