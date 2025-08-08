# Get python:3.10 as base
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt to the container and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
