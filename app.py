from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import markdown
from datetime import datetime
import os
import requests
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 設定用於加密 session 的密鑰:
app.secret_key = ''  

# 使用者列表
users = [
# 設定使用者範例:
# {'username': 'admin', 'password': 'admin'}
]

# 全部的提交結果
submission_results = []
# 分別使用者的提交結果
user_reports = []

# 記錄使用者的上傳次數
user_upload_counts = {}

# 設定上傳檔案的目錄
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    if not session.get('logged_in'):
        # 若使用者未登入，導向登入頁面
        return redirect(url_for('login'))
    
    # 過濾回報紀錄，僅顯示該使用者的回報紀錄
    user_reports = [report for report in submission_results if report['username'] == session['username']]
    # 顯示該使用者的回報紀錄於首頁
    return render_template('index.html', submission_results=user_reports,username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        for user in users:
            if user['username'] == username and user['password'] == password:
                # 登入成功，導向漏洞回報頁面
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('index'))
            
        # 登入失敗，顯示錯誤訊息
        error = '無效的使用者名稱或密碼'
        return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/report')
def report():
    if not session.get('logged_in'):
        # 若使用者未登入，導向登入頁面
        return redirect(url_for('login'))

    # 使用者已登入，顯示通報漏洞頁面
    return render_template('report.html')

@app.route('/logout')
def logout():
    # 將使用者設定為未登入狀態，並清除 session
    session['logged_in'] = False
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/submit-report', methods=['POST'])
def submit_report():
    if not session.get('logged_in'):
        # 若使用者未登入，導向登入頁面
        return redirect(url_for('login'))
    
    username = session['username']
    severity = request.form['severity']
    vulnerability_type = request.form['vulnerability_type']
    attack_description = request.form['attack_description']
    submission_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 更新所有的提交結果
    submission_results.append({
        'username': username,
        'time': submission_time,
        'severity': severity,
        'vulnerability_type': vulnerability_type,
        'attack_description': attack_description
    })


    # 合併成Markdown檔
    markdown = f"## 風險\n\n{severity}\n\n## 類性\n\n{vulnerability_type}\n\n## 敘述\n\n{attack_description}"

    # 線上圖片轉成Markdown格式
    url_pattern = r'(https?://\S+\.(?:png|jpe?g|gif))'

    markdown = re.sub(url_pattern, r'![](\1)', markdown)

    # debug 
    print(request.form)

    # 儲存 Markdown 檔案
    filename = f"{username}-{user_upload_counts.get(username, 0)}.md"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    with open(filepath, 'w') as file:
        file.write(markdown)

    # 更新使用者的上傳次數
    user_upload_counts[username] = user_upload_counts.get(username, 0) + 1

    return redirect(url_for('index'))

# 上傳圖片到Imgur
def upload_to_imgur(image_path):
    client_id = "1a2d4c73c330a74"  # 替换为您的Imgur API客户端ID
    url = "https://api.imgur.com/3/image"

    headers = {
        "Authorization": f"Client-ID {client_id}"
    }

    with open(image_path, "rb") as file:
        files = {"image": file}
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        data = response.json()
        image_url = data["data"]["link"]
        return image_url
    else:
        return None

# 上傳請求
@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"error": "No image found"})

    image = request.files["image"]
    if image.filename == "":
        return jsonify({"error": "No image filename"})

    # 保存上傳的圖片到本地
    image.save("temp_image.png")

    # 上傳圖片到Imgur
    image_url = upload_to_imgur("temp_image.png")

    # 刪除本地臨時圖片檔
    os.remove("temp_image.png")

    if image_url:
        return jsonify({"image_url": image_url})
    else:
        return jsonify({"error": "Image upload failed"})
    
if __name__ == '__main__':
    app.run(debug=True)
