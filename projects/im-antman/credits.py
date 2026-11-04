"""Финальные титры «Я Энтмен!» (2 минуты). Все имена выдуманы.

Строки: ("title", ru, en) — крупный заголовок, ("head", ru, en) — раздел,
("row", роль ru, роль en, имя ru, имя en) — роль и имя, ("text", ru, en), ("gap",).
"""

import math

from PIL import ImageDraw

import draw as D

DURATION = 120.0

CREDITS: list[tuple[str, ...]] = [
    ("title", "Я Энтмен!", "I'm Antman!"),
    ("text", "V3 ORIGINAL представляет", "V3 ORIGINAL presents"),
    ("gap",),
    ("row", "Режиссёр", "Directed by", "Аркадий Тихомиров", "Arkady Tikhomirov"),
    ("row", "Автор сценария", "Screenplay by", "Вера Лунёва", "Vera Luneva"),
    ("row", "Продюсеры", "Producers", "Тимур Галстян", "Timur Galstyan"),
    ("row", "", "", "Ольга Бережная", "Olga Berezhnaya"),
    ("row", "Исполнительный продюсер", "Executive Producer", "Леонид Шапкин", "Leonid Shapkin"),
    ("gap",),
    ("head", "В РОЛЯХ", "CAST"),
    ("row", "Антон Мурашов / Энтмен", "Anton Murashov / Antman", "Глеб Ветров", "Gleb Vetrov"),
    ("row", "Гоша, говорящий муравей", "Gosha, the talking ant", "Савва Кузнечиков", "Savva Kuznechikov"),
    ("row", "Лена Синицына", "Lena Sinitsyna", "Алиса Журавлёва", "Alisa Zhuravleva"),
    ("row", "Мама Антона", "Anton's Mom", "Нина Пряникова", "Nina Pryanikova"),
    ("row", "Профессор Квасов", "Professor Kvasov", "Эдуард Колбин", "Eduard Kolbin"),
    ("row", "Шеф Борис", "Boss Boris", "Роман Баранкин", "Roman Barankin"),
    ("row", "Капитан Петрович", "Captain Petrovich", "Степан Дубровский", "Stepan Dubrovsky"),
    ("row", "Барон Дихлофос", "Baron Bugspray", "Аристарх Шипучий", "Aristarkh Shipuchy"),
    ("row", "Доктор Тапок", "Doctor Slipper", "Фёдор Шлёпов", "Fyodor Shlyopov"),
    ("row", "Мадам Москитка", "Madame Mosquito", "Жанна Звонарёва", "Zhanna Zvonaryova"),
    ("row", "Парикмахер", "The Barber", "Ашот Ножницян", "Ashot Nozhnitsyan"),
    ("row", "Доктор Айболит", "Doctor Feelgood", "Игорь Пилюлин", "Igor Pilyulin"),
    ("row", "Ведущий шоу «Герои»", "Hero Show Host", "Стас Блестящий", "Stas Blestyashchy"),
    ("row", "Гражданка с котом", "Lady with a Cat", "Зинаида Барсикова", "Zinaida Barsikova"),
    ("row", "Прохожий Вася", "Vasya, a Passerby", "Василий Прохоров", "Vasily Prokhorov"),
    ("row", "Кот Барсик", "Barsik the Cat", "в роли самого себя", "as himself"),
    ("row", "Армия муравьёв", "The Ant Army", "1 000 000 муравьёв", "1,000,000 ants"),
    ("gap",),
    ("head", "СЪЁМОЧНАЯ ГРУППА", "CREW"),
    ("row", "Художник-постановщик", "Production Designer", "Полина Акварелли", "Polina Akvarelli"),
    ("row", "Дизайн персонажей", "Character Design", "Лиана Усикова", "Liana Usikova"),
    ("row", "Раскадровка", "Storyboards", "Мирон Карандашов", "Miron Karandashov"),
    ("row", "Ведущий аниматор", "Lead Animator", "Денис Кадров", "Denis Kadrov"),
    ("row", "Аниматоры", "Animators", "Ульяна Шустрая", "Ulyana Shustraya"),
    ("row", "", "", "Рафаэль Мурадян", "Rafael Muradyan"),
    ("row", "", "", "Ким Сон Ми", "Kim Seon-mi"),
    ("row", "", "", "Лука Фалько", "Luca Falco"),
    ("row", "", "", "Агата Прыгунова", "Agata Prygunova"),
    ("row", "Художники фонов", "Background Artists", "Ева Горизонтова", "Eva Gorizontova"),
    ("row", "", "", "Тарас Кирпичко", "Taras Kirpichko"),
    ("row", "Монтаж", "Editor", "Глория Склейкина", "Gloria Skleykina"),
    ("row", "Цветокоррекция", "Colorist", "Аркадий Радугин", "Arkady Radugin"),
    ("row", "Кастинг", "Casting", "Эмма Выборова", "Emma Vyborova"),
    ("gap",),
    ("head", "МУЗЫКА И ЗВУК", "MUSIC AND SOUND"),
    ("row", "Композитор", "Original Music", "Марк Октавин", "Mark Oktavin"),
    ("row", "Звукорежиссёр", "Sound Designer", "Ян Громов", "Yan Gromov"),
    ("row", "Звуковые эффекты", "Sound Effects", "Филипп Хлопков", "Filipp Khlopkov"),
    ("row", "", "", "Дарья Бульк", "Darya Bulk"),
    ("row", "Звук падений", "Falling Sounds", "Мешок картошки", "A Sack of Potatoes"),
    ("gap",),
    ("head", "КОНСУЛЬТАНТЫ", "CONSULTANTS"),
    ("row", "Консультант по муравьям", "Ant Consultant", "проф. Мирмеко Логов", "Prof. Myrmeko Logov"),
    ("row", "Консультант по тапкам", "Slipper Consultant", "Тамара Тапочкина", "Tamara Tapochkina"),
    ("row", "Консультант по пицце", "Pizza Consultant", "Джузеппе Ананасов", "Giuseppe Ananasov"),
    ("row", "Каскадёр (падения)", "Stunt Falls", "Антон Падалкин", "Anton Padalkin"),
    ("row", "Дрессировщик кота", "Cat Wrangler", "Мурат Мяукин", "Murat Myaukin"),
    ("row", "Кейтеринг", "Catering", "Пицца «Мураш»", "Murash Pizza"),
    ("gap",),
    ("head", "ОСОБАЯ БЛАГОДАРНОСТЬ", "SPECIAL THANKS"),
    ("text", "Jouli · Leo Da Vinci · Omar Hayam", "Jouli · Leo Da Vinci · Omar Hayam"),
    ("text", "Zhanel · Marika · Ferracho · Halib", "Zhanel · Marika · Ferracho · Halib"),
    ("text", "Aryubi · Mika · Enrique", "Aryubi · Mika · Enrique"),
    ("text", "и всем мамам, которые напоминают про шапку", "and every mom who reminds you to wear a hat"),
    ("gap",),
    ("text", "Все персонажи и имена вымышлены.", "All characters and names are fictional."),
    ("text", "Голоса, музыка и анимация созданы с помощью ИИ.", "Voices, music and animation were made with AI."),
    ("text", "Ни один муравей не пострадал. Тапки — пострадали.", "No ants were harmed. Several slippers were."),
    ("gap",),
    ("text", "© 2026 V3 ORIGINAL", "© 2026 V3 ORIGINAL"),
    ("gap",),
    ("title", "Конец", "The End"),
]

