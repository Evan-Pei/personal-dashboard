from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# 資料儲存檔案
DATA_FILE = 'tasks.json'

def load_tasks():
    """從 JSON 檔案加載任務"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_tasks(tasks):
    """將任務保存到 JSON 檔案"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def get_next_id(tasks):
    """獲取下一個任務 ID"""
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1

# API 路由

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """獲取所有任務"""
    tasks = load_tasks()
    return jsonify(tasks), 200

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """創建新任務"""
    data = request.get_json()
    
    # 驗證必需字段
    if not data or 'title' not in data:
        return jsonify({'error': '缺少必需字段: title'}), 400
    
    tasks = load_tasks()
    
    new_task = {
        'id': get_next_id(tasks),
        'title': data.get('title', '').strip(),
        'description': data.get('description', '').strip(),
        'due_date': data.get('due_date'),
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """獲取單個任務"""
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': '任務未找到'}), 404
    
    return jsonify(task), 200

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """更新任務"""
    data = request.get_json()
    tasks = load_tasks()
    
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({'error': '任務未找到'}), 404
    
    # 更新字段（如果提供了的話）
    if 'title' in data:
        task['title'] = data['title'].strip()
    if 'description' in data:
        task['description'] = data['description'].strip()
    if 'due_date' in data:
        task['due_date'] = data['due_date']
    if 'completed' in data:
        task['completed'] = data['completed']
    
    task['updated_at'] = datetime.now().isoformat()
    
    save_tasks(tasks)
    
    return jsonify(task), 200

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """刪除任務"""
    tasks = load_tasks()
    
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({'error': '任務未找到'}), 404
    
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(tasks)
    
    return jsonify({'message': '任務已刪除'}), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return jsonify({'status': 'ok', 'message': '後端伺服器正在運行'}), 200

@app.errorhandler(404)
def not_found(error):
    """處理 404 錯誤"""
    return jsonify({'error': '端點未找到'}), 404

@app.errorhandler(500)
def internal_error(error):
    """處理 500 錯誤"""
    return jsonify({'error': '內部伺服器錯誤'}), 500

if __name__ == '__main__':
    print("🚀 個人 Dashboard 後端伺服器啟動中...")
    print("📍 伺服器地址: http://localhost:5000")
    print("📝 API 文件:")
    print("   GET    /api/tasks           - 獲取所有任務")
    print("   POST   /api/tasks           - 創建新任務")
    print("   GET    /api/tasks/<id>      - 獲取單個任務")
    print("   PUT    /api/tasks/<id>      - 更新任務")
    print("   DELETE /api/tasks/<id>      - 刪除任務")
    print("   GET    /api/health          - 健康檢查")
    print("-" * 50)
    app.run(debug=True, host='localhost', port=5000)
