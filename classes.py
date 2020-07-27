import random

from pygame import image as img
from pygame import font
from pygame.math import Vector2
from pygame import mouse
# Студент
#    Оценки - Результат
#    Успеваемость - Заинтересованость в оценках
#    Интеллект - Возможно повысить, возможно понизить влияет на оценки и успеваемость
#    Удача - Врожденный фактор, влияет на оценки и интеллект
#    Прописка - Влияет на мотиацию, интеллект, успеваемость



WIDTH = 800
HEIGHT = 500

CAREER = 0.5 # (0 - 3) # увеличивает
INTEL = 0.5 # (0 - 3) # влияет на оценку
LUCK = 0.5  # (0 - 3) # влияет на оценку
REG = 1 # 1 - дома, 2 - общага, 3 - аренда



class Student():

    def __init__(self, name, career, intelegent, luck, A, B, C, D, image):

        super().__init__()
        self.stay = True
        self.marks = [] # оценки
        self.name = name # имя
        self.career = career # Карьера
        self.intelegent = intelegent # Интеллект
        self.luck = luck # Удача
        self.reg = None # Прописка
        self.steps = 0
        self.ready = True


        self.favorite = None # Любимое место


        self.friend = []

        self.state = 0 # 0 - Улица (В пути), 1 - Университет, 2 - Дома, 3 - В компании

        self.home = None

        self.image = img.load(image) # Картинка для визуала
        self.image.set_colorkey((255,255,255))

        pos = (random.randint(17,450), random.randint(17,450))

        self.rect = self.image.get_rect(center=pos) # Границы


        self.vel = Vector2(0, 0)
        self.pos = Vector2(pos)

        # Положение на поле


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





        text2 = f.render(" Имя {} ".format(self.name), 1, (0, 180, 0))
        text3 = f.render(" Удача {} ".format(self.luck), 1, (0, 180, 0))
        text4 = f.render(" Интеллект {} ".format(self.intelegent), 1, (0, 180, 0))
        text5 = f.render(" Карьера {} ".format(self.career), 1, (0, 180, 0))


        text6 = f.render(" Оценки {}".format(" ".join([str(i) for i in self.marks])), 1, (0, 180, 0))


        text7 = f.render(" Прописка {}".format(self.reg), 1, (0, 180, 0))

        text8 = f.render(" Друзья {}".format("\n".join([str(i.name) for i in self.friend])), 1, (0, 180, 0))


        text = [text2, text3, text4, text5, text6, text7, text8]

        num = 30

        for i in text:
            screen.blit(i, (530, num))
            num += 25

    def update(self, point):

        if self.stay == True:

            # считаем щаги для удобства ввода действий


            try:
                self.vel = (point - self.pos).normalize() * 4
            except:
                pass

            self.pos += self.vel
            self.rect.center = self.pos








        else:
            pass

    # ^ - Как функцию помощи между студентами
    def __xor__(self, other):

        if other in self.friend:

            if self.state == 3:

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
        if self.ready == True:
            gr = self.get_chances()
            # Получить шансы, для оценок

            k = random.randint(1, 100)
            # Великий рандом решает судьбу студента!

            self.intelegent = round(self.intelegent, 4)
            self.luck = round(self.luck, 4)
            self.career = round(self.career, 4)
            #Получил 2
            if k < gr[3][0] and k >= gr[3][1]:
                self.marks.append(2)
                print(self.name+" получил 2")
                self.ready = False


            #Получил 3
            elif k < gr[2][0] and k >= gr[2][1]:
                self.marks.append(3)
                print(self.name+" получил 3")
                self.ready = False


            #Получил 5
            elif k <= gr[0][0] and k >= gr[0][1]:
                self.marks.append(5)
                print(self.name+" получил 5")
                self.ready = False

            #Получил 4
            elif k < gr[1][0] and k >= gr[1][1]:
                self.marks.append(4)
                print(self.name+" получил 4")
                self.ready = False


            # пропустил пару
            else:
                self.intelegent -= 0.04
                self.marks.append(2)
                print(self.name+" прогуглял, и получил 2")
                self.ready = False

            self.career_movement()


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
    def __init__(self, name):
        super().__init__(name, 1, 1, 0.5, 45, 30, 5, 2.5, image="sprites/botan.png")
        #A - 40 , B - 30, C-10, D-5
        self.type = 1

    def spell(self):
        self.steps = 0
        self.career += 0.1
        self.marks.append(5)


# Студент везунчик, может случайно получить пятерку
class Lucker(Student):
    def __init__(self, name):
        super().__init__(name, 0.4, 0.4, 1, 30, 30, 5, 5, image="sprites/Lucker.png")

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
    def __init__(self, name):
        super().__init__(name, 0.2, 0.2, 1, 15, 35, 25, 10, image="sprites/Loser.png")



        self.type = 3


    def spell(self):
        print("{0} пытается быть лучше".format(self.name))
        self.career += 0.1
        self.steps = 0
        # A - 15 , B - 40, C-25, D-10

# класс студент который постоянно прогуливает, без каких то особенностей
class Freeloader(Student):
    def __init__(self, name):
        super().__init__(name, 0.3, 0.3, 1, 5, 25, 35, 12.5, image="sprites/FreeLoader.png")



        self.type = 4


    def spell(self):
        self.steps = 0
        pass
        #A - 5 , B - 35, C-25, D-12.5



# класс студент обычный, без каких то особенностей, просто пытается быть лучше
class Regular(Student):


    def __init__(self, name):

        super().__init__(name, 0.5, 0.5, 0.5, 30, 40, 15, 5, image="sprites/regular.png")


        self.type = 5

    def spell(self):
        self.steps = 0
        self.intelegent += 0.01
        self.career += 0.05
        self.luck += 0.025
        # A - 25 , B - 40, C-18.5, D-7


class Struction():
    def __init__(self, image, x, y, type):
        self.image = img.load(image)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.centerx = x
        self.rect.centery = y
        self.pos = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def __add__(self, other):

        other.home = self.pos

        other.reg = self.type

        print(str(other.name) + " Засилен в структуру")


class RendHouse(Struction):
    def __init__(self, x, y):
        super().__init__(image='sprites/RendHome.png', x=x, y=y, type = "Сьемная квартира")


class Panel(Struction):
    def __init__(self, x, y):
        super().__init__(image='sprites/Panel.png', x=x, y=y, type="Дома с родителями")


class Domintory(Struction):
    def __init__(self, x, y):
        super().__init__(image='sprites/Domintory.png', x=x, y=y, type="Общага")



class University(Struction):
    def __init__(self):

        super().__init__(image='sprites/univer.png', x=250, y=400, type = 0)


    def in_univ(self):
        pass




# a = 25
# b = 40
# d = 18.5
# c = 7
