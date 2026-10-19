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
# 📊 ПОЛНЫЙ АЛГОРИТМ СТРАТЕГИИ «ДАЛЛАС»
# ==========================================
def check_dallas_strategy(match_data: dict) -> tuple[bool, str]:
    """
    Проверяет Live-матч по полному алгоритму Стратегии Далласа:
    1. Время: 15–25 минута.
    2. Предматчевый кэф на фаворита: 1.25 – 1.60.
    3. Счет: 0:0 или фаворит ведет, аутсайдер не забивал.
    4. Статистика давления: владение фаворита >= 60%, 
       удары аутсайдера < 4, удары в створ <= 1, угловые <= 2.
    """
    minute = match_data.get("minute", 0)
    if not (15 <= minute <= 25):
        return False, f"Минута матча ({minute}) вне диапазона 15-25."

    fav_odds = match_data.get("fav_prematch_odds", 0.0)
    if not (1.25 <= fav_odds <= 1.60):
        return False, f"Кэф на фаворита ({fav_odds}) вне диапазона 1.25-1.60."

    underdog_goals = match_data.get("underdog_goals", 0)
    if underdog_goals > 0:
        return False, "Аутсайдер уже забил гол."

    fav_possession = match_data.get("fav_possession", 0)
    if fav_possession < 60:
        return False, f"Низкое владение фаворита: {fav_possession}% (нужно >= 60%)."

    underdog_shots = match_data.get("underdog_shots", 0)
    if underdog_shots >= 4:
        return False, f"Слишком много ударов у аутсайдера: {underdog_shots}."

    underdog_shots_on_target = match_data.get("underdog_shots_on_target", 0)
    if underdog_shots_on_target > 1:
        return False, f"Удары в створ у аутсайдера: {underdog_shots_on_target}."

    underdog_corners = match_data.get("underdog_corners", 0)
    if underdog_corners > 2:
        return False, f"Много угловых у аутсайдера: {underdog_corners}."

    # Если все критерии алгоритма соблюдены — формируем сигнал
    signal_report = (
        f"⚽ Матч: {match_data.get('teams', 'Неизвестно')}\n"
        f"⏱ Минута: {minute}'\n"
        f"📈 Кэф на фаворита: {fav_odds}\n"
        f"📊 Владение фаворита: {fav_possession}%\n"
        f"🎯 Удары аутсайдера (всего/в створ): {underdog_shots}/{underdog_shots_on_target}\n"
        f"🚩 Угловые аутсайдера: {underdog_corners}\n\n"
        f"💡 РЕКОМЕНДАЦИЯ: Ставка на ИТМ 0.5 (или 1.0) аутсайдера."
    )

    return True, signal_report


# ==========================================
# 🚀 ЗАПУСК СКРИПТА
# ==========================================
if __name__ == "__main__":
    # Тестовые данные матча под алгоритм
    live_match_example = {
        "teams": "Манчестер Сити — Фулхэм",
        "minute": 19,
        "fav_prematch_odds": 1.32,
        "fav_possession": 71,
        "underdog_shots": 1,
        "underdog_shots_on_target": 0,
        "underdog_corners": 1,
        "underdog_goals": 0
    }

    print("Анализ матча по стратегии «Даллас»...")
    is_signal, message = check_dallas_strategy(live_match_example)

    if is_signal:
        print("🔥 Найден подходящий матч! Отправляем пуш на устройство...")
        send_pushbullet_notification(
            title="🎯 СИГНАЛ: Стратегия Далласа",
            body=message
        )
    else:
        print(f"❌ Матч отклонен фильтрами: {message}")