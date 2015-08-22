build:
	docker build -t jimrybarski/fylmcritic .

test:	build
	docker run -it jimrybarski/fylmcritic python3.4 /opt/tests.py

run:	build
	docker run -it -v $(experiment_directory):/var/data jimrybarski/fylmcritic python3.4 /opt/run.py
