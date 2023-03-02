style:
	isort --profile=black ./*.py
	black ./*.py
	flake8 --ignore=E501,W503 .

check:
	flake8 --ignore=E501,W503 .
