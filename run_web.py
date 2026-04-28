"""Web entry point — starts the FastAPI PWA server."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("newsfeed.api:app", host="0.0.0.0", port=8000, reload=False)
