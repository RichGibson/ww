Wordwander

docker-compose up
#docker-compose run db psql -h db -U postgres
(database postgres created by default)

docker-compose run web python manage.py createsuperuser


MVP:
1. Enter source info, and paste text or upload file and get a source with words.
2. source list - one source
2. source list - list all sources.

Tasks:
-unicode issues with import/insert into db



Accomplishments
-data_word.py loads text files into source nad words.
-list_sources does it
-show_source shows a source but all fucked up in formatting.
next: probably unicode, or maybe the add.

