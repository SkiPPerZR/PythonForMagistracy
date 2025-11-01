from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Async Calculator", description="Простое FastAPI-приложение для вычисления выражений")

class Expression(BaseModel):
    expression: str

current_expression = ""


@app.get("/")
async def root():
    return {"message": "Добро пожаловать в асинхронный калькулятор!"}


@app.get("/add")
async def add(a: float, b: float):
    return {"operation": f"{a} + {b}", "result": a + b}


@app.get("/subtract")
async def subtract(a: float, b: float):
    return {"operation": f"{a} - {b}", "result": a - b}


@app.get("/multiply")
async def multiply(a: float, b: float):
    return {"operation": f"{a} * {b}", "result": a * b}


@app.get("/divide")
async def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Деление на ноль невозможно")
    return {"operation": f"{a} / {b}", "result": a / b}


@app.post("/set_expression")
async def set_expression(data: Expression):
    global current_expression
    current_expression = data.expression
    return {"message": "Выражение установлено", "expression": current_expression}


@app.get("/get_expression")
async def get_expression():
    if not current_expression:
        return {"message": "Текущее выражение не установлено"}
    return {"current_expression": current_expression}


@app.get("/evaluate_expression")
async def evaluate_expression():
    global current_expression
    if not current_expression:
        raise HTTPException(status_code=400, detail="Нет выражения для вычисления")
    try:
        result = eval(current_expression)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка вычисления: {e}")
    return {"expression": current_expression, "result": result}
