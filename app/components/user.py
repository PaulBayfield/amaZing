from .text2image import ConvertMazet2Image


import asyncio

from random import randint


class User:
    def __init__(self, image: ConvertMazet2Image, coins: int = 5, hearts: int = 3, radius: int = 30, level: int = 1, radiusPrices: list = None):
        self.image = image

        self.coins = coins
        self.hearts = hearts
        self.radius = radius
        self.level = level
        if not radiusPrices:
            self.radiusPrices = [
                {
                    "vision": 35,
                    "price": 10,
                    "claimed": False
                },
                {
                    "vision": 40,
                    "price": 15,
                    "claimed": False
                },
                {
                    "vision": 45,
                    "price": 20,
                    "claimed": False
                },
                {
                    "vision": 50,
                    "price": 30,
                    "claimed": False
                },
                {
                    "vision": 55,
                    "price": 40,
                    "claimed": False
                },
                {
                    "vision": 60,
                    "price": 50,
                    "claimed": False
                },
            ]
        else:
            self.radiusPrices = radiusPrices

        self.alive = True
        self.light = False
        self.blind = False
        self.x2 = False

        self.blindCells = 0

        self.x = 0
        self.y = 0

        self.heart = self.image.itemsData["3"]
        self.coin = self.image.itemsData["5"]
        self.stonks = self.image.itemsData["6"]
        self.blindness = self.image.itemsData["7"]
        self.torch = self.image.itemsData["8"]

        self.pathPrice = 50
        self.heartPrice = 50

        for p in self.radiusPrices:
            if not p["claimed"]:
                self.nextVisionPrice = p['price']
                break


    def checkMove(self, x, y):
        # Droite
        if x == 1 and self.x < self.image.laby.width - 1 and self.image.laby.reachable(self.x, self.y, self.x + x, self.y):
            asyncio.run(self.move((self.x + x, self.y)))
        # Gauche
        if x == -1 and self.x - x > 1 and self.image.laby.reachable(self.x, self.y, self.x + x, self.y):
            asyncio.run(self.move((self.x + x, self.y)))
        # Bas
        if y == 1 and self.y < self.image.laby.height - 1 and self.image.laby.reachable(self.x, self.y, self.x, self.y + y):
            asyncio.run(self.move((self.x, self.y + y)))

        # Haut
        if y == -1 and self.y + y >= 0 and self.image.laby.reachable(self.x, self.y, self.x, self.y + y):
            asyncio.run(self.move((self.x, self.y + y)))


    async def move(self, coord):
        self.image.laby.setItem(self.x, self.y, 0)

        self.x = coord[0]
        self.y = coord[1]


        if self.blind:
            self.blindCells += 1

            if self.blindCells == 5:
                self.blind = False
                self.updateBonus()


        item = self.image.laby.getItem(self.x, self.y)

        if item > 1:
            # Tombe sur la fin
            if item == 2:
                self.coins += 4
                if self.x2:
                    self.coins += 4

                self.updateCoins()

                if self.light:
                    self.light = False
                    self.image.win.timerLight = 0
                    self.radius -= 20

                self.image.win.labyWidth += 2
                self.image.win.labyHeight += 2

                self.image.win.loaded = None
                self.image.win.inGame = False
                await self.image.win.loadMaze()

            # Tombe sur un coeur
            if item == 3:
                self.hearts += 1
                self.updateHealth()

            # Tombe sur un trap
            if item == 4:
                self.hearts -= 1
                self.updateHealth()
                
                if self.hearts == 0:
                    self.alive = False

            # Tombe sur un coin
            if item == 5:
                self.coins += 1
                if self.x2:
                    self.coins += 1

                self.updateCoins()

            # Tombe sur un x2
            if item == 6:
                self.x2 = True
                self.updateBonus()

            # Tombe sur un blindness
            if item == 7:
                p = False
                if self.light:
                    if randint(0, 1) == 0:
                        self.image.laby.setItem(self.x, self.y, 0)
                        p = True

                if not p:
                    self.blind = True
                    self.blindCells = 0
                    self.updateBonus()
                
            # Tombe sur une flashlight
            if item == 8:
                self.radius += 20
                self.light = True
                self.blind = False
                self.updateRadius()
                self.updateBonus()

            # Tombe sur un sac d'or
            if item == 9:
                r = randint(1, 14)
                self.coins += r

                if self.x2:
                    self.coins += r

                self.updateCoins()
        

            await self.image.applyCache(self.x, self.y)

        await self.image.moveCharacter(self)


    def updateHealth(self):
        self.image.win.characterLife.setText(f"Health: {self.heart * self.hearts}")
        self.image.win.characterLife.adjustSize()


    def updateCoins(self):
        self.image.win.characterCoins.setText(f"Coins: {self.coins} {self.coin}")
        self.image.win.characterCoins.adjustSize()

    
    def updateLevel(self):
        self.image.win.characterLevel.setText(f"Level {self.level}")
        self.image.win.characterLevel.adjustSize()

    
    def updateRadius(self):
        self.image.win.characterRadius.setText(f"Vision: {self.radius}")
        self.image.win.characterRadius.adjustSize()

        self.image.win.buyVision.setText(f"Extra Vision [V]: {self.nextVisionPrice} {self.coin}")


    def updateBonus(self):
        bonus = ""
        if self.blind:
            bonus += f"{self.blindness} "
        if self.light:
            bonus += f"{self.torch} "
        if self.x2:
            bonus += f"{self.stonks} "

        self.image.win.characterBonus.setText(f"Bonus: {bonus}")
        self.image.win.characterBonus.adjustSize()
    

    def updateLife(self):
        self.image.win.buyLife.setText(f"Extra Life [E]: {self.heartPrice} {self.coin}")


    def updatePath(self):
        self.image.win.buyPath.setText(f"Exit Path [P]: {self.pathPrice} {self.coin}")


    def display(self):
        self.updateHealth()
        self.updateCoins()
        self.updateLevel()
        self.updateBonus()
        self.updateRadius()
        self.updateLife()
        self.updatePath()


    def buyRange(self):
        for p in self.radiusPrices:
            if not p["claimed"] and self.radius <= p['vision'] and self.coins >= p['price']:
                self.radius += (p['vision'] - self.radius)
                self.coins -= p['price']
                p['claimed'] = True

                for p in self.radiusPrices:
                    if not p["claimed"]:
                        self.nextVisionPrice = p['price']
                        break

                self.updateCoins()
                self.updateRadius()

                break


    def buyPath(self):
        if self.coins >= self.pathPrice:
            self.coins -= self.pathPrice
            self.updateCoins()
            self.updatePath()
            asyncio.run(self.image.showPath(self.x, self.y))
            asyncio.run(self.image.win.updateLabyImage())


    def buyHeart(self):
        if self.coins >= self.heartPrice:
            self.coins -= self.heartPrice
            self.hearts += 1
            self.updateCoins()
            self.updateHealth()


    async def refresh(self):
        await self.image.moveCharacter(self)
        await self.image.win.updateLabyImage()

