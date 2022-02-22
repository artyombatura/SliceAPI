## To start the project you need to:

1. Create virtual environment:

> python3 -m venv env

2. Activate virtual environment:

> source env/bin/activate

3. Install dependencies:
 
> pip install -r requirements.txt

4. Move to silce_api/ folder:

> cd slice_api/

5. Apply migrations:

> python manage.py migrate

7. Full database with data (optionally):

> python manage.py loaddata fixtures.json 

8. Create superuser to use admin panel:

> python manage.py createsuperuser

10. Run server:

> python manage.py runserver

11. Run tests (optionally):

> pytest