FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN apt update && apt install fonts-liberation2 && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt
COPY . .

EXPOSE 9871
CMD ["python3", "-m" , "flask", "run", "-p", "9871", "--host=0.0.0.0"]
