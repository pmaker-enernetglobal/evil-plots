#
# names - a python module implementing the ASIM naming convention
#

.PHONY: all check clean lint 

all:	check
	./names.py gridscape.csv gridscape.txt

check:
	# --full-trace --verbose
	pytest --capture=no --doctest-modules --maxfail=1 \
		--hypothesis-show-statistics examples.py

clean:
	@echo skip

lint:
	flake8 names.py

pylint: # pylint is a bit of a fascist so its unused for now
	pylint names.py




