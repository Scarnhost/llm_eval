from fastapi import FastAPI
from model import call_llm                   
from db import create_table_graph

app=FastAPI()

#testing if server is running
@app.get("/")
def root():
    return "Server is running"

#get call for table or graph creation
@app.get("/table_graph")
def table():
    return create_table_graph()

#post call for string analysis
@app.post("/call_model/{string}")
def call_model(string:str):
    return call_llm(string)