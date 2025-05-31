docker-compose up --build -d

docker exec spark-worker python /app/setup_s3.py

docker exec spark-worker spark-submit /app/process_routes.py