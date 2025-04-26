import os

# Можно через env-переменные, чтобы не держать в коде "в лоб"
IAM_TOKEN  = os.getenv("YANDEX_IAM_TOKEN",  "ваш_iam_токен")
CATALOG_ID = os.getenv("YANDEX_CATALOG_ID", "ваш_catalog_id")

URL_GEN = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"
URL_OP  = "https://llm.api.cloud.yandex.net:443/operations"
