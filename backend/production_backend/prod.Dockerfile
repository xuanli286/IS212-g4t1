FROM python:3.9
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY production_backend/g4t1.py .
EXPOSE 5000
CMD ["python", "g4t1.py"]