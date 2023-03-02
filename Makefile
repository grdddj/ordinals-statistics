style:
	isort ./*.py
	black ./*.py
	flake8 --ignore=E501 .

check:
	flake8 --ignore=E501 .
