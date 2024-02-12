import datetime


PAYMENT_DATA = {
    "organization_name": 'ГО "МУЗЕЙ КОЛИСКОВОЇ"',
    "info": "Безповоротна фінансова допомога від прізвище, ім'я, по-батькові.",
    "iban": "UA353052990000026006035028980",
    "coffee_url": "https://www.buymeacoffee.com/kolyskova",
    "patreon_url": "https://www.patreon.com/KolyskovaMuseum",
    "qr_code_url": "static/payment/Qr.jpg",
}

FAKE_TEAM = [
    {
        "full_name": "Елеонора Хачатрян",
        "photo": "static/our_team/team1.png",
        "description": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa",
    },
    {
        "full_name": "Олег Коробов",
        "photo": "static/our_team/team2.png",
        "description": "Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu",
    },
    {
        "full_name": "Маргарита Скаженик",
        "photo": "static/our_team/team3.png",
        "description": "Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus",
    },
]
FAKE_FOOTER = {
    "reporting": "static/blank.pdf",
    "privacy_policy": "static/blank.pdf",
    "rules_and_terms": "static/blank.pdf",
    "email": "email@example.com",
    "facebook_url": "https://www.facebook.com/groups/1000Songs/",
    "youtube_url": "https://www.youtube.com/@Olegmaestro",
}
FAKE_ABOUT = {
    "content": """<p>Ласкаво просимо на сайт "1000 і 1 пісня" - унікальну онлайн платформу, присвячену збереженню та просуванню найкращих зразків української народної музики.<p class="quill-slider"><img src="http://localhost:8000/static/about/c2d7b6a9d0784f74b68fdbbf4963848a.jpeg"><img src="http://localhost:8000/static/about/885e9fcbb8b34cd3aa533aead8cc12a9.jpeg"><img src="http://localhost:8000/static/about/8af95a5c6b204223bc3ece07214f6fae.jpeg"></p> Наша історія починається з глибокого зацікавлення та поваги до багатої спадщини українського народу, яку ми намагаємося зберегти та подарувати майбутнім поколінням."1000 і 1 пісня" - це проект, заснований ентузіастами музики, які не лише прагнуть зберегти традиційні мелодії, але й дарувати їм нове життя через сучасні технології. Наша команда складається з талановитих музикантів, аранжувальників, звукорежисерів та етнографів, які мають спільну мету - зберегти та популяризувати українське музичне надбання.</p><p>Одним із ключових аспектів нашої діяльності є експедиції, які ми влаштовуємо по різних куточках України. Наш власник разом із командою вирушає у захоплюючі подорожі, де кожне село, кожна область є своєрідним музичним скарбницею. Ми прагнемо не лише записати ці пісні, але й збагатити їх новими аранжуваннями та інтерпретаціями, додаючи сучасний шар до традицій.</p><iframe class="ql-video" frameborder="0" allowfullscreen="true" src="https://www.youtube.com/embed/EDU2xd_bRvM?showinfo=0"></iframe><p><br></p><p>Кожна експедиція - це відкриття нових облич та зустріч з неповторною атмосферою кожного регіону. Ми вивчаємо та розуміємо місцеві особливості та унікальні ритми, що відзначають українську народну музику. Записуючи на багато доріжок, ми намагаємося передати всю глибину та розмаїття цього надзвичайного музичного спадку.</p><p>На нашому сайті ви зможете не лише послухати наші унікальні записи, але й дізнатися більше про історію кожної пісні, про те, як вона знаходиться у відділеній від часу світлині сучасності. Ми також регулярно ділимося інформацією про наші найновіші експедиції, події та проекти.</p><p>"1000 і 1 пісня" - це не просто колекція музики, це спроба зберегти душу та суть українського народу через його найбільш автентичний вираз - музику. Приєднуйтеся до нас у цьому захоплюючому подорожі через звуки та ритми України, допомагайте нам зберегти цей неповторний музичний спадок для майбутніх поколінь. "1000 і 1 пісня" - це ваш шлях до української музичної спадщини!</p>""",
    "title": "Про нас",
}
FAKE_COUNTRIES = [
    {"name": "Україна"},  # 1
    {"name": "Білорусь"},
    {"name": "Польща"},  # 3
    {"name": "Литва"},
    {"name": "Румунія"},  # 5
    {"name": "Молдова"},
    {"name": "Угорщина"},  # 7
    {"name": "Словаччина"},
    {"name": "Росія"},
]
FAKE_REGIONS = [
    {"country_id": 1, "name": "Київська область"},  # 1
    {"country_id": 1, "name": "Вінницька область"},
    {"country_id": 1, "name": "Волинська область"},  # 3
    {"country_id": 1, "name": "Дніпропетровська область"},
    {"country_id": 1, "name": "Донецька область"},  # 5
    {"country_id": 1, "name": "Житомирська область"},
    {"country_id": 1, "name": "Закарпатська область"},
    {"country_id": 1, "name": "Запорізька область"},  # 8
    {"country_id": 1, "name": "Івано-Франківська область"},
    {"country_id": 1, "name": "Кіровоградська область"},  # 10
    {"country_id": 1, "name": "Автономна республіка Крим"},
    {"country_id": 1, "name": "Луганська область"},
    {"country_id": 1, "name": "Львівська область"},  # 13
    {"country_id": 1, "name": "Миколаївська область"},
    {"country_id": 1, "name": "Одеська область"},  # 15
    {"country_id": 1, "name": "Полтавська область"},
    {"country_id": 1, "name": "Рівненська область"},
    {"country_id": 1, "name": "Сумська область"},  # 18
    {"country_id": 1, "name": "Тернопільська область"},
    {"country_id": 1, "name": "Харківська область"},  # 20
    {"country_id": 1, "name": "Херсонська область"},
    {"country_id": 1, "name": "Хмельницька область"},
    {"country_id": 1, "name": "Черкаська область"},  # 23
    {"country_id": 1, "name": "Чернівецька область"},
    {"country_id": 1, "name": "Чернігівська область"},  # 25
    {"country_id": 2, "name": "Берестейська область"},
    {"country_id": 2, "name": "Вітебська область"},
    {"country_id": 2, "name": "Гомельська область"},  # 28
    {"country_id": 2, "name": "Гродненська область"},
    {"country_id": 2, "name": "Могильовська область"},
    {"country_id": 2, "name": "Мінська область"},  # 31
    {"country_id": 3, "name": "Вармінсько-Мазурське воєводство"},
    {"country_id": 3, "name": "Великопольське воєводство"},
    {"country_id": 3, "name": "Західнопоморське воєводство"},  # 34
    {"country_id": 3, "name": "Куявсько-Поморське"},
    {"country_id": 3, "name": "Лодзинське воєводство"},
    {"country_id": 3, "name": "Люблінське воєводство"},  # 37
    {"country_id": 3, "name": "Любуське воєводство"},
    {"country_id": 3, "name": "Мазовецьке воєводство"},
    {"country_id": 3, "name": "Малопольське воєводство"},  # 40
    {"country_id": 3, "name": "Нижньосілезьке воєводство"},
    {"country_id": 3, "name": "Опольське воєводство"},
    {"country_id": 3, "name": "Підкарпатське воєводство"},  # 43
    {"country_id": 3, "name": "Підляське воєводство"},
    {"country_id": 3, "name": "Поморське воєводство"},
    {"country_id": 3, "name": "Свентокшиське воєводство"},  # 46
    {"country_id": 3, "name": "Сілезьке воєводство"},
    {"country_id": 9, "name": "Бєлгородська область"},
    {"country_id": 9, "name": "Брянська область"},  # 49
    {"country_id": 9, "name": "Волгоградська область"},
    {"country_id": 9, "name": "Воронезька область"},
    {"country_id": 9, "name": "Краснодарський край"},  # 52
    {"country_id": 9, "name": "Курська область"},
    {"country_id": 9, "name": "Ростовська область"},  # 54
    {"country_id": 9, "name": "Смоленська область"},
    {"country_id": 9, "name": "Псковська область"},  # 56
]
FAKE_CITY = [
    {
        "name": "Великий Черемель",
        "latitude": 51.53694777241224,
        "longitude": 26.98664264,
        "region_id": 17,
        "country_id": 1,
    },
    {
        "name": "Панасівка",
        "latitude": 49.16807786013173,
        "longitude": 33.91580207,
        "region_id": 16,
        "country_id": 1,
    },
    {
        "name": "Переяслав",
        "latitude": 50.07109815809383,
        "longitude": 31.45105560,
        "region_id": 1,
        "country_id": 1,
    },
    {
        "name": "Сарни",
        "latitude": 51.34585789550963,
        "longitude": 26.60190844,
        "region_id": 17,
        "country_id": 1,
    },
    {
        "name": "Вичівка",
        "latitude": 51.83827317596349,
        "longitude": 26.30865234,
        "region_id": 17,
        "country_id": 1,
    },
    {
        "name": "Долинівка",
        "latitude": 48.381064103932225,
        "longitude": 29.9164294,
        "region_id": 10,
        "country_id": 1,
    },
    {
        "name": "Крячківка",
        "latitude": 50.29955930078993,
        "longitude": 32.30602915,
        "region_id": 16,
        "country_id": 1,
    },
    {
        "name": "Любиковичі",
        "latitude": 51.481537294750396,
        "longitude": 26.6095407,
        "region_id": 17,
        "country_id": 1,
    },
    {
        "name": "Ромни",
        "latitude": 50.74164143409568,
        "longitude": 33.48055516,
        "region_id": 18,
        "country_id": 1,
    },
    {
        "name": "Переброди",
        "latitude": 51.72492134125541,
        "longitude": 26.97966876,
        "region_id": 17,
        "country_id": 1,
    },
    {
        "name": "Козелець",
        "latitude": 50.91333432540429,
        "longitude": 31.11684116,
        "region_id": 25,
        "country_id": 1,
    },
    {
        "name": "Полтава",
        "latitude": 49.587524602380334,
        "longitude": 34.5541248,
        "region_id": 16,
        "country_id": 1,
    },
    {
        "name": "Линове",
        "latitude": 51.32633933569399,
        "longitude": 34.06247588,
        "region_id": 18,
        "country_id": 1,
    },
    {
        "name": "Добровода",
        "latitude": 52.56384037520784,
        "longitude": 23.38293413,
        "region_id": 44,
        "country_id": 3,
    },
    {
        "name": "Спасове",
        "latitude": 48.41031888811295,
        "longitude": 33.03531325,
        "region_id": 10,
        "country_id": 1,
    },
    {
        "name": "Київ",
        "latitude": 50.45367180843008,
        "longitude": 30.51655420,
        "region_id": 1,
        "country_id": 1,
    },
    {
        "name": "Веприк",
        "latitude": 50.36940915453742,
        "longitude": 34.17579265,
        "region_id": 16,
        "country_id": 1,
    },
    {
        "name": "Даше",
        "latitude": 52.554953177126336,
        "longitude": 23.2481166,
        "region_id": 44,
        "country_id": 3,
    },
    {
        "name": "Барахти",
        "latitude": 50.10893144419943,
        "longitude": 30.370125003105485,
        "region_id": 1,
        "country_id": 1,
    },
    {
        "name": "Городище",
        "latitude": 51.799417777248394,
        "longitude": 26.7003323,
        "region_id": 17,
        "country_id": 1,
    },
    {
        "name": "Панасівка",
        "latitude": 50.09495499592963,
        "longitude": 33.98891103,
        "region_id": 16,
        "country_id": 1,
    },
    {
        "name": "Манухівка",
        "latitude": 51.25117899466428,
        "longitude": 34.16242288,
        "region_id": 18,
        "country_id": 1,
    },
    {
        "name": "Бігунь",
        "latitude": 51.40056806374007,
        "longitude": 28.27653221,
        "region_id": 6,
        "country_id": 1,
    },
    {
        "name": "Демидів",
        "latitude": 50.72830636033024,
        "longitude": 30.33105204,
        "region_id": 1,
        "country_id": 1,
    },
    {
        "name": "Прикладники",
        "latitude": 51.915347391109044,
        "longitude": 25.8474856,
        "region_id": 17,
        "country_id": 1,
    },
    {
        "name": "Ромейки",
        "latitude": 51.257855862008924,
        "longitude": 26.2162949,
        "region_id": 17,
        "country_id": 1,
    },
    {
        "name": "Лука",
        "latitude": 50.462630728049405,
        "longitude": 33.2887714,
        "region_id": 16,
        "country_id": 1,
    },
    {
        "name": "Хитці",
        "latitude": 50.19614898477121,
        "longitude": 33.291936457207356,
        "region_id": 16,
        "country_id": 1,
    },
    {
        "name": "Кролевець",
        "latitude": 51.54941216987737,
        "longitude": 33.38774983,
        "region_id": 18,
        "country_id": 1,
    },
    {
        "name": "Оксанина",
        "latitude": 48.68753868015108,
        "longitude": 30.54379355,
        "region_id": 23,
        "country_id": 1,
    },
    {
        "name": "Карильське",
        "latitude": 51.50801861411226,
        "longitude": 33.00563454,
        "region_id": 25,
        "country_id": 1,
    },
    {
        "name": "Хмелівка",
        "latitude": 51.26124389099922,
        "longitude": 27.69049449469027,
        "region_id": 6,
        "country_id": 1,
    },
    {
        "name": "Ясенове",
        "latitude": 50.30918976577461,
        "longitude": 34.72381832,
        "region_id": 18,
        "country_id": 1,
    },
    {
        "name": "Умань",
        "latitude": 48.74755118869285,
        "longitude": 30.22328526,
        "region_id": 23,
        "country_id": 1,
    },
    {
        "name": "Велика Писарівка",
        "latitude": 50.42039664538097,
        "longitude": 35.48127851,
        "region_id": 18,
        "country_id": 1,
    },
    {
        "name": "Оране",
        "latitude": 51.05164269031264,
        "longitude": 30.12337693,
        "region_id": 1,
        "country_id": 1,
    },
    {
        "name": "Веселий Поділ",
        "latitude": 49.5948860381969,
        "longitude": 33.259659505,
        "region_id": 16,
        "country_id": 1,
    },
    {
        "name": "Поворськ",
        "latitude": 51.264868970215396,
        "longitude": 25.1289613,
        "region_id": 3,
        "country_id": 1,
    },
    {
        "name": "Бутове",
        "latitude": 51.797441906113576,
        "longitude": 26.3776508,
        "region_id": 17,
        "country_id": 1,
    },
    {
        "name": "Ветли",
        "latitude": 51.88174710873601,
        "longitude": 25.10697595,
        "region_id": 3,
        "country_id": 1,
    },
]
FAKE_GENRE = [
    {"genre_name": "Зима"},
    {"genre_name": "Колодій"},
    {"genre_name": "Масляна"},
    {"genre_name": "Ранцювання"},
    {"genre_name": "Весна"},
    {"genre_name": "Зелена неділя(Трійця)"},
    {"genre_name": "Купало"},
    {"genre_name": "Жнива"},
    {"genre_name": "Косовиця"},
    {"genre_name": "Осінь"},
    {"genre_name": "Оказія"},
    {"genre_name": "Весілля"},
    {"genre_name": "Колискові"},
    {"genre_name": "Родини/Хрестини"},
    {"genre_name": "Родини: Застілля"},
    {"genre_name": "Похорон"},
    {"genre_name": "Лірика"},
]
FAKE_SONG = [
    {
        "title": "Як вийду на гору - Copy",
        "song_text": "Як вийду на гору та й крикну й додому: - Та вари. мати, ой вечеряти, бо я йду й додому. - Та наварила, доню, небагацько - трошки. Та нема й тобі, ой доню моя, ні миски й ні ложки.",
        "song_descriotion": "",
        "recording_date": datetime.date(2011, 8, 21),
        "performers": "Співачки з села Хитці",
        "ethnographic_district": "Полтавщина",
        "collectors": "Маргарита Скаженик, Олег Коробов",
        "source": "Приватний архів Маргарити Скаженик та Олега Коробова",
        "archive": "Приватний архів Маргарити Скаженик та Олега Коробова",
        "recording_location": "",
        "bibliographic_reference": "",
        "comment_map": "",
        "video_url": "",
        "stereo_audio": "static/song/example.mp3",
        "multichannel_audio1": "static/song/example.mp3",
        "multichannel_audio2": "static/song/example.mp3",
        "multichannel_audio3": "static/song/example.mp3",
        "multichannel_audio4": "static/song/example.mp3",
        "multichannel_audio5": "static/song/example.mp3",
        "multichannel_audio6": "static/song/example.mp3",
        "city_id": 29,
    },
    {
        "title": "Ой якби ж я до Київа доріженьку знала",
        "song_text": "Ой якби ж я до Київа доріженьку знала, Я б своєму миленькому гостинця послала. Ниякого гостинчика – чотири горішки. Як немає чим приїхать, прийди, милий, пішки. І сам іде, коня веде до дівчини в гості. Провалився кінь вороний на кам’яним мості. Провалився й утопився ще й шапочка сплила. Молодая дівчинонька бистру річку брєла. Брєла річку, брєла другу понад берегами. Набачила рибаловця ж з чорними бровами. Риболовці славні хлопці вольніть мою волю – Закидайте тонкий невід по синьому морю. Тягнуть його ж до бережечка – з рота вода ллється. Молодая дівчинонька як орлиця б’ється. Ломить вона виломляє мазиного пальця – Ой нема вже миленького такого красавця.",
        "song_descriotion": "",
        "recording_date": datetime.date(2011, 5, 9),
        "performers": "Анастасія Мартиненко, 1931 р.н.; Надія Погребиська, 1941 р.н.; Лідія Хачева, 1964 р.н.; Валентина Вангородська, 1940 р.н.",
        "ethnographic_district": "Середня Надніпрянщина",
        "collectors": "Клименко Ірина, Олег Коробов, Ірина Данилейко, Мар'яна Мархель",
        "source": "Aрхів",
        "archive": "Проблемна науково дослідна лабораторія етномузикології НМАУ",
        "recording_location": "Барахти",
        "bibliographic_reference": "",
        "comment_map": "",
        "video_url": "https://youtu.be/Zq5MxYrZO-E",
        "city_id": 20,
    },
    {
        "title": "Ой ти Галино",
        "song_text": "Зозуленька рябенькая Й усі луги облітала. А в одному не бувала. А в тім лузі теслі тешуть, Церкву ставляють з трьома йуглами, З трьома йокнами. В першім йокенці - ясне сонечко, В другім йокенці - ясен місяцю, В третім йокенці - ясні зірочки. Щедрий вечор, добрий вечор, Добрим людям на весь вечор! Примовки: Щедрівочка щедрувала, до віконця припадала, Що ти, тітко, наварила, що ти, тітко, напекла, принеси нам до вікна Не щипай, не ламай, а ціленького давай!",
        "song_descriotion": "",
        "recording_date": datetime.date(2022, 1, 1),
        "performers": "Фольклорний ансамбль «Гуртоправці»",
        "ethnographic_district": "Середнє Полісся",
        "collectors": "Клименко Ірина",
        "source": 'Клименко, І. (2003). Ой давно, давно… Київ: "САМЕ ТАК!".',
        "archive": "ЛЕК",
        "recording_location": "Київ",
        "bibliographic_reference": "",
        "comment_map": "",
        "video_url": "",
        "city_id": 33,
    },
    {
        "title": "Проведу я русалочки",
        "song_text": "",
        "song_descriotion": "",
        "recording_date": datetime.date(2022, 1, 1),
        "performers": "Фольклорний ансамбль «Володар»",
        "ethnographic_district": "",
        "collectors": "Клименко Ірина",
        "source": 'Клименко, І. (2003). Ой давно, давно… Київ: "САМЕ ТАК!".',
        "archive": "ЛЕК",
        "recording_location": "",
        "bibliographic_reference": "",
        "comment_map": "",
        "video_url": "",
        "city_id": 36,
    },
    {
        "title": "Косив козак сіно",
        "song_text": "",
        "song_descriotion": "",
        "recording_date": datetime.date(2022, 1, 1),
        "performers": "Фольклорний ансамбль «Гуртоправці»",
        "ethnographic_district": "Середнє Полісся",
        "collectors": "Клименко Ірина",
        "source": 'Клименко, І. (2003). Ой давно, давно… Київ: "САМЕ ТАК!".',
        "archive": "ЛЕК",
        "recording_location": "",
        "bibliographic_reference": "",
        "comment_map": "",
        "video_url": "",
        "city_id": 8,
    },
    {
        "title": "Щедрик-ведрик, дайте",
        "song_text": "Щедрик-ведрик. Дайте вареник, Грудочку кашки, кольце ковбаски! А ще мало – дайте сала! А ще донесу – наверх ковбасу! А ще кишку – з’їм у затишку! Вигукують: Виносьте дохід добрий, Не ламайте та цілим давайте! Хоть коротенький, зате ситенький!",
        "song_descriotion": "Щедрівка дитячого репертуару Фрагмент етнографічного документального фільму Єлєни Самойлової 'Святі вечори на Полтавщині'. Зйомки 13-14 січня 2009 року в селі Крячківка Пирятинського району Полтавської області. Джерело: навчальна відеотека ПНДЛ етномузикології НМАУ",
        "recording_date": datetime.date(2011, 5, 9),
        "performers": "Жителі села Крячківка",
        "ethnographic_district": "Середня Наддніпрянщина",
        "collectors": "Єлена Самойлова",
        "source": "",
        "archive": "",
        "recording_location": "Крячківка",
        "bibliographic_reference": "",
        "comment_map": "Щедрівки дитячого репертуару",
        "video_url": "https://youtu.be/U01Pzqe9k_o",
        "city_id": 7,
    },
    {
        "title": "А я знаю, що пан робіть",
        "song_text": "Щедрий вечор, добрий вечор. А я знаю, що пан робіть: Сидить собі в конці стола, А на йому шуба-люба, А в той шубі калиточка. В тей калитці сєм жучков, сєм жучков, Сєм гранічок, сєм тялічок. Дайте, дядьку, сєм палянічок!",
        "song_descriotion": "Щедрівка господареві дитячого репертуару. Джерело: Щедрий вечор, добрий вечор. А я знаю, що пан робіть. «Рано-рано да зійду на гору». Серія «Традиційна музика Полісся». – Ч. 2: Весілля, зима. Київ: Культурологічна експедиція МНС України +УЕЛФ, 1997. – 1 CD audio (59’42’’, 36 творів) + Букл.: анотація; Іл. – Б. і. – (Серія випущена для поширення в бібліотеках гуманітарних вузів. Не для продажу). [Фонотека ПНДЛ етномузикології НМАУ].",
        "recording_date": datetime.date(2011, 5, 9),
        "performers": "Фольклорний гурт села Сарновичі",
        "ethnographic_district": "Середнє Полісся",
        "collectors": "Єфремов Євген, Ірина Клименко, Маргарита Скаженик, Микола Семиног",
        "source": "",
        "archive": "",
        "recording_location": "Сарновичі",
        "bibliographic_reference": "",
        "comment_map": "Поширення щедрівок з таким ритмічним типом показано на карті (див. легенду до карти)",
        "video_url": "",
    },
    {
        "title": "Зозуленька рябенькая",
        "song_text": "Зозуленька рябенькая Усі луги облітала, Й а в одному не бувала. Й а в тім лузі теслі тешуть Церкву ставляють З трьома углами, з трьома окнами. В першім й окенці – ясне сонечко, В другім й окенці – ясен місяцю, В третім й окенці – ясні зіроньки. Щодрий вечор, добрий вечор, Добрим людям на весь вечор. Примовки: Щедрівочка щедрувала, до віконця припадала, Що ти, тітко, наварила, що ти, тітко, напекла, принеси нам до вікна. Не щипай, не ламай, а ціленького давай!",
        "song_descriotion": "Дитяча щедрівка з примовками. Поширення колядок і щедрівок з таким ритмом див. на карті далі",
        "recording_date": datetime.date(2015, 1, 1),
        "performers": "Виконавська реконструкція. Співає дитяча група фольклорного гурту Володар, м. Київ (кер. І. Клименко). СD Зберімося роде... Ч. 1. «Володар, одчиняй ворота!». Київ, 2003",
        "ethnographic_district": "Західне Полісся (Пінщина)",
        "collectors": "Ірина Клименко",
        "source": "",
        "archive": "",
        "recording_location": "Дубчиці",
        "bibliographic_reference": "",
        "comment_map": "Поширення колядок і щедрівок такого ритмічного типу показано на карті заливкою пурпурного кольору (див. також легенду до карти)",
        "video_url": "",
    },
    {
        "title": "Щедрик-ведрик, дайте-2",
        "song_text": "Щедрик-ведрик. Дайте вареник, Грудочку кашки, кольце ковбаски! А ще мало – дайте сала! А ще донесу – наверх ковбасу! А ще кишку – з’їм у затишку! Вигукують: Виносьте дохід добрий, Не ламайте та цілим давайте! Хоть коротенький, зате ситенький!",
        "song_descriotion": "Щедрівка дитячого репертуару Фрагмент етнографічного документального фільму Єлєни Самойлової 'Святі вечори на Полтавщині'. Зйомки 13-14 січня 2009 року в селі Крячківка Пирятинського району Полтавської області. Джерело: навчальна відеотека ПНДЛ етномузикології НМАУ",
        "recording_date": datetime.date(2011, 5, 9),
        "performers": "Жителі села Крячківка",
        "ethnographic_district": "Середня Наддніпрянщина",
        "collectors": "Єлена Самойлова",
        "source": "",
        "archive": "",
        "recording_location": "Крячківка",
        "bibliographic_reference": "",
        "comment_map": "Щедрівки дитячого репертуару",
        "video_url": "https://youtu.be/U01Pzqe9k_o",
        "city_id": 7,
    },
]
LOREM = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vehicula libero nec justo convallis, nec sodales nunc pellentesque. Sed auctor efficitur sem id vestibulum. Mauris fringilla ullamcorper mauris eget pellentesque. Fusce ullamcorper elit vitae sapien tincidunt, vel molestie lacus tristique. Aliquam in ex ac risus auctor condimentum. Integer hendrerit tincidunt diam eget tempor. Integer sit amet condimentum dolor. Nullam viverra urna sit amet justo sagittis, non vehicula metus consectetur."""
FAKE_DESC_FOR_ES_SONG = """Ритуальні зимові обходи дворів зі спеціальними піснями тривають від Різдва до Водохреща. Мета обходів – побажати господарям добробуту і здоров’я на весь майбутній рік. За давніми (дохристиянськими) уявленнями учасники обходів виконують волю предків – опікунів роду. У більшості традицій на Різдво колядують (колядування могло тривати до Водохреща), ставлять Вертеп; напередодні Нового Року – щедрують (в зоні Карпат, в Галичині щедрування відсутні), водять Козу, Меланку, Коня тощо. На Новий рік посівають. Діти і молодь (хлопці, дівчата) колядують/щедрують попід хатою (під вікном або під дверима), зрідка могли заходити в сіни. Дорослих (одружених чоловіків і жінок), співаків церковної півчої – які співали колядки переважно християнської тематики – запрошують до хати. Ряджену «Козу» заводять до хати. Раніше господарі обдаровували колядників/щедрівників наїдками (ритуальне годування задобрення духів предків): пампушками, млинцями, коржиками, горіхами, насінням; пізніше – солодощами; у наш час – грошима."""
ES_MAIN_SONG_CATEGORY = [
    {
        "title": "Пісні зимового циклу",
        "description": FAKE_DESC_FOR_ES_SONG,
        "recommended_sources": LOREM,
    },
    {
        "title": "Пісні весняного циклу",
        "description": FAKE_DESC_FOR_ES_SONG,
        "recommended_sources": LOREM,
    },
    {
        "title": "Пісні літнього циклу",
        "description": FAKE_DESC_FOR_ES_SONG,
        "recommended_sources": LOREM,
    },
    {
        "title": "Весільні пісні",
        "description": FAKE_DESC_FOR_ES_SONG,
        "recommended_sources": LOREM,
    },
    {
        "title": "Родини і хрестини. Материнський і дитячий фольклор",
        "description": FAKE_DESC_FOR_ES_SONG,
        "recommended_sources": LOREM,
    },
    {
        "title": "Звичайні пісні",
        "description": FAKE_DESC_FOR_ES_SONG,
        "recommended_sources": LOREM,
    },
    {
        "title": "Музичний епос",
        "description": FAKE_DESC_FOR_ES_SONG,
        "recommended_sources": LOREM,
    },
    {
        "title": "Інструментальна музика. Народні танці",
        "description": FAKE_DESC_FOR_ES_SONG,
        "recommended_sources": LOREM,
    },
    {
        "title": "Традиційний похорон: музичне оформлення",
        "description": FAKE_DESC_FOR_ES_SONG,
        "recommended_sources": LOREM,
    },
]
FAKE_SUB_CATEGORY = [
    {
        "title": "Ранньотрадиційний репертуар",
        "main_category_id": 1,
    },
    {
        "title": "Колядки пізнього походження (християнські)",
        "main_category_id": 1,
    },
    {
        "title": "Рання весна. Перехід зима/весна",
        "main_category_id": 2,
    },
    {
        "title": "Період весняного рівнодення. Великдень",
        "main_category_id": 2,
    },
    {
        "title": "Зелені свята",
        "main_category_id": 2,
    },
    {
        "title": "Приурочені ліричні пісні ранньої стилістики",
        "main_category_id": 3,
    },
    {
        "title": "Купальсько-петрівські пісні",
        "main_category_id": 3,
    },
    {
        "title": "Жнивні пісні",
        "main_category_id": 3,
    },
    {
        "title": "Передвесільні обряди і пісні",
        "main_category_id": 4,
    },
    {
        "title": "Весілля. Недільні обряди і пісні",
        "main_category_id": 4,
    },
    {
        "title": "Післявесільні звичаї і пісні",
        "main_category_id": 4,
    },
    {
        "title": "Музичне оформлення народин і хрестин",
        "main_category_id": 5,
    },
    {
        "title": "Музичні жанри «материнського фольклору»",
        "main_category_id": 5,
    },
    {
        "title": "Пісні дитячого репертуару",
        "main_category_id": 5,
    },
    {
        "title": "Ліричні пісні (за музичними ознаками)",
        "main_category_id": 6,
    },
    {
        "title": "Ліричні пісні (за тематикою)",
        "main_category_id": 6,
    },
    {
        "title": "Коломийки",
        "main_category_id": 6,
    },
    {
        "title": "Приспівки",
        "main_category_id": 6,
    },
    {
        "title": "Пісенна творчість пізнішого часу",
        "main_category_id": 6,
    },
    {
        "title": "Билини",
        "main_category_id": 7,
    },
    {
        "title": "Думи",
        "main_category_id": 7,
    },
    {
        "title": "Традиційний лірницький репертуар",
        "main_category_id": 7,
    },
    {
        "title": "Українські традиційні музичні інструменти",
        "main_category_id": 8,
    },
    {
        "title": "Інструментальні капели. «Троїста музика»",
        "main_category_id": 8,
    },
    {
        "title": "Танцювальна музична культура українців",
        "main_category_id": 8,
    },
    {
        "title": "Голосіння",
        "main_category_id": 9,
    },
    {
        "title": "Поминальні псальми",
        "main_category_id": 9,
    },
]
FAKE_GENRE_ES = [
    {
        "main_category_id": 1,
        "sub_category_id": 1,
        "title": "Дитячі колядки та щедрівки",
        "description": LOREM,
    },
    {
        "main_category_id": 1,
        "sub_category_id": 1,
        "title": "Величальні колядки та щедрівки",
        "description": LOREM,
    },
    {
        "main_category_id": 1,
        "sub_category_id": 1,
        "title": "Пісні до новорічних карнавальних процесів",
        "description": LOREM,
    },
    {
        "main_category_id": 1,
        "sub_category_id": 1,
        "title": "Засівання",
        "description": LOREM,
    },
    {
        "main_category_id": 1,
        "sub_category_id": 2,
        "title": "Різдвяні канти",
        "description": LOREM,
    },
    {
        "main_category_id": 1,
        "sub_category_id": 2,
        "title": "Різдвяні псальми",
        "description": LOREM,
    },
    {
        "main_category_id": 1,
        "sub_category_id": 2,
        "title": "Пародійні колядки",
        "description": LOREM,
    },
    {
        "main_category_id": 1,
        "sub_category_id": 2,
        "title": "Вертеп",
        "description": LOREM,
    },
    {
        "main_category_id": 2,
        "sub_category_id": 3,
        "title": "Проводи Зими",
        "description": LOREM,
    },
    {
        "main_category_id": 2,
        "sub_category_id": 3,
        "title": "Колодка",
        "description": LOREM,
    },
    {
        "main_category_id": 2,
        "sub_category_id": 3,
        "title": "Масляні пісні",
        "description": LOREM,
    },
    {
        "main_category_id": 2,
        "sub_category_id": 3,
        "title": "Зустріч весни",
        "description": LOREM,
    },
    {
        "main_category_id": 2,
        "sub_category_id": 3,
        "title": "Креснянка",
        "description": LOREM,
    },
    {
        "main_category_id": 2,
        "sub_category_id": 3,
        "title": "Каша",
        "description": LOREM,
    },
    {
        "main_category_id": 2,
        "sub_category_id": 4,
        "title": "Великодні ранцівки",
        "description": LOREM,
    },
    {
        "main_category_id": 2,
        "sub_category_id": 4,
        "title": "Весняні танки та ігри",
        "description": LOREM,
    },
    {
        "main_category_id": 2,
        "sub_category_id": 5,
        "title": "Похорон Стріли",
        "description": LOREM,
    },
    {
        "main_category_id": 2,
        "sub_category_id": 5,
        "title": "Водіння Куста",
        "description": LOREM,
    },
    {
        "main_category_id": 2,
        "sub_category_id": 5,
        "title": "Русальні пісні",
        "description": LOREM,
    },
    {
        "main_category_id": 3,
        "sub_category_id": 7,
        "title": "Купальсько-петрівські пісні",
        "description": LOREM,
    },
    {
        "main_category_id": 3,
        "sub_category_id": 8,
        "title": "Жнивні пісні",
        "description": LOREM,
    },
    {
        "main_category_id": 3,
        "sub_category_id": 6,
        "title": "Ягідні",
        "description": LOREM,
    },
    {
        "main_category_id": 3,
        "sub_category_id": 6,
        "title": "Спасовки",
        "description": LOREM,
    },
    {
        "main_category_id": 3,
        "sub_category_id": 6,
        "title": "Строкові",
        "description": LOREM,
    },
    {
        "main_category_id": 3,
        "sub_category_id": 6,
        "title": "Косарські",
        "description": LOREM,
    },
    {
        "main_category_id": 3,
        "sub_category_id": 6,
        "title": "Літо",
        "description": LOREM,
    },
    {
        "main_category_id": 3,
        "sub_category_id": 6,
        "title": "До полоття",
        "description": LOREM,
        "description": LOREM,
    },
    {
        "main_category_id": 4,
        "sub_category_id": 9,
        "title": "Передвесільні обряди і пісні",
        "description": LOREM,
    },
    {
        "main_category_id": 4,
        "sub_category_id": 10,
        "title": "Весілля. Недільні обряди і пісні",
        "description": LOREM,
    },
    {
        "main_category_id": 4,
        "sub_category_id": 11,
        "title": "Післявесільні звичаї і пісні",
        "description": LOREM,
    },
    {
        "main_category_id": 5,
        "sub_category_id": 12,
        "title": "Народини та хрестини",
        "description": LOREM,
    },
    {
        "main_category_id": 5,
        "sub_category_id": 13,
        "title": "Колискові пісні",
        "description": LOREM,
    },
    {
        "main_category_id": 5,
        "sub_category_id": 13,
        "title": "Забавлянки",
        "description": LOREM,
    },
    {
        "main_category_id": 5,
        "sub_category_id": 13,
        "title": "Казки зі співом",
        "description": LOREM,
    },
    {
        "main_category_id": 5,
        "sub_category_id": 14,
        "title": "Колядки, щедрівки",
        "description": LOREM,
    },
    {
        "main_category_id": 5,
        "sub_category_id": 14,
        "title": "Веснянки",
        "description": LOREM,
    },
    {
        "main_category_id": 5,
        "sub_category_id": 14,
        "title": "Оказіональні приспівки до дощу, сонця, птахів",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 15,
        "title": "Ранні ліричні пісні ",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 15,
        "title": "Багатоголосні пісні з сольним виводом",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 16,
        "title": "Про кохання",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 16,
        "title": "Про родинні відносини",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 16,
        "title": "Балади",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 16,
        "title": "Чумацькі пісні",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 16,
        "title": "Бурлацькі пісні",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 16,
        "title": "Наймитські пісні",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 16,
        "title": "Козацькі пісні, історичні пісні",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 16,
        "title": "Рекрутські пісні, солдатські пісні, жовнірські пісні",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 16,
        "title": "Жартівливі пісні",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 17,
        "title": "Коломийки",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 18,
        "title": "Приспівки до танців",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 19,
        "title": "Народні романси. Жорстокі романси",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 19,
        "title": "Стрілецькі та повстанські пісні",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 19,
        "title": "Псальми",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 19,
        "title": "Кічі",
        "description": LOREM,
    },
    {
        "main_category_id": 6,
        "sub_category_id": 19,
        "title": "Частушки",
        "description": LOREM,
    },
    {
        "main_category_id": 7,
        "sub_category_id": 20,
        "title": "Билини київського циклу",
        "description": LOREM,
    },
    {
        "main_category_id": 7,
        "sub_category_id": 21,
        "title": "Кобзарство. Думи",
        "description": LOREM,
    },
    {
        "main_category_id": 7,
        "sub_category_id": 22,
        "title": "Лірництво. Псальми і канти",
        "description": LOREM,
    },
    {
        "main_category_id": 8,
        "sub_category_id": 23,
        "title": "Самозвучні",
        "description": LOREM,
    },
    {
        "main_category_id": 8,
        "sub_category_id": 23,
        "title": "Духові",
        "description": LOREM,
    },
    {
        "main_category_id": 8,
        "sub_category_id": 23,
        "title": "Струнні",
        "description": LOREM,
    },
    {
        "main_category_id": 8,
        "sub_category_id": 23,
        "title": "Ударні",
        "description": LOREM,
    },
    {
        "main_category_id": 8,
        "sub_category_id": 24,
        "title": "Інструментальні капели. Троїста музика",
        "description": LOREM,
    },
    {
        "main_category_id": 8,
        "sub_category_id": 25,
        "title": "Питомі танці",
        "description": LOREM,
    },
    {
        "main_category_id": 8,
        "sub_category_id": 25,
        "title": "Напливові танці",
        "description": LOREM,
    },
    {
        "main_category_id": 9,
        "sub_category_id": 26,
        "title": "Голосіння",
        "description": LOREM,
    },
    {
        "main_category_id": 9,
        "sub_category_id": 27,
        "title": "Поминальні псальми",
        "description": LOREM,
    },
]
FAKE_EDUCATION = {
    "title": "Освітній розділ",
    "description": "Пріоритети сучасних – заповнення «білих плям» на фольклористичній карті України (східна Волинь, Наддніпрянщина, південна Чернігівщина, Сумщина, Берестейщина та інші території) та спеціалізовані регіональні програми з видання пісенних збірок за матеріалами певних етнографічних локусів.",
    "recommendations": LOREM,
    "recommended_sources": LOREM,
}
