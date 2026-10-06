from flask import Flask, request, redirect, abort

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

STUDENTS = {
    "23T1020001": {"name": "Nguyễn Văn An", "Lop": "K47A", "scores": {"PMNM": 8.5, "CSDL": 7.0, "MMT": 9.0}},
    "23T1020002": {"name": "Trần Thị Bình", "Lop": "K47A", "scores": {"PMNM": 6.0, "CSDL": 5.5, "MMT": 7.0}},
    "23T1020003": {"name": "Lê Hoàng Cường", "Lop": "K47B", "scores": {"PMNM": 9.5, "CSDL": 9.0}},
    "23T1020004": {"name": "Phạm Minh Dũng", "Lop": "K47B", "scores": {"PMNM": 4.0, "CSDL": 3.5, "MMT": 5.0}},
    "23T1020005": {"name": "Hoàng Thu Hà", "Lop": "K47A", "scores": {}},
    "23T1020006": {"name": "Vũ Quốc Khánh", "Lop": "K47C", "scores": {"PMNM": 7.5, "MMT": 8.0}},
}

def calculate_avg_score(scores):
    if not scores:
        return None
    return round(sum(scores.values()) / len(scores), 2)

def get_grade(score):
    if score is None:
        return "-"
    if score >= 8.5:
        return "Xuất sắc"
    elif score >= 7.0:
        return "Khá"
    elif score >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

@app.route('/')
def index():
    total_students = len(STUDENTS)
    total_classes = len(set(info["Lop"] for info in STUDENTS.values()))
    
    return f"""
    <h1>Thống kê sinh viên</h1>
    <p>Tổng số sinh viên: <b>{total_students}</b></p>
    <p>Tổng số lớp (không trùng): <b>{total_classes}</b></p>
    <hr>
    <h3>Liên kết điều hướng:</h3>
    <ul>
        <li><a href="/students">Xem danh sách sinh viên (/students)</a></li>
        <li><a href="/api/students">Xem API sinh viên (/api/students)</a></li>
    </ul>
    """

@app.route('/api/students')
def api_students():
    return STUDENTS

@app.route('/students')
def student_list():
    all_classes = sorted(list(set(info["Lop"] for info in STUDENTS.values())))
    selected_class = request.args.get('lop', '').strip()

    filter_html = '<a href="/students">Tất cả</a> | '
    for cls in all_classes:
        filter_html += f'<a href="/students?lop={cls}">{cls}</a> | '

    table_rows = ""
    found_any = False

    for mssv, info in STUDENTS.items():
        if selected_class and info["Lop"].lower() != selected_class.lower():
            continue

        found_any = True
        avg_score = calculate_avg_score(info["scores"])
        display_score = avg_score if avg_score is not None else "-"
        grade = get_grade(avg_score)

        table_rows += f"""
        <tr>
            <td><a href="/students/{mssv}">{mssv}</a></td>
            <td>{info['name']}</td>
            <td>{info['Lop']}</td>
            <td>{display_score}</td>
            <td>{grade}</td>
        </tr>
        """

    if not found_any:
        content_html = "<p style='color: red;'><b>Không có sinh viên phù hợp.</b></p>"
    else:
        content_html = f"""
        <table border="1" cellpadding="8" style="border-collapse: collapse;">
            <thead>
                <tr style="background-color: #f2f2f2;">
                    <th>MSSV</th>
                    <th>Họ tên</th>
                    <th>Lớp</th>
                    <th>Điểm TB</th>
                    <th>Xếp loại</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
        """

    return f"""
    <h2>Danh sách Sinh viên</h2>
    <p>Thanh lọc: {filter_html}</p>
    {content_html}
    <br><br>
    <a href="/">← Quay lại Trang chủ</a>
    """

@app.route('/students/<mssv>')
def student_detail(mssv):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")

    student = STUDENTS[mssv]
    avg_score = calculate_avg_score(student["scores"])
    grade = get_grade(avg_score)

    scores_dict = student["scores"]
    if not scores_dict:
        score_table_html = "<p><i>Chưa có dữ liệu điểm học phần.</i></p>"
    else:
        score_rows = ""
        for subject, score in scores_dict.items():
            score_rows += f"<tr><td>{subject}</td><td>{score}</td></tr>"
        
        score_table_html = f"""
        <table border="1" cellpadding="6" style="border-collapse: collapse;">
            <thead>
                <tr style="background-color: #f9f9f9;">
                    <th>Học phần</th>
                    <th>Điểm</th>
                </tr>
            </thead>
            <tbody>
                {score_rows}
            </tbody>
        </table>
        """

    return f"""
    <h2>Chi tiết Sinh viên</h2>
    <p><b>Họ tên:</b> {student['name']}</p>
    <p><b>MSSV:</b> {mssv}</p>
    <p><b>Lớp:</b> <a href="/students?lop={student['Lop']}">{student['Lop']}</a></p>
    <p><b>Điểm TB:</b> {avg_score if avg_score is not None else '-'}</p>
    <p><b>Xếp loại:</b> {grade}</p>
    
    <h3>Bảng điểm từng học phần:</h3>
    {score_table_html}
    
    <br><br>
    <a href="/students">← Quay lại danh sách sinh viên</a>
    """

# CÂU 4: LINK RÚT GỌN (/sv/<mssv>)
@app.route('/sv/<mssv>')
def short_link(mssv):
    # Chuyển hướng tới /students/<mssv> với mã trạng thái HTTP 301
    return redirect(f"/students/{mssv}", code=301)

if __name__ == '__main__':
    app.run(debug=True, port=8000)