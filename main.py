from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.routers import data_handler


app = FastAPI(
    title="CAG API Project (Chat with your PDF)",
    description="API for uploading PDFs, querying content via LLM, and managing data.",
    version="0.1.0"
)


app.include_router(
    data_handler.router,
    prefix="/api/v1",
    tags=["Data Handling And Chat With PDF"],
)


@app.get("/", response_class=HTMLResponse, tags=["Root"])
def read_root():
    """
    Provides a simple HTML welcome page with a link to the Swagger (OpenAPI) docs.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CAG API Project</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 5rem; background: #f9f9f9; }
                .container { max-width: 500px; margin: auto; background: #fff; padding: 2rem; border: 2px solid black; border-radius: 2rem; }
                h1 { color: #333; }
                p { padding: 0.30rem; }
                a { color: #007acc; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to the CAG API Project</h1>
                <p>🎯 View the automatically generated API documentation here:</p>
                <p><a href="/docs" target="_blank">Swagget UI (OpenAPI Docs)</a></p>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


if __name__ == "__main__":

    import uvicorn
    # Run the FastAPI app using uvicorn 
    # You can test this using tools like curl or Postman, or Fastapi's interaction docs at http://127.0.0.1:8000
    uvicorn.run(
        app, host="127.0.0.1", port=8001
    )
# Use different port to avoid conflict if running others

# Please set it to your Google Gemini API key (get key from https://aistudio.google.com/apikey)