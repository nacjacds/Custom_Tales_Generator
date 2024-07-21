from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from openai import OpenAI
import os
from jinja2 import Template
import json
import logging
from dotenv import load_dotenv
from app.database import engine, SessionLocal
from app.models import Base, Interaction  # Asegúrate de que estos se importen correctamente
from langchain_core.prompts import PromptTemplate

load_dotenv()  # Cargar variables de entorno desde el archivo .env

app = FastAPI()

# Configuración de OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")

client = OpenAI(api_key=api_key)

Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)

def load_translations(lang):
    try:
        with open(f"app/translations/{lang}.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading translations: {e}")
        raise HTTPException(status_code=500, detail="Error loading translations")

def format_story(story):
    # Reemplaza dos saltos de línea seguidos por un solo salto de línea y luego agrega un doble salto de línea.
    formatted_story = story.replace('\n\n', '\n').replace('\n', '<br><br>')
    return formatted_story

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request, lang: str = 'en'):
    try:
        translations = load_translations(lang)
        with open("app/templates/index.html") as f:
            template = Template(f.read())
        html_content = template.render(lang=lang, translations=translations)
        return HTMLResponse(content=html_content)
    except Exception as e:
        logging.error(f"Error rendering form: {e}")
        raise HTTPException(status_code=500, detail="Error rendering form")

@app.post("/generate_story", response_class=HTMLResponse)
async def generate_story(
    request: Request,
    lang: str = Form(default='en'),
    child_name: str = Form(...),
    characters: str = Form(None),
    details: str = Form(None),
    length: str = Form(default='medium')
):
    db: Session = SessionLocal()
    try:
        translations = load_translations(lang)
        logging.info(f"Received form data: child_name={child_name}, characters={characters}, details={details}, lang={lang}")

        if lang == 'es':
            prompt_template = PromptTemplate(
                input_variables=["child_name", "characters", "details", "length"],
                template="Escribe un cuento {length} para niños con el nombre {child_name}, que incluya a {characters}, y que ocurra en {details}."
            )
        else:
            prompt_template = PromptTemplate(
                input_variables=["child_name", "characters", "details", "length"],
                template="Write a {length} children's story with the name {child_name}, that includes {characters}, and that takes place in {details}."
            )

        prompt = prompt_template.format(child_name=child_name, characters=characters or "", details=details or "", length=length)
        logging.info(f"Generated prompt using Langchain: {prompt}")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        logging.info(f"OpenAI response: {response}")

        story = response.choices[0].message.content.strip()
        # Eliminar la frase "¡Claro! Aquí tienes el cuento:" del comienzo del cuento
        if story.lower().startswith("¡claro! aquí tienes el cuento:"):
            story = story[len("¡claro! aquí tienes el cuento:"):].strip()
        formatted_story = format_story(story)
        logging.info(f"Generated story: {formatted_story}")

        # Guardar en la base de datos
        interaction = Interaction(
            child_name=child_name,
            characters=characters,
            details=details,
            story=formatted_story
        )
        db.add(interaction)
        db.commit()
        db.refresh(interaction)

        with open("app/templates/index.html") as f:
            template = Template(f.read())
        html_content = template.render(lang=lang, translations=translations, story=formatted_story)
        return HTMLResponse(content=html_content)
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=500, detail="OpenAI API error")
    finally:
        db.close()

@app.post("/change_language")
async def change_language(lang: str = Form(...)):
    return RedirectResponse(url=f"/?lang={lang}", status_code=303)