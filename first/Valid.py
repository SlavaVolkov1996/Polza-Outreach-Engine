import re


def valid(email):
    """Проверяет валидность email адреса"""
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return bool(re.match(pattern, email))


def split_email(line):
    """Разделяет строку на отдельные email адреса"""
    if not line.strip():
        return []
    parts = re.split(r'[,\s;]+', line.strip())
    return [part.strip('"') for part in parts if part.strip()]


def from_file(file_path):
    """Считывает email адреса из файла"""
    valid_emails = []
    invalid_emails = []

    with open(file_path, encoding="utf-8") as f:
        for line in f:
            emails = split_email(line)
            for email in emails:
                if valid(email):
                    valid_emails.append(email)
                else:
                    invalid_emails.append(email)

    return valid_emails, invalid_emails


def from_input():
    """Получает email адреса через интерактивный ввод"""
    print('Вводите email через enter или подряд, как удобно.\n'
          'Для завершения введите STOP')

    valid_emails = []
    invalid_emails = []

    while True:
        user_input = input('Введите email (или STOP для завершения): \n').strip()

        if user_input.upper() == 'STOP':
            break

        emails = split_email(user_input)
        for email in emails:
            if valid(email):
                valid_emails.append(email)
            else:
                invalid_emails.append(email)

    return valid_emails, invalid_emails


def MX_status(email):
    """Проверка email-доменов"""
    import dns.resolver

    domain = email.split('@')[1]
    try:
        resolver = dns.resolver.Resolver()
        mx_records = resolver.resolve(domain, 'MX')

        if len(mx_records) > 0:
            return 'Домен валиден'
        else:
            return "MX-записи отсутствуют или некорректны"

    except dns.resolver.NXDOMAIN:
        return 'Домен отсутствует'
    except dns.resolver.NoAnswer:
        return "MX-записи отсутствуют или некорректны"
    except Exception as e:
        return f"Ошибка: {str(e)}"


def print_res(results, invalid_emails, file=None):
    """Выводит данные"""
    print('Валидные email', file=file)
    for email, status in results:
        print(f'{email} - {status}', file=file)
    print('Не валидные данные', file=file)
    for email in invalid_emails:
        print(email, file=file)


def main():
    """Настроечная логика"""
    input_data = input('Каким образом вводим данные?\n1 - Файл .txt\n2 - Из консоли\n')
    if input_data == '1':
        file = input('Введите адрес к файлу и имя\n')
        valid_emails, invalid_emails = from_file(file)
    else:
        valid_emails, invalid_emails = from_input()

    results = []
    for email in valid_emails:
        status = MX_status(email)
        results.append((email, status))

    input_data = input('Каким образом выводим данные?\n1 - Файл .txt\n2 - Из консоли\n')
    if input_data == '1':
        with open('res.txt', 'w', encoding="utf-8") as file:
            print_res(results, invalid_emails, file)
    else:
        print_res(results, invalid_emails)


if __name__ == '__main__':
    main()
