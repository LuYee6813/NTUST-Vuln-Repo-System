from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import markdown
from datetime import datetime
import os
import requests
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 設定用於加密 session 的密鑰
app.secret_key = 'NTUST-XX@@@!!@!@'  

# 使用者列表
users = [
    {'username': 'root', 'password': 'root'},
    {'username': 'user1', 'password': 'password1'},
    {'username': 'user2', 'password': 'password2'},
    {'username': 'A10815003', 'password': 'A10815003'},
    {'username': 'B10730032', 'password': 'B10730032'},
    {'username': 'B10801013', 'password': 'B10801013'},
    {'username': 'B10801032', 'password': 'B10801032'},
    {'username': 'B10807005', 'password': 'B10807005'},
    {'username': 'B10808058', 'password': 'B10808058'},
    {'username': 'B10815025', 'password': 'B10815025'},
    {'username': 'B10815029', 'password': 'B10815029'},
    {'username': 'B10815030', 'password': 'B10815030'},
    {'username': 'B10815053', 'password': 'B10815053'},
    {'username': 'B10815062', 'password': 'B10815062'},
    {'username': 'B10902118', 'password': 'B10902118'},
    {'username': 'B10915001', 'password': 'B10915001'},
    {'username': 'B10915003', 'password': 'B10915003'},
    {'username': 'B10915017', 'password': 'B10915017'},
    {'username': 'B10915018', 'password': 'B10915018'},
    {'username': 'B10915019', 'password': 'B10915019'},
    {'username': 'B10915020', 'password': 'B10915020'},
    {'username': 'B10915021', 'password': 'B10915021'},
    {'username': 'B10915022', 'password': 'B10915022'},
    {'username': 'B10915023', 'password': 'B10915023'},
    {'username': 'B10915024', 'password': 'B10915024'},
    {'username': 'B10915025', 'password': 'B10915025'},
    {'username': 'B10915026', 'password': 'B10915026'},
    {'username': 'B10915027', 'password': 'B10915027'},
    {'username': 'B10915029', 'password': 'B10915029'},
    {'username': 'B10915030', 'password': 'B10915030'},
    {'username': 'B10915031', 'password': 'B10915031'},
    {'username': 'B10915032', 'password': 'B10915032'},
    {'username': 'B10915033', 'password': 'B10915033'},
    {'username': 'B10915034', 'password': 'B10915034'},
    {'username': 'B10915036', 'password': 'B10915036'},
    {'username': 'B10915037', 'password': 'B10915037'},
    {'username': 'B10915038', 'password': 'B10915038'},
    {'username': 'B10915040', 'password': 'B10915040'},
    {'username': 'B10915043', 'password': 'B10915043'},
    {'username': 'B10915044', 'password': 'B10915044'},
    {'username': 'B10915045', 'password': 'B10915045'},
    {'username': 'B10915047', 'password': 'B10915047'},
    {'username': 'B10915048', 'password': 'B10915048'},
    {'username': 'B10915049', 'password': 'B10915049'},
    {'username': 'B10915050', 'password': 'B10915050'},
    {'username': 'B10915052', 'password': 'B10915052'},
    {'username': 'B10915053', 'password': 'B10915053'},
    {'username': 'B10915054', 'password': 'B10915054'},
    {'username': 'B10915057', 'password': 'B10915057'},
    {'username': 'B10915060', 'password': 'B10915060'},
    {'username': 'B10915061', 'password': 'B10915061'},
    {'username': 'B10915062', 'password': 'B10915062'},
    {'username': 'B10915065', 'password': 'B10915065'},
    {'username': 'B10930002', 'password': 'B10930002'},
    {'username': 'B10930003', 'password': 'B10930003'},
    {'username': 'B10930005', 'password': 'B10930005'},
    {'username': 'B10930012', 'password': 'B10930012'},
    {'username': 'B10930031', 'password': 'B10930031'},
    {'username': 'B10930032', 'password': 'B10930032'},
    {'username': 'B10930033', 'password': 'B10930033'},
    {'username': 'B10930039', 'password': 'B10930039'},
    {'username': 'B10930218', 'password': 'B10930218'},
    {'username': 'B10931040', 'password': 'B10931040'},
    {'username': 'B10932002', 'password': 'B10932002'},
    {'username': 'B10932009', 'password': 'B10932009'},
    {'username': 'B10932012', 'password': 'B10932012'},
    {'username': 'B10932013', 'password': 'B10932013'},
    {'username': 'B10932014', 'password': 'B10932014'},
    {'username': 'B10932015', 'password': 'B10932015'},
    {'username': 'B10932017', 'password': 'B10932017'},
    {'username': 'B10932023', 'password': 'B10932023'},
    {'username': 'B10932026', 'password': 'B10932026'},
    {'username': 'B10932029', 'password': 'B10932029'},
    {'username': 'B10932031', 'password': 'B10932031'},
    {'username': 'B10932033', 'password': 'B10932033'},
    {'username': 'B10932043', 'password': 'B10932043'},
    {'username': 'B10932056', 'password': 'B10932056'},
    {'username': 'B10932058', 'password': 'B10932058'},
    {'username': 'B10933029', 'password': 'B10933029'},
    {'username': 'B11015020', 'password': 'B11015020'},
    {'username': 'B11015033', 'password': 'B11015033'},
    {'username': 'B11015034', 'password': 'B11015034'},
    {'username': 'B11031010', 'password': 'B11031010'},
    {'username': 'B11032011', 'password': 'B11032011'},
    {'username': 'B11032020', 'password': 'B11032020'},
    {'username': 'M11115016', 'password': 'M11115016'},
    {'username': 'M11115082', 'password': 'M11115082'},
    {'username': 'B11015018', 'password': 'B11015018'},
    {'username': 'B11015087', 'password': 'B11015087'},
    {'username': 'teacher', 'password': 'teacher'},
    {'username': 'admin', 'password': 'admin'}
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
