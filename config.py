TOKEN = '5620396282:AAEt3qAUEfcIymylrl1rDOixtiHlwytMR3A'


DB_HOST = 'localhost'
DB_PORT = 3306
DB_LOGIN = 'root'
DB_PASS = 'Neetqw2110'  # mac Neetqw2110 | Neetqw2110+++
DB_NAME = 'taskdb'


# ---------- dadata ------------

D_KEY = '4dc3b433f0ba3cec514a5019580c0688be029c16'
D_SECRET_KEY = '7b0549cd7cfae55471dcceb815f515d402655ffa'

# ------------ yandex --------------

Y_TOKEN = '334f77fd-ed61-4f8d-8b91-6b78273063bf'

# --------- object text ---------

OBJECT_TEXT = {
    'user': {
        # login
        'finish_registration': '✅ Регистрация успешна',
        'login': '😈 Привет',
        'no_login': '🤡 Укажите username и повторите попытку',
        'finish_reg_text': 'Для начала работы введите любое сообщение',
        # key
        'users': '😎 Работяги',
        'add_task': '🥺 Напрячь',
        'my_task': '🥲 Мои задачи',
        
    },
    'task': {
        # login
        'start_add': 'Добавление объекта\nДля проверки корректности вводимых данных я использую возможности "Яндекс.Карты".\nПотому для максимальной валидность, перед добавлением объекта, вы можете свериться с ними 😎',
        'finish_add': '✅ Задача создана',
        # enter data
        'enter_title': ' 📝 Введите заголовок:',
        'enter_text': ' 📝 Введите текст задачи:',
        'enter_executor': ' 📝 Выбор исполнителя:',
        'enter_deadline': ' 📝 Введите кол-во ДНЕЙ до дедлайна:',
        'int_exec': ' ❌ Ошибка ввода. Только числа',
        'enter_rooms': ' 📝 Введите кол-во комнат:',
        'enter_no_rooms': '📝 Тип недвижимости "Земля"\nДля пропуска пунка введите любое число',
        'enter_no_stage': '📝 Тип недвижимости "Земля" или "Дом"\nДля пропуска пунка введите любое число',
        'enter_stage': ' 📝 Введите этаж:',
        'enter_description': ' 📝 Введите описание объекта:',
        'enter_price': ' 📝 Введите цену:',
        'enter_quadrature': ' 📝 Введите площадь:',
        'enter_property_type': '📋 Выберите тип недвижимости:',
        'enter_number_of_storeys': '📋 Введите этажность дома:',
        'no_enter_number_of_storeys': '📝 Тип недвижимости "Земля"\nДля пропуска пунка введите любое число',
        'enter_phone': ' 📝 Введите телефон\nНомер должен начинаться с "+" кода страны\nПример: +79293438481',
        'enter_advertising': ' 📝 Объект в рекламе?',
        # exception
        'exc_stage': '❌ Ошибка ввода. Повторите запрос.\nТекст должен содержать только цифры',
        'exc_price': '❌ Ошибка ввода. Повторите запрос.\nДопустимы только целые числа.',
        'exc_rooms': '❌ Ошибка ввода. Повторите запрос.\nДопустимы только целые числа.',
        'exc_quadrature': '❌ Ошибка ввода. Повторите запрос.\nДопустимы дробные и целые числа.',
        'exc_region': '❌ Ошибка ввода. Повторите запрос.',
        'exc_city': '❌ Ошибка ввода. Повторите запрос.',
        'exc_address': '❌ Ошибка ввода. Повторите запрос.',
        'exc_area': '❌ Ошибка ввода. Повторите запрос.',
        'loading': '💤 Загрузка...'
    },
    'main': {
        'sale_btn': '🏛 Разместить',
        'feed_btn': '🏘 Поиск объекта',
        'my_objects_btn': '🏗 Мои объекты',
        'notification_btn': '🛎 Уведомления',
        'my_settings': '👤 Мои профиль',
        'my_update': 'Редактировать ✏',
        'cancel_btn': '↩️ Отмена',
        'cancel_ok': 'Ок',
        'back_btn': '⬅️ Назад',
        'back_ok': 'Ок',
        'user_info': 'Информация о пользователе 👤'
    },
    'feed': {
        'enter_current_price': '📝 Введите минимальную и максимально допустимую цену в формате: "0000-1111", где 0000-минимальная, а 1111-максимальная цена',
        'no_objects': '🙁 Данных нет',
        'exc_current_price': '❌ Ошибка ввода. \nДанные должны иметь вид: "где 0000-минимальная, а 1111-максимальная цена.',
        'filter': '📋 Фильтр',
        'switch_filter': 'Применить фильтр к ленте ?',
        'feed': 'Лента',
        'objects_with_filter': '✅ Объекты с фильтром:',
        'objects_without_filter': 'Все объекты:',
        'city_btn': 'Населенный пункт',
        'area_btn': 'Район',
        'advertising_btn': 'Реклама',
        'region_btn': 'Регион',
        'rooms_btn': 'Кол-во комнат',
        'price': 'Цена',
        'feed_ok_filter': '✅ Показать ',
        'clear': '❌ Очистить'
    },
    'my_objects': {
        'all': 'Все объекты'
    },
    'notification': {
        'yes': 'Вкл 🔔',
        'no': 'Выкл 🔕',
        'filter': '📋 Фильтр',
        'all': '▶️ Все',
        'settings': 'Настройки уведомлений',
        'filter_btn_ok': ' ✅ Готово',
        'enter_value': '📝 Введите значение',
        'filter_ok': 'Фильтр сохранен.\nУведомления включены🔔',
        'new_object': '🆕 Новый объект 🏠'
    }
}