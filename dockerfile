# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files (main.py, templates, etc.)
COPY . .

# We use Gunicorn to "bind" (-b) the app to 0.0.0.0 on port 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]