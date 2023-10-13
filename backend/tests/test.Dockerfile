FROM python:3.9
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY tests/g4t1_test.py .
EXPOSE 5001
CMD ["python", "g4t1_test.py"]