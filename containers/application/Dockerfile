FROM python:3.6.1

RUN apt-get update -y && apt-get upgrade -y

#RUN apt-get install libgdal-dev software-properties-common -y


#RUN add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable
#RUN apt update -y
#RUN apt upgrade -y
RUN apt install gdal-bin python-gdal python3-gdal -y

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
