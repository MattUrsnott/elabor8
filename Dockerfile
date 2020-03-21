FROM python:3.7-slim-buster
RUN pip3 install requests
WORKDIR /elabor8
RUN mkdir output
COPY src/main.py /elabor8 
CMD python /elabor8/main.py -f /elabor8/output/reporters.txt
