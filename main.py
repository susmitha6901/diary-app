from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# -------- FastAPI App --------
app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- Database Setup --------
# -------- Database Setup --------
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # fallback to SQLite for local development
    DATABASE_URL = "sqlite:///./diary.db"

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DiaryEntry(Base):
    __tablename__ = "entries"
    date = Column(String, primary_key=True, index=True)  # format: dd-mm-yyyy
    text = Column(Text, nullable=True)

# Create tables if not exist
Base.metadata.create_all(bind=engine)

# -------- Serve Frontend --------
@app.get("/", response_class=HTMLResponse)
def serve_ui():
    with open("t1.html", "r", encoding="utf-8") as f:
        return f.read()

# -------- API Routes --------
@app.get("/entries/{date}")
def get_entry(date: str):
    """Get diary entry for a specific date (dd-mm-yyyy)."""
    db = SessionLocal()
    entry = db.query(DiaryEntry).filter(DiaryEntry.date == date).first()
    db.close()
    return {"date": date, "entry": entry.text if entry else ""}

@app.post("/entries")
def save_entry(entry_data: dict = Body(...)):
    """Save or update diary entry."""
    date = entry_data.get("date")
    text = entry_data.get("text", "")
    if not date:
        return {"status": "error", "message": "Valid date is required"}
    db = SessionLocal()
    entry = db.query(DiaryEntry).filter(DiaryEntry.date == date).first()
    if entry:
        entry.text = text
    else:
        entry = DiaryEntry(date=date, text=text)
        db.add(entry)
    db.commit()
    db.close()
    return {"status": "success", "message": f"Entry for {date} saved."}

@app.get("/highlighted-dates")
def get_highlighted_dates():
    """Return all dates that have entries."""
    db = SessionLocal()
    entries = db.query(DiaryEntry).all()
    highlighted = []
    for entry in entries:
        if entry.text and entry.text.strip():
            d, m, y = entry.date.split("-")
            highlighted.append(f"{y}-{m}-{d}")
    db.close()
    return {"dates": highlighted}
