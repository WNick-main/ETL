FROM python:3.9-slim-bullseye

RUN python3 -m venv /opt/venv

# Install dependencies:
COPY requires.txt .
RUN pip install -r requires.txt
CMD cd /app/ && python3 init.py