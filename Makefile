# convenience makefile to build the dev env and run common commands
.EXPORT_ALL_VARIABLES:

all: .installed

install:
	@rm -f .installed  # force re-install
	@make .installed

.installed: poetry.lock
	@echo "poetry(.lock) is newer than .installed, (re)installing"
	@poetry install
	@poetry run pre-commit install -f --hook-type pre-commit
	@poetry run pre-commit install -f --hook-type pre-push
	@echo "This file is used by 'make' for keeping track of last install time. If Pipfile or Pipfile.lock are newer then this file (.installed) then all 'make *' commands that depend on '.installed' know they need to run poetry install first." \
		> .installed

# Run validaion
validate: .installed
	@poetry run python .circleci/validate.py

# Testing and linting targets
lint: .installed
	@poetry run pre-commit run --all-files --hook-stage push

type: types
types: .installed
	@poetry run mypy .circleci/*.py

sort: .installed
	@poetry run isort -rc --atomic .circleci/*.py

fmt: format
black: format
format: .installed sort
	@poetry run black .circleci/*.py

clean:
	@rm -rf .venv
	@rm -rf .git/hooks/pre-commit .git/hooks/pre-push
	@rm -f .installed

gen: codegen
	poetry run python .circleci/csv2html.py csv/electronics.csv Countries/.common/electronics
	poetry run python .circleci/csv2html.py csv/bookstore.csv Countries/.common/bookstore
	poetry run python .circleci/csv2html.py csv/toys.csv Countries/.common/toys
	poetry run python .circleci/csv2html.py csv/jewellery.csv Countries/.common/jewellery

optimize:
	find Countries/.common/ -iname "*.jpg" -exec convert {} -resize 960x960\> {} \;
	jpegoptim  --all-progressive --strip-all -m75 -o -t Countries/.common/*/*.jpg

codegen:
	poetry run python .codegen/update_const.py
