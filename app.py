from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Функции для работы с JSON
def load_entries():
    """Загружает записи из файла entries.json"""
    if not os.path.exists('entries.json'):
        return []
    with open('entries.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_entries(entries):
    """Сохраняет записи в файл entries.json"""
    with open('entries.json', 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

# Загружаем записи при старте
entries = load_entries()

# Задание 13. Главная страница
@app.route('/')
def index():
    return render_template('index.html', entries=entries)

# Задание 14. Просмотр записи
@app.route('/entry/<int:entry_id>')
def view_entry(entry_id):
    entry = next((e for e in entries if e['id'] == entry_id), None)
    if entry:
        return render_template('detail.html', entry=entry)
    return "Запись не найдена", 404

# Задание 15. Добавление записи
@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        # Генерируем новый ID
        new_id = max([e['id'] for e in entries], default=0) + 1
        
        # Создаём запись
        new_entry = {
            'id': new_id,
            'title': title,
            'content': content,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        entries.append(new_entry)
        save_entries(entries)
        return redirect(url_for('index'))
    
    return render_template('add.html')

# Задание 16. Редактирование записи
@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    entry = next((e for e in entries if e['id'] == entry_id), None)
    if not entry:
        return "Запись не найдена", 404
    
    if request.method == 'POST':
        entry['title'] = request.form['title']
        entry['content'] = request.form['content']
        save_entries(entries)
        return redirect(url_for('index'))
    
    return render_template('edit.html', entry=entry)

# Задание 17. Удаление записи
@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    global entries
    entries = [e for e in entries if e['id'] != entry_id]
    save_entries(entries)
    return redirect(url_for('index'))

# Задание 18. Поиск
@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    if query:
        filtered_entries = [e for e in entries if query in e['title'].lower()]
    else:
        filtered_entries = entries
    return render_template('index.html', entries=filtered_entries)

# Задание 19. Фильтр по последним 7 дням
@app.route('/filter/week')
def filter_week():
    week_ago = datetime.now() - timedelta(days=7)
    filtered_entries = []
    
    for e in entries:
        try:
            entry_date = datetime.strptime(e['date'], '%Y-%m-%d %H:%M:%S')
            if entry_date >= week_ago:
                filtered_entries.append(e)
        except:
            # Если дата в неправильном формате, пропускаем
            pass
    
    return render_template('index.html', entries=filtered_entries)

# Задание 20. Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
