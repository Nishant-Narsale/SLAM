import math
import pygame


class buildEnvironment:
    def __init__( self,MapDimensions ):
        pygame.init()
        self.pointCloud = []
        self.mapImage = pygame.image.load('image.png')
        self.mapHeight, self.mapWidth = MapDimensions
        self.mapWindowName = "RRT Path Planning"

        pygame.display.set_caption(self.mapWindowName)

        self.map = pygame.display.set_mode((self.mapWidth, self.mapHeight))
        self.map.blit(self.mapImage, (0,0))

        self.color_black = (0,0,0)
        self.color_grey = (70,70,70)
        self.color_blue = (0,0,255)
        self.color_green = (0,255,0)
        self.color_red = (255,0,0)
        self.color_white = (255,255,255)


    def angle_distance_to_position(self, distance, angle, robotPosition):
        x = distance * math.cos(angle) + robotPosition[0]
        y = -distance * math.sin(angle) + robotPosition[1]
        return [int(x),int(y)]

    def dataStorage(self,data):
        print(len(data))
        for element in data:
            point = self.angle_distance_to_position(element[0], element[1], element[2])
            if point not in self.pointCloud:
                self.pointCloud.append(point)

    def printMap(self):
        self.outputMap = self.map.copy()
        for point in self.pointCloud:
            self.outputMap.set_at( (int(point[0]), int(point[1])), (255,0,0))

            