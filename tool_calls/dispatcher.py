from tools import get_weather,  forecast

# f-jos pavadinimas, parametrai buna perduodami į šią funkciją
def execute(name: str, **kwargs):
    if name == "weather":
        return get_weather(**kwargs)
    elif name == "forecast":
        return forecast(**kwargs)

