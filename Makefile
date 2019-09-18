run-mysql:
	docker run \
		--name mysql \
		--rm \
		-p 3306:3306 \
		--detach \
		--env MYSQL_ALLOW_EMPTY_PASSWORD=true \
		--env MYSQL_USER=user \
		--env MYSQL_PASSWORD=user123 \
		--env MYSQL_DATABASE=mglu \
		--volume "$(PWD):/mnt/host" \
		mysql:5.7

stop-mysql:
	docker stop mysql

setup-mysql:
	docker exec -it mysql /mnt/host/setup-sql.sh

install-deps:
	pip3 install -r requirements.txt

run:
	python3 app.py