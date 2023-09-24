FROM python:latest


RUN git clone https://github.com/dyler2/downloadvideo.git /downloadvideo
WORKDIR /downloadvideo
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r downloadvideo/requirements.txt
CMD python3 main.py
