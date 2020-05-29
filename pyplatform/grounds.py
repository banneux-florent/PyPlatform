import pygamefrom pyplatform import miscellaneousground_types = {    1: {        "friction": 0.12,        "restitution": 0.2,        "color": "4e4763"    },    2: {        "friction": 1,        "restitution": 0.2,        "color": "464341"    },    3: {        "friction": 0.015,        "restitution": 0.2,        "color": "8ABCCD"    },    4: {        "friction": 0.12,        "restitution": 1.15,        "color": "7A318D"    },    5: {        "friction": 0.12,        "restitution": 15,        "color": "E08427"    }}class Grounds:    def __init__(self):        self.ground_list = []    def add_ground(self, rect, ground_type):        new_ground = Ground(rect, ground_type)        self.ground_list.append(new_ground)    def add_ground_g(self, new_ground):        if isinstance(new_ground, Ground):            self.ground_list.append(new_ground)    def show(self, screen):        for ground in self.ground_list:            ground.draw_sprite(screen)class Ground:    def __init__(self, rect, ground_type):        self.type = GroundType(ground_type)        self.rect = pygame.Rect(rect)    def draw_sprite(self, screen):        pygame.draw.rect(screen, miscellaneous.hex_to_list(self.type.color), self.rect)    def switch_ground_type_to(self, ground_type):        self.type.switch_to(ground_type)class GroundType:    def __init__(self, ground_type):        self.type = 0        self.friction = 0        self.restitution = 0        self.color = "000000"        self.switch_to(ground_type)    def switch_to(self, ground_type):        if ground_type in ground_types:            self.type = ground_type            self.friction = ground_types[self.type]["friction"]            self.restitution = ground_types[self.type]["restitution"]            self.color = ground_types[self.type]["color"]        else:            print("Ce type de sol n'existe pas !")