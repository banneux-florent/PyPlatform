import pygamefrom pygame import gfxdrawfrom pyplatform import miscellaneous, physics, mapsclass Player:    properties = {        "width": 20,        "height": 20,        "color": "FF0000"    }    def __init__(self):        self.id = ""        self.x = 0        self.y = 0        self.color = Player.properties["color"]        self.room_name = ""        self.can_jump = False        self.can_spawn = True        self.is_spawned = False        self.on_the_ground = False        self.collision_state = False        self.collision_ground = None        self.sprite = None    def __str__(self):        return str(self.id) + "\x1F" + str(self.x) + "\x1F" + str(self.y) + "\x1F" + str(self.color) + "\x1F" + str(self.is_spawned)    def draw_sprite(self, screen):        self.sprite = gfxdraw.rectangle(screen, (self.x, self.y, Player.properties["width"], Player.properties["height"]), miscellaneous.hex_to_list(self.color))    def get_id_and_room_name(self):        id = "'" + str(self.id) + "'"        if self.id == "":            id = "None"        room_name = "'" + self.room_name + "'"        if self.room_name == "":            room_name = "None"        return id + " ~ " + room_nameclass PhysicPlayer(Player):    def __init__(self):        super().__init__()        self.w = Player.properties["width"]        self.h = Player.properties["height"]        self.vx = 0        self.vy = 0        self.px = 0        self.py = 0        self.pvx = 0        self.pvy = 0        self.rectangle = None    def apply_physic(self, pressed):        if self.is_spawned:            if self.can_jump:                if pressed[pygame.K_UP]:  # Jump                    self.can_jump = False                    self.on_the_ground = False                    self.vy = -physics.Physics.jump_velocity                if self.on_the_ground:                    # Accélération                    if pressed[pygame.K_RIGHT]:                        self.vx += physics.Physics.dtf * (physics.Physics.move_speed["ground"] * pow(self.collision_ground.type.friction, 1 / 3))                    if pressed[pygame.K_LEFT]:                        self.vx -= physics.Physics.dtf * (physics.Physics.move_speed["ground"] * pow(self.collision_ground.type.friction, 1 / 3))                    if self.vx != 0:  # Friction slow-down                        self.vx /= 1 + self.collision_ground.type.friction                else:                    # Acceleration                    if pressed[pygame.K_RIGHT]:                        self.vx += physics.Physics.dtf * physics.Physics.move_speed["air"]                    if pressed[pygame.K_LEFT]:                        self.vx -= physics.Physics.dtf * physics.Physics.move_speed["air"]                    if self.vx != 0:  # Friction slow-down                        self.vx /= physics.Physics.air_deceleration            else:                # Acceleration                if pressed[pygame.K_RIGHT]:                    self.vx += physics.Physics.dtf * physics.Physics.move_speed["air"]                if pressed[pygame.K_LEFT]:                    self.vx -= physics.Physics.dtf * physics.Physics.move_speed["air"]                if self.vx != 0:  # Friction slow-down                    self.vx /= physics.Physics.air_deceleration            if abs(self.vx) > physics.Physics.max_speed * physics.Physics.dtf:                self.vx = (abs(self.vx) / self.vx) * physics.Physics.max_speed * physics.Physics.dtf            elif self.vx != 0 and self.on_the_ground and abs(self.vx) < 0.02:                self.vx = 0            # if self.vx != 0 and self.on_the_ground and abs(self.vx) < 0.02:            #      self.vx = 0            self.vy += physics.Physics.dtf * physics.Physics.gravity    def update_position(self, game):        if self.is_spawned:            self.y += self.vy            self.x += self.vx            if self.y > game.size['h']: # If player is out of bound (too low)                self.despawn()                game.send_data("player-died")            else:                self.rectangle = pygame.Rect(self.x, self.y, self.w, self.h)    def save_past_position(self):        self.px, self.py, self.pvx, self.pvy = self.x, self.y, self.vx, self.vy    def check_holes_collision(self, game):        if self.is_spawned:            if game.current_map.checkpointsLeft == 0:                for hole in game.current_map.holes:                    if self.rectangle.colliderect(hole.rect):  # If there is collision                        game.send_data("player-entered-hole")    def check_checkpoints_collision(self, game):        if self.is_spawned:            if game.current_map.checkpointsLeft > 0:                for checkpoint in game.current_map.checkpoints:                    if not checkpoint.state:                        if self.rectangle.colliderect(checkpoint.rect):  # If there is collision                            game.current_map.checkpointsLeft -= 1                            checkpoint.state = True    def respawn(self, current_map):        print("________________ RESPAWN _______________ " + str(self.can_spawn))        if self.can_spawn:            self.x = current_map.spawn['x'] - (self.w / 2) + (maps.Spawn.properties["width"] / 2)            self.y = current_map.spawn['y'] - (self.h / 2) + (maps.Spawn.properties["height"] / 2)            self.vx = 0            self.vy = 0            self.px = self.x            self.py = self.y            self.pvx = 0            self.pvy = 0            self.can_jump = True            self.is_spawned = True            self.on_the_ground = False            self.collision_state = False            self.collision_ground = None    def despawn(self):        self.x = 0        self.y = 0        self.vx = 0        self.vy = 0        self.px = 0        self.py = 0        self.pvx = 0        self.pvy = 0        self.can_jump = False        self.is_spawned = False        self.on_the_ground = False        self.collision_state = False        self.collision_ground = None        self.rectangle = None    def toggle_can_spawn(self):        if self.can_spawn:            self.despawn()            self.can_spawn = False        else:            self.can_spawn = True