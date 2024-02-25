import pygame

class Fighter():
    def __init__(self, player, x, y, data, sprite_sheet, animation_steps): # add flip variable? and change False to  to flip
        self.size = data[0]
        self.image_scale = data [1]
        self.offset = data [2]
        self.player = player
        self.flip = False
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 # 0 = idle, etc.
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()   # or not?
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True
        self.shoot = 0
        self.duck = False

    def load_images(self, sprite_sheet, animation_steps):
        # continue
        # extract images from sprite_sheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # get key presses
        key = pygame.key.get_pressed()

        # Can only perform other actions if not attacking ## or dead
        if self.health <= 0:   
            self.health = 0   
            self.alive = False   
            # self.update_action(6)

        if not self.attacking and self.alive and not round_over and self.shoot <= 8:
            #check player 1 controls
            if self.player == 1:
                if key[pygame.K_a]:          # movement
                    dx = -SPEED
                    self.running =  True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running =  True
                if key[pygame.K_w] and not self.jump:              # jump
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_s] and not self.jump:
                    self.duck = True
                # attack
                if key[pygame.K_r] or key[pygame.K_t] or key[pygame.K_f] or key[pygame.K_g] or key[pygame.K_SPACE]:
                    if self.attack_cooldown == 0:
                        self.attacking = True
                        if key[pygame.K_r] or key[pygame.K_t]:          # determine which attack type
                            self.high_attack(surface, target)
                            if key[pygame.K_r]:
                                self.attack_type = 1
                            if key[pygame.K_t]:
                                self.attack_type = 2
                        if key[pygame.K_f] or key[pygame.K_g]:
                            self.low_attack(surface, target)
                            if key[pygame.K_f]:
                                self.attack_type = 3
                            if key[pygame.K_g]:
                                self.attack_type = 4
                        if key[pygame.K_SPACE]:
                            self.shooting_attack(surface, target)
                            self.shoot += 1
                            self.attack_type = 5
                            if self.shoot >= 8:
                                self.attack_cooldown = 50
                                self.shoot = 0
                self.attacking = False
                if not key[pygame.K_s]:
                    self.duck = False

                # player 2
            elif self.player == 2:
                if key[pygame.K_LEFT]:                 # movement
                    dx = -SPEED
                    self.running =  True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running =  True
                if key[pygame.K_UP] and not self.jump:     # jump
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_DOWN] and not self.jump:
                    self.duck = True
                # attack
                if key[pygame.K_KP4] or key[pygame.K_KP5] or key[pygame.K_KP1] or key[pygame.K_KP2] or key[pygame.K_KP0]:
                    if self.attack_cooldown == 0:
                        self.attacking = True
                        if key[pygame.K_KP4] or key[pygame.K_KP5]:
                            self.high_attack(surface, target)
                            if key[pygame.K_KP4]:
                                self.attack_type = 1
                            if key[pygame.K_KP5]:
                                self.attack_type = 2
                        if key[pygame.K_KP1] or key[pygame.K_KP2]:
                            self.low_attack(surface, target)
                            if key[pygame.K_KP1]:
                                self.attack_type = 3
                            if key[pygame.K_KP2]:
                                self.attack_type = 4
                        if key[pygame.K_KP0]:
                            self.shooting_attack(surface, target)
                            self.shoot += 1
                            self.attack_type = 5
                            if self.shoot >= 8:
                                self.attack_cooldown = 50
                                self.shoot = 0
                self.attacking = False
                if not key[pygame.K_DOWN]:
                    self.duck = False

        # physics
        # apply gravity
        self.vel_y +=  GRAVITY
        dy += self.vel_y
        # ensure player stays on screen
        if self.rect.left + dx <0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom
        #ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
        #apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        # update player position
        self.rect.x += dx
        self.rect.y += dy

        if self.player == 1:
            if not key[pygame.K_a] and not key[pygame.K_d]:
                    self.running = False # reset self.running
        if self.player == 2:
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                    self.running = False # reset self.running

    # handle animation updates
    def update(self):
        animation_cooldown =  100
        self.image = self.animation_list[self.action][self.frame_index]
        # check what action the player is performing
        if self.hit:
            self.update_action(2) # getting hit
        elif self.duck:
            self.update_action(3)
            """Signifcant number of animations to implement still."""
        # elif self.attacking:
            # if self.attack_type == 1:
                # self.update_action(3) # 3:attack 1
            # elif self.attack_type == 2:
                # self.update_action(4) # 4:attack 2
            # elif self.attack_type == 3:
                # self.update_action(5) # 5:attack 3
            # elif self.attack_type == 4:
                # self.update_action(6) # 6:attack 4
            # else:
                # self.update_action(7) # shoot attack
        # elif self.jump:
            # self.update_action(2) # 2:jump
        elif self.running:
            self.update_action(1) # 1:run
        else:
            self.update_action(0) # 0:idle

        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
    # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
        # if the player is dead then end the animation_list
            #  if self.alive ==  False:
                #self.frame_index = len(self.animation_list[self.action]) - 1
            # else:
            if not self.duck:
                self.frame_index = 0
                self.hit = False
            elif self.duck and not self.hit:
                self.frame_index = 4
            else:
                self.frame_index = 0
                self.hit = False
                # check if an attack was executed
                # if self.action == 3 or self.action ==4:
                    # self.attacking = False
                    # self.attack_cooldown = 20
                ## check if damage was taken
                # if self.action == 5:



    # create attack space
    def high_attack(self, surface, target):
            attacking_rect = pygame.Rect(self.rect.centerx - (1.5 * self.rect.width * self.flip), self.rect.y, 1.5 * self.rect.width, self.rect.height / 2)
            if attacking_rect.colliderect(target.rect) and not target.duck:
                target.health -= 10
                target.hit = True
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
            self.attack_cooldown = 20

    def low_attack(self, surface, target):
            attacking_rect = pygame.Rect(self.rect.centerx - (1.5 * self.rect.width * self.flip), self.rect.centery, 1.5 * self.rect.width, self.rect.height / 2)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
            self.attack_cooldown = 20

    def shooting_attack(self, surface, target):
            attacking_rect = pygame.Rect(self.rect.centerx - (0.5 * self.rect.width * self.flip) +  50 * self.shoot - (100 * self.shoot * self.flip), (self.rect.centery - 50), 0.5 * self.rect.width, self.rect.height / 4)
            if attacking_rect.colliderect(target.rect):
                target.health -= 5
                target.hit = True
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def update_action(self, new_action):
        # check if the new action is different to previous one
        if new_action != self.action:
            self.action = new_action
            # update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        # pygame.draw.rect(surface, (255, 255, 255), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
        # blit 
