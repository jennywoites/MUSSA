FROM python
ADD  MUSSA_Flask/requirements.txt  /tmp/requirements.txt
WORKDIR /app
RUN pip install --trusted-host pypi.python.org -r  /tmp/requirements.txt
RUN apt-get update && apt-get install -y mysql-client && rm -rf /var/lib/apt


