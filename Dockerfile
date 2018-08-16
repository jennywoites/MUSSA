# Use an official Python runtime as a parent image
FROM python

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD  MUSSA_Flask  /app


RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN apt-get update && apt-get install -y mysql-client && rm -rf /var/lib/apt


EXPOSE 5000

CMD /bin/bash /init-scripts/initdb.sh && \
    python manage.py runserver 
