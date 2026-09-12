FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONUNBUFFERED=1
ENV OMP_NUM_THREADS=1

ENTRYPOINT ["python", "-m", "funsearch.cli"]
CMD ["--problem", "snakey", "--model", "gemini-3.6-flash", "--iterations", "10000", "--samples-per-prompt", "2", "--islands", "10", "--in-process", "--no-live"]
