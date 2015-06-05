build:
	docker build -t jimrybarski/fylmcritic .

test:
	docker run -it jimrybarski/fylmcritic python3.4 /opt/tests.py

run:
	docker run -it jimrybarski/fylmcritic python3.4 /opt/run.py $(data_dir) $(data_date)
