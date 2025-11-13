from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
import json
from pathlib import Path
import re

app = FastAPI(title="Сервис обращений абонентов")
DATA_FILE = Path("data.json")


class UserRequest(BaseModel):
    фамилия: str
    имя: str
    дата_рождения: date
    телефон: str
    email: EmailStr

    @field_validator("фамилия", "имя")
    def validate_name(cls, value):
        if not re.match(r"^[А-ЯЁ][а-яё]+$", value):
            raise ValueError("Допустима только кириллица, первая буква заглавная.")
        return value

    @field_validator("телефон")
    def validate_phone(cls, value):
        if not re.match(r"^\+7\d{10}$", value):
            raise ValueError("Телефон должен быть в формате +7ХХХХХХХХХХ.")
        return value

    @field_validator("дата_рождения")
    def validate_birthdate(cls, value):
        if value > date.today():
            raise ValueError("Дата рождения не может быть в будущем.")
        return value


@app.post("/add_request/")
async def add_request(request: UserRequest):
    data = request.model_dump()

    # читаем старые данные
    if DATA_FILE.exists():
        try:
            old_data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            old_data = []
    else:
        old_data = []

    old_data.append(data)

    # сохраняем
    DATA_FILE.write_text(
        json.dumps(old_data, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )

    return {"message": "Данные сохранены", "data": data}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)