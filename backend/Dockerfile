FROM python:3.12

# python environment
ENV PYTHONUNBUFFERED=1
# ENV PYTHONDONTWRITEBYTECODE=1

# setup container
WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt
# RUN pip3 install --no-cache-dir --no-compile -r requirements.txt
COPY . .

# run django
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/bin/sh", "entrypoint.sh"]
