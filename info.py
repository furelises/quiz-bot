import json
import os
from pathlib import Path

project = {"project": "https://github.com/furelises/quiz-bot.git"}
photo = 'images.jpg'
db_path = "./db"
btn_id_sequence = 0
seasons_images_path = "./seasons_images"


class Btn:
    def __init__(self, question: str, title: str, autumn: int, winter: int, summer: int, spring: int):
        global btn_id_sequence
        self.id = str(btn_id_sequence)
        btn_id_sequence += 1
        self.question = question
        self.title = title
        self.winter = winter
        self.autumn = autumn
        self.spring = spring
        self.summer = summer


class User:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.vars = {}
        for file in os.listdir(db_path):
            if str(user_id) == Path(file).stem:
                with open(f"{db_path}/{file}") as f:
                    self.vars = json.load(f)
                    break

    def dump(self):
        with open(f"./db/{self.user_id}.json", "w") as f:
            json.dump(self.vars, f)

    def restart(self):
        self.vars={}
        self.dump()


    def get_next_question(self) -> str:
        keys_list = list(set(questions_list.keys()) - set(self.vars.keys()))
        if len(keys_list) != 0:
            return keys_list[0]

    def get_answer(self):
        winter = 0
        spring = 0
        summer = 0
        autumn = 0
        for i in self.vars:
            winter += self.vars[i]['winter']
            spring += self.vars[i]['spring']
            summer += self.vars[i]['summer']
            autumn += self.vars[i]['autumn']
        list = {'winter': winter, 'spring': spring, 'summer': summer, 'autumn': autumn}
        a = max(list, key=list.get)

        return answers_list[a]

    def handler(self,btn_id):
        btn = get_button(btn_id)
        self.vars[btn.question] = {
            "winter": btn.winter,
            "summer": btn.summer,
            "autumn": btn.autumn,
            "spring": btn.spring,
        }
        self.dump()


answers_list = {
    'autumn': {
        "title": "Скорее всего,ваш цветотип - осень!🍁🍁🍁",
        "image": f"{seasons_images_path}/autumn.jpg"
    },
    'winter': {
        'title':"Скорее всего,ваш цветотип - зима!❄️❄️❄️",
        "image": f"{seasons_images_path}/winter.jpg"
    },
    'spring': {
        "title":"Скорее всего,ваш цветотип - весна!🌿🌿🌿",
        "image": f"{seasons_images_path}/spring.jpg"
    },
    'summer': {
        "title":"Скорее всего,ваш цветотип - лето!🍓🍓🍓",
               "image": f"{seasons_images_path}/summer.jpg"
    }
}

questions_list = {
    "question1": {
        "title": "Выберите ваш цвет волос ;",
        "list": [
            Btn("question1", "брюнет", autumn=1, winter=1, spring=0, summer=0),
            Btn("question1", "шатен", autumn=1, winter=1, spring=1, summer=0),
            Btn("question1", "русый", autumn=0, winter=0, spring=1, summer=1),
            Btn("question1", "блондин", autumn=0, winter=0, spring=1, summer=1),
            Btn("question1", "рыжий", autumn=1, winter=0, spring=0, summer=0)

        ]},
    "question2": {
        "title": "Выберите ваш цвет глаз ;",
        "list": [
            Btn("question2", "голубые", autumn=0, winter=1, spring=0, summer=1),
            Btn("question2", "зеленые", autumn=1, winter=0, spring=1, summer=0),
            Btn("question2", "серые", autumn=1, winter=1, spring=1, summer=1),
            Btn("question2", "карие", autumn=1, winter=1, spring=1, summer=0),
            Btn("question2", "черные", autumn=1, winter=1, spring=0, summer=0)

        ]},
    "question3": {
        "title": "Выберите цвет и оттенок вашей кожи ;",
        "list": [
            Btn("question3", "светлая, с холодным подтоном", autumn=0, winter=1, spring=0, summer=1),
            Btn("question3", "от светлой, до средней смуглости, с теплым подтоном", autumn=1, winter=0, spring=0,
                summer=0),
            Btn("question3", "розоватый оттенок кожи, с теплым подтоном", autumn=1, winter=0, spring=1, summer=0),

        ]}

}


def get_button(id: str) -> Btn:
    for i in questions_list:
        for b in questions_list[i]['list']:
            if b.id == id:
                return b


def project_to_str() -> str:
    a = ''
    for i in project:
        b = f'{i} : {project[i]}\n'
        a += b
    return a


def get_photo():
    a = open(photo, 'rb')
    return a
