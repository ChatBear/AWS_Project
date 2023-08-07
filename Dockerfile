FROM python

WORKDIR src/
COPY requirement.txt requirement.txt
RUN pip3 install -r requirement.txt 

