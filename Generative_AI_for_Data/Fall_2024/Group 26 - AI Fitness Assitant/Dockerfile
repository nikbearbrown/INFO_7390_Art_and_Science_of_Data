FROM python:3.10
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=80", "--server.address=0.0.0.0"]
