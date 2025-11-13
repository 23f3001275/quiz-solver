# docker/Dockerfile
FROM python:3.11-slim

# Install apt deps for Playwright
RUN apt-get update && apt-get install -y \
    wget ca-certificates gnupg libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxss1 libx11-xcb1 libgbm1 libasound2 libpangocairo-1.0-0 libgtk-3-0 libxcomposite1 libxdamage1 libxrandr2 xdg-utils \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

# Install Playwright browsers
RUN playwright install --with-deps

ENV PYTHONUNBUFFERED=1
ENV EXPECTED_SECRET=replace_with_your_secret

EXPOSE 8000
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
