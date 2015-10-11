.PHONY: info build test run shell

info:
	@echo "make build|test|run|shell"

build:
	docker build -t jimrybarski/fylmcritic .

test:	
	docker run --rm -v $(CURDIR):/opt/ -it jimrybarski/fylmcritic python3.4 /opt/tests.py

run:	
	docker run --rm -v $(CURDIR):/opt/ -v $(experiment_directory):/var/data -it jimrybarski/fylmcritic python3.4 /opt/run.py

shell:	
	docker run --rm -v $(CURDIR):/opt/ -v $(experiment_directory):/var/data -it jimrybarski/fylmcritic bash
