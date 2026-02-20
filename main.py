from fastapi import FastAPI, Request
import openai
import firebase_admin
from firebase_admin import credentials, firestore

app = FastAPI()

# Initialize Firebase
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# OpenAI Key
openai.api_key = "YOUR_OPENAI_API_KEY"

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    data = await request.form()
    
    message = data.get("Body")
    
    # AI summary
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"Summarize and categorize this link: {message}"
        }]
    )
    
    summary = response['choices'][0]['message']['content']
    
    # Save to Firebase
    db.collection("links").add({
        "link": message,
        "summary": summary
    })
    
    return {"status": "saved"}
