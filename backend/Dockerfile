FROM python:3.9
WORKDIR /app
COPY requirements.txt .
COPY .env .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "g4t1.py"]