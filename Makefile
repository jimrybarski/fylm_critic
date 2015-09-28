.PHONY: info build test run

info:
	@echo "make build|test|run"

build:
	docker build -t jimrybarski/fylmcritic .

test:	build
	docker run --rm -v ~/code/fylm3:/opt/ -it jimrybarski/fylmcritic python3.4 /opt/tests.py

run:	build
	docker run --rm -v ~/code/fylm3:/opt/ -v $(experiment_directory):/var/data -it jimrybarski/fylmcritic python3.4 /opt/run.py

shell:	build
	docker run --rm -v ~/code/fylm3:/opt/ -v $(experiment_directory):/var/data -it jimrybarski/fylmcritic bash
