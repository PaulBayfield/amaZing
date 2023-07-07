from .Maze import Maze
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji
from emoji import is_emoji
from random import randint

import json


OVER = 140


class ConvertMazet2Image:
    def __init__(self, win, laby: Maze):
        self.win = win
        self.laby = laby

        self.start = (0, 0)
        self.end = (self.laby.width-1, self.laby.height-1)

        self.chemin = self.laby.solve_rhr(self.start, self.end)
        self.chemin.pop(0)

        self.unicodefont = ImageFont.truetype(f"{self.win.pathAssets}/fonts/unifont.ttf")


        with open(f"{self.win.pathAssets}/data.json", "r", encoding="utf-8") as file:
            self.itemsData = json.load(file)


        self.cache = Image.new('RGBA', (10, 10), color=(0, 0, 0))
        self.block = False


    async def generateImage(self):
        # Creéation d'une nouvelle image de 1 pixel sur 1 pixel pour pouvoir calculer la taille du texte...
        img = Image.new('RGBA', (1, 1))
        drawer = ImageDraw.Draw(img)

        # Lignes du laby sous forme de list
        lines = str(self.laby).split('\n')

        # Taille d'une ligne
        size = drawer.textsize(lines[0], font=self.unicodefont)

        # Taille du labyrinthe en pixel
        width = size[0]
        height = (size[1]+2)*(len(lines)-1)-3
        
        # Création de l'image du labyrinthe...
        img = img.resize((width+OVER*2, height+OVER*2))

        self.drawer = ImageDraw.Draw(img)
        self.drawer.multiline_text((OVER, OVER), str(self.laby), font=self.unicodefont)

        self.rawLaby = img
        self.image = img


    def getPixelX(self, x):
        """
        Renvoie le pixel de la cellule
        """
        return int((x + 1) * 20 - 12) + OVER

    
    def getPixelY(self, y):
        """
        Renvoie le pixel de la cellule
        """
        return int((y + 2) * 26 - 38) + OVER


    async def displayEmoji(self, x: int, y: int, char: str, get: bool = True, save: bool = False):
        if get:
            self.image = self.rawLaby.copy()

        if is_emoji(char):
            Pilmoji(image=self.image, draw=self.drawer).text((self.getPixelX(x), self.getPixelY(y)), char, font=self.unicodefont)

        if save:
            self.rawLaby = self.image.copy()


    async def generateEnd(self):
        self.laby.setItem(self.end[0], self.end[1], 2)
        await self.displayEmoji(self.end[0], self.end[1], self.itemsData["2"], save = True)


    async def applyCache(self, x, y):
        self.rawLaby.paste(self.cache, (self.getPixelX(x), self.getPixelY(y)))


    async def showPath(self, x, y):
        chemin = self.laby.solve_rhr((y, x), self.end)
        chemin.pop(0)

        temp = []
        self.block = True

        cell = (x, y)

        self.image = self.rawLaby.copy()
        Pilmoji(image=self.image).text((self.getPixelX(x), self.getPixelY(y)), self.itemsData["1"], font=self.unicodefont)

        for c in chemin:
                if c not in temp:
                    if self.laby.isValid(c[1], c[0]) and c != self.end:
                        Pilmoji(image=self.image).text((self.getPixelX(c[1]), self.getPixelY(c[0])), "•", font=self.unicodefont)
                    
                    temp.append(cell)
                    cell = (c[1], c[0])

        await self.updateImage(self.getPixelX(x), self.getPixelY(y), 60, False, True)


    async def generateItems(self):
        print("starting...")
        await self.generateEnd()
        await self.generateIcon(3, randint(1, self.laby.width*self.laby.height // 50))
        await self.generateIcon(4, randint(1, self.laby.width*self.laby.height // 25))
        await self.generateIcon(5, randint(1, self.laby.width*self.laby.height // 10))
        await self.generateIcon(6, randint(1, 1))
        await self.generateIcon(7, randint(3, self.laby.width*self.laby.height // 20))
        await self.generateIcon(8, randint(1, self.laby.width*self.laby.height // 100))
        await self.generateIcon(9, randint(1, self.laby.width*self.laby.height // 50))
        print("done...")
        

    async def generateIcon(self, priority: str, amount: int):
        count = 0
        while count != amount:
            coord = (randint(0, self.laby.width-1), randint(0, self.laby.height-1))
            if self.laby.isValid(coord[0], coord[1]) and coord != self.start and coord != self.end:
                await self.displayEmoji(coord[0], coord[1], self.itemsData[str(priority)], save = True)
                self.laby.setItem(coord[0], coord[1], priority)
                count += 1


    async def moveCharacter(self, user):
        x = user.x
        y = user.y

        self.laby.setItem(x, y, 1)
        await self.displayEmoji(x, y, self.itemsData["1"])
        await self.updateImage(self.getPixelX(x), self.getPixelY(y), radius = user.radius, blind = user.blind, light = user.light)


    async def updateImage(self, x, y, radius, blind: bool = False, light: bool = False):
        x += 5
        y += 5


        radius += 20

        mask = Image.new('L', (self.image.size[0], self.image.size[1]), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=255)
        self.image.putalpha(mask)

        
        overlay = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)


        if blind:
            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(0, 0, 0, 0), outline=(0, 0, 0, 110), width=55)
            self.image = Image.alpha_composite(self.image, overlay)

            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(0, 0, 0, 0), outline=(0, 0, 0, 150), width=45)
            self.image = Image.alpha_composite(self.image, overlay)
            
            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(0, 0, 0, 0), outline=(0, 0, 0, 190), width=35)
            self.image = Image.alpha_composite(self.image, overlay)

            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(0, 0, 0, 0), outline=(0, 0, 0, 220), width=20)
            self.image = Image.alpha_composite(self.image, overlay)

            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(0, 0, 0, 0), outline=(0, 0, 0, 250), width=5)
            self.image = Image.alpha_composite(self.image, overlay)
        elif light:
            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(0, 0, 0, 0), outline=(0, 0, 0, 20), width=35)
            self.image = Image.alpha_composite(self.image, overlay)
            
            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(0, 0, 0, 0), outline=(0, 0, 0, 50), width=25)
            self.image = Image.alpha_composite(self.image, overlay)

            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(0, 0, 0, 0), outline=(0, 0, 0, 60), width=20)
            self.image = Image.alpha_composite(self.image, overlay)
            
            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(0, 0, 0, 0), outline=(0, 0, 0, 70), width=10)
            self.image = Image.alpha_composite(self.image, overlay)

            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(0, 0, 0, 0), outline=(0, 0, 0, 90), width=5)
            self.image = Image.alpha_composite(self.image, overlay)
        else:
            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(0, 0, 0, 0), outline=(0, 0, 0, 70), width=35)
            self.image = Image.alpha_composite(self.image, overlay)
            
            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(0, 0, 0, 0), outline=(0, 0, 0, 90), width=25)
            self.image = Image.alpha_composite(self.image, overlay)

            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(0, 0, 0, 0), outline=(0, 0, 0, 110), width=20)
            self.image = Image.alpha_composite(self.image, overlay)
            
            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(0, 0, 0, 0), outline=(0, 0, 0, 150), width=10)
            self.image = Image.alpha_composite(self.image, overlay)

            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(0, 0, 0, 0), outline=(0, 0, 0, 180), width=5)
            self.image = Image.alpha_composite(self.image, overlay)

        self.image = self.image.crop((x-radius, y-radius, x+radius, y+radius))
        self.image = self.image.resize((800, 800), resample=Image.BOX)
