import random

from pygame import image as img
from pygame import font
#Студент
# Оценки - Результат
# Успеваемость - Заинтересованость в оценках
# Интеллект - Возможно повысить, возможно понизить влияет на оценки и успеваемость
# Удача - Врожденный фактор, влияет на оценки и интеллект
# Прописка - Влияет на мотиацию, интеллект, успеваемость



WIDTH = 800
HEIGHT = 500

CAREER = 0.5 # (0 - 3) # increase luck
INTEL = 0.5 # (0 - 3) # chance to have mark
LUCK = 0.5  # (0 - 3) # chance to have big mark
REG = 1 # 1 - home, 2 - domintory, 3 - rend



class Student():

    def __init__(self, name, career, intelegent, luck, registarition, A, B, C, D, image):

        super().__init__()

        self.marks = [] # оценки
        self.name = name # имя
        self.career = career # Карьера
        self.intelegent = intelegent # Интеллект
        self.luck = luck # Удача
        self.reg = registarition # Прописка
        self.steps = 0 # количество пройденных шагов

        self.image = img.load(image) # Картинка для визуала
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect() # Границы

        # Положение на поле
        self.rect.centerx = random.randint(17,450)
        self.rect.centery = random.randint(17,450)

        #Скорость двиежния
        self.speed_x = random.randint(1, 6)
        self.speed_y = random.randint(1, 6)


        # Шансы на оценку
        self.consts = [A, B, C, D]


    def draw(self, screen):
        screen.blit(self.image, self.rect)



    # Вывод текста
    def get_info(self, screen):

        f = font.Font(None, 24) # Шрифт
        try:
            k = self.marks[-1]  # Последняя оценка
        except:
            k = None

        text1 = f.render("Тип - Обычный ", 1, (0, 180, 0))
        text2 = f.render(" Имя {0} ".format(self.name), 1, (0, 180, 0))
        text3 = f.render(" Удача {0} ".format(self.luck), 1, (0, 180, 0))
        text4 = f.render(" Интеллект {0} ".format(self.intelegent), 1, (0, 180, 0))
        text5 = f.render(" Карьера {0} ".format(self.career), 1, (0, 180, 0))
        text6 = f.render(" Последняя оценка {0} ".format(k), 1, (0, 180, 0))
        text7 = f.render(" Прописка {0}".format(self.reg), 1, (0, 180, 0))

        text = [text1, text2, text3, text4, text5, text6, text7]

        num = 30

        for i in text:
            screen.blit(i, (530, num))
            num += 25

    def update(self):

        # считаем щаги для удобства ввода действий
        self.steps += 1

        # изменение позиции
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.centerx > (HEIGHT - 16) or (self.rect.centerx < 16):
            self.speed_x = -1 * self.speed_x

        if self.rect.centery > (HEIGHT - 16) or (self.rect.centery < 16):
            self.speed_y = -1 * self.speed_y



    # ^ - Как функцию помощи между студентами
    def __xor__(self, other):

        # Только для общащных
        if (self.reg == other.reg) and self.reg == 2:
            steps = 30 # если студенты из одной группы прописки

        else:
            steps = 60 # если из разных

        # для студентов из группы одной прописки все гораздо проще

        if self.steps > steps:

            if (self.intelegent >= other.intelegent) :

                other.intelegent += 0.2
                self.intelegent += 0.1

                self.intelegent = round(self.intelegent, 4)
                other.intelegent = round(other.intelegent, 4)

                print(str(self.name) + " помог " + str(other.name))

            self.steps = 0

        else:
            pass


    # вернуть последную оценку
    def last_mark(self):
        try:
            return self.marks[-1]
        except:
            return None

    # Разчитать шансы, на получение оценок
    def chanese(self):
        k = (1+self.luck) * (2+self.intelegent) * (3 * self.career)

        Ch_A = self.consts[0] + k # шанс получить пятерку

        Ch_B = self.consts[1] + k # шанс получить четверку

        Ch_C = self.consts[2] - k # шанс получить тройку

        Ch_D = self.consts[3] - k # шанс получить двойку

        chanses = [Ch_A, Ch_B, Ch_C, Ch_D]

        return chanses

    # Разчитать шансы, на получение оценок
    def get_chances(self):
        num = 100
        gr = []

        for i in self.chanese():
            p = []

            p.append(num)

            b = num - i

            num = b

            p.append(b)

            gr.append(p)

        return gr

    # Обучение в вузе
    def go_to_study(self):
        if self.steps > 100:
            gr = self.get_chances()
            # Получить шансы, для оценок

            k = random.randint(1, 100)
            # Великий рандом решает судьбу студента!

            #Получил 2
            if k < gr[3][0] and k >= gr[3][1]:
                self.marks.append(2)
                print("Получил 2")


            #Получил 3
            elif k < gr[2][0] and k >= gr[2][1]:
                self.marks.append(3)
                print("Получил 3")


            #Получил 5
            elif k <= gr[0][0] and k >= gr[0][1]:
                self.marks.append(5)
                print("Получил 5")

            #Получил 4
            elif k < gr[1][0] and k >= gr[1][1]:
                self.marks.append(4)
                print("Получил 4")



            # пропустил пару
            else:
                self.intelegent -= 0.04
                self.marks.append(2)
                print("Прогуглял, и получил два")

            self.career_movement()
            self.steps = 0


    # Поднятие по карьерной лестнице // Самообучение, пять 5 подряд, увеличивают ваш скилл
    def career_movement(self):
        l = 0

        for i in self.marks[::-1]:

            if l == 5:
                self.career += 0.1
                if i == 5:
                    l += 1
                elif i == 2:
                    self.career -= 0.05
                else:
                    break


