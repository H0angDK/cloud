from opensearchpy import OpenSearch, helpers
import csv

# Подключение к OpenSearch
client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    http_compress=True,
    use_ssl=False,
    verify_certs=False
)

# Создание индекса
index_name = "flights"
index_body = {
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    },
    "mappings": {
        "properties": {
            "id": {"type": "integer"},
            "Airline": {"type": "keyword"},
            "Flight": {"type": "keyword"},
            "AirportFrom": {"type": "keyword"},
            "AirportTo": {"type": "keyword"},
            "DayOfWeek": {"type": "byte"},
            "Time": {"type": "integer"},
            "Length": {"type": "integer"},
            "Delay": {"type": "boolean"}
        }
    }
}

client.indices.create(index_name, body=index_body)

# Загрузка данных из CSV
def generate_data():
    with open('./data/Airlines.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield {
                "_index": index_name,
                "_id": row['id'],
                "_source": {
                    "id": int(row['id']),
                    "Airline": row['Airline'],
                    "Flight": row['Flight'],
                    "AirportFrom": row['AirportFrom'],
                    "AirportTo": row['AirportTo'],
                    "DayOfWeek": int(row['DayOfWeek']),
                    "Time": int(row['Time']),
                    "Length": int(row['Length']),
                    "Delay": bool(int(row['Delay']))
                }
            }

helpers.bulk(client, generate_data())
print(f"Данные загружены в индекс {index_name}")