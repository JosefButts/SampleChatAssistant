FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    libboost-all-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Install dependencies in specific order
RUN pip install --no-cache-dir langchain-core==0.3.29 && \
    pip install --no-cache-dir langchain-openai==0.2.14 && \
    pip install --no-cache-dir langchain-community==0.3.14 && \
    pip install --no-cache-dir -r requirements.txt

RUN echo "list dir: ", ls
# Copy the application code and docs
COPY . .
# copy everything inside local app folder
# add bash
RUN apt-get update && apt-get install -y \
    bash \
    && rm -rf /var/lib/apt/lists/*


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 