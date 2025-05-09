# Файловое хранилище

Проект представляет собой персональное файловое хранилище с графическим интерфейсом и аунтейикацией пользователей.  

## Компоненты

`.example.env` - переменные окружения  
`.docker-compose.yml` - конфиг для docker compose   
`Makefile` - основные скрипты запуска  
`poetry.lock` - служебный файл poetry  
`pyproject.toml` - конфигурационный файл для сборки

### Backend

#### Конфигурация (`config.py`)
- Класс `Config`: Конфигурация приложения
  - Настройки базы данных (PostgreSQL)
  - Настройки JWT аутентификации
  - Настройки хранилища файлов
  - URL префиксы

#### База данных (`db/`)
- `connection.py`: Управление подключениями к БД
  - `async_engine`: Асинхронный движок SQLAlchemy
  - `AsyncSessionLocal`: Фабрика асинхронных сессий
  - `get_db()`: Dependency injection для FastAPI

- `tables.py`: Модели данных
  - `User`: Модель пользователя
    - Поля: id, name, hashed_password, files_count, file_total_size_byte
    - Связи: files (one-to-many)
  - `File`: Модель файла
    - Поля: id, user_id, bytesize, name, index_name, link, is_available, live_time, path
    - Связи: user (many-to-one)

- `initial.py`: Инициализация БД
  - `create_db()`: Создание таблиц
  - `drop_db()`: Удаление таблиц
- `migrations`: Служебная папка системы миграций бд alembic
  - `migrations/versions`: история миграций бд

#### Приложение (`app/`)
##### Безопасность (`security.py`)
- Настройка JWT аутентификации
- Конфигурация AuthX
- Управление токенами доступа

##### Утилиты (`utils.py`)
- `hash_password()`: Хеширование паролей
- `check_hash_password()`: Проверка паролей

#### Точка входа (`main.py`)
- `app` - основной объект приложения fastapi

##### Пользователи (`user/`)
- `api.py`: API endpoints для пользователей (будут далее)
- `schemas.py`: Pydantic модели
  - `UserCreate`: Создание пользователя
  - `UserGet`: Получение информации
  - `UserGetList`: Список пользователей
  - `UserUpdate`: Обновление данных

- `service.py`: Бизнес-логика
  - `UserService`: Управление пользователями
    - Методы: create, get_by_id, get_by_name, get_list, delete_by_id, update

##### Файлы (`file/`)
- `api.py`: API endpoints для файлов (будут далее)
- `schemas.py`: Pydantic модели
  - `FileCreate`: Создание файла
  - `FileGet`: Получение информации
  - `FileGetList`: Список файлов
  - `FileUpdate`: Обновление файла
- `service.py`: Бизнес-логика
  - `FileService`: Управление файлами
    - Методы: create, update, get_list, get_by_link, get, delete

## API Endpoints

### Пользователи
- `POST /file-storage-api/users` - Создание пользователя
- `POST /file-storage-api/users/login` - Авторизация
- `GET /file-storage-api/users` - Список пользователей
- `GET /file-storage-api/users/{name}` - Информация о пользователе

### Файлы
- `POST /file-storage-api/files` - Загрузка файла
- `GET /file-storage-api/files` - Список файлов
- `GET /file-storage-api/files/{index_name}` - Скачивание файла
- `GET /file-storage-api/files/user/{user_id}` - Файлы пользователя
- `PUT /file-storage-api/files/{file_id}` - Обновление файла
- `DELETE /file-storage-api/files/{file_id}` - Удаление файла

#### Тесты (`tests/`)
- `test_config.py`: Тесты конфигурации
- `test_utils.py`: Тесты утилит
- `test_db_initial.py`: Тесты инициализации БД
- `conftest.py`: Конфигурация тестов

### Фронтенд:
`index.html`
- `loginTab/registerTab` - Переключение между вкладками 
-  `registerForm` - Отправка данных регистрации 
- `loginForm` - Отправка данных входа 
- `catOverlay` - Показ анимации с котиком 

`files.html`
- `loadFiles()` - Загружает список файлов пользователя с сервера и отображает их в интерфейсе.
- `formatLiveTime(isoDuration)` -  Форматирует срок хранения файла (из ISO-формата P7D → 7 дней
- `renderFiles(files)` - Отрисовывает список файлов в виде карточек.
- `logout()` - Выход из системы
- `fileUploadForm` Отправляет файл на бэкенд (POST /files):
- `deleteFile(fileId)` Удаляет файл (DELETE /files/{fileId}):
- `showDownloadModal(fileLink) / hideDownloadModal()` Показывает/скрывает модальное окно с ссылкой для скачивания:
