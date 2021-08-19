"""Animation maker"""
import tkinter.filedialog

import pygame
import ctypes
import os
import pickle
import imageio


class SettingsScene:
    """SettingsScene Class"""

    def __init__(self, screen, startX, endX, startY, endY):
        """Initialize SettingsScene Class"""
        pygame.init()
        # screen width and height
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        # colors
        self.background = (45, 45, 45)
        self.borderColors = (60, 60, 60)
        self.lightBackground = (50, 50, 50)

        self.rect = pygame.Rect((startX, startY), (endX-startX, endY-startY))

        self.font = pygame.font.Font("freesansbold.ttf", 35)

        # delay between movement
        self.delay = 0.1
        self.delayText = self.font.render(f"Delay: {self.delay}", True, self.borderColors)
        self.delayRect = self.delayText.get_rect(topleft=(self.rect.left+15, self.rect.top+15))

        # increase and decrease
        self.increase = pygame.image.load("IMG\\Run.png")
        self.decrease = pygame.transform.flip(self.increase, True, False)

        # rects of increase and decrease
        self.decreaseRect = self.decrease.get_rect(topleft=(self.delayRect.right + 15, self.delayRect.top))
        self.increaseRect = self.increase.get_rect(topleft=(self.decreaseRect.right + 15, self.delayRect.top))

        # dicts for accessing
        self.imgDict = {"increase": self.increase, "decrease": self.decrease}
        self.rectDict = {"increase": self.increaseRect, "decrease": self.decreaseRect}

        self.maxWidth = self.rect.width-40
        try:
            self.imgRect = None
            self.img = None
            self.imgRect = self.img.get_rect(center=self.rect.center)
        except:
            pass
        self.alpha = 200

    def setImg(self, img):
        """Set Img"""
        self.img = img
        self.imgRect = self.img.get_rect(center=self.rect.center)

    def changeHover(self):
        """Change hover"""
        x, y = pygame.mouse.get_pos()

        for key in ["increase", "decrease"]:

            # define rect and img
            rect = self.rectDict[key]
            img = self.imgDict[key]

            if rect.left <= x <= rect.right and rect.top <= y <= rect.bottom:
                img.set_alpha(self.alpha)
            else:
                img.set_alpha(255)

    def decreaseIncrease(self):
        """decreaseIncrease"""
        x, y = pygame.mouse.get_pos()

        for key in ["increase", "decrease"]:

            # define rect and img
            rect = self.rectDict[key]

            if rect.left <= x <= rect.right and rect.top <= y <= rect.bottom:
                print(key)
                if key == "increase": self.delay += 0.1
                elif key == "decrease" and self.delay > 0: self.delay -= 0.1
                self.reset()


    def reset(self):
        """Reset"""
        self.delayText = self.font.render("Delay: {:.1f}".format(self.delay), True, self.borderColors)
        self.delayRect = self.delayText.get_rect(topleft=(self.rect.left+15, self.rect.top+15))

        # increase and decrease
        self.increase = pygame.image.load("IMG\\Run.png")
        self.decrease = pygame.transform.flip(self.increase, True, False)

        # rects of increase and decrease
        self.decreaseRect = self.decrease.get_rect(topleft=(self.delayRect.right + 15, self.delayRect.top))
        self.increaseRect = self.increase.get_rect(topleft=(self.decreaseRect.right + 15, self.delayRect.top))

        self.rectDict = {"increase": self.increaseRect, "decrease": self.decreaseRect}


    def draw(self):
        """Draw"""
        pygame.draw.rect(self.screen, self.borderColors, self.rect, width=5)
        self.screen.blit(self.delayText, self.delayRect)

        # check click and hover
        self.changeHover()

        # draw increase and decrease
        self.screen.blit(self.increase, self.increaseRect)
        self.screen.blit(self.decrease, self.decreaseRect)

        print("d")

        try:
            self.screen.blit(self.img, self.imgRect)
        except:
            pass


