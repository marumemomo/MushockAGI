.PHONY: run
run:
	@while true; do \
		git checkout main; \
		git pull origin main; \
		python main.py; \
		sleep 300; \
	done
