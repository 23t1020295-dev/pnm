from flask import Flask, render_template, request

app = Flask(__name__)

def parse_number(val_str):
    """
    Chuyển chuỗi thành số thực (float), hỗ trợ cả dấu phẩy (,) và dấu chấm (.)
    """
    if val_str is None or val_str.strip() == "":
        return None, "Vui lòng nhập một số."
    
    val_clean = val_str.strip().replace(',', '.')
    try:
        num = float(val_clean)
        return num, None
    except ValueError:
        return None, "Vui lòng nhập một số."

def format_number(val):
    """Định dạng số: nếu là số nguyên thì hiển thị số nguyên, loại bỏ số 0 vô nghĩa sau dấu phẩy"""
    if val is None:
        return ""
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return str(val)

@app.route('/', methods=['GET', 'POST'])
def calculator():
    raw_a = ""
    raw_b = ""
    op = "+"
    
    error_a = None
    error_b = None
    general_error = None
    result = None

    if request.method == 'POST':
        raw_a = request.form.get('a', '').strip()
        raw_b = request.form.get('b', '').strip()
        op = request.form.get('op', '').strip()

        allowed_ops = ['+', '-', '*', '/']
        if op not in allowed_ops:
            general_error = "Phép toán không hợp lệ."

        num_a, err_a = parse_number(raw_a)
        num_b, err_b = parse_number(raw_b)

        if err_a and err_b:
            error_a = "Vui lòng nhập một số."
            error_b = "Vui lòng nhập một số."
        else:
            if err_a:
                error_a = err_a
            if err_b:
                error_b = err_b

        if not err_b and op == '/' and num_b == 0:
            error_b = "Không thể chia cho 0."

        if not error_a and not error_b and not general_error:
            res_val = None
            if op == '+':
                res_val = num_a + num_b
            elif op == '-':
                res_val = num_a - num_b
            elif op == '*':
                res_val = num_a * num_b
            elif op == '/':
                res_val = num_a / num_b

            str_a = format_number(num_a)
            str_b = format_number(num_b)
            str_res = format_number(round(res_val, 4))
            result = f"{str_a} {op} {str_b} = {str_res}"

    return render_template(
        'index.html',
        raw_a=raw_a,
        raw_b=raw_b,
        op=op,
        error_a=error_a,
        error_b=error_b,
        general_error=general_error,
        result=result
    )

if __name__ == '__main__':
    app.run(debug=True)
