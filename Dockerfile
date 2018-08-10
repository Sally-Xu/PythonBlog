# base os image
FROM ubuntu:17.10

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /code/requirements.txt

# install python and pip 
RUN apt-get clean && \
    apt-get update -y && \
    apt-get install -y python3.7 python3-pip --fix-missing && \
    python3 -m pip install --upgrade pip

# set container's code/app folder as working directory, following command will be run from this directory
WORKDIR /code

# pip install all requirements
RUN python3 -m pip install -r requirements.txt

# copy file from app folder to container's code/app folder
COPY ./app /code/app

# set container's code/app folder as working directory, following command will be run from this directory
WORKDIR /code/app

# set eviroment variables
ENV EMAIL_USER {SenderEmail}
ENV EMAIL_PASSWORD {SenderPassword}

# expose port 5000
EXPOSE 5000

# configures the container to run as an executable; only the last ENTRYPOINT instruction executes
ENTRYPOINT [ "python3" ]

# commands 
CMD [ "manage.py" ]