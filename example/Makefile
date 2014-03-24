fix_pythonpath=export PYTHONPATH=$$(perl -MCwd=realpath -e "print realpath '../src/'")":$$PYTHONPATH" &&

test:
	$(fix_pythonpath) python -B test.py

simple:
	$(fix_pythonpath) python -B simple.py
