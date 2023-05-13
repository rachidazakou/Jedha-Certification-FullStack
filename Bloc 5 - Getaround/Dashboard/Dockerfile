FROM continuumio/miniconda3

WORKDIR /home/app

RUN apt-get update -y
RUN apt-get install nano unzip
RUN apt-get install -y python3.10
RUN apt install curl -y

RUN curl -fsSL https://get.deta.dev/cli.sh | sh

COPY requirements.txt /dependencies/requirements.txt
RUN conda install -c conda-forge shap psutil && pip install -r /dependencies/requirements.txt

CMD streamlit run --server.port $PORT app.py