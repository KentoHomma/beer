FROM python:3.6-alpine3.6

MAINTAINER Robley Gori <ro6ley.github.io>

EXPOSE 8000

RUN echo "http://dl-cdn.alpinelinux.org/alpine/v3.6/community" >> /etc/apk/repositories \
  && apk update \
  && apk add --update-cache --no-cache gcc libquadmath musl-dev \
  && apk add --update-cache --no-cache gfortran \
  && apk add --update-cache --no-cache lapack-dev 

RUN apk add --no-cache python3-dev

ADD . /ml_app1

WORKDIR /ml_app1
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-use-pep517 scikit-learn==0.22.2.post1
RUN pip install --no-use-pep517 scipy==1.4.1
RUN pip install --no-use-pep517 pandas

CMD [ "python", "ml_app1/manage.py", "runserver", "0.0.0.0:8000" ]