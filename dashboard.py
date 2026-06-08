import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import calendar
import requests
import threading


class PersonalDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("個人 Dashboard")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')

        # API 基礎 URL
        self.api_url = "http://localhost:5000/api"

        # 當前顯示的月份
        self.current_date = datetime.now()

        # 存儲任務
        self.tasks = []

        # 創建 UI
        self.create_ui()

        # 加載任務
        self.load_tasks()

    def create_ui(self):
        """創建主 UI"""
        # 主容器
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 頂部：時間和標題
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=10)

        title_label = ttk.Label(top_frame, text="個人 Dashboard", font=("Arial", 24, "bold"))
        title_label.pack(side=tk.LEFT)

        self.time_label = ttk.Label(top_frame, text="", font=("Arial", 14))
        self.time_label.pack(side=tk.RIGHT)

        self.update_time()

        # 中間：月曆和任務列表（左右分割）
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # 左側：月曆
        left_frame = ttk.LabelFrame(content_frame, text="月曆", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.create_calendar_widget(left_frame)

        # 右側：任務列表
        right_frame = ttk.LabelFrame(content_frame, text="任務", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.create_task_widget(right_frame)

    def create_calendar_widget(self, parent):
        """創建月曆部件"""
        # 月份控制
        nav_frame = ttk.Frame(parent)
        nav_frame.pack(fill=tk.X, pady=10)

        prev_btn = ttk.Button(nav_frame, text="< 上月", command=self.prev_month)
        prev_btn.pack(side=tk.LEFT)

        self.month_label = ttk.Label(nav_frame, text="", font=("Arial", 12, "bold"))
        self.month_label.pack(side=tk.LEFT, expand=True, padx=20)

        next_btn = ttk.Button(nav_frame, text="下月 >", command=self.next_month)
        next_btn.pack(side=tk.RIGHT)

        # 日曆顯示
        self.calendar_frame = ttk.Frame(parent)
        self.calendar_frame.pack(fill=tk.BOTH, expand=True)

        self.update_calendar()

    def create_task_widget(self, parent):
        """創建任務部件"""
        # 新增任務按鈕
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        add_btn = ttk.Button(btn_frame, text="+ 新增任務", command=self.add_task_dialog)
        add_btn.pack(side=tk.LEFT)

        # 任務列表（可滾動）
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 10),
            height=15
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.task_listbox.bind('<Double-Button-1>', self.on_task_double_click)
        self.task_listbox.bind('<Delete>', self.on_task_delete)

        scrollbar.config(command=self.task_listbox.yview)

        # 任務操作按鈕
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill=tk.X, pady=(10, 0))

        complete_btn = ttk.Button(action_frame, text="✓ 完成", command=self.mark_task_complete)
        complete_btn.pack(side=tk.LEFT, padx=2)

        delete_btn = ttk.Button(action_frame, text="✕ 刪除", command=self.delete_selected_task)
        delete_btn.pack(side=tk.LEFT, padx=2)

        refresh_btn = ttk.Button(action_frame, text="⟳ 刷新", command=self.load_tasks)
        refresh_btn.pack(side=tk.LEFT, padx=2)

    def update_time(self):
        """更新時間顯示"""
        now = datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=time_str)
        self.root.after(1000, self.update_time)

    def update_calendar(self):
        """更新月曆顯示"""
        # 清除舊的日曆
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # 更新月份標籤
        month_str = self.current_date.strftime("%Y 年 %B 月")
        self.month_label.config(text=month_str)

        # 創建日期網格
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)

        # 星期標題
        weekdays = ["一", "二", "三", "四", "五", "六", "日"]
        for i, day in enumerate(weekdays):
            label = ttk.Label(self.calendar_frame, text=day, font=("Arial", 9, "bold"))
            label.grid(row=0, column=i, padx=2, pady=2, sticky="nsew")

        # 日期按鈕
        today = datetime.now().date()
        for week_num, week in enumerate(cal, start=1):
            for day_num, day in enumerate(week):
                if day == 0:
                    label = ttk.Label(self.calendar_frame, text="")
                else:
                    date_obj = datetime(self.current_date.year, self.current_date.month, day).date()
                    bg_color = "lightblue" if date_obj == today else ""

                    btn = tk.Label(
                        self.calendar_frame,
                        text=str(day),
                        font=("Arial", 10),
                        bg=bg_color,
                        relief=tk.RAISED,
                        padx=5,
                        pady=5
                    )
                    btn.grid(row=week_num, column=day_num, padx=2, pady=2, sticky="nsew")

    def prev_month(self):
        """顯示上一個月"""
        self.current_date -= timedelta(days=1)
        self.current_date = self.current_date.replace(day=1)
        self.update_calendar()

    def next_month(self):
        """顯示下一個月"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.update_calendar()

    def load_tasks(self):
        """從後端加載任務"""

        def fetch():
            try:
                response = requests.get(f"{self.api_url}/tasks", timeout=5)
                if response.status_code == 200:
                    self.tasks = response.json()
                    self.update_task_list()
            except requests.exceptions.RequestException as e:
                messagebox.showerror("錯誤", f"無法連接後端: {str(e)}")

        # 在後台線程中執行請求
        thread = threading.Thread(target=fetch, daemon=True)
        thread.start()

    def update_task_list(self):
        """更新任務列表顯示"""
        self.task_listbox.delete(0, tk.END)

        for i, task in enumerate(self.tasks):
            status = "✓" if task['completed'] else " "
            task_str = f"[{status}] {task['title']}"
            if task['due_date']:
                task_str += f" (期限: {task['due_date']})"

            self.task_listbox.insert(tk.END, task_str)

            # 已完成的任務用灰色顯示
            if task['completed']:
                self.task_listbox.itemconfig(i, fg='gray')

    def add_task_dialog(self):
        """打開新增任務對話框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("新增任務")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()

        # 標題
        ttk.Label(dialog, text="任務標題:").pack(padx=10, pady=(10, 0), anchor="w")
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.pack(padx=10, pady=5)

        # 描述
        ttk.Label(dialog, text="描述:").pack(padx=10, pady=(10, 0), anchor="w")
        desc_text = tk.Text(dialog, height=5, width=40)
        desc_text.pack(padx=10, pady=5)

        # 期限
        ttk.Label(dialog, text="期限 (YYYY-MM-DD):").pack(padx=10, pady=(10, 0), anchor="w")
        due_entry = ttk.Entry(dialog, width=40)
        due_entry.pack(padx=10, pady=5)

        def save_task():
            title = title_entry.get().strip()
            if not title:
                messagebox.showwarning("警告", "請輸入任務標題")
                return

            description = desc_text.get("1.0", tk.END).strip()
            due_date = due_entry.get().strip() if due_entry.get().strip() else None

            def post_task():
                try:
                    payload = {
                        'title': title,
                        'description': description,
                        'due_date': due_date
                    }
                    response = requests.post(f"{self.api_url}/tasks", json=payload, timeout=5)
                    if response.status_code == 201:
                        self.load_tasks()
                        dialog.destroy()
                    else:
                        messagebox.showerror("錯誤", "無法創建任務")
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("錯誤", f"無法連接後端: {str(e)}")

            thread = threading.Thread(target=post_task, daemon=True)
            thread.start()

        save_btn = ttk.Button(dialog, text="保存", command=save_task)
        save_btn.pack(pady=10)

    def on_task_double_click(self, event):
        """雙擊任務編輯"""
        selection = self.task_listbox.curselection()
        if not selection:
            return

        task_idx = selection[0]
        task = self.tasks[task_idx]

        # 編輯對話框
        dialog = tk.Toplevel(self.root)
        dialog.title("編輯任務")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="任務標題:").pack(padx=10, pady=(10, 0), anchor="w")
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.insert(0, task['title'])
        title_entry.pack(padx=10, pady=5)

        ttk.Label(dialog, text="描述:").pack(padx=10, pady=(10, 0), anchor="w")
        desc_text = tk.Text(dialog, height=5, width=40)
        desc_text.insert("1.0", task['description'])
        desc_text.pack(padx=10, pady=5)

        def update_task():
            payload = {
                'title': title_entry.get().strip(),
                'description': desc_text.get("1.0", tk.END).strip()
            }

            def put_task():
                try:
                    response = requests.put(f"{self.api_url}/tasks/{task['id']}", json=payload, timeout=5)
                    if response.status_code == 200:
                        self.load_tasks()
                        dialog.destroy()
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("錯誤", f"無法連接後端: {str(e)}")

            thread = threading.Thread(target=put_task, daemon=True)
            thread.start()

        save_btn = ttk.Button(dialog, text="更新", command=update_task)
        save_btn.pack(pady=10)

    def mark_task_complete(self):
        """標記任務為完成"""
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "請選擇一個任務")
            return

        task_idx = selection[0]
        task = self.tasks[task_idx]

        def put_task():
            try:
                payload = {'completed': True}
                response = requests.put(f"{self.api_url}/tasks/{task['id']}", json=payload, timeout=5)
                if response.status_code == 200:
                    self.load_tasks()
            except requests.exceptions.RequestException as e:
                messagebox.showerror("錯誤", f"無法連接後端: {str(e)}")

        thread = threading.Thread(target=put_task, daemon=True)
        thread.start()

    def delete_selected_task(self):
        """刪除選定任務"""
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "請選擇一個任務")
            return

        if messagebox.askyesno("確認", "確定要刪除此任務嗎？"):
            task_idx = selection[0]
            task = self.tasks[task_idx]

            def delete_task():
                try:
                    response = requests.delete(f"{self.api_url}/tasks/{task['id']}", timeout=5)
                    if response.status_code == 200:
                        self.load_tasks()
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("錯誤", f"無法連接後端: {str(e)}")

            thread = threading.Thread(target=delete_task, daemon=True)
            thread.start()

    def on_task_delete(self, event):
        """按 Delete 鍵刪除任務"""
        self.delete_selected_task()


if __name__ == '__main__':
    root = tk.Tk()
    app = PersonalDashboard(root)
    root.mainloop()