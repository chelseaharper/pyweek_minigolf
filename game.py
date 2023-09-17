import utilities
import pygame
import pymunk
import objects


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
        self.bodies = None

    def change_course(self, course):
        self.course = course
        self.space = pymunk.Space()
        for y, row in enumerate(course.tiles):
            for x, tile in enumerate(row):
                if tile == utilities.COURSE_TILE_OFFCOURSE:
                    ground = pymunk.Poly(
                        self.space.static_body,
                        [
                            (x * utilities.SCALE, y * utilities.SCALE),
                            ((x + 1) * utilities.SCALE, y * utilities.SCALE),
                            ((x + 1) * utilities.SCALE, (y + 1) * utilities.SCALE),
                            (x * utilities.SCALE, (y + 1) * utilities.SCALE),
                        ],
                    )
                    ground.elasticity = 0.9
                    self.space.add(ground)

        self.ball = objects.Object(
            self.course.start[0],
            self.course.start[1],
            utilities.SCALE,
            utilities.SCALE,
            "ball",
        )
        self.objects = []
        self.bodies = []
        for obj in [self.ball] + self.course.objects:
            self.objects.append(obj)

            mass = 1
            radius = utilities.SCALE / 2
            moment = pymunk.moment_for_circle(
                mass=mass, inner_radius=0, outer_radius=radius
            )
            body = pymunk.Body(mass, moment)
            body.position = (
                obj.position[0] + utilities.SCALE / 2,
                obj.position[1] + utilities.SCALE / 2,
            )
            shape = pymunk.Circle(body, radius)
            shape.elasticity = 0.9
            self.space.add(body, shape)
            self.bodies.append(body)

    def update(self, dt):
        self.handle_events()  # accepts input from keyboard or mouse

        self.screen.fill(utilities.BLACK)

        if self.course is not None:
            self.space.step(dt)
            for i, body in enumerate(self.bodies):
                self.objects[i].update_position(
                    (
                        body.position[0] - utilities.SCALE / 2,
                        body.position[1] - utilities.SCALE / 2,
                    )
                )
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
                    self.bodies[0].apply_force_at_local_point((0, -4000), (0, 0))
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    print("DOWN")
                    self.bodies[0].apply_force_at_local_point((0, 4000), (0, 0))
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    print("LEFT")
                    self.bodies[0].apply_force_at_local_point((-4000, 0), (0, 0))
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    print("RIGHT")
                    self.bodies[0].apply_force_at_local_point((4000, 0), (0, 0))
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
