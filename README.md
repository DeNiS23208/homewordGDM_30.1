# 📦 Django REST API с CI/CD и деплоем

## 🚀 Развёртывание на сервере

1. Подключитесь к серверу по SSH:
   ```bash
   ssh -i ~/.ssh/id_rsa denis@89.169.178.245
   ```

2. Клонируйте репозиторий:
   ```bash
   git clone <URL_РЕПОЗИТОРИЯ>
   cd homewordGDM_30.1
   ```

3. Скопируйте переменные окружения:
   ```bash
   cp .env.template .env
   ```

4. Запустите проект:
   ```bash
   docker-compose up -d --build
   ```

---

## ⚙️ CI/CD через GitHub Actions

Проект использует автоматическую систему CI/CD:

- ✅ При `push` в ветку `develop`:
  - запускается GitHub Actions
  - выполняются тесты с помощью `pytest`
  - если тесты прошли — выполняется деплой на сервер

### 📌 Секреты GitHub (Secrets)

- `HOST` — IP сервера
- `USERNAME` — SSH-логин (например, `denis`)
- `SSH_KEY` — приватный SSH-ключ

---

## 🧪 Запуск пайплайна вручную (если включено)

Если настроено `workflow_dispatch`, можно запустить CI/CD руками:
- Перейти во вкладку **Actions**
- Выбрать **CI/CD workflow**
- Нажать **Run workflow**
