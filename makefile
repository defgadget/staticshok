run:
	python src/main.py
	python server.py --dir public

test:
	python -m unittest discover -s src
