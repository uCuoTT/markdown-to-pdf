FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    pandoc \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-extra-utils \
    texlive-latex-extra \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

# Install Python dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app .

EXPOSE 5000

CMD ["python", "app.py"]