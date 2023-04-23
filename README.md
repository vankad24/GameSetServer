# Инструкция по запуску сервера
- Если сильно лень - два раза кликните левой кнопкой мыши на `app.py`
- Если же вы тёртый лимон и любите танцевать с бубном, следующая инструкция по установке Nginx + Gunicorn + Flask на Ubuntu для вас:
1. Устанавливаем пакеты
```
sudo apt update
sudo apt install python3 python3-pip gunicorn nginx mc
pip3 install flask
```
2. Создаём папку
```
cd ~
mkdir flask-app
cd flask-app
```
3. Качаем проект
```
git clone https://github.com/vankad24/GameSetServer
```
4. Проверяем единорога
```
gunicorn --bind 0.0.0.0:8000 wsgi:app
```
5. Создаём сервис командой `sudo nano /etc/systemd/system/flaskapp.service` и вводим туда
```
[Unit]
Description=flaskapp.service - A Flask application run with Gunicorn.
After=network.target

[Service]
User=имя_пользователя
Group=имя_пользователя
WorkingDirectory=/home/имя_пользователя/flask-app
ExecStart=/usr/bin/gunicorn --workers 3 \
--bind unix:/home/имя_пользователя/flask-app/flaskapp.sock wsgi:app

[Install]
WantedBy=multi-user.target
```
где вместо `имя_пользователя` нужно ввести ваше имя

6. Проверяем сервис
```
sudo service flaskapp start
sudo service flaskapp status
```
7. Добавляем сервис в автозагрузку
```
sudo systemctl enable flaskapp
```
8. Настраиваем Nginx. Переходим в `cd /etc/nginx/` и открываем `sudo mc`
9. В папке sites-available создаём копию default и через **Ctrl+X отпустить + S** делаем ссылку на этот файл в sites-enabled
10. Редактируем в этом файле следующее:
```
location / {
	# First attempt to serve request as file, then
	# as directory, then fall back to displaying a 404.
	# try_files $uri $uri/ =404;
	proxy_pass http://unix:/home/имя_пользователя/flask-app/flaskapp.sock;
}
```
В строках `listen 80` убрать слова `default-server`

11. Проверяем Nginx
```
sudo service nginx configtest
sudo service nginx restart
```
Заходим в браузере на **localhost** или проверяем утилитой `links`:
```
links http://127.0.0.1
```
12. Если nginx выдаёт страницу "bad gateway", смотрим в логи `tail /var/log/nginx/error.log`. Если там ошибка **"(13: Permission denied) while connecting to upstream"**, значит Nginx не имеет прав на запуск сокета.
Для решения проблемы нужно открыть файл `sudo nano /etc/nginx/nginx.conf` и в первой строчке поменять `user www-data;` на `user имя_вашего_пользователя;`
13. Если вы видите многообещающую надпись - поздаравляю, у вас получилось!
