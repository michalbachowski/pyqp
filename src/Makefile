doctest:
	find pyqp -name "*.py" -not -name "test*" -exec python -B -m doctest {} \;

sloc:
	radon raw -s pyqp/

complexity:
	radon cc -a pyqp/

maintability:
	radon mi pyqp/

wc:
	wc -l pyqp/*.py pyqp/*/*.py | sort -nr
