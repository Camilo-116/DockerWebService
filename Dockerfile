FROM python:3.9-alpine
WORKDIR /app
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk --update add nano
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 3306
EXPOSE 5000
COPY . .
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["./docker-entrypoint.sh"]
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]