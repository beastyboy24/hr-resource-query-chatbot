FROM python:3.11-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install standard-imghdr>=1.0.0 altair<5.0.0 setuptools>=68.0.0
COPY . .
EXPOSE 7860
CMD ["streamlit", "run", "frontend/streamlit_app.py", "--server.address", "0.0.0.0", "--server.port", "7860", "--server.fileWatcherType", "none", "--browser.gatherUsageStats", "false"]