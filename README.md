Wordwander

docker-compose up
#docker-compose run db psql -h db -U postgres
(database postgres created by default)

docker-compose run web python manage.py createsuperuser


MVP:
1. Enter source info, and paste text or upload file and get a source with words.
(currenty 'works' via command line)

works 2. source list - one source
works 3. source list - list all sources.



Tasks:

unicode sort of works now. total hack
    -lives of others.srt appears to be latin-1, others are utf-8 fuck.
    -unicode issues with import/insert into db-sort of works, 

have now-need word view
-need word lookup, enter a word and get word view.
-noun version, article noun(ending) do the right thing.

-users
-check boxes! for 'ignore' and 'know'
-add number of words per source to list_sources



Accomplishments
-data_word.py loads text files into source nad words.
-list_sources does it
-show_source shows a source but all fucked up in formatting.
next: probably unicode, or maybe the add.

