# Base image
FROM python:3.11
# Replace with your desired Python version if needed

# Create a working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy your application code
COPY . .

# Optional: Download pre-trained models or data
# RUN curl https://path/to/model.h5 -o model.h5

# Expose a port (if your application listens on a specific port)
# EXPOSE 8000

# Set the command to execute your application
CMD ["python", "/src/app_main.py"]
