ARG PYTHON_VER=3.12





FROM python:${PYTHON_VER}
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN apt update
RUN apt install libpq5 -y
ENV PATH="/app/.venv/bin:$PATH"
#COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
#COPY --from=base /usr/local/bin /usr/local/bin

#CMD uvicorn --host 0.0.0.0 --port 9000 main:app
CMD [ "python3", "main.py" ]
