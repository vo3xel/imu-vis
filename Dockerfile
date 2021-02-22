FROM continuumio/miniconda3

ENV CONDA_ENV /home/imu-vis/env
RUN mkdir -p $CONDA_ENV
WORKDIR $CONDA_ENV

COPY environment.yml .
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "imu-vis", "/bin/bash", "-c"]

WORKDIR /home/occ/data
COPY . .
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "imu-vis", "python", "app.py"]