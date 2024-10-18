# main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db  # Adjusted import
from app.crud import get_product_by_name  # Ensure this function is correctly imported
from app.schemas import ProductBase

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")

# Root endpoint to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Placeholder endpoints for data processing
@app.get("/raw-data")
async def get_raw_data():
    return {"message": "Raw data placeholder"}

@app.get("/clean-raw-data")
async def clean_raw_data():
    return {"message": "Cleaned raw data placeholder"}

@app.get("/transform-data")
async def transform_data():
    return {"message": "Data transformation placeholder"}

@app.get("/load-data")
async def load_data():
    return {"message": "Data loading placeholder"}

@app.get("/explore-data")
async def explore_data():
    return {"message": "Data exploration placeholder"}

# Endpoint for "Search by Product"
@app.get("/search-product/", response_model=List[ProductBase])
async def search_product(product_name: str, db: Session = Depends(get_db)):
    print(f"Search requested for: {product_name}")  # Debug log
    products = get_product_by_name(db=db, product_name=product_name)

    if not products:
        raise HTTPException(status_code=404, detail="Product not found")

    product_dicts = [
        {
            "channel_id": p.channel.channel_id,
            "channel_username": p.channel.channel_username,
            "channel_title": p.channel.channel_title,
            "product_id": p.product_id,
            "product_name": p.product_name,
            "price_in_birr": p.price_in_birr,
        }
        for p in products
    ]

    print(f"Products found: {product_dicts}")  # Log the products found
    return product_dicts  # Return the structured response