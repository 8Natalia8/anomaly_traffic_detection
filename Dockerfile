FROM python:3.7

WORKDIR /app

COPY . /app

RUN pip install pandas scikit-learn joblib ipaddress

CMD ["python", "launch_script.py"]