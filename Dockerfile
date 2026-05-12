FROM node:20-bookworm-slim

WORKDIR /app

# Install Python for ML scripts
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip python3-venv python-is-python3 \
    && rm -rf /var/lib/apt/lists/*

# Create isolated Python environment (required on Debian bookworm / PEP 668)
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy project
COPY . .

# Install Python dependencies into venv
RUN pip install --no-cache-dir -r ml/requirements.txt

# Install Node dependencies
RUN npm --prefix api install

# Install tsx to run TypeScript server in container
RUN npm install -g tsx

# Generate model artifacts at build time
RUN python3 ml/train.py

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

# Start Express API
CMD ["tsx", "api/src/server.ts"]
