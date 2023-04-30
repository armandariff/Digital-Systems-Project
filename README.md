# Armand Ariff Bin Abdul Razak (19046705)
# Digital-Systems-Project - Movie Recommendation System
This is my Final Year Project for a Movie Recommendation System 


## Instructions on how to run the server with the CSV file:
Open the project in VSCode
Install Prerequisites onto your machine:  
  pip install -r "requirements.txt"

Apply pending migrations to database:  
  python manage.py migrate

Run the Web Server:  
  python manage.py runserver

Load The .CSV data file (make sure the data file is in the same directory):  
  python manage.py load_movies data.csv

To access the admin panel after loading server:  
  python manage.py createsuperuser  
Then follow instructions shown on the terminal  
Access admin panel by directing to http://127.0.0.1:8000/admin
