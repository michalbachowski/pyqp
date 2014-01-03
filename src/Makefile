test:
	python -B -m pyqp.test

doctest:
	find pyqp -name "*.py" -not -name "test*" -exec python -B -m doctest {} \;

wc:
	wc -l pyqp/*.py | sort -nr
