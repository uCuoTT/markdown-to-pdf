import os
import subprocess
import redis
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp'
cache = redis.Redis(host='redis-db', port=6379, socket_timeout=3)

@app.route('/', methods=['GET', 'POST'])
def index():
    count = 0
    try:
        val = cache.get('conversions')
        if val: count = int(val)
    except:
        count = "N/A"

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Nessun file caricato', 400
        
        file = request.files['file']
        if file.filename == '':
            return 'Nome file vuoto', 400

        output_format = request.form.get('format', 'pdf')
        input_path = os.path.join(UPLOAD_FOLDER, 'input.md')
        
        # Nome file interno (non importa l'estensione qui, pandoc la gestisce)
        output_filename = f'output.{output_format}'
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        
        file.save(input_path)

        cmd = ['pandoc', input_path, '-o', output_path]

        # Definizione MIME Type corretti
        mimetype = 'application/pdf' # Default

        if output_format == 'pdf':
            cmd.extend(['--pdf-engine=xelatex', '--variable', 'mainfont=Liberation Serif'])
            mimetype = 'application/pdf'
        elif output_format == 'docx':
            mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif output_format == 'html':
            cmd.append('--standalone') # Importante per avere <html> e <body>
            mimetype = 'text/html'

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            try:
                cache.incr('conversions')
            except:
                pass

            # Inviamo il file specificando il tipo corretto!
            return send_file(
                output_path, 
                as_attachment=True, 
                download_name=f'documento_convertito.{output_format}',
                mimetype=mimetype
            )

        except subprocess.CalledProcessError as e:
            print("ERRORE PANDOC:", e.stderr)
            return f"Errore conversione: {e.stderr}", 500

    return render_template('index.html', count=count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)