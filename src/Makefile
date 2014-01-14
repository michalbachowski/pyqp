test:
	python -B -m pyqp.test

doctest:
	find pyqp -name "*.py" -not -name "test*" -exec python -B -m doctest {} \;

sloc:
	radon raw -s pyqp/*.py

complexity:
	radon cc -a pyqp/*.py

maintability:
	radon mi pyqp/*.py

wc:
	wc -l pyqp/*.py | sort -nr
