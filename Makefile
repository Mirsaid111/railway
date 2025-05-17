build:
	docker compose up --build
up:
	docker compose up
down:
	docker compose down
test:
	docker compose exec backend pytest src/medbook/tests/ -v --color=yes	
# restart:
#     down up
logs-frontend:
	docker logs medbook-frontend-1 --tail=100 -f
logs-backend:
	docker logs medbook-backend-1 --tail=100 -f
logs-db:
	docker logs medbook-db-1 --tail=100 -f
shell-backend:
	docker exec -it medbook-backend-1 sh
status:
	docker ps --filter "name=medbook-*"