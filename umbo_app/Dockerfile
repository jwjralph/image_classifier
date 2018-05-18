FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -r requirements.txt
 RUN apt-get remove -y curl
 RUN wget http://curl.haxx.se/download/curl-7.50.2.tar.bz2
 RUN tar -xvjf curl-7.50.2.tar.bz2
 WORKDIR /code/curl-7.50.2
 RUN ./configure
 RUN make
 RUN make install
 RUN ldconfig
 WORKDIR /code 
 ADD . /code/

