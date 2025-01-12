# kinderchef

## Piku

### First deployment

- Create Procfile
- Create ENV
- Update settings.py
- Open port 80 in the firewall to allow the Let's Encrypt challenge
- Make sure you can compile psycopg2 by running `apt install build-essential python3-dev libpq-dev`
- Execute my custom plugin `ssh piku@example.com postgres:create kinderchef`
- Configure remote with `just add-remote`
- Deploy with `git push piku main`
- `kinderchef` now appears among `ssh piku@example.com apps`
- Replace `SECRET_KEY` with `ssh piku@CHANGEME config:set kinderchef DJANGO_SECRET_KEY=CHANGEME`
- Create a superuser with `just createsuperuser`
