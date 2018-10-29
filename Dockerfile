# FROM tensorflow/tensorflow:latest-py3
FROM tensorflow/tensorflow:latest-gpu-py3

RUN apt-get update
RUN apt-get install graphviz -y

RUN pip install networkx
RUN pip install graphviz
RUN pip install pydot
RUN pip install firebase_admin

# Copy over codefiles:
VOLUME /src
COPY . /src

WORKDIR /src

ENV LANG="C.UTF-8"
ENV EA_NAS_UPLOAD_TO_FIREBASE="1"

# Ready to run: 
# RUN python tests.py
CMD python -u main.py