# 2.1
https://github.com/Tonigard/ml_project/actions/runs/40132703458

docker pull ghcr.io/tonigard/fraud-detection-services/sha-d338e80b3f3532b3a45d59437cc68c8e4e7ced36:latest

# 2.2
https://github.com/Tonigard/ml_project/pull/2

# 2.3
https://github.com/Tonigard/ml_project/actions/runs/40136800520/job/121000225093

Падает smoke test джоба деплой. Тесты проходит потому что дефолтные значения корреткные. При поднятии кластера уже берутся переменные из конфиг мапы.
FileNotFoundError: [Errno 2] No such file or directory: 'artifacts/fraud_detection_salam.pkl'

