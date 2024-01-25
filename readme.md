Для установки зависимостей в терминале наберите poetry install
Переименуйте env_example в .env и заполните переменные окружения своими значениями
Создайте базу данных в Postgres с именем, указанным в .env POSTGRES_DB=
Создайте суперпользователя командой python manage.py csu

Для запуска рассылок вручную используйте команду python manage.py start_mailing
Для добавления cron задачи используйте команду python manage.py crontab add