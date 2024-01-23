from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import time
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session



app = FastAPI()

# models.Base.metadata.create_all(bind=engine)

class MatrixInput(BaseModel):
    matrix : List[List[int]]


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_submatrices(matrix):
    submatrices = []
    rows = len(matrix)
    cols = len(matrix[0])
    
    for i in range(rows):
        for j in range(cols):
            for k in range(i, rows):
                for l in range(j, cols):
                    submatrix = [row[j:l+1] for row in matrix[i:k+1]]
                    if is_same_values(submatrix):
                        submatrices.append(submatrix)
    
    return submatrices

def is_same_values(submatrix):
    value = submatrix[0][0]
    for row in submatrix:
        for element in row:
            if element != value:
                return False
    return True  

@app.post("/largest-rectangle")
def largest_rectangle(matrix_input: MatrixInput, db: Session = Depends(get_db)):
    start_time = time.time()
    matrix = matrix_input.matrix
    try:
        dict={}
        submatrices = get_submatrices(matrix)
        for submatrix in submatrices:
            if len(submatrix)!=len(submatrix[0]):
                dict[len(submatrix)*len(submatrix[0])] = submatrix[0][0]
        
        # print(dict)
        area = max(dict.keys())
        number = dict[area]

        # area, number = k, p  

        # Log request and response in the database
        request_log = models.RequestLog(matrix=matrix_input.matrix, area=area, number=number)
        db.add(request_log)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        end_time = time.time()
        # converting time in milliseconds
        turnaround_time = int((end_time - start_time) * 1000)  
        if request_log:
            request_log.turnaround_time = turnaround_time
            db.commit()

    return {"area": area, "number": number, "turnaround_time": turnaround_time}

