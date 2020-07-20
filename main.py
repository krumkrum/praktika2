import random
import pygame
import classes

WHITE = (255,255,255)
BLACK = (0  ,0  ,0  )

WIDTH = 800
HEIGHT = 500

#----------------------------------------------------------------------


#----------------------------------------------------------------------

class University():
    def __init__(self):
        self.image = pygame.image.load('sprites/univer.png')
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()

        self.rect.centerx = 250
        self.rect.centery = 400

    def draw(self, screen):
        screen.blit(self.image, self.rect)




# Класс игры, удобно для 1. создание внутри обьектов, удобство их взаимодействие
class Game():

    def __init__(self):
        super().__init__()

        pygame.init() # инициализируем библиотеку

        self.screen = pygame.display.set_mode((WIDTH,HEIGHT)) # создать экран

        self.background = pygame.image.load("sprites/screen.png").convert() # БГ

        self.multi_enemies = [] # Массив студентов


        self.univ = University() # Универ

        # create 3 enemies 0...2



        self.regboy = classes.Regular("Михаил Патапько", random.randint(1,3)) # Наш подопытный

        self.regboy.update() # Отрисовка Михаила

        self.multi_enemies.append(self.regboy) # Добавление его в массив  студентов


        # Создание студентов рекомендуется 2, но можно 5

        for i in range(0, 2):
            botan = classes.Botan(random.randint(10, 40), random.randint(1,3)) # Числа испольюузется как имена
            loser = classes.Loser(random.randint(10, 40), random.randint(1,3)) # Для удобоства
            regular = classes.Regular(random.randint(10, 40), random.randint(1,3)) # Замятин "мы" наше все
            loader = classes.Freeloader(random.randint(10, 40), random.randint(1,3))
            lucker = classes.Lucker(random.randint(10, 40), random.randint(1,3))

            loser.update()
            botan.update()
            regular.update()
            loader.update()
            lucker.update()

            self.multi_enemies.append(botan)
            self.multi_enemies.append(loser)
            self.multi_enemies.append(regular)
            self.multi_enemies.append(loader)
            self.multi_enemies.append(lucker)

    #------------

    def run(self):

        clock = pygame.time.Clock()

        RUNNING = True

        while RUNNING:
            # --- events ---

            # Список процессов в обработчике
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    RUNNING = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        RUNNING = False

                    # changes position when key is pressed


            # Перебор студентов и действия над ними
            for std in self.multi_enemies:

                if std.steps > 100:
                    std.spell()

                std.update()

                k = std.rect.collidelistall(self.multi_enemies)

                if len(k) == 2:

                    self.multi_enemies[k[0]]^self.multi_enemies[k[1]]

                u = self.univ.rect.collidelistall(self.multi_enemies)

                if u:
                        self.multi_enemies[u[0]].go_to_study()






            # Заполнение черным цветом экрана
            self.screen.fill(BLACK)

            # Отрисовка экрана
            self.screen.blit(self.background, self.background.get_rect())


            # Отрисовка университета
            self.univ.draw(self.screen)

            # Отрисовка Михаила
            self.regboy.get_info(self.screen)

            # Отриосвка остальных студентов
            for std in self.multi_enemies:

                std.draw(self.screen)

            # Обновление экрана
            pygame.display.update()

            pygame.display.flip()


        pygame.quit()

#----------------------------------------------------------------------
# ЗАПУСК
if __name__ == '__main__':
    Game().run()