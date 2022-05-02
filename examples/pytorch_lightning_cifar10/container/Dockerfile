#FROM pytorch/pytorch
FROM pytorch/pytorch:1.8.1-cuda10.2-cudnn7-devel
WORKDIR /opt/model

COPY requirements.txt .
COPY train.py .

RUN pip install -r requirements.txt

CMD ['bash']