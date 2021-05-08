FROM python:3.7.10-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

# CMD ["scrapy", "crawl", "actress", "--loglevel", "ERROR", "-a", "url=https://jav.guru/actress/julia/"]
