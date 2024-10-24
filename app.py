from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Модель для видео
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)  # Название видео
    description = db.Column(db.Text, nullable=True)    # Описание видео
    file_path = db.Column(db.String(150), nullable=False)  # Путь к файлу видео

# Главная страница с пагинацией
@app.route('/')
@app.route('/page/<int:page>')
def index(page=1):
    per_page = 10  # Количество видео на странице
    pagination = Video.query.order_by(Video.id.desc()).paginate(page, per_page, error_out=False)
    videos = pagination.items
    return render_template('index.html', videos=videos, pagination=pagination)

# Поиск видео
@app.route('/search')
def search():
    query = request.args.get('q')
    if query:
        results = Video.query.filter(Video.title.ilike(f'%{query}%')).all()  # Поиск по названию
    else:
        results = []
    return render_template('search_results.html', results=results, query=query)

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
