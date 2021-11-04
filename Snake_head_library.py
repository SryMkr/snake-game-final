'''
    author SryMkr
    date:2021.3.15
    this library is for snake head
'''


# import package
import pygame
from pygame.locals import *


class MySprite_head(pygame.sprite.Sprite):
    # initialize some parameters
    def __init__(self):
        # extend pygame.sprite.Sprite
        pygame.sprite.Sprite.__init__(self)
        # main picture consists of neat frames
        self.multi_frames = None
        # the number of current frame
        self.current_frame = 0
        # the number of first frame
        self.first_frame = 0
        # the number of last frame
        self.last_frame = 1
        # the width of one frame
        self.one_frame_width =1
        # the height of one frame
        self.one_frame_height = 1
        # the columns of main picture
        self.multi_frames_columns = 1
        # for record last change time
        self.last_time = 0
        # control the direction of head
        self.head_direction = 0
    # get x_coordinate of one frame
    def _get_x_coordinate(self):
        return self.rect.x
    # set x_coordinate of one frame
    def _set_x_coordinate(self,value):
        self.rect.x = value

    x_coordinate = property(_get_x_coordinate,_set_x_coordinate)

    # get y_coordinate of one frame
    def _get_y_coordinate(self):
        return self.rect.y

    # set y_coordinate of one frame
    def _set_y_coordinate(self, value):
        self.rect.y = value

    y_coordinate = property(_get_y_coordinate, _set_y_coordinate)

    # load frame parameters
    def load_head_frames(self, multi_frames_filepath, one_frame_width, one_frame_height, multi_frames_columns):
        # load main picture
        self.multi_frames = pygame.image.load(multi_frames_filepath).convert_alpha()
        # load frame width
        self.one_frame_width = one_frame_width
        # load frame height
        self.one_frame_height = one_frame_height
        # Create frame Rect(left, top, width, height) the position
        self.rect = Rect(0, 0, one_frame_width, one_frame_height)
        # frame's columns
        self.multi_frames_columns = multi_frames_columns

    # snake head action
    def head_update(self, current_time, change_rate=30):
        if current_time > self.last_time + change_rate:
            # frame loop
            if self.current_frame > self.last_frame:
                self.current_frame = self.first_frame
            print(self.current_frame, self.first_frame, self.last_frame)
            # record time
            self.last_time = current_time
            # the x coordinate of current frame
            frame_x = (self.current_frame % self.multi_frames_columns) * self.one_frame_width
            # the y coordinate of current frame
            frame_y = (self.current_frame // self.multi_frames_columns) * self.one_frame_height
            # locate target range
            rect = Rect(frame_x, frame_y, self.one_frame_width, self.one_frame_height)
            # get target frame   return surface
            self.image = self.multi_frames.subsurface(rect)
            # change to next frame
            self.current_frame += 1

# define the snake head direction
def snake_head_direction(snake, snake_direction):
    # up
    if snake_direction.second_variate < 0:
        snake.snake_head.first_frame = 1 * snake.snake_head.multi_frames_columns
        snake.snake_head.last_frame = snake.snake_head.first_frame + 1
    #down
    elif snake_direction.second_variate > 0:
        snake.snake_head.first_frame = 3 * snake.snake_head.multi_frames_columns
        snake.snake_head.last_frame = snake.snake_head.first_frame + 1
    #lift
    elif snake_direction.first_variate < 0:
        snake.snake_head.first_frame = 0 * snake.snake_head.multi_frames_columns
        snake.snake_head.last_frame = snake.snake_head.first_frame + 1
    # right
    elif snake_direction.first_variate > 0:
        snake.snake_head.first_frame = 2 * snake.snake_head.multi_frames_columns
        snake.snake_head.last_frame = snake.snake_head.first_frame + 1
    # 其实大小方向都变了，只不过小于在这边，大于在update里面变了
    if snake.snake_head.current_frame < snake.snake_head.first_frame:
        snake.snake_head.current_frame = snake.snake_head.first_frame