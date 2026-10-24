# 2.1
https://github.com/Tonigard/ml_project/actions/runs/40132703458

docker pull ghcr.io/tonigard/fraud-detection-services/sha-d338e80b3f3532b3a45d59437cc68c8e4e7ced36:latest

# 2.2
https://github.com/Tonigard/ml_project/pull/2

# 2.3

# config
https://github.com/Tonigard/ml_project/actions/runs/40136800520/job/121000225093

Падает smoke test джоба деплой. Тесты проходит потому что дефолтные значения корреткные. При поднятии кластера уже берутся переменные из конфиг мапы.
FileNotFoundError: [Errno 2] No such file or directory: 'artifacts/fraud_detection_salam.pkl'

https://github.com/Tonigard/ml_project/actions/runs/40137496770

# secret

https://github.com/Tonigard/ml_project/actions/runs/40138041552

Контейнер не может стартовать потому что не находит нужных секрктов

https://github.com/Tonigard/ml_project/actions/runs/40138756321

Found 2 pods, using pod/fraud-detection-service-555b8d645f-l4bbb
Error from server (BadRequest): container "api" in pod "fraud-detection-service-555b8d645f-l4bbb" is waiting to start: CreateContainerConfigError