HEIGHT = {"title": 100, "head": 80, "row": 48, "text": 48, "gap": 50}


def render(d: ImageDraw.ImageDraw, t: float, dur: float, lang: str) -> None:
    """Scroll the credits; the last line stops at screen center."""
    li = 0 if lang == "ru" else 1
    total = sum(HEIGHT[r[0]] for r in CREDITS)
    scroll_end = dur - 6.0
    k = min(1.0, t / scroll_end)
    # first line starts just below the screen, last line ends at the center
    start, end = D.H + 60, D.H / 2 - (total - HEIGHT["title"] / 2)
    y = start + (end - start) * k
    for r in CREDITS:
        h = HEIGHT[r[0]]
        cy = y + h / 2
        y += h
        if cy < -60 or cy > D.H + 60:
            continue
        kind = r[0]
        if kind == "title":
            D.text_center(d, 640, cy, r[1 + li], 72, D.GOLD, 6, (150, 20, 20))
        elif kind == "head":
            D.text_center(d, 640, cy, r[1 + li], 40, (255, 200, 120), 3)
        elif kind == "text":
            D.text_center(d, 640, cy, r[1 + li], 30, (235, 235, 235), 2)
        elif kind == "row":
            role, name = r[1 + li], r[3 + li]
            if role:
                d.text((615, cy), role, font=D.font(28), fill=(190, 190, 210), anchor="rm", stroke_width=2, stroke_fill=(0, 0, 0))
            d.text((665, cy), name, font=D.font(32), fill=(255, 255, 255), anchor="lm", stroke_width=2, stroke_fill=(0, 0, 0))
    # little mascots dancing in the corner
    import cast as C

    D.hero(d, 1150, 705, 0.5, arms=(20 + 20 * math.sin(t * 4), 150 + 20 * math.sin(t * 6)))
    C.ant(d, 1225, 705, 0.6, wave=1.0)
