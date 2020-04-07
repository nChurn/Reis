run tests
 python manage.py test passport_app.tests
 python manage.py test passport_app.tests.test_email
install requirements
    pip freeze > requirements.txt
    pip install -r requirements.txt


#run tasks like rake
python manage.py run_tasks

python manage.py createsuperuser

conda:
conda create --name my_env python=3
Activate the new environment like so:

conda activate my_env
sudo pip install pycurl
conda deactivate
