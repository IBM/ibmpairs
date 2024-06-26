#===============================================================
# IBM Confidential
#
# OCO Source Materials
#
# Copyright IBM Corp. 2021
#
# The source code for this program is not published or otherwise
# divested of its trade secrets, irrespective of what has been
# deposited with the U.S. Copyright Office.
#===============================================================

PYTHON_ENV:="/usr/bin/python"

test: ## Runs unit tests
test:
	@echo 'Running unit tests ...'
	@if $(PYTHON_ENV) -m pytest tests/test_authentication.py; then exit 0; else exit 1; fi
	@if $(PYTHON_ENV) -m pytest tests/test_catalog.py; then exit 0; else exit 1; fi
	@if $(PYTHON_ENV) -m pytest tests/test_client.py; then exit 0; else exit 1; fi
	@if $(PYTHON_ENV) -m pytest tests/test_common.py; then exit 0; else exit 1; fi
	@if $(PYTHON_ENV) -m pytest tests/test_query.py; then exit 0; else exit 1; fi
	@if $(PYTHON_ENV) -m pytest tests/test_upload.py; then exit 0; else exit 1; fi

test-authentication: ## Runs authentication unit tests
test-authentication:
	@echo 'Running authentication unit tests ...'
	@if $(PYTHON_ENV) -m pytest tests/test_authentication.py; then exit 0; else exit 1; fi

test-catalog: ## Runs catalog unit tests
test-catalog:
	@echo 'Running unit tests ...'
	@if $(PYTHON_ENV) -m pytest tests/test_catalog.py; then exit 0; else exit 1; fi
	
test-client: ## Runs client unit tests
test-client:
	@echo 'Running unit tests ...'
	@if $(PYTHON_ENV) -m pytest tests/test_client.py; then exit 0; else exit 1; fi

test-common: ## Runs common unit tests
test-common:
	@echo 'Running unit tests ...'
	@if $(PYTHON_ENV) -m pytest tests/test_common.py; then exit 0; else exit 1; fi

test-query: ## Runs query unit tests
test-query:
	@echo 'Running query unit tests ...'
	@if $(PYTHON_ENV) -m pytest tests/test_query.py; then exit 0; else exit 1; fi

test-upload: ## Runs upload unit tests
test-upload:
	@echo 'Running upload unit tests ...'
	@if $(PYTHON_ENV) -m pytest tests/test_upload.py; then exit 0; else exit 1; fi

docker-build: ## Builds docker container
docker-build:
	@echo 'Building docker container ibmpairs'
	@docker build -t ibmpairs .

docker-run: ## Runs ibmpairs container
docker-run:
	@echo 'Running docker container ibmpairs on port 18380'
	@docker run -dit -p 18380:18380 --name ibmpairs ibmpairs:latest

doc: ## Create SDK documentation
doc:
	@echo 'Creating ibmpairs SDK docs'
	@rm -rf sphinx/build
	@rm -rf sphinx/source/tutorials
	@pip install -r requirements-development.txt
	@mkdir -p sphinx/source/tutorials
	@cp -R tutorials/notebooks/* sphinx/source/tutorials
	@cd sphinx && make html

pages: # Copy sphinx/build/html to docs to create GitHub pages 
pages:
	@echo 'Copying documentation to docs'
	@cp -r sphinx/build/html/* docs 
