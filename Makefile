.PHONY: all actor_json actor_replacement word_replacement clean
SHELL = /bin/bash


ACTOR_DICTS = $(wildcard actor_dictionary_*.csv)
ACTOR_JSON = $(ACTOR_DICTS:%.csv=output_%.json)

all: actor_json actor_replacement word_replacement

output_%.json: %.csv
	python3 actor_parser.py $< --label=$(subst actor_dictionary_,,$(basename $<))

actor_json: $(ACTOR_JSON)

actor_replacement:
	@cp Protester.jsonl output.jsonl ; \
	for actor in output_actor_dictionary_*.json; do \
		echo -e "\n\n---> Actor replacement: $$actor\n\n"; \
		python3 actor_replacement_json.py output.jsonl $$actor; \
		mv output_output.jsonl output.jsonl ;\
	done

word_replacement:
	@echo -e "\n\nWord to actor, word to word replacement...\n\n"
	python3 actor_replacement.py output.jsonl words_to_actor.csv words_to_words.csv
	@mv output_output.jsonl final_output.jsonl
	@echo -e "\n\nResults in: final_output.jsonl"

clean:
	rm $(ACTOR_JSON)
