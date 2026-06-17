import json
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Initialize the FastAPI app
app = FastAPI(title="Netflix Command Center API")

# Mount the static folder so the browser can access your HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

# Route for the main dashboard page
@app.get("/")
async def serve_dashboard():
    return FileResponse("static/index.html")

# --- GET ROUTES (Reading Data) ---

@app.get("/api/history")
async def get_history():
    """Reads the history JSON file and sends it to the frontend"""
    with open("static/data.json", "r") as file:
        data = json.load(file)
    return data

@app.get("/api/watchlist")
async def get_watchlist():
    """Reads the watchlist JSON file and sends it to the frontend"""
    try:
        with open("static/watchlist.json", "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return []

# --- POST ROUTE (Saving Data) ---

@app.post("/api/watchlist/save")
async def save_watchlist(request: Request):
    """Catches the updated watchlist from the frontend and saves it permanently"""
    updated_data = await request.json()
    
    # Overwrite the JSON file with the new data!
    with open("static/watchlist.json", "w") as file:
        json.dump(updated_data, file, indent=4)
        
    return {"status": "success", "message": "Watchlist saved permanently!"}