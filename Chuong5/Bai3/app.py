from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ================= Các hàm hỗ trợ =================
def parse_number_bai1(val_str):
    if val_str is None or val_str.strip() == "": return None, "Vui lòng nhập một số."
    try: return float(val_str.strip().replace(',', '.')), None
    except ValueError: return None, "Vui lòng nhập một số."

def format_number(val):
    if val is None: return ""
    if isinstance(val, float) and val.is_integer(): return str(int(val))
    return str(val)

def check_score_bai2(val_str):
    if val_str is None or val_str.strip() == "": return None, "Vui lòng nhập một số."
    try:
        num = float(val_str.strip().replace(',', '.'))
        if num < 0 or num > 10: return None, "Điểm phải từ 0 đến 10."
        return num, None
    except ValueError: return None, "Vui lòng nhập một số."

def check_bmi_value(val_str, min_val, max_val, error_msg_range):
    """Kiểm tra điều kiện đầu vào cho bài 3 BMI"""
    if not val_str or val_str.strip() == "":
        return None, "Vui lòng nhập một số."
    try:
        val = float(val_str.strip().replace(',', '.'))
        if val < min_val or val > max_val:
            return None, error_msg_range
        return val, None
    except ValueError:
        return None, "Vui lòng nhập một số."

# ================= Định tuyến =================
@app.route('/')
def index():
    return redirect(url_for('bai1'))

# --------- Bài 1 ---------
@app.route('/bai1', methods=['GET', 'POST'])
def bai1():
    raw_a = raw_b = ""
    op = "+"
    error_a = error_b = general_error = result = None

    if request.method == 'POST':
        raw_a = request.form.get('a', '').strip()
        raw_b = request.form.get('b', '').strip()
        op = request.form.get('op', '').strip()

        if op not in ['+', '-', '*', '/']: general_error = "Phép toán không hợp lệ."

        num_a, err_a = parse_number_bai1(raw_a)
        num_b, err_b = parse_number_bai1(raw_b)

        if err_a and err_b:
            error_a = error_b = "Vui lòng nhập một số."
        else:
            error_a, error_b = err_a, err_b

        if not error_b and op == '/' and num_b == 0:
            error_b = "Không thể chia cho 0."

        if not error_a and not error_b and not general_error:
            res_val = num_a + num_b if op == '+' else \
                      num_a - num_b if op == '-' else \
                      num_a * num_b if op == '*' else \
                      num_a / num_b
            str_a = format_number(num_a)
            str_b = format_number(num_b)
            str_res = format_number(round(res_val, 4))
            result = f"{str_a} {op} {str_b} = {str_res}"

    return render_template('index.html', active_page='bai1', 
                           raw_a=raw_a, raw_b=raw_b, op=op, 
                           error_a=error_a, error_b=error_b, 
                           general_error=general_error, result=result)

# --------- Bài 2 ---------
@app.route('/bai2', methods=['GET', 'POST'])
def bai2():
    raw_cc = raw_gk = raw_ck = ""
    raw_w_cc = "10"; raw_w_gk = "30"; raw_w_ck = "60"
    
    error_cc = error_gk = error_ck = error_weight = None
    he_10 = he_4 = diem_chu = trang_thai = None
    calculated = False

    if request.method == 'POST':
        raw_cc = request.form.get('cc', '').strip()
        raw_gk = request.form.get('gk', '').strip()
        raw_ck = request.form.get('ck', '').strip()
        
        raw_w_cc = request.form.get('weight_cc', '10').strip()
        raw_w_gk = request.form.get('weight_gk', '30').strip()
        raw_w_ck = request.form.get('weight_ck', '60').strip()

        num_cc, error_cc = check_score_bai2(raw_cc)
        num_gk, error_gk = check_score_bai2(raw_gk)
        num_ck, error_ck = check_score_bai2(raw_ck)

        w_cc = w_gk = w_ck = 0
        try:
            w_cc = float(raw_w_cc)
            w_gk = float(raw_w_gk)
            w_ck = float(raw_w_ck)
            if w_cc + w_gk + w_ck != 100:
                error_weight = "Tổng trọng số phải đúng bằng 100%."
        except ValueError:
            error_weight = "Trọng số phải là dạng số."

        if not error_cc and not error_gk and not error_ck and not error_weight:
            calculated = True
            he_10 = round((num_cc * (w_cc / 100)) + (num_gk * (w_gk / 100)) + (num_ck * (w_ck / 100)), 1)

            if num_ck < 1.0:
                diem_chu = "F"; he_4 = 0.0
            else:
                if he_10 >= 8.5: diem_chu = "A"; he_4 = 4.0
                elif he_10 >= 7.0: diem_chu = "B"; he_4 = 3.0
                elif he_10 >= 5.5: diem_chu = "C"; he_4 = 2.0
                elif he_10 >= 4.0: diem_chu = "D"; he_4 = 1.0
                else: diem_chu = "F"; he_4 = 0.0
                    
            trang_thai = "Trượt môn" if diem_chu == "F" else "Qua môn"

    return render_template('index.html', active_page='bai2', 
                           raw_cc=raw_cc, raw_gk=raw_gk, raw_ck=raw_ck,
                           raw_w_cc=raw_w_cc, raw_w_gk=raw_w_gk, raw_w_ck=raw_w_ck,
                           error_cc=error_cc, error_gk=error_gk, error_ck=error_ck,
                           error_weight=error_weight,
                           calculated=calculated, he_10=he_10, he_4=he_4, 
                           diem_chu=diem_chu, trang_thai=trang_thai)

# --------- Bài 3 ---------
@app.route('/bai3', methods=['GET', 'POST'])
def bai3():
    raw_cao = raw_nang = ""
    error_cao = error_nang = None
    bmi = phan_loai = mau_sac = can_nang_ly_tuong = None
    calculated = False

    if request.method == 'POST':
        raw_cao = request.form.get('cao', '').strip()
        raw_nang = request.form.get('nang', '').strip()

        # Kiểm tra khoảng giới hạn theo đề bài
        num_cao, error_cao = check_bmi_value(raw_cao, 50, 250, "Giá trị phải từ 50 đến 250.")
        num_nang, error_nang = check_bmi_value(raw_nang, 10, 300, "Giá trị phải từ 10 đến 300.")

        if not error_cao and not error_nang:
            calculated = True
            # Chuyển cm sang m
            h_m = num_cao / 100.0
            # Công thức BMI
            bmi = round(num_nang / (h_m ** 2), 1)

            # Phân loại Châu Á & Chọn màu
            if bmi < 18.5:
                phan_loai = "Thiếu cân"
                mau_sac = "warning" # Vàng
            elif bmi < 23.0:
                phan_loai = "Bình thường"
                mau_sac = "success" # Xanh
                # Cân nặng lý tưởng chỉ hiển thị khi BMI bình thường
                min_w = round(18.5 * (h_m ** 2), 1)
                max_w = round(22.9 * (h_m ** 2), 1)
                can_nang_ly_tuong = f"{min_w} - {max_w} kg"
            elif bmi < 25.0:
                phan_loai = "Thừa cân"
                mau_sac = "warning" # Vàng
            else:
                phan_loai = "Béo phì"
                mau_sac = "danger" # Đỏ

    return render_template('index.html', active_page='bai3',
                           raw_cao=raw_cao, raw_nang=raw_nang,
                           error_cao=error_cao, error_nang=error_nang,
                           calculated=calculated, bmi=bmi,
                           phan_loai=phan_loai, mau_sac=mau_sac,
                           can_nang_ly_tuong=can_nang_ly_tuong)

if __name__ == '__main__':
    app.run(debug=True)