# Студент ботан, быстро учится, можетслучайно словить пятерку
class Botan(Student):
    def __init__(self, name, registartion):
        super().__init__(name, 1, 1, 0.5, registartion, 40, 30, 10, 5, image="sprites/botan.png")
        #A - 40 , B - 30, C-10, D-5
        self.type = 1

    def spell(self):
        self.steps = 0
        self.career += 0.1
        self.marks.append(5)


# Студент везунчик, может случайно получить пятерку
class Lucker(Student):
    def __init__(self, name, registartion):
        super().__init__(name, 0.4, 0.4, 1, registartion, 25, 30, 20, 10, image="sprites/Lucker.png")

        self.type = 2

    def spell(self):
        self.steps = 0
        k = random.randint(0, 100)
        self.career += 0.1
        if k > 50:
            self.marks.append(5)

        # A - 25 , B - 30, C-20, D-10


# класс студент Лузер, без каких то особенностей, просто пытается быть лучше. Верит в то что может изменить мир
class Loser(Student):
    def __init__(self, name, registartion):
        super().__init__(name, 0.2, 0.2, 1, registartion, 15, 40, 25, 10, image="sprites/Loser.png")



        self.type = 3


    def spell(self):
        print("{0} пытается быть лучше".format(self.name))
        self.career += 0.1
        self.steps = 0
        # A - 15 , B - 40, C-25, D-10

# класс студент который постоянно прогуливает, без каких то особенностей
class Freeloader(Student):
    def __init__(self, name, registartion):
        super().__init__(name, 0.3, 0.3, 1, registartion, 5, 35, 25, 12.5, image="sprites/FreeLoader.png")



        self.type = 4


    def spell(self):
        self.steps = 0
        pass
        #A - 5 , B - 35, C-25, D-12.5



# класс студент обычный, без каких то особенностей, просто пытается быть лучше
class Regular(Student):


    def __init__(self, name, registartion):

        super().__init__(name, 0.5, 0.5, 0.5, registartion, 25, 40, 18.5, 7, image="sprites/regular.png")


        self.type = 5

    def spell(self):
        self.steps = 0
        self.intelegent += 0.01
        self.career += 0.05
        self.luck += 0.025
        # A - 25 , B - 40, C-18.5, D-7


# a = 25
# b = 40
# d = 18.5
# c = 7
