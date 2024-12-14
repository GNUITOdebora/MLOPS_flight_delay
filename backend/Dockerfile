FROM python:3.10

WORKDIR /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy the requirements file and install dependencies
COPY requirements.txt . 
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . . 

# Expose the port specified by the environment variable
EXPOSE $PORT

# Start the application with Gunicorn and Uvicorn worker
CMD ["sh", "-c", "gunicorn -w 3 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT"]
