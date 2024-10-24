echo "BUILD START"
python3 -m pip install -r requirements.txt
echo "Fetching db.sqlite3 from GitHub"
curl -o db.sqlite3 https://raw.githubusercontent.com/dixituwindsor/AdventureMinds/dixit/db.sqlite3
# Move it to a writable directory, such as /tmp
mv db.sqlite3 /tmp/db.sqlite3

# Modify the Django settings to point to this new location
sed -i 's#NAME": "db.sqlite3"#NAME": "/tmp/db.sqlite3"#' AdventureMinds/settings.py
python3 manage.py collectstatic --noinput --clear
mv staticfiles_build/static public/
echo "BUILD END"