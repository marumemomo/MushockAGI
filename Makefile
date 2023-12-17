.PHONY: run
run:
	@git checkout main; \
	git pull origin main; \
	while true; do \
		python main.py; \
		sleep 300; \
	done
