.PHONY: all

all:
	./actor_parser.py actor_dictionary_city.csv --label=city
	./actor_parser.py actor_dictionary_police.csv --label=police
	./actor_parser.py actor_dictionary_protesters.csv --label=protesters
	./actor_parser.py actor_dictionary_independent.csv --label=independent
