import os, time, random, base64, requests
import config as cfg

def generate_logo(forma: str, style: str, description: str, output_dir="static") -> str:
    """
    Отправляет запрос в YandexART, ждёт готовности и сохраняет результат.
    Возвращает путь к файлу или текст ошибки.
    """
    headers = {
        "Authorization": f"Bearer {cfg.IAM_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "modelUri": f"art://{cfg.CATALOG_ID}/yandex-art/latest",
        "generationOptions": {
            "seed": str(random.randint(0, 1_000_000)),
            "aspectRatio": {"widthRatio": "1", "heightRatio": "1"}
        },
        "messages": [
            {
                "weight": "1",
                "text": f"Нарисуй логотип в форме {forma}, под описание: {description}, в стиле: {style}"
            }
        ]
    }

    # 1. Отправляем задачу
    resp = requests.post(cfg.URL_GEN, headers=headers, json=payload)
    if resp.status_code != 200:
        return f"Ошибка запроса: {resp.status_code} — {resp.text}"

    request_id = resp.json().get("id")
    # 2. Ждём готовности (примерно 20 сек)
    time.sleep(20)

    # 3. Получаем результат
    headers.pop("Content-Type", None)
    op = requests.get(f"{cfg.URL_OP}/{request_id}", headers=headers)
    if op.status_code != 200:
        return f"Ошибка ответа: {op.status_code} — {op.text}"

    img_b64 = op.json().get("response", {}).get("image")
    if not img_b64:
        return "Изображение не готово или неверный формат ответа."

    # 4. Сохраняем файл
    os.makedirs(output_dir, exist_ok=True)
    image_path = os.path.join(output_dir, f"{request_id}.jpeg")
    with open(image_path, "wb") as f:
        f.write(base64.b64decode(img_b64))

    return image_path
