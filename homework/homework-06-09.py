import requests
 
model = "gemma3:4b"
 
with open(r'homework/anyksciai.txt', 'r', encoding='utf-8') as file:
    context = file.read()
 
user_prompt = input("Prašome užduoti klausimą apie Anykščius: ")
 
response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": model,
        "messages": [
            {
    "role": "system",
    "content": (
        "Tu esi Anykščių meras, atsakinėjantis tik apie Anykščius. "
        "Atsakyk tik lietuvių kalba. Griežtai draudžiama atsakyti anglų kalba. "
        "Jeigu naudosi kitą kalbą nei lietuvių, tai bus laikoma klaida. "
        "Atsakymai turi būti aiškūs, taisyklingi, suprantami visiems žmonėms. "
        "Jei klausimas ne apie Anykščius – atsakyk, kad gali atsakyti tik apie Anykščius."
        "Atsakymas privalo būti tarp 1 ir 3 sakinių ilgio, aiškus ir glaustas."
    )
},
            {
                "role": "user",
                "content": f"Kontekstas: \"{context}\". Klausimas: \"{user_prompt}\""
            }
        ],
        "stream": False
    }
)
 
response = response.json()
 
print("\nAtsakymas:")
print(response['message']['content'])