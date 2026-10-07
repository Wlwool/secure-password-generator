import secrets
import string

from flask import Flask, render_template, request
from flask.typing import ResponseReturnValue

app = Flask(__name__)

MIN_LENGTH = 4
MAX_LENGTH = 32
SYMBOLS = "!@#$%^&*()_+"
LENGTH_ERROR = f"Длина пароля должна быть от {MIN_LENGTH} до {MAX_LENGTH}."


def generate_password(
    length_pass: int = 12,
    use_upper: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """Генерация безопасного пароля с указанными параметрами"""
    pools = [string.ascii_lowercase]
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append(SYMBOLS)

    if length_pass < len(pools):
        raise ValueError("Длина меньше числа выбранных типов символов")

    all_chars = "".join(pools)
    chars = [secrets.choice(pool) for pool in pools]
    chars += [secrets.choice(all_chars) for _ in range(length_pass - len(pools))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def calculate_password_strength(
    password: str, use_upper: bool, use_digits: bool, use_symbols: bool
) -> int:
    """Расчет сложности пароля (0-100)"""
    score = 0
    length = len(password)

    # Оценка по длине (максимум 40 баллов)
    if length >= 16:
        score += 40
    elif length >= 12:
        score += 30
    elif length >= 8:
        score += 20
    else:
        score += 10

    # Оценка по типам символов (максимум 60 баллов)
    char_types = 1  # всегда есть строчные буквы
    if use_upper:
        char_types += 1
    if use_digits:
        char_types += 1
    if use_symbols:
        char_types += 1

    score += (char_types - 1) * 20  # 0, 20, 40, 60 баллов

    return min(score, 100)


@app.route("/")
def home() -> str:
    return render_template("home.html", min_length=MIN_LENGTH, max_length=MAX_LENGTH)


@app.route("/generate", methods=["GET"])
def generate() -> ResponseReturnValue:
    try:
        length = int(request.args.get("length", "12"))
    except ValueError:
        return LENGTH_ERROR, 400
    if not MIN_LENGTH <= length <= MAX_LENGTH:
        return LENGTH_ERROR, 400

    use_upper = "use_upper" in request.args
    use_digits = "use_digits" in request.args
    use_symbols = "use_symbols" in request.args

    try:
        password = generate_password(length, use_upper, use_digits, use_symbols)
        strength = calculate_password_strength(
            password, use_upper, use_digits, use_symbols
        )
        return render_template("password.html", password=password, strength=strength)
    except Exception:
        app.logger.exception("Ошибка при генерации пароля")
        return "Произошла внутренняя ошибка", 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
