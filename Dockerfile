# 1. Base Image: Use a lightweight Python version
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirements first (Optimization: Docker Layer Caching)
COPY requirements.txt .

# 4. Install dependencies
# --no-cache-dir reduces image size
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
COPY . .

# 6. Expose the port Streamlit runs on
EXPOSE 8501

# 7. Define the command to run the app
# --server.address=0.0.0.0 is required for Docker networking
CMD ["streamlit", "run", "src/ui/app.py", "--server.address=0.0.0.0"]