class ImgScene:
    """ImgScene Class"""
    def __init__(self, screen, imgPath, maxHeight, x, y):
        """Initialize ImgScene Class"""

        # screen, width and height
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        # colors
        self.background = (45, 45, 45)
        self.borderColors = (60, 60, 60)
        self.lightBackground = (50, 50, 50)

        # img values
        self.imgPath = imgPath
        self.relImg = pygame.image.load(self.imgPath)
        self.img = self.relImg.copy()


        # resize img

        # set width that works if img height smaller than maxHeight
        ratio = self.img.get_width() / self.img.get_height()
        self.img = pygame.transform.scale(self.img, (int(ratio * maxHeight), maxHeight))

        # rect
        self.rect = self.img.get_rect(topleft=(x, y))
        self.rect.centery = y

        self.exit = pygame.image.load("IMG\\Exit.png")
        self.exitRect = self.exit.get_rect(topright=self.rect.topright)

    def checkClick(self):
        """CheckClick"""
        x, y = pygame.mouse.get_pos()

        if self.rect.left <= x <= self.rect.right and self.rect.top <= y <= self.rect.bottom:
            return True
        return False

    def checkExit(self):
        """Check delete from list"""
        x, y = pygame.mouse.get_pos()

        if self.exitRect.left <= x <= self.exitRect.right and self.exitRect.top <= y <= self.exitRect.bottom:
            return True
        return False


    def changeRect(self, padding):
        """change draw button"""
        # copy rect
        center = self.rect.center

        # change size
        self.rect.width += padding
        self.rect.height += padding

        # draw
        self.rect.center = center

    def drawRect(self, padding):
        """draw add button"""
        self.changeRect(padding)
        pygame.draw.rect(self.screen, self.lightBackground, self.rect)
        pygame.draw.rect(self.screen, self.borderColors, self.rect, width=5)
        self.changeRect(-padding)

    def draw(self):
        """Draw ImgScene"""
        self.drawRect(15)
        self.screen.blit(self.img, self.rect)
        self.screen.blit(self.exit, self.exitRect)


