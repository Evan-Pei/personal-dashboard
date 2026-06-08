from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
CORS(app)


# 數據模型
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.Date)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed': self.completed
        }


# 創建數據庫表
with app.app_context():
    db.create_all()


# API 路由

# 獲取所有任務
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])


# 創建新任務
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': '標題不能為空'}), 400

    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        due_date=datetime.fromisoformat(data['due_date']).date() if data.get('due_date') else None
    )

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201


# 更新任務
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = data['completed']
    if 'due_date' in data:
        task.due_date = datetime.fromisoformat(data['due_date']).date() if data['due_date'] else None

    db.session.commit()
    return jsonify(task.to_dict())


# 刪除任務
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': '任務已刪除'})


# 健康檢查
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
