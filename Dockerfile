FROM apache/superset:latest

# Switch to root user 
USER root


# Activate Superset venv and install Trino driver
RUN . /app/.venv/bin/activate && \
    python -m ensurepip --upgrade && \
    python -m pip install --upgrade pip && \
    python -m pip install 'trino' 'flask-cors'

# Switch back to the superset user
USER superset
