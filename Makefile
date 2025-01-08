build:
	poetry build
publish:
	poetry publish --dry-run
package-install:
	python3 -m pip install --user dist/*.whl --force
lint:
	poetry run flake8 simplecrud
coverage:
	poetry run pytest --cov=simplecrud --cov-report=xml
