FROM python:3.10

WORKDIR /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy the requirements file and install dependencies
COPY requirements.txt . 
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . . 

# Expose the port if needed (uncomment if required)
# EXPOSE 8501

# Start the Streamlit app using the environment variable
#CMD ["sh", "-c", "streamlit run --server.port $PORT main.py --bind 0.0.0.0:$PORT"]
CMD ["sh","-c","streamlit run main.py --server.port=$PORT --server.address=0.0.0.0"]
