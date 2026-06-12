from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to tifligpt!"}

@app.get("/chat")
def chat_endpoint(prompt: str):
    # This is where my GPT logic will go later
    return {"response": f"You said: {prompt}"}