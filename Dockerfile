# FROM tensorflow/tensorflow:latest-py3
FROM tensorflow/tensorflow:latest-gpu-py3

RUN pip install --upgrade tensorflow
RUN pip install networkx

# Copy over codefiles:
VOLUME /src
COPY . /src

WORKDIR /src

# Ready to run: 
# RUN python tests.py
CMD python main.py