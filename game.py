import utilities
import pygame
import pymunk
import object
import menu_builder


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
        self.taking_shot = False
        self.course_num = 0
        self.strokes = 0

    def change_course(self, course):
        self.course = course
        self.course_num += 1
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
        self.taking_shot = True

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
                               "scaled_arrow",
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
            self.course.render_course(self.screen)
            for i, object in enumerate(self.objects):
                if hasattr(object, "body"):
                    self.objects[i].update_position(object.body.position)
                if self.check_ball_in_hole():
                    self.ball.body.velocity = (0, 0)
                    self.taking_shot = False
                    display = menu_builder.TextDisplay(200, 100, "You WIN!")
                    display.render(self.screen)
            for i in self.objects:
                if i.name == "putter":
                    i.update_position([(self.ball.position[0] - 5), (self.ball.position[1] + 30)])
            if int(self.ball.body.velocity[0]) != 0 or int(self.ball.body.velocity[1] != 0):
                self.taking_shot = False
            elif int(self.ball.body.velocity[0]) == 0 and int(self.ball.body.velocity[1] == 0) and not self.check_ball_in_hole():
                self.taking_shot = True
            for object in self.objects:
                if object.name == "putter":
                    if self.taking_shot == True:
                        object.render_object(self.screen)
                else:
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
            elif self.playstate == utilities.PlayState.COURSE and self.taking_shot == True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    impulse = self.putter.get_angle(self.putter.force)
                    self.ball.body.apply_impulse_at_local_point((impulse[0], impulse[1]), (0, 0))
                    self.strokes += 1
                    print(self.strokes)
                mouse_pos = pygame.mouse.get_pos()
                self.putter.update(mouse_pos)
