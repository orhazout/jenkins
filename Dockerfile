FROM python:3.7
RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000:5000
CMD [ "python" ,"app.py"  ]
