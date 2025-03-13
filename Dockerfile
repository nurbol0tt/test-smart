FROM python:3.10 as builder

WORKDIR .

COPY . .

RUN pip install --upgrade pip
RUN pip install -r req.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "db.py"]
