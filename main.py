import env, sensors
import pygame

envi = env.buildEnvironment((600,1200))
envi.originalMap = envi.map.copy()
laser = sensors.Laser(200, envi.originalMap, uncertainity=[0.5,0.01])


# filling main map with black color and then drawing red dots over it using laser data
envi.map.fill((0,0,0))
envi.outputMap = envi.map.copy()



done = False

while not done:
    # this will be set True only if mouse cursor is inside the window
    # to prevent getting negative values
    isSensorOn = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if pygame.mouse.get_focused():
            isSensorOn = True
        elif not pygame.mouse.get_focused():
            isSensorOn = False
        

    if isSensorOn:
        # setting robot position to mouse position
        mousePosition = pygame.mouse.get_pos()
        laser.position = mousePosition

        # getting sensed obstacles in range
        sensor_data = laser.sense_obstacle()
        # print('sensor data : ' , sensor_data)
        # this will store point cloud data in envi.pointCloud
        envi.dataStorage(sensor_data)

        # drawing point cloud data to map
        envi.printMap()
    
    envi.map.blit(envi.outputMap, (0,0))
        

    pygame.display.update()