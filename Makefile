style:
	isort --profile=black ./*.py
	black ./*.py
	flake8 --ignore=E501,W503 --exclude=ordinals-collections,alembic .

check:
	flake8 --ignore=E501,W503 --exclude=ordinals-collections,alembic .
