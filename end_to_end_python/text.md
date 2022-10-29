# Comando para rodar a imagem do postgres

docker run -it \
 -e POSTGRES_USER='root' \
 -e POSTGRES_PASSWORD='root' \
 -e POSTGRES_DB='twitter_data' \
 -v $(pwd)/twitter_postgres_data:/var/lib/postgresql/data \
 -p 5432:5432 \
 --network=pg-network \
 --name pg-database3 \
 postgres:13

# Acessar o postgres no CLI

    pgcli -h localhost -p 5432 -u root -d twitter_data

# Rodar o arquivo para teste

python ingest_data.py \
 --host=localhost \
 --port=5432 \
 --user=root \
 --password=root \
 --db=twitter_data \
 --table_name=twitter_data_data \
 --query="#VagasDev"

# Acessar o postgres web com o banco de dados

docker run -it \
 -e PGADMIN_DEFAULT_EMAIL='admin@admin.com' \
 -e PGADMIN_DEFAULT_PASSWORD='root' \
 -p 8080:80 \
 --network=pg-network \
 --name pgadmin-12 \
 dpage/pgadmin4

docker build -t twitter_ingest:v001 .

# Executar o script com a imagem

docker run -it \
 --network=pg-network \
 twitter_ingest:v001 \
 --host=pg-database3 \
 --port=5432 \
 --user=root \
 --password=root \
 --db=twitter_data \
 --table_name=twitter_data_data \
 --query="#VagasDev"

# Iniciar todos os scripts

docker-compose up
docker-compose down
