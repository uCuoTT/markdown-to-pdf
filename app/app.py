import os
import subprocess
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Nessun file caricato', 400
        file = request.files['file']
        if file.filename == '':
            return 'Nome file vuoto', 400

        # 1. Salva il file Markdown caricato
        input_path = os.path.join(UPLOAD_FOLDER, 'input.md')
        output_path = os.path.join(UPLOAD_FOLDER, 'output.pdf')
        file.save(input_path)

        # 2. Esegue il comando PANDOC (il cuore del progetto)
        # Questo comando funziona solo perché siamo nel container giusto!
        try:
            subprocess.run(
                ['pandoc', input_path, '-o', output_path], 
                check=True
            )
        except subprocess.CalledProcessError as e:
            return f"Errore nella conversione: {e}", 500

        # 3. Restituisce il PDF
        return send_file(output_path, as_attachment=True, download_name='documento.pdf')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)