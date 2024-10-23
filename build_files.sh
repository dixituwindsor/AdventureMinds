echo "BUILD START"
python3 -m pip install -r requirements.txt
python3 manage.py collectstatic --noinput --clear
mv staticfiles_build/static public/
echo "BUILD END"
