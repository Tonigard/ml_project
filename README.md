# ml_project
Обертка мл модели


### 1. Тесты
```bash
uv run pytest
```

### 2. Docker Compose
```bash
docker compose up -d --build
```

### 3. Kind
```bash
kind create cluster --name fraud-detection
docker build -t fraud-detection-service:1.0 .
kind load docker-image fraud-detection-service:1.0 --name fraud-detection

# одна команда, проброска секретов
PW=$(openssl rand -hex 16) && kubectl create secret generic fraud-detection-service --from-literal=POSTGRES_PASSWORD="$PW" --from-literal=DATABASE_URL="postgresql://postgres:$PW@postgres:5432/fraud_detection"


kubectl apply -f k8s/

```







![uv pytest](screenshots/pytest.png)

![logs predictions](screenshots/predict_logs.png)

![k9s](screenshots/k9s.png)

![predictions](screenshots/predictions.png)