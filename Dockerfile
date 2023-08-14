FROM python

WORKDIR /Users/shiraz/Desktop/ML Engineer prep/AWS_Project/src
COPY requirement.txt requirement.txt

COPY src/ ./
RUN pip3 install -r requirement.txt 

