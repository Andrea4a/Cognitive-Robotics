
first=python3 -m rasa
option:=--debug

duckling:
	docker run -p 8000:8000 rasa/duckling

server:
	$(first) run -m models --endpoints  endpoints.yml --port 5002 --credentials credentials.yml --enable-api

train:
	$(first) train

action:
	$(first) run actions

train_and_actions:train action

shell:
	$(first) shell

shell_debug:
	$(first) shell $(option)

shell_nlu:
	$(first) shell nlu

interactives:
	$(first) interactive

clean:
	./remove_files.sh

test_stories:
	$(first) test core --stories tests/test_stories.yml --out results
