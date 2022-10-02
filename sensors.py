# simulating sensor data

import pygame
import math
import numpy as np





# making sensor data noisy 
# by adding uncertainity using Gaussian distribution
# taking normal distance, angle at which an obstacle is detected
# then returning noisy data from obstacle using main data as mean and sigma or degree of uncertainity as variance
def add_uncertainity_to_sensor_data(distance, angle, sigma):
    mean = np.array([distance, angle])
    # getting variance in the form required for multivariate_normal function.
    variance = np.diag(sigma ** 2)
    
    # function to get random values from distribution using mean and variance
    distance, angle = np.random.multivariate_normal(mean, variance)

    return [distance, angle]






# Simulating a Laser sensor data
class Laser:
    # Light Range of Sensor, Map of environment, Uncertainity attached to sensor
    def __init__(self, Range, map, uncertainity):
        # Range of the LIDAR sensor
        self.Range = Range
        self.speed = 4 # rounds per second for sensor(LIDAR) rotation
        # User defined error or uncertainity to add in sensor data, to make it noisy.
        self.sigma = np.array([uncertainity[0],uncertainity[1]]) #Error in sensor data
        # position of robot
        self.position = (0,0)
        # taking map as input
        self.map = map

        self.w, self.h = pygame.display.get_surface().get_size()
        # storing sensed obstacles
        self.sensedObstacles = []


    # Euclidean distance between robot and obstacle
    def disance(self, obstaclePosition):
        px = (obstaclePosition[0]-self.position[0])**2  
        py = (obstaclePosition[1]-self.position[1])**2
        return math.sqrt(px+py)

    
    # sensing obstacles based on black color in range of lidar(i.e, given range)
    def sense_obstacle(self):
        data = []
        
        # coordinates of robot position
        x1, y1 = self.position[0], self.position[1]

        # we are gonna determine the obsatacle by checking in 360 degree from robot under the range of lidar, if there
        # exist an obstacle it will have black color in such way we can simulate obstacles such that we are detecting it
        # from lidar.
        # x2 ,y2 -> coordinates of line end
        # we are gonna search for black color i.e, wall by searching in 360 degree around robot within position of robot and line end coordinates.
        # using linspace we can decide frequency of lidar (to not include 360 again, endpoint is set to False)
        for angle in np.linspace(0, 2*math.pi, 60, False):
            # determinig range line end using Range and angle of Lidar
            x2 = (x1 + self.Range * math.cos(angle))
            y2 = (y1 + self.Range * math.sin(angle))

            # Now we are gonna divide line into 100 parts and check whether there is black color in any part on line
            # interpolation loop
            for part in range(100):
                # interpolation formula to calculate coordinates of point on the line
                u = part/100
                x = int(x2 * u + x1 * (1-u))
                y = int(y2 * u + y1 * (1-u))

                # if calculated point within window (for edge cases)
                if 0 < x < self.w and 0 < y < self.h:
                    # pygame function to get the color at given position on surface
                    color = self.map.get_at((x,y))
                    print(color)
                    if (color[0], color[1], color[2] == (0,0,0)): #if color is black
                        distance_from_robot = self.disance((x,y))
                        output = add_uncertainity_to_sensor_data(distance_from_robot, angle, self.sigma)
                        # appending position of robot to output
                        output.append(self.position)
                        # store measurement to data
                        data.append(output)
                        break

        if len(data)>0:
            return data
        else:
            return False







if __name__=='__main__':
    # sigma = np.array([2,1])
    # add_uncertainity_to_sensor_data(10, 30, sigma)
    pass