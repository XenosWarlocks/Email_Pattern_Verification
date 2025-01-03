

```bash
python api.py
streamlit run streamlit_app.py
```

- Build and run the Docker container:

```bash
docker build -t email-verifier .
docker run -p 5000:5000 email-verifier
```

## For cloud deployment:

1. Heroku:

```bash
# Create a Procfile
echo "web: python app.py" > Procfile
# Deploy
heroku create
git push heroku main
```

2. Google Cloud Run:

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/email-verifier
gcloud run deploy --image gcr.io/PROJECT_ID/email-verifier --platform managed
```

## Directory structure

```
email_verifier/
├── api.py
├── email_verifier.py
├── requirements.txt
├── templates/
│   ├── streamlit_app.py
│   └── index.html
└── Dockerfile
```

```bash
# DockerFile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
# Dockerfile.frontend
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

WORKDIR /app/frontend
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
```bash
# Dockerfile.api
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "api.py"]
```
```bash
# docker-compose.yml
version: '3.8'

services:
  api:
    build: 
      context: .
      dockerfile: Dockerfile.api
    ports:
      - "5000:5000"
    volumes:
      - ./logs:/app/logs
    environment:
      - FLASK_ENV=production

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "8501:8501"
    depends_on:
      - api
    environment:
      - API_URL=http://api:5000
      
```