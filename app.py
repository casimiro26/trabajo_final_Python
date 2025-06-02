from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
import random
import PyPDF2
from datetime import datetime

app = Flask(__name__)

# Directorio para guardar archivos subidos
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Almacenamiento de resultados (simulación de base de datos)
evaluations = []

# Áreas de evaluación y sus pesos
EVALUATION_AREAS = {
    "Logística": 0.2,
    "Recursos Humanos": 0.6,
    "Mesa de Partes": 0.2
}

# Áreas disponibles para postular
POSTULATION_AREAS = [
    "Área de Imagen Institucional y Relaciones Públicas",
    "Secretaría y Atención al Ciudadano",
    "ATM",
    "Área de Informática",
    "Área de Administración"
]

# Simulación de análisis del CV
def analyze_cv(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
        
        # Simular puntajes para cada área (valores aleatorios para simulación)
        scores = {area: random.randint(0, 100) for area in EVALUATION_AREAS}
        
        # Calcular puntaje total ponderado
        total_score = sum(scores[area] * weight for area, weight in EVALUATION_AREAS.items())
        
        # Determinar resultado y mensaje
        if total_score >= 70:
            result = "Aprobado"
            message = "¡Felicidades! Cumples todas las expectativas. 🎉"
            icon = "✅"
        elif total_score >= 50:
            result = "Observado"
            message = "Se cumplen parcialmente los requisitos. Mejora tu presentación. 📝"
            icon = "⚠️"
        else:
            result = "Desaprobado"
            message = "No cumple con las expectativas. Intenta de nuevo. 😔"
            icon = "❌"
            
        return scores, total_score, result, message, icon
    except Exception:
        # En caso de error, simular puntajes
        scores = {area: random.randint(0, 100) for area in EVALUATION_AREAS}
        total_score = sum(scores[area] * weight for area, weight in EVALUATION_AREAS.items())
        if total_score >= 70:
            result = "Aprobado"
            message = "¡Felicidades! Cumples todas las expectativas. 🎉"
            icon = "✅"
        elif total_score >= 50:
            result = "Observado"
            message = "Se cumplen parcialmente los requisitos. Mejora tu presentación. 📝"
            icon = "⚠️"
        else:
            result = "Desaprobado"
            message = "No cumple con las expectativas. Intenta de nuevo. 😔"
            icon = "❌"
        return scores, total_score, result, message, icon

@app.route('/')
def welcome():
    return render_template('welcome.html', areas=POSTULATION_AREAS)

@app.route('/seleccion-area/<area>')
def seleccion_area(area):
    if area not in POSTULATION_AREAS:
        return redirect(url_for('welcome'))
    return render_template('seleccion-area.html', area=area)

@app.route('/upload', methods=['POST'])
def upload_cv():
    area = request.form.get('area')
    if 'file' not in request.files or not area:
        return redirect(url_for('seleccion_area', area=area))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('seleccion_area', area=area))
    
    if file and (file.filename.endswith('.pdf') or file.filename.endswith('.docx')):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Analizar el CV
        scores, total_score, result, message, icon = analyze_cv(file_path)
        
        # Guardar evaluación
        evaluation = {
            'area': area,
            'file': file.filename,
            'scores': scores,
            'total_score': total_score,
            'result': result,
            'message': message,
            'icon': icon,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        evaluations.append(evaluation)
        
        return render_template('resultado.html', evaluation=evaluation)
    return redirect(url_for('seleccion_area', area=area))

@app.route('/evaluaciones')
def evaluaciones():
    return render_template('evaluaciones.html', evaluations=evaluations)

if __name__ == '__main__':
    app.run(debug=True, port=5001)