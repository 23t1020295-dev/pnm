from flask import Flask, render_template, request

app = Flask(__name__)

def check_score(val_str):
    if val_str is None or val_str.strip() == "":
        return None, "Vui lòng nhập một số."
    val_clean = val_str.strip().replace(',', '.')
    try:
        num = float(val_clean)
        if num < 0 or num > 10:
            return None, "Điểm phải từ 0 đến 10."
        return num, None
    except ValueError:
        return None, "Vui lòng nhập một số."

@app.route('/', methods=['GET', 'POST'])
def calculate_grade():
    raw_cc = raw_gk = raw_ck = ""
    error_cc = error_gk = error_ck = None
    he_10 = he_4 = diem_chu = trang_thai = None
    calculated = False

    if request.method == 'POST':
        raw_cc = request.form.get('cc', '').strip()
        raw_gk = request.form.get('gk', '').strip()
        raw_ck = request.form.get('ck', '').strip()

        num_cc, error_cc = check_score(raw_cc)
        num_gk, error_gk = check_score(raw_gk)
        num_ck, error_ck = check_score(raw_ck)

        if not error_cc and not error_gk and not error_ck:
            calculated = True
            he_10 = round(num_cc * 0.1 + num_gk * 0.3 + num_ck * 0.6, 1)

            if num_ck < 1.0:
                diem_chu = "F"
                he_4 = 0.0
            else:
                if he_10 >= 8.5:
                    diem_chu = "A"; he_4 = 4.0
                elif he_10 >= 7.0:
                    diem_chu = "B"; he_4 = 3.0
                elif he_10 >= 5.5:
                    diem_chu = "C"; he_4 = 2.0
                elif he_10 >= 4.0:
                    diem_chu = "D"; he_4 = 1.0
                else:
                    diem_chu = "F"; he_4 = 0.0
                    
            trang_thai = "Trượt môn" if diem_chu == "F" else "Qua môn"

    return render_template(
        'index.html',
        raw_cc=raw_cc, raw_gk=raw_gk, raw_ck=raw_ck,
        error_cc=error_cc, error_gk=error_gk, error_ck=error_ck,
        calculated=calculated, he_10=he_10, he_4=he_4, diem_chu=diem_chu, trang_thai=trang_thai
    )

if __name__ == '__main__':
    app.run(debug=True)