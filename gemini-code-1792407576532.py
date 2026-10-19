import requests

# ==========================================
# 🔑 КОНФИГУРАЦИЯ И КЛЮЧИ
# ==========================================
PUSHBULLET_TOKEN = "o.w9M6Z3LIMZxiqoLRLHFGzGNbrRqoN0BC"
API_KEY = "ad67a9b5dd04d7ec035f243f12fc8d14"


# ==========================================
# 📲 ФУНКЦИЯ ОТПРАВКИ УВЕДОМЛЕНИЯ В PUSHBULLET
# ==========================================
def send_pushbullet_notification(title: str, body: str):
    """
    Отправляет пуш-уведомление на ваши устройства через Pushbullet API.
    """
    url = "https://api.pushbullet.com/v2/pushes"
    headers = {
        "Access-Token": PUSHBULLET_TOKEN,
        "Content-Type": "application/json"
    }
    data = {
        "type": "note",
        "title": title,
        "body": body
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("✅ Пуш-уведомление успешно отправлено!")
        else:
            print(f"❌ Ошибка отправки: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")


# ==========================================
# 📊 ЛОГИКА СТРАТЕГИИ ДАЛЛАСА
# ==========================================
def check_dallas_strategy(match_data: dict) -> tuple[bool, str]:
    """
    Проверяет Live-матч на соответствие критериям Стратегии Далласа.
    """
    minute = match_data.get("minute", 0)
    if not (15 <= minute <= 25):
        return False, f"Минута матча ({minute}) не подходит (нужно 15-25)."

    fav_prematch_odds = match_data.get("fav_prematch_odds", 0.0)
    if not (1.25 <= fav_prematch_odds <= 1.65):
        return False, f"Кэф на фаворита ({fav_prematch_odds}) вне диапазона 1.25–1.65."

    fav_possession = match_data.get("fav_possession", 0)
    underdog_shots = match_data.get("underdog_shots", 0)
    underdog_shots_on_target = match_data.get("underdog_shots_on_target", 0)
    underdog_corners = match_data.get("underdog_corners", 0)
    underdog_goals = match_data.get("underdog_goals", 0)

    # Фильтры безопасности
    if underdog_goals > 0:
        return False, "Аутсайдер уже забил гол."

    if fav_possession < 60:
        return False, f"Низкое владение фаворита: {fav_possession}%."

    if underdog_shots >= 4:
        return False, f"Слишком много ударов у аутсайдера: {underdog_shots}."

    if underdog_shots_on_target > 1:
        return False, f"Удары в створ у аутсайдера: {underdog_shots_on_target}."

    if underdog_corners > 2:
        return False, f"Много угловых у аутсайдера: {underdog_corners}."

    # Текст уведомления
    body_text = (
        f"Матч: {match_data.get('teams', 'Неизвестно')}\n"
        f"Минута: {minute}'\n"
        f"Владение фаворита: {fav_possession}%\n"
        f"Удары аутсайдера (всего/в створ): {underdog_shots}/{underdog_shots_on_target}\n"
        f"Угловые аутсайдера: {underdog_corners}\n\n"
        f"💡 Рекомендация: Ставка на ИТМ 0.5 (или ИТМ 1.0) аутсайдера."
    )

    return True, body_text


# ==========================================
# 🚀 ЗАПУСК И ПРОВЕРКА
# ==========================================
if __name__ == "__main__":
    # Тестовый матч
    test_match = {
        "teams": "Реал Мадрид — Хетафе",
        "minute": 20,
        "fav_prematch_odds": 1.35,
        "fav_possession": 68,
        "underdog_shots": 1,
        "underdog_shots_on_target": 0,
        "underdog_corners": 1,
        "underdog_goals": 0
    }

    is_signal, message = check_dallas_strategy(test_match)

    if is_signal:
        print("Найден сигнал по стратегии Далласа! Отправляем пуш...")
        send_pushbullet_notification(
            title="🎯 Сигнал: Стратегия Далласа",
            body=message
        )
    else:
        print(f"Матч не подходит: {message}")