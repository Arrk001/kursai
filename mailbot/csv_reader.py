import csv


def get_bday_people():
    data = []

    with open('mailbot/data/data.csv', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            processed_row = {
                (key or '').strip(): (value or '').strip()
                for key, value in row.items()
            }
            data.append(processed_row)
    return data
