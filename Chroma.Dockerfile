# Base image with Python
FROM python:3.11.0

# Set working directory in the container
WORKDIR /app

# Install ChromaDB
RUN pip install --no-cache-dir chromadb

# Default command: Start a Python interactive shell (or you can customize this)
CMD ["python"]
