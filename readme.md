# Проект Team Finder
## Локальный запуск (Docker)

Для запуска проекта на вашем компьютере должны быть установлены Docker и Docker Compose.

### 1. Подготовка окружения
Клонируйте репозиторий и перейдите в папку с проектом:
```bash
git clone https://github.com/yapimiu/team-finder-ad
cd team-finder
```

Создайте файл `.env` в корневой директории проекта и укажите необходимые переменные окружения:
```env
SECRET_KEY=xqew%b$$zd@27!2=!(yf5*$$bqu8c^&xs#pp#@ec3b9k&cz+a1u!
DJANGO_DEBUG=True

POSTGRES_DB=team_finder-bd
POSTGRES_USER=postgres
POSTGRES_PASSWORD=superpassword123
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

TASK_VERSION=1

DB_NAME=teamfinder_db
DB_USER=postgres
DB_PASSWORD=supersecretpassword
DB_HOST=db
DB_PORT=5432
```

### 2. Сборка и запуск контейнеров
Запустите сборку образов и старт контейнеров в фоновом режиме:
```bash
docker-compose up --build -d
```

### 3. Настройка базы данных
Примените миграции для создания структуры таблиц в PostgreSQL:
```bash
docker-compose exec web python manage.py migrate
```

Создайте учетную запись суперпользователя для доступа к панели администратора:
```bash
docker-compose exec web python manage.py createsuperuser
```

### 4. Использование
После успешного запуска проект будет доступен в браузере по адресу:
* Главная страница: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* Панель администратора: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

#### Созданные пользователи
1. Логин - yapimiu@gmail.com (супер пользователь)
    
    Пароль - 1
2. Логин - petr@gmail.com (обычный пользователь)
    
    Пароль - 12

Для остановки работы проекта используйте команду:
```bash
docker-compose down
```

