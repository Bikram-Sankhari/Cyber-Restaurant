![](https://github.com/Bikram-Sankhari/Cyber_Restaurant/blob/main/development_static/assets/extra-images/Readme_logo.png?raw=true)
# A Multiple Restaurant Marketplace Web Application

![](https://img.shields.io/badge/Python-3.11.6-green) ![](https://img.shields.io/badge/Django-5.0-blue) ![](https://img.shields.io/badge/GDAL-purple) ![](https://img.shields.io/badge/PostgreSQL-16.2-blue) ![](https://img.shields.io/badge/NGINX-1.24.0-red
) ![](https://img.shields.io/badge/Gunicorn-21.2-orange)

## Usage
With the Deployed version of this Web App:
- Vendors  can Register their Restaurants to have an online presence and receive orders remotely.
- Vendors can manage their opening hours, menu, range of delivery etc.
- Buyers can search restaurants or food by their current location or for another location within a specific radius
- Buyers can generate single order from multiple restaurants and the rest will be taken care by the application
- Buyers can pay securely through PhonePe payment gateway with their preferrable payment method (e.g.- Card, Netbanking, UPI etc.)

## Key Features

- Location based Restaurant search using GDAL, GeoDjango & Google Maps API
- Live payment using PhonePe payment Gateway
- Single order generation from Multiple Restaurants
- Token Verification for authentication
- Refresh-less cart functionalities using AJAX
- Responsive UI to suit every device
- Clean, Maintainable & Scalable codebase

**However it is not possible to list down all the tiny but complex functionalities this app can perform. So to have a glance of the working app, have a look**  [**here**](https://youtu.be/w94kJWzct4o "Have a Glance Here")

------------

## Table of Contents
- [Usage](#usage)
- [Key Features](#key-features)
- [Server Setup Guide](#server-setup-guide)
  * [Prerequisites](#prerequisites)
  * [Windows Setup](#windows-setup)
    + [Make a clone of this repo at your preferred location](#1-make-a-clone-of-this-repo-at-your-preferred-location)
    + [Create a Virtual Environment](#3-create-a-virtual-environment)
    + [Activate the Virtual Evironment](#4-activate-the-virtual-evironment)
    + [Install the required packages](#5-install-the-required-packages)
    + [Set environment variables](#6-set-environment-variables)
    + [Install GDAL from the wheel provided](#7-install-gdal-from-the-wheel-provided)
    + [Configure GDAL](#8-configure-gdal)
    + [Create a Database](#10-create-a-database)
    + [Create necessary tables in the Database](#11-create-necessary-tables-in-the-database)
    + [Install PostGIS](#12-install-postgis)
    + [Collect Static Files](#13-collect-static-files)
    + [Good to go. Run the server](#14-good-to-go-run-the-server)
  * [Linux Setup](#linux-setup)
    + [Go to your User Directory](#1-go-to-your-user-directory)
    + [Clone the repository](#2-clone-the-repository)
    + [Change working Directory to the newly cloned "Cyber_Restaurant" Directory in terminal](#3-change-working-directory-to-the-newly-cloned-cyber_restaurant-directory-in-terminal)
    + [Create a Virtual Environment](#4-create-a-virtual-environment)
    + [Activate the Virtual Environment](#5-activate-the-virtual-environment)
    + [Install the required packages](#6-install-the-required-packages)
    + [Set environment variables](#7-set-environment-variables)
    + [Install GDAL](#8-install-gdal)
    + [Install and Enable PostgreSQL](#9-install-and-enable-postgresql)
    + [Configure PostgreSQL](#10-configure-postgresql)
    + [Install PostGIS](#11-install-postgis)
    + [Collect Static Files](#12-collect-static-files)
    + [Run the server on 8000 port](#13-run-the-server-on-8000-port)
    + [Setup Gunicorn to serve the Django Application](#14-setup-gunicorn-to-serve-the-django-application)
    + [Setup NGINX as a Reverse Proxy to serve Static and Media Files](#15-setup-nginx-as-a-reverse-proxy-to-serve-static-and-media-files)
    + [Allow required ports](#16-allow-required-ports)
- [Open Issues](#open-issues)
  * [User is not prompted to give location access automatically after reaching the site.](#1-user-is-not-prompted-to-give-location-access-automatically-after-reaching-the-site)
  * [Users can continue to place an order to a Restaurant even when it is Closed](#2-users-can-continue-to-place-an-order-to-a-restaurant-even-when-it-is-closed)
- [Want to Contribute?](#want-to-contribute)
  * [Create a Fork of this Repository](#1-create-a-fork-of-this-repository)
  * [Clone Your Fork](#2-clone-your-fork)
  * [Create a New Branch with a name that best describes the contribution you are about to make](#3-create-a-new-branch-with-a-name-that-best-describes-the-contribution-you-are-about-to-make)
  * [Now you can work on your new Branch](#4-now-you-can-work-on-your-new-branch)
  * [Commit the changes in your new Branch and push the code to your Forked Repository](#5-commit-the-changes-in-your-new-branch-and-push-the-code-to-your-forked-repository)
  * [Give a Pull request to this Upstream Repo](#6-give-a-pull-request-to-this-upstream-repo)
- [Found a BUG 🐞 ??](#found-a-bug--)
- [Acknowledgements](#acknowledgements)

## Server Setup Guide
As this is a pretty complex project and uses various different technologies, it is a quite long process to run the project locally or on a server. But the good news is, I have covered it all here and after following  these steps you can deploy it or run it locally.

### Prerequisites
- Linux or Windows OS
- Python version 3.11.6 (Because as on 31/03/24 there is no GDAL release for higher python version)
- Git Installed
- Google Maps API Key with Geocoding, Maps Javascript and Places API enabled

### Windows Setup

#### 1. Make a clone of this repo at your preferred location

	git clone https://github.com/Bikram-Sankhari/Cyber_Restaurant.git

#### 2. Open the just cloned "Cyber_Restaurant" directory in terminal

#### 3. Create a Virtual Environment

	python -m venv env

#### 4. Activate the Virtual Evironment

	env\Scripts\activate

#### 5. Install the required packages

	pip install -r requirements.txt

#### 6. Set environment variables
- Create a copy of the '.env-sample' file in the root directory of the project and rename the copy to ".env"
- Some of the fields will be pre-filled, no need to change them. Fill out the rest
- 'DB_NAME' can be anything as your wish, but in the upcoming steps you will need to create a database with the same name
- 'GEMINI_API_KEY' is optional, if you don&apos;t have one then just remove the line

#### 7. Install GDAL from the wheel provided

	pip install GDAL-3.4.whl

#### 8. Configure GDAL
- Open 'settings.py' in 'Restaurant' sub-directory
- Under the comment "GDAL Configuration"  replace the IF block with the following code


	pwd = os.getcwd()
	os.environ['PATH'] = os.path.join(pwd, 'env\Lib\site-packages\osgeo') + ';' + os.environ['PATH']
    os.environ['PROJ_LIB'] = os.path.join(pwd, 'env\Lib\site-packages\osgeo\data\proj') + ';' + os.environ['PATH']
    GDAL_LIBRARY_PATH = os.path.join(pwd, 'env\Lib\site-packages\osgeo\gdal304.dll')
    GEOS_LIBRARY_PATH = os.path.join(pwd, 'env\Lib\site-packages\osgeo\geos_c.dll')


#### 9. Download and Install PostgreSQL from <a href="https://www.enterprisedb.com/downloads/postgres-postgresql-downloads">here</a>
  (Make sure you install PgAdmin and Application Stack Builder).
  <br>For a step by step guide watch <a href="https://www.youtube.com/watch?v=qeSzBXsjVzY">this video</a>


#### 10. Create a Database
- Open "PGAdmin" and enter your password
- Expand the Servers menu
- Right Click on 'Databases' and create a new Database
- Database Name should be same as in your .env file  and let the user be 'postgres' by default

#### 11. Create necessary tables in the Database

	python manage.py makemigrations

 
	python manage.py migrate

#### 12. Install PostGIS
- Open "Application Stack Builder"
- Select PostgreSQL and click 'Next'
- It will show the list of available extensions. From here expand the 'Spatial Extensions' menu and check the latest version of PostGIS
- Continue the installation as per prompt
- After completition of the installation process, open "PGAdmin"
- Expand the Database that you created
- Click on the "Query Tool (🛢)" at top
- Write the following command to create the postgis extension on the database


	CREATE EXTENSION postgis;

- Click on the "Execute (▶)" button

#### 13. Collect Static Files

	python manage.py collectstatic

#### 14. Good to go. Run the server

	python manage.py runserver

## Open [127.0.0.1:8000](127.0.0.1:8000) on your browser.
# And CONGRATULATIONS You have Successfully run the Server !!!!! 🥳

------------

### Linux Setup
For Linux Operating System, the installation is little more complex than windows, because it is similar to deploying the application on a remote server. The only difference is, for local machine you run the comands on your local terminal and for a remote server you run the commands on a secure shell connected and authenticated with the server.

#### 1. Go to your User Directory
- Open Terminal by pressing CTRL + ALT + T

- Change working directory to your user directory



	  cd ~

#### 2. Clone the repository

	git clone https://github.com/Bikram-Sankhari/Cyber_Restaurant.git

#### 3. Change working Directory to the newly cloned "Cyber_Restaurant" Directory in terminal


	cd Cyber_Restaurant/

#### 4. Create a Virtual Environment

	python3 -m venv env

#### 5. Activate the Virtual Environment

	source env/bin/activate

#### 6. Install the required packages

	pip install -r requirements.txt

#### 7. Set environment variables
- Create a copy of the '.env-sample' file in the root directory of the project and rename the copy to ".env"
- Some of the fields will be pre-filled, if you have valid values for them then you can change them otherwise let them be as they are. Fill out the rest
- 'DB_NAME' can be anything as your wish, but in the upcoming steps you will need to create a database with the same name
- 'GEMINI_API_KEY' is optional, if you don&apos;t have one then just remove the line

#### 8. Install GDAL
- As a prerequisite for installing GDAL, install python3-dev


	  sudo apt install python3-dev

- Add GDAL release package to your apt repository


	  sudo add-apt-repository ppa:ubuntugis/ppa

- Update system packages


	  sudo apt-get update && sudo apt-get upgrade -y


- Install GDAL binary


	  sudo apt-get install gdal-bin

#### 9. Install and Enable PostgreSQL


	sudo apt-get install postgresql postgresql-contrib
	sudo systemctl start postgresql.service
	sudo systemctl enable postgresql.service

#### 10. Configure PostgreSQL
- By default PostgrSQL creates a user named 'postgres'
- Set a password for the 'postgres' user


	  sudo passwd postgres

- Switch to 'postgres' user


	  sudo su - postgres

- You may need to reset the password again. If you face any error in the next steps then run this command and follow the next steps again
<br>[Replace 'NEW PASSWORD' with your desired password]


	  psql -d postgres -c "ALTER USER postgres WITH PASSWORD 'NEW PASSWORD';"

- Login to PostgreSQL Shell


	  psql postgres

- Create a new Database.
<br>[Replace 'db_name' with the name you entered in the .env file]


	  CREATE DATABASE 'db_name';

- Get back to the SUDO user terminal


	  exit
	  exit

- Create tables in the database


	  python3 manage.py makemigrations
	  python3 manage.py migrate

#### 11. Install PostGIS
- Install 'ca-certificates' package to download and install certificates


	  sudo apt install ca-certificates

- Install 'gnupg' package to dearmor ASCII files


	  sudo apt install gnupg

- Add pgdg keys and main repo


	  curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg >/dev/null
	  sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

- Update system packages


	  sudo apt update &&  sudo apt upgrade -y

- Check the version of PostgreSQL you are using


	  pg_config --version

- Install PostGIS for your PostgreSQL version
<br>[Replace &lt;version&gt; with the version of PostgreSQL you just checked]


	  sudo apt install postgresql-<version>-postgis-3

- Create PostGIS extension on your database
<br>[Replace &lt;database name&gt; with the name of your database]


    	 sudo su postgres
    	 psql postgres
    	 \connect <database name>
    	 CREATE EXTENSION postgis;
    	 exit
    	 exit

#### 12. Collect Static Files

	python manage.py collectstatic

#### 13. Run the server on 8000 port
- Install 'ufw' package to enable 8000 port


	  sudo apt install ufw

- Enable 8000 port


	  sudo ufw allow 8000

- Run the server


	  gunicorn --bind 127.0.0.1:8000 Restaurant.wsgi

- Now if you reach out to [this](127.0.0.1:8000) url you should see your server running, but there should be something wrong. The stylings and static files are not loading right? Don&apos;t worry we are going to fix them in the next steps.

- Stop the server by pressing CTRL + C

#### 14. Setup Gunicorn to serve the Django Application
- Create a Gunicorn socket file


	  sudo nano /etc/systemd/system/gunicorn.socket

- Enter the following configuration in the file and save


    	[Unit]
    	Description=gunicorn socket
    	[Socket]
    	ListenStream=/run/gunicorn.sock
    	[Install]
    	WantedBy=sockets.target

- Create a Gunicorn service file


  	  sudo nano /etc/systemd/system/gunicorn.service

- Enter the following configuration in the file and save
<br>[Replace &lt;username&gt; with the name of your sudo user]


    	[Unit]
    	Description=gunicorn daemon
    	Requires=gunicorn.socket
    	After=network.target
    	
    	[Service]
    	User=<username>
    	Group=www-data
    	WorkingDirectory=/home/<username>/Cyber_Restaurant
    	ExecStart=/home/<username>/Cyber_Restaurant/env/bin/gunicorn \
    	          --access-logfile - \
    	          --workers 3 \
    	          --bind unix:/run/gunicorn.sock \
    	          Restaurant.wsgi:application
    	
    	[Install]
    	WantedBy=multi-user.target

- Restart Gunicorn


	  sudo systemctl restart gunicorn

#### 15. Setup NGINX as a Reverse Proxy to serve Static and Media Files
- Create a NGINX configuration file


	  sudo nano /etc/nginx/sites-available/Cyber_Restaurant

- Enter the following code in the file and save
<br>[Replace &lt;username&gt; with the name of your sudo user]
<br>[Change the 'server_name' if you want to deploy the Application on a remote server]


    	server {
    	listen 80;
    	server_name 127.0.0.1;
    
    	location = /favicon.ico { access_log off; log_not_found off; }
    
    	location /static/ {
    		root /home/<username>/Cyber_Restaurant;
    	}
    
    	location /media/ {
    		root /home/<username>/Cyber_Restaurant;
    	}
    
    	location / {
    		include proxy_params;
    		proxy_pass http://unix:/run/gunicorn.sock
    	}
    	}

- Create a link to the configuration file


	  sudo ln -s /etc/nginx/sites-available/Cyber_Restaurant etc/nginx/sites-enabled/

- Change the NGINX user


	  sudo nano /etc/nginx/nginx.conf

- Set  'user' to your sudo username and save the file

- Restart NGINX


    	sudo systemctl restart nginx

#### 16. Allow required ports
- Allow the required ports


    	 sudo ufw allow 586
    	 sudo ufw allow 80
    	 sudo ufw allow 'Nginx Full'

- Remove 8000 port


	   sudo ufw delete allow 8000


## Open [127.0.0.1](127.0.0.1) on your browser.
# And CONGRATULATIONS You have Successfully DEPLOYED the Web Application !!!!! 🥳 </p>

------------

## Open Issues

### 1. User is not prompted to give location access automatically after reaching the site.
> I have kept this issue open, to show How Location based search functionalities are working behind the scene to show relevant Restaurants nearby? How it is using GeoDjango with Google Maps API to fetch Restaurants inside a certain Radius? However this issue can be solved very easily.

### 2. Users can continue to place an order to a Restaurant even when it is Closed
> I am planning to create a Celery Asynchronous job to intimate the Restaurant as well as the Customer whenever the Restaurant gets opened. And also there may be some scenarios when the Restaurant has actually not closed but due to some minute differences in Opening Hours Slabs, the system is showing the status Closed. In that case, we can ask the Restaurant owner whether to accept the order or not. So looking forward for some additional Features

------------

## Want to Contribute? 
All contributions are Welcome. If you want to contribute to this project follow the steps.

### 1. Create a Fork of this Repository
See [GitHub Documentation for Forks](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github)

### 2. Clone Your Fork


	git clone <URL TO YOUR FORK>

### 3. Create a New Branch with a name that best describes the contribution you are about to make


	git checkout -b <YOUR BRANCH NAME>

### 4. Now you can work on your new Branch
> After making the changes, Test your code well before committing

### 5. Commit the changes in your new Branch and push the code to your Forked Repository

See [This Documentation](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)

### 6. Give a Pull request to this Upstream Repo
See [The GitHub Documentation on Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)
> Be Descriptive about the Contribution you have made

------------


## Found a BUG 🐞 ??
As this Application is in the very early stage of it&apos;s development lifecycle, it is anticipated that there are some bugs in the code. So if you find out one, then Please -
Let me know directly by Email: bikramsankhari2024@gmail.com

------------



## Acknowledgements

I would like to Thank [Django Official Forum](https://forum.djangoproject.com/) for helping me out on RUNTIME MODEL VALIDATION issue.

------------


