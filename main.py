from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from database import SessionLocal, engine
import models

# Datenbanktabellen erzeugen, falls sie noch nicht existieren
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lebensmittel ERP")

# Verzeichnis für statische Dateien (CSS etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Dependency: Datenbankverbindung bereitstellen und sauber schließen
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Startseite ---
@app.get("/", response_class=HTMLResponse)
def start(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

# --- Kundenübersicht ---
@app.get("/kunden", response_class=HTMLResponse)
def kunden(request: Request, db: Session = Depends(get_db)):
    kunden = db.query(models.Kunde).all()
    return templates.TemplateResponse("kunden.html", {"request": request, "kunden": kunden})

# --- Kunden hinzufügen ---
@app.post("/kunden/neu")
def add_kunde(
    name: str = Form(...),
    adresse: str = Form(""),
    typ: str = Form("B2C"),
    db: Session = Depends(get_db)
):
    k = models.Kunde(name=name, adresse=adresse, typ=typ)
    db.add(k)
    db.commit()
    return RedirectResponse("/kunden", status_code=303)

# --- Produkte ---
@app.get("/produkte", response_class=HTMLResponse)
def produkte(request: Request, db: Session = Depends(get_db)):
    produkte = db.query(models.Produkt).all()
    return templates.TemplateResponse("produkte.html", {"request": request, "produkte": produkte})

@app.post("/produkte/neu")
def add_produkt(
    name: str = Form(...),
    preis: float = Form(...),
    db: Session = Depends(get_db)
):
    p = models.Produkt(name=name, preis=preis)
    db.add(p)
    db.commit()
    return RedirectResponse("/produkte", status_code=303)

# --- Chargen ---
@app.get("/chargen", response_class=HTMLResponse)
def chargen(request: Request, db: Session = Depends(get_db)):
    chargen = db.query(models.Charge).all()
    produkte = db.query(models.Produkt).all()
    return templates.TemplateResponse("chargen.html", {"request": request, "chargen": chargen, "produkte": produkte})

@app.post("/chargen/neu")
def add_charge(
    produkt_id: int = Form(...),
    datum: str = Form(...),
    menge: float = Form(...),
    db: Session = Depends(get_db)
):
    c = models.Charge(
        produkt_id=produkt_id,
        datum=datetime.strptime(datum, "%Y-%m-%d").date(),
        menge=menge
    )
    db.add(c)
    db.commit()
    return RedirectResponse("/chargen", status_code=303)
