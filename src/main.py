# src/main.py

import sys
sys.path.append('./src/')
import uvicorn
from pickle5 import pickle
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
# import os
# print(os.listdir("."))  # show all files in the cwd

settings = get_settings()

# Initializing the fast API server
app = FastAPI()
origins = ["*"]
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Loading up the trained model
model = pickle.load(open('./src/model/hireable.pkl', 'rb'))

# Defining the model input types
class Candidate(BaseModel):
  gender: int
  bsc: float
  workex: int
  etest_p: float
  msc: float

# Setting up the home route
@app.get("/")
def read_root():
  return {
    "data": "Welcome to online employee hireability prediction model"
  }

# Setting up the prediction route


@app.post("/prediction/")
async def get_predict(data: Candidate):
  sample = [[
    data.gender,
    data.bsc,
    data.workex,
    data.etest_p,
    data.msc
  ]]
  hired = model.predict(sample).tolist()[0]
  return {
    "data": {
      'prediction': hired,
      'interpretation': 'Candidate can be hired.' if hired == 1 else 'Candidate can not be hired.'
    }
  }

# Configuring the server host and port
def main():
  uvicorn.run(app, port=settings.port, host='0.0.0.0', log_level="info")

if __name__ == '__main__':
  main()
