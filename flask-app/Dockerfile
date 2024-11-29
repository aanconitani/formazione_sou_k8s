# Use the official Python 3.10 Alpine image for a smaller image size
FROM --platform=linux/arm64 python:3.10-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Set the default command to run the application
ENTRYPOINT ["python3"]
CMD ["app.py"]
