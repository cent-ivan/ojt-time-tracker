#Instructions to the app

# Use Python 3.12 as base image.Recent stable
FROM python:3.12-slim-bookworm

#sets the container to Asia Manila
ENV TZ=Asia/Manila
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set working directory inside the container
WORKDIR /flask-app

# Install uv package manager
RUN pip install uv

# Copy Python requirements and install them using uv
COPY requirements.txt ./
RUN uv pip install --system -r requirements.txt

# Copy the rest of the app code
COPY . .

EXPOSE 5000

# Set the default command to run your Flask app
CMD ["python3", "run.py"]
