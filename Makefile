install:
	./install.sh

install-dev:
	./install-dev.sh

test:
	pytest

fmt:
	black .