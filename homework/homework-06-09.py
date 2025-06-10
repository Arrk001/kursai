import requests


model = "gemma3:4b"


with open('./homework/anyksciai.txt', 'r', encoding='utf-8') as file:
    context = file.read()

user_prompt = input("Prašome užduoti klausimą apie Anykščius: ")

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": model,
        "messages": [
    {
      "role": "system",
      "content": "Visada atsakysi taisyklinga ir natūralia lietuvių kalba."
    },
    {
      "role": "system",
      "content": "Esi naudingas ir draugiškas asistentas, padedantis vartotojams su jų klausimais lietuvių kalba."
    },
    {
      "role": "system",
      "content": "Reikalavimas: Atsakymai turi būti trumpi (1–3 sakiniai) ir orientuoti į aiškų faktą arba rekomendaciją."
    },
    {
      "role": "system",
      "content": "Jei klausimas reikalauja išsamesnio paaiškinimo – pateikti santrauką su nuoroda į papildomą šaltinį (jei prieinamas)."
    },
    {
      "role": "system",
      "content": "Tavo rolė: Anykščių turizmo informacijos centro specialistas, teikiantis praktinę informaciją turistams."
    },
    {
      "role": "system",
      "content": "Turėtumėte atsakyti į vartotojų klausimus tik apie Anykščius. Jei vartotojas prašo pateikti kitos informacijos, tiesiog pasakykite jam, kad klaustų apie Anykščius."
    },
    {
      "role": "user",
      "content": f"context: \"{context}\". question: \"{user_prompt}\""
  }
  ],
        "stream": False
    }
)

response = response.json()
print()
print(response['message']['content'])
