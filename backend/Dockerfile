FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/bin/sh", "entrypoint.sh"]
