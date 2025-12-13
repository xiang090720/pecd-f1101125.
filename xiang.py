import tkinter as tk
from tkinter import messagebox

def on_button_click():
    name = entry.get()
    if name.strip():
        messagebox.showinfo("訊息", f"你好，{name}！")
    else:
        messagebox.showwarning("警告", "請輸入名字。")

# 建立主視窗
root = tk.Tk()
root.title("Tkinter 示例視窗")
root.geometry("300x180")

# 標籤
label = tk.Label(root, text="請輸入你的名字：", font=("Arial", 12))
label.pack(pady=10)

# 輸入框
entry = tk.Entry(root, width=25)
entry.pack()

# 按鈕
button = tk.Button(root, text="打招呼", command=on_button_click)
button.pack(pady=15)

# 主迴圈
root.mainloop()

