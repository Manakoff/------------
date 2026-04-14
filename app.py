from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
# Добавляем импорт валидатора
from email_validator import validate_email, EmailNotValidError

load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    try:
        # 1. ЗАЩИТА ОТ БОТОВ (Honeypot)
        # Если это поле заполнено — значит, форму отправил скрипт-бот
        if request.form.get('honeypot_field'):
            print("Обнаружен бот (Honeypot)")
            return '', 200  # Возвращаем успех, чтобы бот не пытался снова

        # Получаем данные
        name = request.form.get('name', 'Не указано')
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', 'Не указано')
        message = request.form.get('message', 'Без сообщения')

        # 2. ПРОВЕРКА НА ССЫЛКИ (Защита от спам-рекламы)
        # Если в сообщении есть http или www — блокируем
        forbidden = ["http://", "https://", "www.", ".com", ".ru", ".net"]
        if any(link in message.lower() for link in forbidden):
            return "Ссылки в сообщении запрещены для защиты от спама", 400

        # 3. ВАЛИДАЦИЯ EMAIL
        try:
            # check_deliverability=True проверяет реальность домена почты
            valid = validate_email(email, check_deliverability=True)
            email = valid.normalized
        except EmailNotValidError as e:
            return f"Некорректный адрес почты: {str(e)}", 400

        # 4. ОТПРАВКА ПИСЬМА (если проверки пройдены)
        body = f"Имя: {name}\nEmail: {email}\nТелефон: {phone}\nСообщение: {message}"
        msg = MIMEText(body)
        msg['Subject'] = 'ЗАЯВКА С САЙТА ЛИЧНЫЙ ЮРИСТ'
        msg['From'] = os.getenv('MAIL_USER')
        msg['To'] = os.getenv('MAIL_RECEIVER')

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(os.getenv('MAIL_USER'), os.getenv('MAIL_PASS'))
            server.send_message(msg)
        
        return '', 200 

    except Exception as e:
        print(f"Ошибка: {e}")
        return "Произошла ошибка при отправке", 500

if __name__ == '__main__':
    # На живом сервере порт 80 часто требует прав sudo
    app.run(host='0.0.0.0', port=80)