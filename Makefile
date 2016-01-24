.PHONY: info build test run shell

info:
	@echo "make build|test|run|shell"

build:
	docker build -t jimrybarski/fylmcritic .

test:	
	docker run --rm -v $(CURDIR):/opt/ -it jimrybarski/fylmcritic python3.5 /opt/tests.py

ftest:	
	xhost local:root > /dev/null; docker run --rm -v $(CURDIR):/opt/ -v /tmp/.X11-unix:/tmp/.X11-unix -v /var/fylmtest:/var/experiment -e DISPLAY=unix$(DISPLAY) -it jimrybarski/fylmcritic python3.5 /opt/ftest.py

shell:	
	xhost local:root > /dev/null; docker run --rm -v $(CURDIR):/opt/ -v /tmp/.X11-unix:/tmp/.X11-unix -v /home/jim/nd2s:/var/nd2s -e DISPLAY=unix$(DISPLAY) -it jimrybarski/fylmcritic bash

py3: 
	xhost local:root > /dev/null; docker run --rm -v $(CURDIR):/opt/ -v /home/jim/nd2s/:/var/nd2s -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$(DISPLAY) -it jimrybarski/fylmcritic bash
