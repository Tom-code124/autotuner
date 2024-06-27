# Autotuner

Autotuner is an ongoing distributed platform project for vehicle software technicians to accept files and get payments from their customers. The system consists of 2 applications: Autodata and Autoremover. Autodata is the service for supplying vehicle related data. Autoremover is the main service that is used by the employees and the customers.

# Requirements

You should have PostgreSQL 14.12, Python 3.10, and npm 10.7 installed on your system.

# Data

There are raw vehicle data in the data directory. Also, you can find the postgresql db dump there too. You have to insert the data to the database before running the system.

# Environment

You can find the example activate files in the venv_activate_files directory. You can make use of them while configuring your environment duing setup.

# Setup

1. Clone the repository

2. Create a postgresql database for autodata app

3. Create a postgresql database for autoremover app

4. Create a virtual environment for autodata app with Python 3.10

5. Set the necessary environment variables for autodata app (check below for more info)

6. Create a virtual environment for autoremover app with Python 3.10

7. Set the necessary environment variables for autoremover app (check below for more info)

8. Activate autodata environment.

9. Change directory to autodata.

10. Install the required packages listed in requirements.txt file.

11. Make autodata migrations by running:

```bash
python manage.py makemigrations
```

11. Migrate to autodata database by running:

```bash
python manage.py migrate
```

12. Create admin user by running:

```bash
python manage.py createsuperuser
```

13. Run following command to start autodata server on port 5000:

```bash
python manage.py runserver 0.0.0.0:5000
```

14. Open a new terminal window and change directory to autoremover.

15. Activate autoremover environment in this window.

16. Install the required packages listed in requirements.txt file.

17. Make autoremover migrations by running:

```bash
python manage.py makemigrations
```

18. Migrate to autoremover database by running:

```bash
python manage.py migrate
```

19. Install npm modules

```bash
npm install
```

20. Run following command to generate output.css:

```bash
npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css
```

21. Run the following command tu start server:

```bash
python manage.py runserver
```

# Additionally

You have to configure the system from the application interface and the django admin interface. There are settings for connecting 2 applications to each other. Also, you have to set the tax rate and such information too. The applications may give error otherwise. Additionally, all pricings and contents should be given to the system from admin interfaces before customers start to use the system.
