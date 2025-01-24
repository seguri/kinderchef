echo '-----> migrate'
python manage.py migrate --no-input
echo '-----> compilemessages'
python manage.py compilemessages
echo '-----> collectstatic'
python manage.py collectstatic --no-input
echo '-----> fix permissions'
chmod +x manage.py
