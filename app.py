from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # HTML-файл с Вашей формой

@app.route('/send', methods=['POST'])
def send():
    try:
        # Получаем данные из формы
        name = request.form.get('name', 'Не указано')
        email = request.form.get('email', 'Не указано')
        phone = request.form.get('phone', 'Не указано')
        message = request.form.get('message', 'Без сообщения')

        # Формируем письмо
        body = f"Имя: {name}\nEmail: {email}\nТелефон: {phone}\nСообщение: {message}"
        msg = MIMEText(body)
        msg['Subject'] = 'ЗАЯВКА С САЙТА ЛИЧНЫЙ ЮРИСТА'
        msg['From'] = 'manakoooov@gmail.com'
        msg['To'] = 'manakoooov@gmail.com'

        print("--- Попытка подключения к SMTP Gmail ---")
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.set_debuglevel(1)  # ВКЛЮЧАЕМ ПОДРОБНЫЙ ЛОГ
            server.starttls()
            # Убедитесь, что здесь ваш актуальный 16-значный пароль приложения
            server.login(os.getenv('MAIL_USER'), os.getenv('MAIL_PASS'))
            server.send_message(msg)
        
        return '', 200  # Возвращаем пустой ответ и статус "ОК"
    except Exception as e:
        print(f"Ошибка: {e}")
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
