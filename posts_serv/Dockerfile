FROM python:3.9-slim
WORKDIR /app
COPY posts_serv/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY proto/ ./proto/
COPY broker/ ./broker/
EXPOSE 50051
CMD ["python", "posts_serv/post_service.py"]