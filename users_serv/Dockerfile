FROM python:3.9-slim
WORKDIR /app
COPY users_serv/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY broker/ ./broker/
EXPOSE 5000
CMD ["python", "users_serv/user_service.py"]