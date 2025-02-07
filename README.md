# Advertisements Platform

## Описание проекта
Веб-приложение для продажи б/у вещей от юридических лиц физическим. Основные пользователи – обычные люди, которые ищут товары на вторичном рынке.

### Основные функции:
- Размещение объявлений о продаже товаров
- Переписка между покупателем и продавцом
- Простой поиск по названию товаров
- В разработке: поиск по категориям и предпочтениям пользователя

## Технологический стек

### Backend (Django):
- **Django** (последняя версия)
- **Django REST Framework** (API)
- **Django SimpleJWT** (аутентификация)
- **Django Corsheaders** (CORS)
- **Библиотека для работы с изображениями**
- **База данных: MySQL** (планируется переход на PostgreSQL)

### Frontend (Angular):
- **Angular** (последняя версия)
- **ky** (облегченный HTTP-клиент)
- **jwt-decode** (декодирование JWT-токенов)

## Развертывание проекта

### Backend (Django)
1. **Установить зависимости** (устанавливаются автоматически при клонировании проекта).
2. **Создать и применить миграции**:
   ```sh
   py manage.py makemigrations
   py manage.py migrate
   ```
3. **Создать суперпользователя**:
   ```sh
   py manage.py createsuperuser
   ```
4. **Запустить сервер**:
   ```sh
   py manage.py runserver
   ```

### Frontend (Angular)
1. Перейти в каталог фронтенда.
2. Запустить Angular-приложение:
   ```sh
   ng serve
   ```  

## API и взаимодействие
Взаимодействие между фронтендом и бэкендом происходит через **REST API**, реализованный на Django REST Framework.

## Будущие доработки
- Разработка алгоритма поиска по категориям и предпочтениям пользователя
- Полный переход на PostgreSQL
- Улучшение дизайна и интерфейса
- Создание админ-панели для модерации сайта

## Репозитории
- **Backend**: [Advertisements_back](https://github.com/Walk1ngScythe/Advertisements_back)
- **Frontend**: [Advertisements_fe](https://github.com/Walk1ngScythe/Advertisements_fe)

