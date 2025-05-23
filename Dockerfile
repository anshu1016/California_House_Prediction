FROM python:3.10

# Copy current directory contents into the container
COPY . /app

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (default Flask runs on 5000)
EXPOSE 5000

# # Define environment variable for Flask
# ENV FLASK_ENV=production

# Run the application
CMD ["python", "app.py"]
