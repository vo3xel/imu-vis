FROM continuumio/miniconda3

ENV CONDA_ENV /home/imu-vis/env
RUN mkdir -p $CONDA_ENV
WORKDIR $CONDA_ENV

COPY environment.yml .
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "imu-vis", "/bin/bash", "-c"]

RUN mkdir -p /home/imu-vis/app
WORKDIR /home/imu-vis/app
COPY . .
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "imu-vis", "gunicorn", "-w", "1", "-b", ":9123", "app:server"]