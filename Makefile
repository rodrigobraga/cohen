build:
	docker-compose build


# utilities
# -----------------------------------------------------------------------------
recreatedb:
	rm -rf cohen/db.sqlite3 cohen/properties/migrations cohen/core/access/migrations
	docker-compose run --rm --user=`id -u` application python manage.py makemigrations core access properties
	docker-compose run --rm --user=`id -u` --no-deps application python manage.py makemigrations --empty properties

createsuperuser:
	docker-compose run --rm application python manage.py createsuperuser --username admin --email admin@nospam.com

dependencies:
	docker-compose run --rm --no-deps application pip list --outdated --format=column

shell:
	docker-compose run --rm --no-deps application python manage.py shell

collectstatic:
	docker-compose run --rm --no-deps application python manage.py collectstatic --clear --no-input -v 3

migrate:
	docker-compose run --rm application python manage.py migrate


# tests and code quality
# -----------------------------------------------------------------------------
test:
	docker-compose run --rm application pytest tests

coverage:
	docker-compose run --rm application pytest tests --cov=core --cov=properties --cov-fail-under=85 tests

codestyle:
	docker-compose run --rm --no-deps application pycodestyle core properties tests --exclude=migrations


# run
# -----------------------------------------------------------------------------
development:
	docker-compose stop
	docker-compose up -d postgres
	docker-compose up nginx

production:
	docker-compose stop
	docker-compose up -d postgres
	docker-compose -f docker-compose.yml -f docker-compose.production.yml run --rm application python manage.py migrate
	docker-compose -f docker-compose.yml -f docker-compose.production.yml run --rm --no-deps application python manage.py collectstatic --clear --no-input -v 0
	docker-compose -f docker-compose.yml -f docker-compose.production.yml up -d  nginx
