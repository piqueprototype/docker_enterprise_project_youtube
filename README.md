# Docker Dev Box

## Articles
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Django/React Tutorial](https://www.honeybadger.io/blog/docker-django-react/)
- [Separate into separate containers](https://medium.com/@gagansh7171/dockerize-your-django-and-react-app-68a7b73ab6e9)
- [PostgreSQL in Docker](https://towardsdatascience.com/getting-started-with-postgres-in-docker-616127e2e46d)

## Required downloads
- Docker
    - [Download webpage](https://www.docker.com)
- Docker Compose
    - **NOTE! This comes default when you download docker from the above link**
    - [Download webpage with options](https://docs.docker.com/compose/install/)
- Django
    - You'll install this with Python
- Node.js
    - [Download webpage](https://nodejs.org/en/download/)
- Python
    - [Download webpage](https://www.python.org/downloads/)

## Create the project Instructions
- Open the Gitbash terminal

### Create Virtual Environment
```bash
python -m venv <YOUR VIRTUAL ENVIRONMENT NAME> .  # . = Current directory
```
- Connect Pycharm to virtual environment you just created. ([Here's how](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#python_create_virtual_env))

### Connect to virtual environment
```bash
source Scripts/activate
```

### Install needed packages
```bash
pip install django
```

### Create Django project
```bash
mkdir django_project                              # Create the folder to house the project
cd django_project                                 # Navigate into the newly created folder
django-admin startproject <YOUR PROJECT NAME> .   # . = Current directory
mkdir <YOUR APP NAME>                             # Create the folder to house the app
cd <YOUR APP NAME>                                # Navigate into the newly created folder
django-admin startapp <YOUR APP NAME> .           # . = Current directory
cd ../../                                         # Backup to project folder
```

#### Add custom shell script
Even if its a simply ```echo "HELLO";``` do this now, so the build of the project doesn't fail :)
Note: File directory = ```shell_scripts/your_bash_script.sh```
```BASH
#!/bin/bash
# Needed at one point, but found out how to resolve the known_hosts issue with a Dockerfile command
sshpass -p 'somepasssssswwordd' rsync -rvzh username@101.102.103.104:data_directory /django_project
```

#### Requirements file
Here are the python libraries I felt were most relevant for this project
Note: File directory = ```./django_project/requirements.txt```
```
Django==4.1
django-cors-headers
redis
psycopg2
requests
schedule
pysftp
```

### Create React project
```bash
mkdir react_app                           # Create the folder to house the react UI app
cd react_app                              # Navigate into the folder
npx create-react-app <YOUR REACT UI NAME> # Create the React application 
```

## Build the environment files
- ```bash
  mkdir env
  cd env
  touch django.env
  touch docker_compose.env
  touch postgres_creditionals.env
  touch project.env
  cd ../
  ```
  
## Populate the environment files
- django.env
  - ```env
    REACT_URL=http://localhost:3000
    DJANGO_URL=https://localhost:8000
    POSTGRES_PORT=5432
    REMOTE_IP=123.123.123.123
    REMOTE_USERNAME=the_username
    REMOTE_PASSWORD=the_password
    ```
- docker_compose.env
  - ```env
    REACT_NAME=YOUR_REACT_APP_NAME
    DJANGO_NAME=YOUR_DJANGO_APP_NAME
    VOLUME_NAME=YOUR_VOLUME_NAME
    ```
- postgres_creditionals.env
  - ```env
    POSTGRES_HOST=mockup_database
    POSTGRES_USER=the_admin_of_database
    POSTGRES_PASSWORD=the_admins_password
    POSTGRES_DB=the_database_name
    ```
- project.env
  - ```env
    ```

## Build the docker files
- Docker Compose
  - filename = docker-compose.yaml (unless you have a better reason not to) 
  - Parent directory
  - ```
    version: "3.8"

    services:
      django:
        container_name: ${DJANGO_NAME}
        build:
          context: ./django_project
        env_file:
          - ./env/django.env
          - ./env/postgres_creditionals.env
        ports:
          - "8000:8000"
        volumes:
          - ./django_project:/${DJANGO_NAME}
        depends_on:
          - database
          - redis
        networks:
          - db-net
        command: bash -c "python manage.py makemigrations ; python manage.py migrate ; python manage.py runserver 0.0.0.0:8000 ;"
      
      react:
        container_name: ${REACT_NAME}
        build:
          context: ./react_app
        ports:
          - "3000:3000"
        volumes:
          - ./react_app:/${REACT_NAME}
        depends_on:
          - database
          - redis
      
      redis:
        container_name: ${REDIS_NAME}
        restart: always
        image: redis
        ports:
          - "6379:6379"
        depends_on:
          - database
        networks:
          - db-net
      
      database:
        container_name: ${POSTGRES_NAME} 
        hostname: mockup_database
        image: postgres:15-bullseye
        ports:
          - "5432:5432"
        restart: unless-stopped
        logging:
          options:
            max-size: 10m
            max-file: "3"
        volumes:
          - ./data/${VOLUME_NAME}:/data/${VOLUME_NAME}
        env_file:
          - ./env/postgres_creditionals.env
        networks:
          - db-net
      
    networks:
      db-net:
        driver: bridge
    ```
- Django
  - Filename = ```Dockerfile```
  - Directory = ```./django_project/```
  - ```
    # Target machine to copy from
    FROM python:3.8.13-bullseye
    
    # Alter environment variable
    ENV PYTHONUNBUFFERED=1
    ENV THE_REMOTE_IP=123.123.123.123
    
    # Install some OS level stuff
    RUN /bin/bash -c "apt-get -y update"
    RUN /bin/bash -c "apt-get -y upgrade"
    RUN /bin/bash -c "apt-get -y install vim"
    
    # Move the working directory here
    WORKDIR /django_project
    
    # Copy from host machine current directory to target container current directory
    COPY . .
    
    # Allow bash scripts to be executable
    RUN /bin/bash -c "chmod 777 -R /django_project/shell_scripts/*"
    
    # Automate adding target remote server with known_hosts
    RUN /bin/bash -c "mkdir /root/.ssh"
    RUN /bin/bash -c "touch /root/.ssh/known_hosts"
    RUN ssh-keyscan ${THE_REMOTE_IP} >> /root/.ssh/known_hosts
    
    # Install Python Libraries listed from the requirements.txt
    RUN pip install -r requirements.txt
    
    # Open port
    EXPOSE 8000
    ```
- React
  - Filename = ```Dockerfile```
  - Directory = ```./react_app/```
  - ```
    FROM node:14.17.3
    ENV REACT_DIRECTORY=mockup_ui
    WORKDIR /${REACT_DIRECTORY}
    COPY ./${REACT_DIRECTORY}/ .
    RUN npm install
    RUN yarn add recharts
    RUN apt update -y
    RUN apt upgrade -y
    RUN apt install vim -y
    EXPOSE 3000
    CMD ["npm", "start"]
    ```

### Build Docker Image(s)
- ```docker-compose --env-file ./env/docker_compose.env build --no-cache ;```
- Note #1: You must reference docker-compose.env every time.
- Note #2: You'll need to turn on the Docker desktop application

### Run Docker Image(s)
- ```docker-compose --env-file ./env/docker_compose.env up ;```
- Note: You must reference docker-compose.env every time.

## Troubleshooting
- [Manually add PYTHONPATH](https://datatofish.com/add-python-to-windows-path/)
- [Stop microsoft store from popping up](https://youtu.be/umyc3Yo87Qc)
- Enable "SVM Mode" in "Advanced CPU settings" within the BIOS.

## Tidbits
- [Docker Volumes Explained](https://docs.docker.com/storage/)
- [Docker Compose Cheatsheet](https://devhints.io/docker-compose)

