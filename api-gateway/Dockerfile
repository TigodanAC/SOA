FROM python:3.9-slim
WORKDIR /app
COPY proto/ ./proto/
COPY api-gateway/requirements.txt .
COPY api-gateway/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/app
COPY api-gateway/ .
EXPOSE 8080
CMD ["python", "api_gateway.py"]