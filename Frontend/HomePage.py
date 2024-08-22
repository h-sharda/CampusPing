from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import csv
import os
import uvicorn


app = FastAPI()

# Set up templates and static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory=".")

@app.on_event("startup")
async def startup_event():
    # Check if the CSV file exists; if not, create it with headers
    if not os.path.exists("student_data.csv"):
        with open("student_data.csv", "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Roll Number", "Email ID", "Phone"])

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("static/test_kushagra.html", {"request": request})

@app.post("/submit")
async def submit_form(rollNumber: str = Form(...), email: str = Form(...), phone: str = Form(...)):
    # Append data to the CSV file
    with open("student_data.csv", "a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([rollNumber, email, phone])

    return {"message": "Data submitted successfully!"}

if __name__ == "__main__":
    uvicorn.run("HomePage:app", host="127.0.0.1", port=8000, reload=True)