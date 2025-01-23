set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

python_dir := "venv/" + if os_family() == "windows" { "Scripts" } else { "bin" }
python := python_dir + if os_family() == "windows" { "/python.exe" } else { "/python3" }

server := "CHANGEME"
appname := "kinderchef"
appdir := "/home/piku/.piku/apps/" + appname

export PIKU_SERVER := 'piku@{{server}}'

system-info:
    @echo "This is an {{arch()}} machine,"
    @echo "With {{num_cpus()}} CPUs,"
    @echo "Running on {{os()}} ({{os_family()}})."

add-remote:
    git remote add piku piku@{{server}}:{{appname}}

deploy:
    git push -f piku main

restart:
    ssh.exe piku@{{server}} restart {{appname}}

createdb:
    ssh.exe piku@{{server}} postgres:create {{appname}}

createsuperuser:
    ssh.exe -t piku@{{server}} run {{appname}} -- ./manage.py createsuperuser --username CHANGEME --email admin@example.com --no-input
    ssh.exe -t piku@{{server}} run {{appname}} -- ./manage.py changepassword CHANGEME

logs:
    ssh.exe piku@{{server}} logs {{appname}}

nginx-logs:
    ssh.exe -t root@{{server}} -- 'multitail /var/log/nginx/access.log /var/log/nginx/error.log'

format:
    {{python}} -m black .

dev:
    {{python}} manage.py runserver

test:
    pytest -s

install:
    {{python}} -m pip install -U pip
    {{python}} -m pip install -r requirements.txt

migrate:
    {{python}} manage.py makemigrations
    {{python}} manage.py migrate

makemessages:
    {{python}} manage.py makemessages -l de -l it

compilemessages:
    {{python}} manage.py compilemessages

repo:
    Start-Process "https://github.com/seguri/{{appname}}"

dumpdata:
    ssh.exe piku@{{server}} run {{appname}} -- './manage.py dumpdata --natural-foreign --natural-primary --format=json --indent=2'

fixperms:
    ssh.exe root@{{server}} -- 'chmod 744 {{appdir}}/manage.py; chown -R piku:www-data {{appdir}}/db.sqlite3'
