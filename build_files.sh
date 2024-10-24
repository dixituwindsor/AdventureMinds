echo "BUILD START"
python3 -m pip install -r requirements.txt
echo "Fetching db.sqlite3 from GitHub"
curl -o db.sqlite3 https://raw.githubusercontent.com/dixituwindsor/AdventureMinds/dixit/db.sqlite3
chmod 777 db.sqlite3
python3 manage.py collectstatic --noinput --clear
mv staticfiles_build/static public/
echo "BUILD END"