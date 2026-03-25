from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from db.session import init_db, get_db
from models.database import User, BiosRelease, BiosConfig
from exporters.core import export_me_xml, export_gpio_h
import uvicorn
import os

app = FastAPI(
    title="BIOS Portal API",
    description="BIOS Portal 後端：支援下載、設定匯出與 AD 整合",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to BIOS Portal API"}

@app.post("/export/me")
def create_me_export(
    project: str = "BajaSur",
    version: str = "V1.0",
    settings: dict = Body({
        "MeVersion": "15.0",
        "FlashProtection": "Enabled",
        "BootGuard": "Enabled"
    }),
    user: str = "Lyons"
):
    try:
        file_path = export_me_xml(project, version, settings, user)
        return {
            "status": "Success",
            "file_name": os.path.basename(file_path),
            "full_path": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/export/gpio")
def create_gpio_export(
    project: str = "BajaSur",
    gpio_settings: dict = Body({
        "GPP_A0": "0x40000302",
        "GPP_B1": "0x40000201",
        "GPP_C2": "0x40000100"
    })
):
    try:
        file_path = export_gpio_h(project, gpio_settings)
        return {
            "status": "Success",
            "file_name": os.path.basename(file_path),
            "full_path": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mock-ad-login/{username}")
def mock_ad_login(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        new_user = User(
            username=username,
            display_name=f"AD User: {username}",
            department="BIOS Department",
            email=f"{username}@yourcompany.com"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user = new_user
    
    return {
        "status": "Logged in via Mock AD",
        "user_info": {
            "id": user.id,
            "display_name": user.display_name,
            "department": user.department
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
