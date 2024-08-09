from flask import Flask, render_template
from hdbcli import dbapi

app = Flask(__name__)

def obtener_datos():
    # Conexión a SAP HANA
    conn = dbapi.connect(
        address='192.168.0.108',
        port=30015,
        user='SAPINST',
        password='Mutt1.20!',
        database='MUT_PRODUCTIVA'
    )

    query = """
    SELECT T0."Cedula", T0."Nombre", T0."Cargo", T0."Supervisor"
    FROM "MUT_PRODUCTIVA"."CF_Organigrama_V02" T0
    """

    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    empleados = []
    for row in rows:
        empleados.append({
            'Cedula': row[0],
            'Nombre': row[1],
            'Cargo': row[2],
            'Supervisor': row[3] if row[3] != 's/d' else None  # Establece None si no hay supervisor
        })

    cursor.close()
    conn.close()

    return empleados

@app.route('/')
def organigrama():
    empleados = obtener_datos()
    return render_template('organigrama.html', empleados=empleados)

if __name__ == '__main__':
    app.run(debug=True)
