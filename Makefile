.PHONY: install run lint test docker-build

install:
	pip install -r requirements.txt

run:
	uvicorn src.app.main:app --host 0.0.0.0 --port 8000

lint:
	ruff src tests

test:
	pytest -q

docker-build:
	docker build -t quiz-solver:latest -f docker/Dockerfile .
