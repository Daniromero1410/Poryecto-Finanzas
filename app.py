from flask import Flask, request, jsonify, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# Configuración de Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(creds)

# ID DE HOJA
SPREADSHEET_ID = "1z4Am_Y1C_FT5dUivvyXDJJIJAERyxi_Ox_yhyG0RhDA"

def agregar_registro(mes, categoria, descripcion, valor_euros):
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(mes.upper())
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    
    # Definir las columnas para cada categoría
    columnas = {
        "comida": {
            "fecha": "A",
            "descripcion": "B",
            "valor": "C"
        },
        "otros": {
            "fecha": "E",
            "descripcion": "F",
            "valor": "G"
        }
    }
    
    categoria = categoria.lower()
    if categoria not in columnas:
        return "Categoría inválida"
    
    # Obtener las columnas correspondientes
    cols = columnas[categoria]
    
    # Encontrar la primera fila vacía en la columna de fecha de la categoría
    fecha_col = cols["fecha"]
    fila_vacia = len(sheet.col_values(ord(fecha_col) - ord('A') + 1)) + 1
    
    # Convertir punto decimal a coma para compatibilidad con Excel
    valor_euros = valor_euros.replace(".", ",")
    
    # Actualizar las celdas
    sheet.update_acell(f"{cols['fecha']}{fila_vacia}", fecha_actual)
    sheet.update_acell(f"{cols['descripcion']}{fila_vacia}", descripcion)
    sheet.update_acell(f"{cols['valor']}{fila_vacia}", valor_euros)
    
    return "Registro agregado exitosamente"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/agregar", methods=["POST"])
def agregar():
    data = request.json
    mes = data.get("mes")
    categoria = data.get("categoria")
    descripcion = data.get("descripcion")
    valor_euros = data.get("valor_euros")
    
    if not all([mes, categoria, descripcion, valor_euros]):
        return jsonify({"error": "Faltan datos"}), 400
    
    resultado = agregar_registro(mes, categoria, descripcion, valor_euros)
    return jsonify({"mensaje": resultado})

if __name__ == "__main__":
    app.run(debug=True)
