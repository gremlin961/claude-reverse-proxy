# Claude Reverse Proxy

A simple reverse proxy designed to allow Claude Cowork and Claude Code to access a local vLLM server that is not secured with an SSL certificate.

## Purpose

Claude requires HTTPS for API connections unless the gateway is `127.0.0.1`. This reverse proxy acts as a bridge, allowing you to configure Claude to use `http://127.0.0.1:8000` while it forwards all requests to your actual local vLLM server.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd claude-reverse-proxy
    ```

2.  **Set up a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Open `main.py` and modify the `TARGET_SERVER` variable to point to your local vLLM server:

```python
# The destination server where requests will be forwarded
TARGET_SERVER = "http://<YOUR_VLLM_SERVER>:8000"
```

## Usage

Run the proxy using `uvicorn`:

```bash
uvicorn main.py:app --host 127.0.0.1 --port 8000
```

Once running, you can point Claude Cowork or Claude Code to `http://127.0.0.1:8000` as the API base URL.
