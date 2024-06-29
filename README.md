# SiresStatus
![Текст подсказки](RPC-Discord-Life-status/Frame 2.png)

SiresStatus - это приложение, которое позволяет отслеживать вашу текущую активность и обновлять статус на Discord в реальном времени. Это удобный инструмент для пользователей, которые хотят информировать друзей и коллег о своей занятости или текущих действиях, а также иметь возможность быстро менять статус через системный трей.

## Основные функции

- **Отслеживание активностей:** приложение поддерживает множество предустановленных активностей, таких как "Ем", "В туалете", "Играю", "Занят важными делами", "Общаюсь с важным человеком", "Отошел", и "Ничего не делаю".
- **Автоматическое обновление статуса:** текущее состояние активности автоматически обновляется в вашем статусе Discord через Rich Presence.
- **Системный трей:** иконка в системном трее позволяет быстро менять текущую активность, а также выходить из приложения.
- **Создание приглашений в голосовые каналы:** если вы находитесь в голосовом канале, приложение автоматически создаст приглашение, которое можно отправить друзьям для присоединения.

## Установка

1. Скачайте или клонируйте репозиторий с GitHub.
2. Установите необходимые зависимости, используя `pip`:
    ```bash
    pip install -r requirements.txt
    ```
3. Настройте конфигурационные параметры: введите свой `client_id`, `bot_token`, `guild_id` и `user_id` в соответствующие переменные в коде.

## Использование

Для запуска приложения выполните следующую команду:
```bash
python main.py
```

После запуска, в системном трее появится иконка приложения. Кликните на неё правой кнопкой мыши, чтобы выбрать текущую активность или выйти из приложения.

## Пример использования

- Запустите приложение.
- Выберите текущую активность через меню в системном трее.
- Ваш статус в Discord будет автоматически обновлён.
- При необходимости приложение создаст приглашение для голосового канала.

## Примечание

Для корректной работы приложения необходимо, чтобы ваш бот был добавлен в сервер Discord с соответствующими правами и включёнными намерениями (intents).

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности можно найти в файле LICENSE.

## Контакты

Если у вас есть вопросы или предложения, пожалуйста, создайте issue на GitHub или свяжитесь с разработчиком по Discord: `siresmacro`.

---

Этот проект поможет вам легко и удобно обновлять ваш статус в Discord, предоставляя друзьям и коллегам актуальную информацию о вашей текущей деятельности.
