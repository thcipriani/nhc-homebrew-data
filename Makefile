HEADERS ?= ""
default: nhc.db

tmp/winners.html:
	curl -s \
		-o $@ \
		-d 'action=post_search' \
		-d 'post_type=recipes' \
		-d 'winnersOnly=true' \
		-XPOST http://www.homebrewersassociation.org/wp-admin/admin-ajax.php

tmp/id_list.txt: tmp/winners.html
	pup '.list-group-item attr{id}' < $< > $@

nhc.db: tmp/id_list.txt
	/usr/bin/env python2 create_db.py "$(HEADERS)"
