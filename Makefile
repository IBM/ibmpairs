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
