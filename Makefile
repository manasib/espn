.PHONY: all all-unittest install-dependencies run-etl run-backend run-ui run-etl-unittest run-backend-unittest

all: | install-dependencies run-etl run-backend run-ui  

all-unittest: | run-etl-unittest run-backend-unittest

install-dependencies:
	@echo "Installing dependencies for UI..."
	(cd ui && poetry install --no-root)
	@echo "Installing dependencies for Backend..."
	(cd backend && poetry install --no-root)
	@echo "Installing dependencies for Feed ETL..."
	(cd feed_etl && poetry install --no-root)

run-etl:
	@echo "Running ETL..."
	cd feed_etl && PYTHONPATH=${PWD} poetry run python etl.py

run-ui:
	@echo "Running UI..."
	(cd ui && PYTHONPATH=.. poetry run streamlit run ui.py)

run-backend:
	@echo "Running Backend..."
	cd backend && PYTHONPATH=${PWD} poetry run python backend.py &

run-backend-unittest:
	@echo "Running Backend unittest..."
	cd backend && PYTHONPATH=${PWD} poetry run python -m unittest

run-etl-unittest:
	@echo "Running ETL unittest..."
	cd feed_etl && PYTHONPATH=${PWD} poetry run python -m unittest