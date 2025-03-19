FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p db
RUN chmod +x entrypoint.sh


EXPOSE ${PORT}

ENTRYPOINT ["./entrypoint.sh"]