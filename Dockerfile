FROM python:3.9-slim

# Installiamo TUTTO quello che serve per evitare errori di stile o font mancanti
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    pandoc \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-plain-generic \
    fonts-liberation \
    lmodern \
    texlive-latex-extra && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 5000

CMD ["python", "app.py"]