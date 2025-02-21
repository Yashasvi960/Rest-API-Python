from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

# Define the app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/courses/{course_name}")
def read_course(course_name):
    return {"course_name": course_name}

course_items = [{"course_name": "Python"}, {"course_name": "NodeJS"}, {"course_name": "Machine Learning"}]
@app.get("/courses/")
def read_courses(start: int, end: int):
    return course_items[start: start+end]

class Course(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    author: Optional[str] = None

app = FastAPI()

@app.post("/courses/")
def create_course(course: Course):
    return course