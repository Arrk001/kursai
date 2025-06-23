from datetime import date, datetime


def filter_bday_people(people_list):
    today = date.today()
    filtered_people = []

    for person in people_list:
        bday = datetime.strptime(person['dob'], '%Y-%m-%d').date()
        if bday.month == today.month and bday.day == today.day:
            filtered_people.append(person)
    return filtered_people
