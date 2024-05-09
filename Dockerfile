# Use an official Python runtime as a base image
FROM python:3.12

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt requirements.txt

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .


EXPOSE 8000

# Run the Django development server using manage.py
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]