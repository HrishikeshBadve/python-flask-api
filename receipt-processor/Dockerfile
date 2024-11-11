FROM python:3.12.4-slim

# Set the working directory in the container
WORKDIR /app

# Install Flask
RUN pip install Flask

# Copy the current directory contents into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]
