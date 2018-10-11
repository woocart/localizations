# convenience makefile to build the dev env and run common commands
.EXPORT_ALL_VARIABLES:
PIPENV_VENV_IN_PROJECT = 1
PIPENV_IGNORE_VIRTUALENVS = 1

all: .installed

install:
	@rm -f .installed  # force re-install
	@make .installed

.installed: Pipfile Pipfile.lock
	@echo "Pipfile(.lock) is newer than .installed, (re)installing"
	@pipenv install --dev
	@pipenv run pre-commit install -f --hook-type pre-commit
	@pipenv run pre-commit install -f --hook-type pre-push
	@echo "This file is used by 'make' for keeping track of last install time. If Pipfile or Pipfile.lock are newer then this file (.installed) then all 'make *' commands that depend on '.installed' know they need to run pipenv install first." \
		> .installed

# Run validaion
validate: .installed
	@pipenv run python .travis/validate.py

# Testing and linting targets
lint: .installed
	@pipenv run pre-commit run --all-files --hook-stage push

type: types
types: .installed
	@pipenv run mypy .travis/*.py

sort: .installed
	@pipenv run isort -rc --atomic .travis/*.py

fmt: format
black: format
format: .installed sort
	@pipenv run black .travis/*.py

clean:
	@if [ -d ".venv/" ]; then pipenv --rm; fi
	@rm -rf .git/hooks/pre-commit .git/hooks/pre-push
	@rm -f .installed

gen:
	pipenv run python .travis/csv2html.py csv/electronics.csv Countries/.common/electronics
	pipenv run python .travis/csv2html.py csv/bookstore.csv Countries/.common/bookstore
	pipenv run python .travis/csv2html.py csv/toys.csv Countries/.common/toys
	pipenv run python .travis/csv2html.py csv/jewellery.csv Countries/.common/jewellery


optimize:
	jpegoptim  --all-progressive --strip-all -m75 -o -t Countries/.common/*/*.jpg
