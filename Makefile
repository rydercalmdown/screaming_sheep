PI_IP_ADDRESS=10.0.2.224
PI_USERNAME=ryder

.PHONY: run
run:
	@cd src && python app.py

.PHONY: install
install:
	@cd scripts && bash install.sh

.PHONY: copy
copy:
	@rsync -a $(shell pwd) --exclude env $(PI_USERNAME)@$(PI_IP_ADDRESS):/home/$(PI_USERNAME)

.PHONY: shell
shell:
	@ssh $(PI_USERNAME)@$(PI_IP_ADDRESS)

.PHONY: ssh
ssh:
	@make shell

.phony: ping
ping:
	@ping $(PI_IP_ADDRESS)
