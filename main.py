from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx
from starlette.background import BackgroundTask

app = FastAPI()

# The destination server where requests will be forwarded
TARGET_SERVER = "http://<YOUR_VLLM_SERVER>:8000"

# Using a global client enables HTTP connection pooling, making the proxy much faster
client = httpx.AsyncClient(base_url=TARGET_SERVER, timeout=None)

# Catch-all route to intercept any method and path
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"])
async def reverse_proxy(request: Request, path: str):
    # Reconstruct the exact path and query parameters
    url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))

    # Forward the headers, but strip out the original 'host' header.
    # This forces httpx to generate the correct host header for 'spark.local'.
    headers = dict(request.headers)
    headers.pop("host", None)

    # Build the exact same request bound for the new target
    req = client.build_request(
        method=request.method,
        url=url,
        headers=headers,
        content=request.stream(),
    )

    # Send the request and stream the response to avoid memory bottlenecks on large files
    resp = await client.send(req, stream=True)

    # Stream the response directly back to the original client
    return StreamingResponse(
        resp.aiter_raw(),
        status_code=resp.status_code,
        headers=resp.headers,
        background=BackgroundTask(resp.aclose), # Ensures the connection closes properly
    )