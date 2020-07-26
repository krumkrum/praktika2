import random
import pygame
import classes

names = ["Александр","Сергей","Владимир","Елена","Татьяна","Андрей","Алексей","Ольга","Николай","Наталья","Анна","Иван",
         "Веня", "Петя", "Колян", "Толян", "Саня", "Марина", "Соня", "Данил", "Денис", "Стас", "Митя"]
WHITE = (255,255,255)
BLACK = (0  ,0  ,0  )

WIDTH = 800
HEIGHT = 500

#----------------------------------------------------------------------


#----------------------------------------------------------------------




# Класс игры, удобно для 1. создание внутри обьектов, удобство их взаимодействие
class Game():

    def __init__(self):
        super().__init__()

        pygame.init() # инициализируем библиотеку

        self.screen = pygame.display.set_mode((WIDTH,HEIGHT)) # создать экран

        self.background = pygame.image.load("sprites/screen.png").convert() # БГ

        self.multi_enemies = [] # Массив студентов

        self.min = 0
        self.hour = 0
        self.day = 0

        self.font = pygame.font.Font(None, 24)

        self.domintory = classes.Domintory(100, 300)
        self.house = classes.RendHouse(100, 100)
        self.panel_1 = classes.Panel(400, 100)
        self.panel_2 = classes.Panel(400, 300)
        self.univ = classes.University() # Универ

        self.struction = []



        self.struction.append(self.domintory)
        self.struction.append(self.house)
        self.struction.append(self.panel_1)
        self.struction.append(self.panel_2)
        self.struction.append(self.univ)



        # Создание студентов рекомендуется 2, но можно 5
        for i in range(0, 2):
            botan = classes.Botan(names[random.randint(0,11)]+ " Заучка")
            loser = classes.Loser(names[random.randint(0,11)]+ " Неудачник")
            regular = classes.Regular(names[random.randint(0,11)] + " Обычный")
            loader = classes.Freeloader(names[random.randint(0,11)]+ " Лодырь")
            lucker = classes.Lucker((names[random.randint(0,11)]+" Везунчик"))

            loser.update((0,0))
            botan.update((0,0))
            regular.update((0,0))
            loader.update((0,0))
            lucker.update((0,0))

            self.multi_enemies.append(botan)
            self.multi_enemies.append(loser)
            self.multi_enemies.append(regular)
            self.multi_enemies.append(loader)
            self.multi_enemies.append(lucker)


        # Расселение + Создание связи между учениками (Дружба) Бывает и так что никто не нашел друзей!
        for n, i in enumerate(self.multi_enemies):
            k = (random.randint(0, len(self.multi_enemies))-1)

            favorite_places_coordinat = [random.randint(30, 470), random.randint(320, 450)]

            if (i not in self.multi_enemies[k].friend) and (i != self.multi_enemies[k]) and (i.friend == []):

                i.friend.append(self.multi_enemies[k])
                self.multi_enemies[k].friend.append(i)

                i.favorite = favorite_places_coordinat
                self.multi_enemies[k].favorite = favorite_places_coordinat

            #Заселение "+"
            if n % 2 == 0:
                self.struction[0]+i
            elif n % 3 == 0:
                self.struction[2]+i
            elif n % 5 == 0:
                self.struction[3]+i
            else:
                self.struction[1]+i

        for i in self.multi_enemies:
            print("\n")
            print(i.name + " в компании с \n")

            for k in i.friend:
                print(k.name)



    #------------



    def run(self):
        n = 0

        RUNNING = True

        clock = pygame.time.Clock()

        while RUNNING:

            self.time = self.font.render("{0} дней : {1} часов : {2} минут".format(self.day, self.hour, self.min), 1,
                                         (0, 0, 0))
            if self.min == 60:
                self.hour += 1
                self.min = 0

            if self.hour == 24:
                self.day += 1
                self.hour = 0

            self.min +=1




            pygame.time.wait(50)

            # Список процессов в обработчике
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    RUNNING = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if n <= 9:
                            try:
                                self.multi_enemies[n-1].stay = True
                            except:
                                pass
                            p = self.multi_enemies[n]

                            n += 1
                        else:
                            n = 0

                    ### Допилить в обратную сторону !

                    if event.key == pygame.K_SPACE:
                        # self.multi_enemies[n+1].stay = True

                        self.multi_enemies[n-1].stay = True
                        n = 0
                        p = None








            # Перебор студентов и действия над ними
            for std in self.multi_enemies:
                if self.min == 45:
                    std.ready = True

                # Студент идет в любимое место
                if (self.hour == 12) or (self.hour == 20):

                    std.update(std.favorite)

                    k = std.rect.collidelistall(self.multi_enemies)

                    for i in k:

                        try:
                            self.multi_enemies[i] ^ self.multi_enemies[i+1]

                        except:
                            pass

                #  В университет
                elif ((self.hour >= 7) and (self.hour < 15)):

                    std.update(self.univ.pos)

                    u = self.univ.rect.collidelistall(self.multi_enemies)

                    if self.min == 30:
                        for i in u:
                            self.multi_enemies[i].go_to_study()


                    # могут проявлять навыки на учебе
                    if std.steps > 150:
                        std.spell()
                        std.ready = True

                # Время идти домой
                elif (self.hour >= 15):
                    std.update(std.home)

                # Время идти спать
                else:
                    std.update(std.home)













            # Заполнение черным цветом экрана
            self.screen.fill(BLACK)

            # Отрисовка экрана
            self.screen.blit(self.background, self.background.get_rect())


            # Отрисовка зданий
            for strct in self.struction:

               strct.draw(self.screen)

            self.screen.blit(self.time, self.background.get_rect())




            # Отриосвка остальных студентов
            for std in self.multi_enemies:

                std.draw(self.screen)

            # Вывод информации
            try:

                p.get_info(self.screen)
                p.stay = False

            except:
                pass








            # Обновление экрана

            pygame.display.update()

            pygame.display.flip()

            clock.tick(60)







        pygame.quit()

#----------------------------------------------------------------------
# ЗАПУСК
if __name__ == '__main__':
    Game().run()