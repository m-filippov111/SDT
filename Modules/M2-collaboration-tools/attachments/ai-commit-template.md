````
# Автоматизация написания коммитов через ИИ

## Назначение

Скрипт для автоматической генерации commit message на основе изменений в коде с использованием ИИ-ассистента.

## Установка

1. Установите зависимости:
```bash
pip install openai  # или anthropic, или другие
````

2. Настройте API ключ:

**bash**

```
export OPENAI_API_KEY="your-api-key"
```

3. Настройте Git alias:

**bash**

```
git config --global alias.ai-commit '!python scripts/ai_commit.py'
```

## Использование

**bash**

```
git add <files>
git ai-commit
```

## Примеры

### Пример 1: Добавление новой функции

**Изменения:**

**diff**

```
+ def calculate_average(data: list[float]) -> float:
+     return sum(data) / len(data) if data else 0.0
```

**Сгенерированный коммит:**

**text**
