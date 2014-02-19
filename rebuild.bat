python manage.py sqlclear app1 app2 appN | sed -n "2,$p" | sed -n "$ !p" | sed "s/";/" CASCADE;/" | sed -e "1s/^/BEGIN;/" -e "$s/$/COMMIT;/" | python manage.py dbshell
python manage.py syncdb

pause  