# Инструкция по запуску приложения async-calc
## 1. Установка зависимостей
Убедитесь, что установлен FastApi и Uvicorn:

```pip install fastapi uvicorn```

## 2. Запуск приложения
В терминале (в папке с файлом main.py):

```uvicorn main:app --reload```

## Примеры запросов

`+` **Сложение**

```GET /add?a=10&b=5```


*Ответ:*

```{"operation": "10 + 5", "result": 15}```

**Сложное выражение**

```
POST /set_expression
{
  "expression": "(2+3)*4+(10-2)/(6-3)"
}
```

```GET /evaluate_expression```


*Ответ:*

```{"expression": "(2+3)*4+(10-2)/(6-3)", "result": 26.6666666667}```