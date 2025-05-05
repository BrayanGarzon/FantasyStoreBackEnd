init:
	test -n "$(name)"
	rm -rf ./.git
	find ./ -type f -exec perl -pi -e 's/FantasyStore/$(name)/g' *.* {} \;
	mv ./FantasyStore ./$(name)

superuser:
	docker exec -it FantasyStore ./manage.py createsuperuser

shell:
	docker exec -it FantasyStore ./manage.py shell

enter:
	docker exec -it FantasyStore bash

makemigrations:
	docker exec -it FantasyStore ./manage.py makemigrations

migrate:
	docker exec -it FantasyStore ./manage.py migrate

initialfixture:
	docker exec -it FantasyStore ./manage.py loaddata initial

testfixture:
	docker exec -it FantasyStore ./manage.py loaddata test

test:
	docker exec -it FantasyStore ./manage.py test

collectstatic:
	docker exec -it FantasyStore ./manage.py collectstatic --noinput

makemessages:
	docker exec -it FantasyStore django-admin makemessages

compilemessages:
	docker exec -it FantasyStore django-admin compilemessages