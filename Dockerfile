# ------------------------------
# S&P500 Dashboard Dockerfile
# ------------------------------
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for pandas, pyarrow, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements_dashboard.txt .

# Upgrade pip and install requirements
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements_dashboard.txt

# Copy project files
COPY . .

# Streamlit config
EXPOSE 8501

# Run the dashboard
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
