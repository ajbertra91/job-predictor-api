# Importing necessary libraries
import uvicorn
from pickle5 import pickle
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

PORT = 8080
# Initializing the fast API server
app = FastAPI()
origins = [
  "http://localhost",
  f"http://localhost:{PORT}",
  "https://job-predictor-api.herokuapp.com/"
]
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Loading up the trained model
model = pickle.load(open('./model/hireable.pkl', 'rb'))
# Loading up the trained model
model = pickle.load(open('./model/hireable.pkl', 'rb'))

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
if __name__ == '__main__':
  uvicorn.run(app, port=PORT, host='0.0.0.0', log_level="info")
