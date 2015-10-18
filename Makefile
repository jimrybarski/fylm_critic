.PHONY: info build test run shell

info:
	@echo "make build|test|run|shell"

build:
	docker build -t jimrybarski/fylmcritic .

test:	
	docker run --rm -v $(CURDIR):/opt/ -it jimrybarski/fylmcritic python3.4 /opt/tests.py

run:	
	xhost local:root; docker run --rm -v $(CURDIR):/opt/ -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$(DISPLAY) -it jimrybarski/fylmcritic python3.4 /opt/bug.py --verbose-helpful

shell:	
	xhost local:root; docker run --rm -v $(CURDIR):/opt/ -v $(experiment_directory):/var/data -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$(DISPLAY) -it jimrybarski/fylmcritic bash
