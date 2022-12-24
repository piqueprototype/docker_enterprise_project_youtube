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