FROM python:3.11-slim
WORKDIR /app

# Install system deps and pip packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

ENV FLASK_ENV=production
ENV PORT=8000
EXPOSE 8000

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]