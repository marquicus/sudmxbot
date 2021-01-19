#
##
##
APPMAIL?="soporte@zentek.com.mx"
GROUPREPO=ztst
NOCLR=\x1b[0m
OKCLR=\x1b[32;01m
ERRCLR=\x1b[31;01m
WARNCLR=\x1b[33;01m
EXECUTABLES=pip python
include .env
export $(shell sed 's/=.*//' .env)
DATABASE=$(firstword $(subst :, ,$(DATABASE_URL)))

define usage =
Build and development task automation tool for project"

Usage:
  make [task]
endef

## Built in tasks ##

#: env - Shows current working environment
env:
	@echo -e "\n\tAvailable Spiders:"
	@echo "`grep "name =" */spiders/*.py | cut -d/ -f3`"
	@echo -e "\n\tDatabase [${OKCLR}${DATABASE}${NOCLR}]\n"

#: help - Show Test info
help: env
	$(info $(usage))
	@echo -e "\n  Available targets:"
	@egrep -o "^#: (.+)" [Mm]akefile  | sed 's/#: /    /'
	@echo "  Please report errors to ${APPMAIL}"

#: check - Check that system requirements are met
check:
	$(info Required: ${EXECUTABLES})
	$(foreach bin,$(EXECUTABLES),\
	    $(if $(shell command -v $(bin) 2> /dev/null),$(info Found `$(bin)`),$(error Please install `$(bin)`)))

# clean-build - Remove build and python files
clean-build:
	@rm -fr .tox/
	@rm -fr *.egg-info
	@rm -rf .pytest_cache
	@rm -rf .scrapy

# clean-pyc - Remove build and python files
clean:
	@find . -name '*.py[cod~]' -exec rm -rf {} +

# populate - Run test from different version managed in tox
populate: env
	@echo "TODO"

#: build-docs - Build docs
build-docs:
	# sphinx-build -b html docs/ docs/_build/ TODO
	@echo "TODO"

# pipdep - Tweak pip dependencies before 20.3+
pipdep:
	@pip install pip==19.3.1  # for now ugly tweak to bypass any reference error

#: dependencies - Install dependencies
dependencies: pipdep
	pip install -r requirements.txt

#: jupyterlab - Runs notebook
jupyterlab: env
	@jupyter lab --ip=0.0.0.0 --no-browser --notebook-dir ./notebook

#: jupyterlab-extensions - Install extensions
jupyterlab-extensions:
	jupyter labextension install jupyterlab-execute-time
	jupyter labextension install @jupyter-widgets/jupyterlab-manager
	jupyter labextension install @jupyterlab/toc
	jupyter labextension install @jupyterlab/debugger
	jupyter labextension install jupyterlab-jupytext
	jupyter labextension install @axlair/jupyterlab_vim
	jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-leaflet
	jupyter labextension install jupyterlab-topbar-extension jupyterlab-system-monitor
	jupyter labextension install @bokeh/jupyter_bokeh
	jupyter labextension install jupyterlab-drawio
	jupyter labextension install @jupyterlab/commenting-extension
	jupyter labextension install @jupyterlab/google-drive

# postgres - Start postgres container
postgres:
	@if [[ ! $$(docker ps -a | grep "${SLUG}-postgres") ]]; then \
		docker run -d --rm --name ${SLUG}-postgres -p ${POSTGRES_PORT}:${POSTGRES_PORT} -e POSTGRES_DB=${POSTGRES_DB} -e POSTGRES_USER=${POSTGRES_USER} -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} postgres:12-alpine; \
	else \
		echo "[${SLUG}-postgres] There is an existing postgres container name, I will use"; \
	fi

#: postgres-stop - Start backend services
postgres-stop:
	if [[ $$(docker ps -a | grep "${SLUG}-postgres") ]]; then \
		docker stop ${SLUG}-postgres; \
	fi;
	@echo "Backend services stopped..."

#: fixtures - Load fixtures
fixtures: env
	@echo "TODO"  # TODO

#: service-start - Initializes task queue in background
service-start: env
	@if [[ ! $$(pgrep scrapyd") ]]; then \
		echo "TODO"; \
	else \
		echo "There is an existing scrapyd service"; \
	fi
	@echo -e "\nTo access manage service use the following command:\n\tTODO"

#: taskqueue-stop - Stop task queue working in background
service-stop:
	@pkill scrapyd

#: shell - Access django admin shell
shell:
	@ipython --matplotlib

#: dbshell - Access database shell
dbshell:
	@echo "TODO"

#: dumpfixture - Dump fixture
dumpfixture:
ifeq ("$(fx)","")
	@echo "Must specify argument: make dumpfixture fx=..."
else
	@echo "Generating fixtures for: $(fx)"
	@echo "TODO"
	@echo "Done."
endif

#: model - Generate database schema
model:
	@echo "Generating models..."
	@python sudmxbot/models.py

#: ddl - Dump database ddl
ddl:
ifeq (${DATABASE},sqlite)
	@sqlite3 db.sqlite3 .schema > fixtures/ddl/ddl.sql3.sql
else
	@pg_dump "${DATABASE_URL}" -s > fixtures/ddl/ddl.sql
endif

#: schema - Dump database schema
schema:
ifeq (${DATABASE},sqlite)
	@sqlite3 db.sqlite3 .schema > fixtures/ddl/schema.sql3.sql
else
	@pg_dump "${DATABASE_URL}" > fixtures/ddl/schema.sql
endif

#: crawl - Run
crawl: env
ifeq ("$(spider)","")
	@echo "Must specify argument: make crawl spider=..."
else
	@echo "Crawling spider: $(spider)"
	@scrapy crawl $(spider)
endif

#: telegram - Long running telegram bot
telegram:
	@echo "Long running telegram bot..."
	@python sudmxbot/msgbots/telegrambot.py

.PHONY: env docs clean
.DEFAULT_GOAL := check
