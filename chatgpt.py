import openai
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Created base prompt to enact like popoye
prompt = [{"role": "system", "content": "I am an AI language model or you can call me Popoye the sailor man, and I'm here to help you. You can sometimes add popoye character in your answers."}]

app = FastAPI()
openai.api_key = "YOUR_API_KEY"

# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class UserQuery(BaseModel):
    user_input: str


def create_prompt(user_input):
    prompt.append({"role":"user","content":user_input})
    return prompt


def generate_response(user_input):
    prompt = create_prompt(user_input)

    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=prompt
    )
    
    message = response.choices[0].message.content
    
    # Updating prompt with GPT-4 response as well
    prompt.append({"role": "system", "content": message})
    
    return message

@app.get("/", response_class=HTMLResponse)
async def chatgpt_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chatgpt/")
async def chatgpt_endpoint(user_query: UserQuery):
    response = generate_response(user_query.user_input)
    return {"response": response}
