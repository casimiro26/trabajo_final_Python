from flask import Flask, request, render_template
import os
import PyPDF2
import random

app = Flask(__name__)

# Directorio para guardar los CVs subidos
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Palabras clave para cada área (simulación)
AREA_KEYWORDS = {
    "Mesa de Partes": ["atención al cliente", "gestión documental", "archivos", "oficina"],
    "Logística": ["almacén", "inventario", "distribución", "transporte"],
    "Recursos Humanos": ["selección de personal", "capacitación", "nomina", "contratación"],
    "Diseño Gráfico": ["diseño", "gráfico", "photoshop", "ilustración"],
    "Locutor/Maestro de Ceremonia": ["locución", "ceremonia", "voz", "presentación"],
    "Limpieza": ["limpieza", "mantenimiento", "higiene", "orden"],
    "Secretaría": ["secretaria", "asistente", "organización", "correspondencia"]
}

# Simulación de análisis de Machine Learning
def analyze_cv(file_path, selected_area):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
        
        percentages = {}
        for area, keywords in AREA_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    score += 20  # Aumentar el puntaje por cada coincidencia
            score = min(100, score + random.randint(-10, 10))
            percentages[area] = max(0, score)
        
        score = percentages.get(selected_area, 0)
        passes = score >= 50
        return percentages, passes, score
    except Exception:
        percentages = {area: random.randint(20, 80) for area in AREA_KEYWORDS}
        score = percentages.get(selected_area, 0)
        passes = score >= 50
        return percentages, passes, score

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_cv():
    if 'cv' not in request.files:
        return render_template('index.html', error="No se seleccionó ningún archivo")
    
    file = request.files['cv']
    selected_area = request.form.get('area')
    
    if not selected_area:
        return render_template('index.html', error="Por favor, selecciona un área a la que postulas")
    
    if file.filename == '':
        return render_template('index.html', error="No se seleccionó ningún archivo")
    
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        percentages, passes, score = analyze_cv(file_path, selected_area)
        
        return render_template('result.html', 
                             percentages=percentages, 
                             passes=passes, 
                             score=score, 
                             selected_area=selected_area)
    return render_template('index.html', error="Por favor, sube un archivo PDF")
    
if __name__ == '__main__':
    app.run(debug=True, port=5001)