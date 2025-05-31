# Инструкция по запуску проекта

## Предварительные требования

- Docker
- Python 3.x
- pip (менеджер пакетов Python)

## Установка и запуск

### Linux

1. **Запуск обучения модели**
```bash
# Определяем текущий путь
parent_path=$(pwd)

# Запускаем обучение модели
docker run \
    -v ${parent_path}/data:/data  \
    -v ${parent_path}/config:/config \
    -v ${parent_path}/models:/models \
    ludwigai/ludwig:master \
    experiment --config /config/config.yaml \
        --dataset /data/Airlines.csv \
        --output_directory /models
```

2. **Запуск LocalStack**
```bash
docker run \
  --rm -it \
  -p 127.0.0.1:4566:4566 \
  -p 127.0.0.1:4510-4559:4510-4559 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  localstack/localstack
```

3. **Установка AWS CLI Local**
```bash
pip install awscli-local
```

4. **Создание S3 бакета и загрузка модели**
```bash
# Создаем бакет
awslocal s3api create-bucket --bucket ludwig

# Указываем путь к папке с моделью
LUDWIG_EXPERIMENT_FOLDER="experiment_run"  # Замените на вашу папку
parent_path=$(pwd)
LOCAL_MODEL_DIR="${parent_path}/models/${LUDWIG_EXPERIMENT_FOLDER}/model"
S3_TARGET_PATH="s3://ludwig/trained_models/"

# Загружаем модель в S3
awslocal s3 cp "${LOCAL_MODEL_DIR}" "${S3_TARGET_PATH}" --recursive --exclude "*.DS_Store*"
```

5. **Запуск предсказаний**
```bash
docker run \
  -v ${parent_path}/data:/data \
  -v ${parent_path}/result:/result \
  -e AWS_ENDPOINT_URL=http://localhost.localstack.cloud:4566 \
  -e AWS_ACCESS_KEY_ID=test \
  -e AWS_SECRET_ACCESS_KEY=test \
  -e AWS_DEFAULT_REGION=us-east-1 \
  -e S3_USE_SSL=false \
  -e S3_VERIFY_SSL=false \
  --network="host" \
  ludwigai/ludwig:master \
  predict \
  --model_path "${S3_TARGET_PATH}" \
  --dataset /data/Airlines.test.hdf5 \
  --output_directory /result
```

6. **Запуск OpenSearch**
```bash
docker run -p 9200:9200 -p 9600:9600 \
-e "discovery.type=single-node" \
-e "plugins.security.disabled=true" \
-e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=coRrecth0rseba++ery9.23.2007staple$" \
opensearchproject/opensearch:latest
```

7. **Установка OpenSearch Python клиента и запуск приложения**
```bash
pip install opensearch-py
python launch.py
```

### Windows

1. **Запуск обучения модели**
```powershell
# Определяем текущий путь
$parent_path = (Get-Location).Path

# Запускаем обучение модели
docker run `
    -v ${parent_path}/data:/data  `
    -v ${parent_path}/config:/config `
    -v ${parent_path}/models:/models `
    ludwigai/ludwig:master `
    experiment --config /config/config.yaml `
        --dataset /data/Airlines.csv `
        --output_directory /models
```

2. **Запуск LocalStack**
```powershell
docker run `
  --rm -it `
  -p 127.0.0.1:4566:4566 `
  -p 127.0.0.1:4510-4559:4510-4559 `
  -v /var/run/docker.sock:/var/run/docker.sock `
  localstack/localstack
```

3. **Установка AWS CLI Local**
```powershell
pip install awscli-local
pip install awscli
```

4. **Создание S3 бакета и загрузка модели**
```powershell
# Создаем бакет
awslocal s3api create-bucket --bucket ludwig

# Указываем путь к папке с моделью
$LUDWIG_EXPERIMENT_FOLDER = "experiment_run"  # Замените на вашу папку
$parent_path = (Get-Location).Path
$LOCAL_MODEL_DIR = "${parent_path}/models/${LUDWIG_EXPERIMENT_FOLDER}/model"
$S3_TARGET_PATH = "s3://ludwig/trained_models/"

# Загружаем модель в S3
awslocal s3 cp "${LOCAL_MODEL_DIR}" "${S3_TARGET_PATH}" --recursive --exclude "*.DS_Store*"
```

5. **Запуск предсказаний**
```powershell
docker run `
  -v ${parent_path}/data:/data `
  -v ${parent_path}/result:/result `
  -e AWS_ENDPOINT_URL=http://localhost.localstack.cloud:4566 `
  -e AWS_ACCESS_KEY_ID=test `
  -e AWS_SECRET_ACCESS_KEY=test `
  -e AWS_DEFAULT_REGION=us-east-1 `
  -e S3_USE_SSL=false `
  -e S3_VERIFY_SSL=false `
  --network="host" `
  ludwigai/ludwig:master `
  predict `
  --model_path "${S3_TARGET_PATH}" `
  --dataset /data/Airlines.test.hdf5 `
  --output_directory /result
```

6. **Запуск OpenSearch**
```powershell
docker run -p 9200:9200 -p 9600:9600 `
-e "discovery.type=single-node" `
-e "plugins.security.disabled=true" `
-e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=coRrecth0rseba++ery9.23.2007staple$" `
opensearchproject/opensearch:latest
```

7. **Установка OpenSearch Python клиента и запуск приложения**
```powershell
pip install opensearch-py
python launch.py
```

## Проверка работы

### Поиск рейсов из определенного аэропорта
```bash
curl -XGET "http://localhost:9200/flights/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "term": {
      "AirportFrom": "SFO"
    }
  }
}'
```

### Получение средней длительности полета
```bash
curl -XGET "http://localhost:9200/flights/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "aggs": {
    "avg_flight_length": {
      "avg": { "field": "Length" }
    }
  }
}'
```

## Примечания

- Убедитесь, что все необходимые порты (4566, 4510-4559, 9200, 9600) свободны перед запуском
- В Windows используйте PowerShell для выполнения команд
- При возникновении проблем с правами доступа в Linux, возможно, потребуется использовать `sudo`
- Убедитесь, что Docker запущен перед выполнением команд 