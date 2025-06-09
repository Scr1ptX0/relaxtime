from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'admin' 

ROOMS_DATA = [
    {
        'id': 1,
        'name': 'Стандартний номер',
        'price': 2500,
        'size': 25,
        'guests': 2,
        'image': '/static/images/rooms/standard.jpg',
        'description': 'Комфортний номер з усіма необхідними зручностями для приємного відпочинку.',
        'amenities': ['Wi-Fi', 'Smart TV', 'Кондиціонер', 'Сейф', 'Міні-холодильник']
    },
    {
        'id': 2,
        'name': 'Номер Делюкс',
        'price': 4200,
        'size': 40,
        'guests': 3,
        'image': '/static/images/rooms/deluxe.jpg',
        'description': 'Просторий номер преміум-класу з елегантним дизайном та розширеними зручностями.',
        'amenities': ['Wi-Fi', 'Smart TV', 'Кондиціонер', 'Сейф', 'Міні-бар', 'Балкон', 'Халати']
    },
    {
        'id': 3,
        'name': 'Джуніор Сьют',
        'price': 6800,
        'size': 65,
        'guests': 4,
        'image': '/static/images/rooms/junior-suite.jpg',
        'description': 'Розкішний сьют з окремою зоною відпочинку та панорамним видом на місто.',
        'amenities': ['Wi-Fi', 'Smart TV', 'Кондиціонер', 'Сейф', 'Міні-бар', 'Джакузі', 'Вітальня', 'Room Service']
    },
    {
        'id': 4,
        'name': 'Президентський сьют',
        'price': 12000,
        'size': 120,
        'guests': 6,
        'image': '/static/images/rooms/presidential.jpg',
        'description': 'Найрозкішніший номер готелю з приватною терасою та ексклюзивними послугами.',
        'amenities': ['Wi-Fi', 'Smart TV', 'Кондиціонер', 'Сейф', 'Міні-бар', 'Джакузі', 'Тераса', 'Консьєрж', 'Кабінет']
    }
]

@app.route('/')
def home():
    return render_template('index.html', rooms=ROOMS_DATA[:3])  # Показуємо 3 кращі номери

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/rooms')
def rooms():
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    guests = request.args.get('guests', type=int)
    
    filtered_rooms = ROOMS_DATA.copy()
    
    if min_price:
        filtered_rooms = [room for room in filtered_rooms if room['price'] >= min_price]
    if max_price:
        filtered_rooms = [room for room in filtered_rooms if room['price'] <= max_price]
    if guests:
        filtered_rooms = [room for room in filtered_rooms if room['guests'] >= guests]
    
    return render_template('rooms.html', rooms=filtered_rooms)

@app.route('/room/<int:room_id>')
def room_detail(room_id):
    room = next((room for room in ROOMS_DATA if room['id'] == room_id), None)
    if not room:
        flash('Номер не знайдено', 'error')
        return redirect(url_for('rooms'))
    return render_template('room_detail.html', room=room)

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form.get('first-name', '') + ' ' + request.form.get('last-name', '')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        if not all([name.strip(), email, subject, message]):
            flash('Будь ласка, заповніть всі обов\'язкові поля', 'error')
            return render_template('contacts.html')
        
        try:
            save_contact_message(name, email, phone, subject, message)
            flash('Дякуємо за ваше повідомлення! Ми зв\'яжемося з вами найближчим часом.', 'success')
            return redirect(url_for('contacts'))
        except Exception as e:
            flash('Виникла помилка при відправці повідомлення. Спробуйте пізніше.', 'error')
    
    return render_template('contacts.html')

@app.route('/booking', methods=['POST'])
def booking():
    """Обробка заявки на бронювання"""
    room_id = request.form.get('room_id')
    check_in = request.form.get('check_in')
    check_out = request.form.get('check_out')
    guests = request.form.get('guests')
    
    room = next((room for room in ROOMS_DATA if room['id'] == int(room_id)), None)
    if not room:
        return jsonify({'status': 'error', 'message': 'Номер не знайдено'})
    
    
    return jsonify({
        'status': 'success', 
        'message': f'Заявка на бронювання номера "{room["name"]}" прийнята! Ми зв\'яжемося з вами для підтвердження.'
    })

def save_contact_message(name, email, phone, subject, message):
    """Зберігає повідомлення від клієнта (можна замінити на запис у базу даних)"""
    with open('contact_messages.txt', 'a', encoding='utf-8') as f:
        f.write(f"\n--- {datetime.now()} ---\n")
        f.write(f"Ім'я: {name}\n")
        f.write(f"Email: {email}\n")
        f.write(f"Телефон: {phone}\n")
        f.write(f"Тема: {subject}\n")
        f.write(f"Повідомлення: {message}\n")
        f.write("-" * 50 + "\n")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)