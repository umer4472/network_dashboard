# Choose platform explicitly
FROM --platform=linux/amd64 python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements first and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Make start.sh executable
RUN chmod +x start.sh

# Expose ports
EXPOSE 8501
EXPOSE 8000

# Start both services
CMD ["./start.sh"]
