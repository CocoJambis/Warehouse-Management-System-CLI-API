FROM python:3.12-slim

WORKDIR /AppRivApi
COPY App/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN rm -rf __pycache__ App/__pycache__ Tests/__pycache__ Tests/.pytest_cache

EXPOSE 5000

CMD ["python", "mainapi.py"]