class AnimationMaker:
    """Animation Maker Class"""

    def __init__(self):
        """Initialize Animation Maker Class"""
        # define screen, width and height
        self.width = ctypes.windll.user32.GetSystemMetrics(0)
        self.height = ctypes.windll.user32.GetSystemMetrics(1)
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        pygame.display.set_caption("Animation Maker")

        # clock of game and FPS
        self.FPS = 60
        self.clock = pygame.time.Clock()

        # colors
        self.background = (45, 45, 45)
        self.borderColors = (60, 60, 60)
        self.lightBackground = (50, 50, 50)

        # running state of application
        self.running = True

        # rects and imgs
        self.animationRect = pygame.Rect((10, 10), (self.width-20, int(self.height/100*65)))
        self.imgListRect = pygame.Rect((10, self.animationRect.bottom+20), (self.width-20, self.height-self.animationRect.bottom-30))

        # add button for add img and add rect
        self.addImg = pygame.image.load("IMG\\Add.png").convert_alpha()
        self.addRect = self.addImg.get_rect(topright=(self.animationRect.right-20, self.animationRect.top+20))

        # save button for save img and save rect
        self.saveImg = pygame.image.load("IMG\\Save.png").convert_alpha()
        self.saveRect = self.saveImg.get_rect(topright=(self.addRect.left-25, self.addRect.top))

        # settings button for settings img and settings rect
        self.settingsImg = pygame.image.load("IMG\\Settings.png").convert_alpha()
        self.settingsRect = self.settingsImg.get_rect(topright=(self.saveRect.left-25, self.addRect.top))

        # run button for run img and run rect
        self.runImg = pygame.image.load("IMG\\Run.png").convert_alpha()
        self.runRect = self.runImg.get_rect(topright=(self.settingsRect.left-25, self.addRect.top))

        # open button for open img and open rect
        self.openImg = pygame.image.load("IMG\\Open.png").convert_alpha()
        self.openRect = self.openImg.get_rect(topright=(self.runRect.left-15, self.addRect.top-8))

        # dict of imgs
        self.imgDicts = {"open": self.openImg, "settings": self.settingsImg, "save": self.saveImg, "add": self.addImg, "run": self.runImg}
        self.rectDicts = {"open": self.openRect, "settings": self.settingsRect, "save": self.saveRect, "add": self.addRect, "run": self.runRect}
        self.commandDicts = {"open": self.openCommand, "settings": self.settingsCommand, "save": self.saveCommand, "add": self.addCommand, "run": self.runCommand}

        self.imgKeyList = ["open", "settings", "save", "add", "run"]

        # list of img scene
        self.imgScenesY = self.imgListRect.top+int(self.imgListRect.height/2)
        self.imgScenesMaxHeight = self.imgListRect.height-50
        self.imgScenes = []

        # settings screen
        self.settingsScene = SettingsScene(self.screen, self.openRect.left, self.addRect.right+8, self.addRect.bottom+15, self.animationRect.bottom-15)
        self.settingsSceneShow = False

        self.separator = pygame.Rect((self.openRect.left - 20, self.openRect.top), (10, self.openRect.left - 25 - self.animationRect.bottom))

        # seen rect
        self.chosenImg = None
        self.chosenRect = None

        # showing vars
        self.increase = 0.1
        self.delay = 0.1
        self.number = 0
        self.index = 0

        # showing
        self.show = False
        self.imgList = []


        # data
        self.widthOfImg = self.separator.left - self.animationRect.left
        self.heightOfImg = self.separator.top - self.animationRect.top
        self.centerOfImg = (self.animationRect.left + int(self.widthOfImg / 2), self.separator.top + int(self.separator.height / 2))


        self.gifImgs = []
        self.path = ""
        self.saveGif = False

        self.alpha = 200

    def checkHover(self):
        """
            check hover affect of the buttons
            name = open, settings, add, save
        """

        x, y = pygame.mouse.get_pos()
        for key in self.imgKeyList:

            # set img and rect
            img = self.imgDicts[key]
            rect = self.rectDicts[key]

            # set alpha value
            if rect.left <= x <= rect.right and rect.top <= y <= rect.bottom:
                img.set_alpha(self.alpha)
                self.setColor(key, 80, img)

            else:
                img.set_alpha(255)
                self.setColor(key, 60, img)

    def checkPresses(self):
        """CheckPress"""
        x, y = pygame.mouse.get_pos()
        for key in self.imgKeyList:

            # set rect
            rect = self.rectDicts[key]

            # set alpha value
            if rect.left <= x <= rect.right and rect.top <= y <= rect.bottom:
                self.commandDicts[key]()

    def openCommand(self):
        """Open"""
        try:
            tkinter.Tk().withdraw()
            path = tkinter.filedialog.askopenfilename(initialdir="C:\\Users\\%USERNAME%\\Desktop",
                                                      title="Select A File",
                                                      filetypes=[
                                                          ("AnimationData", ".animData"),
                                                      ])
            file = open(path, "r", encoding="utf8")
            lines = file.readlines()

            # remove lines
            for i in range(len(lines)): lines[i] = lines[i].replace("\n", "")

            self.imgScenes.clear()
            self.delay = self.settingsScene.delay = float(lines[0])
            for i in range(1, len(lines)):
                path = lines[i]
                try:
                    if path != "":
                        x = self.imgScenes[-1].rect.right + 25
                        self.imgScenes.append(
                            ImgScene(self.screen, path, self.imgScenesMaxHeight, x, self.imgScenesY))
                except IndexError:
                    self.imgScenes.append(ImgScene(self.screen, path, self.imgScenesMaxHeight, self.imgListRect.left + 25, self.imgScenesY))
        except :
            pass

    def settingsCommand(self):
        """Settings"""
        self.settingsSceneShow = not self.settingsSceneShow

    def saveCommand(self):
        """Save"""
        tkinter.Tk().withdraw()
        path = tkinter.filedialog.asksaveasfilename(initialdir="C:\\Users\\%USERNAME%\\Desktop", title="Select A File",
                                                    filetypes=[
                                                        ("AnimationData", ".animData"),
                                                        ("GIF", ".gif")
                                                    ])
        # if ".animData" in path:
        path.replace(".animData", "")
        os.mkdir(path)  # create folder
        self.path = path + "\\animation.gif"
        dataPath = path + "\\AnimationData.animData"

        # create file
        file = open(dataPath, "w")
        file.write(f"{self.settingsScene.delay}\n")

        # create
        for i in range(len(self.imgScenes)):
            file.write(self.imgScenes[i].imgPath)
        file.close()
        self.saveGif = True


    def runCommand(self):
        """Run"""
        self.gifImgs.clear()
        self.delay = self.settingsScene.delay
        self.show = not self.show

        if self.show is True: self.runImg = pygame.image.load("IMG\\Stop.png")
        else: self.runImg = pygame.image.load("IMG\\Run.png")

        # append
        self.imgList.clear()
        for scene in self.imgScenes:
            ratio = scene.relImg.get_width() / scene.relImg.get_height()
            img = pygame.transform.scale(scene.relImg, (int(ratio * self.separator.height - 20), self.separator.height - 20))
            rect = img.get_rect(center=self.centerOfImg)
            self.imgList.append((img, rect))

    def addCommand(self):
        """add"""
        tkinter.Tk().withdraw()
        path = tkinter.filedialog.askopenfile(initialdir="C:\\Users\\%USERNAME%\\Desktop", title="Select A File",
                                              filetypes=[
                                                    ("Png file", ".png"),
                                                    ("JPG file", ".jpg"),
                                                    ("Jpeg file", ".jpeg"),
                                              ])
        try:
            if path.name != "":
                x = self.imgScenes[-1].rect.right + 25
                self.imgScenes.append(ImgScene(self.screen, path.name, self.imgScenesMaxHeight, x, self.imgScenesY))
        except IndexError:
            self.imgScenes.append(ImgScene(self.screen, path.name, self.imgScenesMaxHeight, self.imgListRect.left + 25, self.imgScenesY))

    @staticmethod
    def setColor(key, color, img):
        """Set color of imgs"""
        if key != "open":
            w, h = img.get_size()
            for x in range(w):
                for y in range(h):
                    a = img.get_at((x, y))[3]
                    img.set_at((x, y), pygame.Color(color, color, color, a))

    def scrollImgScenes(self):
        """Scroll All the Elements that is inside of ImgScene"""
        x, y = pygame.mouse.get_pos()

        try:
            if self.imgListRect.left <= x <= self.imgListRect.right and self.imgListRect.top <= y <= self.imgListRect.bottom:
                keys = pygame.key.get_pressed()
                num = 0
                if keys[pygame.K_LEFT] and self.imgScenes[-1].rect.right > self.imgListRect.right-15: num = -3
                if keys[pygame.K_RIGHT] and self.imgScenes[-1].rect.left < 15: num = 3
                for scene in self.imgScenes:
                    scene.rect.x += num
                    scene.exitRect.x += num
        except:
            pass

    def event(self):
        """Event function of app"""

        for event in pygame.event.get():
            # main event loop
            keys = pygame.key.get_pressed()  # get keys

            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                # quit from app
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.checkPresses()
                self.settingsScene.decreaseIncrease()

                # check setting imgs
                for scene in self.imgScenes:
                    if scene.checkClick() is True:
                        self.settingsScene.setImg(scene.img)

                        # set img and rect
                        self.chosenImg = scene.relImg
                        ratio = self.chosenImg.get_width()/self.chosenImg.get_height()
                        self.chosenImg = pygame.transform.scale(self.chosenImg, (int(ratio*self.separator.height-20), self.separator.height-20))
                        self.chosenRect = self.chosenImg.get_rect(center=self.centerOfImg)
                        break

                # delete scene
                for index, scene in enumerate(self.imgScenes):
                    if scene.checkExit() is True:
                        self.imgScenes.pop(index)

                        # reset imgScenes
                        try:
                            x = self.imgListRect.left + 25
                            self.imgScenes[0].rect.x = x
                            self.imgScenes[0].exitRect.right = self.imgScenes[0].rect.right

                            for i in range(1, len(self.imgScenes)):
                                x = self.imgScenes[i - 1].rect.right + 25
                                self.imgScenes[i].rect.x = x
                                self.imgScenes[i].exitRect.right = self.imgScenes[i].rect.right
                        except IndexError:
                            pass
                        break

    def main(self):
        """Main Function of app"""

        while self.running:
            # main loop of game
            self.clock.tick(self.FPS)

            self.event()
            self.draw()

    # Rect button functions
    def changeRect(self, padding, rect):
        """change draw button"""
        # copy rect
        center = rect.center

        # change size
        rect.width += padding
        rect.height += padding

        # draw
        rect.center = center


    def drawButton(self, padding, rect):
        """draw add button"""
        self.changeRect(padding, rect)
        pygame.draw.rect(self.screen, self.lightBackground, rect)
        pygame.draw.rect(self.screen, self.borderColors, rect, width=5)
        self.changeRect(-padding, rect)
    # endregion

    def drawShow(self):
        """Draw show"""
        # show animation
        try:
            if self.show is False: self.screen.blit(self.chosenImg, self.chosenRect)
        except TypeError:
            pass


    def drawImgScenes(self):
        """Draw Img Scenes"""
        for img in self.imgScenes:
            img.draw()

    def setAnimation(self):
        """Set animations"""
        # show settings scene
        if self.settingsSceneShow is True:
            self.settingsScene.draw()

        if self.show is True:
            img, rect = self.imgList[self.index]
            self.screen.blit(img, rect)
            if self.saveGif is True:
                self.gifImgs.append(imageio.imread(self.imgScenes[self.index].imgPath))

            # set number and index
            if self.number == self.delay:
                self.number = 0
                self.index += 1

            self.number += self.increase

            # check index
            if self.index == len(self.imgList):
                self.index = 0
                if self.saveGif is True:
                    imageio.mimsave(self.path, self.gifImgs)
                self.saveGif = False

    def draw(self):
        """Main draw function of app"""
        self.screen.fill(self.background)

        # set alpha
        self.checkHover()

        # draw rectangles
        pygame.draw.rect(self.screen, self.borderColors, self.animationRect, width=10)
        pygame.draw.rect(self.screen, self.borderColors, self.imgListRect, width=10)
        pygame.draw.rect(self.screen, self.borderColors, self.separator)

        # draw buttons border
        self.drawButton(15, self.addRect)
        self.drawButton(15, self.saveRect)
        self.drawButton(15, self.settingsRect)
        self.drawButton(15, self.runRect)

        # draw buttons img
        self.screen.blit(self.addImg, self.addRect)
        self.screen.blit(self.openImg, self.openRect)
        self.screen.blit(self.saveImg, self.saveRect)
        self.screen.blit(self.settingsImg, self.settingsRect)
        self.screen.blit(self.runImg, self.runRect)

        if self.settingsSceneShow is True:
            self.settingsScene.draw()

        self.scrollImgScenes()
        self.drawImgScenes()
        self.setAnimation()


        pygame.display.flip()



if __name__ == '__main__':
    AnimationMaker().main()
