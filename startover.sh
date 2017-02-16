# zero out the databases - pretty dangerous really

rm ww/migrations/*

# I wanted to use -f startover.sql, but db doesn't mount the directory, and this doesn't seem like important enough to change that.
sudo docker-compose run db psql -h db -U postgres -c "drop table ww_word cascade;"

sudo docker-compose run web python manage.py makemigrations ww 
sudo docker-compose run web python manage.py migrate ww 


# you might need to create a superuser
#docker-compose run web python manage.py createsuperuser
