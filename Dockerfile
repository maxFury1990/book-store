FROM python:3.7

EXPOSE 5000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app
ENV PYTHONPATH=/app
ENTRYPOINT ["python"]
CMD ["./books_app/main.py"]