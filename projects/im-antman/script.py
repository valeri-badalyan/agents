"""Сценарий короткометражки «I'm Antman! (Я Энтмен!)» — комедия 12+.

Каждая сцена: фон/тип анимации, музыка и реплики.
Реплика: (говорящий, текст RU, текст EN, опции).
Опции: sfx — звук в начале реплики, sfx_end — звук в конце, hold — пауза после.
"""

from typing import Any

TITLE_RU = "Я Энтмен!"
TITLE_EN = "I'm Antman!"

# Говорящие: N — рассказчик, A — Антон/Энтмен, S — учёный,
# M — мама, P — парикмахер, B — Барон Дихлофос.
SPEAKER_NAMES: dict[str, dict[str, str]] = {
    "ru": {"N": "Рассказчик", "A": "Энтмен", "S": "Учёный", "M": "Мама",
           "P": "Парикмахер", "B": "Барон Дихлофос"},
    "en": {"N": "Narrator", "A": "Antman", "S": "Scientist", "M": "Mom",
           "P": "Barber", "B": "Baron Bugspray"},
}

SCENES: list[dict[str, Any]] = [
    {"kind": "title", "music": "happy", "lines": [
        ("N", "Комедия. Двенадцать плюс. «Я Энтмен!»",
              "A comedy. Rated twelve plus. I'm Antman!", {"sfx": "fanfare", "hold": 1.0}),
    ]},
    {"kind": "city", "music": "happy", "lines": [
        ("N", "Город Муравейск. Здесь живёт Антон Мурашов: курьер, неудачник "
              "и чемпион мира по спотыканию на ровном месте.",
              "The city of Anthill Falls. Meet Anton Murashov: delivery guy, "
              "loser, and world champion of tripping over absolutely nothing.", {}),
        ("A", "Доставка пиццы! Ой-ой-ой... Асфальт опять напал первым!",
              "Pizza delivery! Whoa-whoa-whoa... The sidewalk attacked me first again!",
              {"sfx": "trip", "hold": 0.6}),
    ]},
    {"kind": "lab", "music": "happy", "lines": [
        ("N", "Однажды Антон привёз пиццу в секретную лабораторию.",
              "One day, Anton delivered a pizza to a secret laboratory.", {}),
        ("S", "Осторожно, молодой человек! Не подходите к чану с регенерином!",
              "Careful, young man! Stay away from the Regenerin vat!", {}),
        ("A", "К какому чану? Вот к этому?",
              "Which vat? This one right here?", {}),
        ("N", "Бульк.", "Splash.", {"sfx": "splash", "hold": 1.6}),
    ]},
    {"kind": "kitchen", "music": "happy", "lines": [
        ("N", "Наутро Антон заметил кое-что странное.",
              "The next morning, Anton noticed something strange.", {}),
        ("A", "Ай! Порезал палец... А, нет. Уже не порезал.",
              "Ouch! I cut my finger... Oh, wait. Never mind.", {"sfx_end": "heal"}),
        ("A", "Я заживаю за секунду! Мама! Мама, я супергерой!",
              "I heal in one second! Mom! Mom, I'm a superhero!", {}),
        ("M", "Сынок, супергерои тоже надевают шапку. Надень шапку.",
              "Sweetie, superheroes wear a hat too. Put on a hat.", {"hold": 0.6}),
    ]},
    {"kind": "barber", "music": "happy", "lines": [
        ("N", "Жить с регенерацией оказалось непросто.",
              "Living with regeneration turned out to be tricky.", {}),
        ("P", "Так, подстригаю... подстригаю... Почему оно отрастает обратно?!",
              "Okay, snip... snip... Why is it growing back?!", {"sfx": "snip"}),
        ("A", "Простите. Это у меня суперсила такая.",
              "Sorry. That's kind of my superpower.", {}),
        ("P", "А это у меня теперь нервный тик!",
              "And this is my brand new nervous twitch!", {"hold": 0.6}),
    ]},
    {"kind": "food", "music": "happy", "lines": [
        ("N", "А ещё Антон теперь ел за трёх слонов. Регенерация очень любит котлеты.",
              "Also, Anton now ate like three elephants. Regeneration really loves meatballs.", {}),
        ("A", "Добавки, пожалуйста! И компот. Два компота.",
              "Seconds, please! And a milkshake. Two milkshakes.", {"hold": 0.6}),
    ]},
    {"kind": "park", "music": "villain", "lines": [
        ("N", "Но однажды в городе появился злодей. Барон Дихлофос!",
              "But one day, a villain came to town. Baron Bugspray!", {}),
        ("B", "Ха-ха-ха! Я опрыскаю весь этот город! Никаких муравьёв! Никаких пикников!",
              "Ha-ha-ha! I will spray this entire city! No ants! No picnics!", {"sfx": "spray"}),
        ("A", "Стой, Барон! Я Энтмен!",
              "Stop right there, Baron! I'm Antman!", {"sfx": "land"}),
        ("B", "Энтмен? Звучит как то, что я травлю по выходным.",
              "Antman? Sounds like something I exterminate on weekends.", {"hold": 0.4}),
    ]},
    {"kind": "fight", "music": "villain", "lines": [
        ("B", "Получай облако!", "Eat my cloud!", {"sfx": "spray"}),
        ("A", "Кхе-кхе... Невкусно. Но я уже здоров!",
              "Cough, cough... Tastes awful. But I'm already fine!", {"sfx_end": "heal"}),
        ("B", "Тогда — гигантский тапок!", "Then, the giant slipper!",
         {"sfx_end": "splat", "hold": 0.8}),
        ("A", "Я плоский... но это ненадолго!",
              "I'm flat... but not for long!", {"sfx_end": "boing", "hold": 1.0}),
    ]},
    {"kind": "climax", "music": "villain", "lines": [
        ("A", "Можешь бить меня хоть до вечера, Барон. Я отрастаю. А твой баллончик — нет.",
              "You can hit me all day, Baron. I grow back. Your spray can doesn't.", {}),
        ("B", "Пшш... пшш... Пусто?! Это нечестно!",
              "Psst... psst... Empty?! That's not fair!", {"sfx": "sputter"}),
        ("N", "Барона увезла полиция, а город был спасён.",
              "The police took the Baron away, and the city was saved.",
         {"sfx": "siren", "hold": 0.8}),
    ]},
    {"kind": "ending", "music": "happy", "lines": [
        ("N", "А Антон так и живёт со своей суперсилой. Подстричься он больше не пытается.",
              "And Anton still lives with his superpower. He has given up on haircuts.", {}),
        ("A", "Зато я никогда не болею! Я Энтмен!",
              "But I never get sick! I'm Antman!", {"sfx_end": "fanfare", "hold": 1.5}),
    ]},
    {"kind": "credits", "music": "happy", "lines": [], "duration": 9.0},
]

CREDITS: dict[str, list[str]] = {
    "ru": ["«Я Энтмен!»", "", "Комедия · 12+", "", "Энтмен — Антон Мурашов",
           "Барон Дихлофос — злодей", "Учёный · Парикмахер · Мама", "",
           "Озвучка, анимация и музыка:", "сделано ИИ", "",
           "Ни один муравей не пострадал.", "Тапок — пострадал."],
    "en": ["I'm Antman!", "", "Comedy · 12+", "", "Antman — Anton Murashov",
           "Baron Bugspray — the villain", "Scientist · Barber · Mom", "",
           "Voices, animation and music:", "made by AI", "",
           "No ants were harmed.", "The slipper was."],
}
