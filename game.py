import utilities
import pygame
import pymunk
import object
import math


class Game:
    def __init__(self, screen, courses, menu):
        self.screen = screen
        self.objects = []
        self.playstate = utilities.PlayState.MENU
        self.courses = courses
        self.course = None
        self.menu = menu
        self.gamestate = utilities.GameState.NONE
        self.ball = None
        self.space = None
        self.putter = None

    def change_course(self, course):
        self.course = course
        self.space = pymunk.Space()
        ground = self.space.static_body
        for y, row in enumerate(course.tiles):
            for x, tile in enumerate(row):
                if tile == utilities.COURSE_TILE_OFFCOURSE:
                    # Renamed the former "ground" object to "wall" so I could use "ground" to describe the body creating friction
                    wall = pymunk.Poly(
                        self.space.static_body,
                        [
                            (x * utilities.SCALE, y * utilities.SCALE),
                            ((x + 1) * utilities.SCALE, y * utilities.SCALE),
                            ((x + 1) * utilities.SCALE, (y + 1) * utilities.SCALE),
                            (x * utilities.SCALE, (y + 1) * utilities.SCALE),
                        ],
                    )
                    wall.elasticity = 0.9
                    self.space.add(wall)

        self.ball = object.Object(
            self.course.start[0] + 0.2,
            self.course.start[1] + 0.2,
            utilities.SCALE * 0.6,
            utilities.SCALE * 0.6,
            "ball",
        )
        self.objects = []
        for obj in [self.course.hole] + [self.ball] + self.course.objects:
            self.objects.append(obj)
            if obj.needsbody == True:
                pivot = pymunk.PivotJoint(ground, obj.body, (0, 0), (0, 0))
                pivot.max_bias = 0 # disable joint correction
                pivot.max_force = 500 # Emulate linear friction
                self.space.add(obj.body, obj.shape, pivot)
        self.putter = self.create_putter()
        self.objects.append(self.putter)
    
    def create_putter(self):
        putter = object.Putter((self.ball.position[0] / utilities.SCALE),
                               (self.ball.position[1] / utilities.SCALE),
                               utilities.SCALE,
                               utilities.SCALE,
                               "arrow",
                               name="putter",
                               needsbody=False
                               )
        return putter

    def check_ball_in_hole(self):
        hole_radius = 0.5
        ball_x_distance = abs((self.ball.position[0] / utilities.SCALE) - (self.course.hole_location[0] + 0.5))
        ball_y_distance = abs((self.ball.position[1] / utilities.SCALE) - (self.course.hole_location[1] + 0.5))
        ball_dist = (ball_x_distance ** 2) + (ball_y_distance ** 2)
        if ball_dist <= (hole_radius ** 2):
            return True

    def update(self, dt):
        self.handle_events()  # accepts input from keyboard or mouse

        self.screen.fill(utilities.BLACK)

        if self.course is not None:
            self.space.step(dt)
            for i, object in enumerate(self.objects):
                if hasattr(object, "body"):
                    self.objects[i].update_position(object.body.position)
                if self.check_ball_in_hole():
                    self.ball.body.velocity = (0, 0)
            for i in self.objects:
                if i.name == "putter":
                    i.update_position([(self.ball.position[0] - 5), (self.ball.position[1] + 30)])
            self.course.render_course(self.screen)
            for object in self.objects:
                object.render_object(self.screen)

        if self.playstate == utilities.PlayState.MENU:
            self.menu.render_menu(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                utilities.end_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playstate = utilities.PlayState.MENU
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    print("UP")
                    self.ball.body.apply_impulse_at_local_point((0, -400), (0, 0))
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    print("DOWN")
                    self.ball.body.apply_impulse_at_local_point((0, 400), (0, 0))
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    print("LEFT")
                    self.ball.body.apply_impulse_at_local_point((-400, 0), (0, 0))
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    print("RIGHT")
                    self.ball.body.apply_impulse_at_local_point((400, 0), (0, 0))
            if self.playstate == utilities.PlayState.MENU:
                for i in self.menu.buttons:
                    if i.handle_events():
                        if i.name == "Quit Game":
                            utilities.end_game()
                        if i.name == "Play Game":
                            if self.course is None:
                                self.change_course(self.courses[0])
                            self.playstate = utilities.PlayState.COURSE
                            self.gamestate = utilities.GameState.RUNNING
            elif self.playstate == utilities.PlayState.COURSE:
                mouse_pos = pygame.mouse.get_pos()
                self.putter.update(mouse_pos)
