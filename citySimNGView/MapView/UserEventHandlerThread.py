import threading
import pygame
from Building import Building
from Consts import RED, LEFT, RIGHT, FPS, GREEN


class UserEventHandlerThread(threading.Thread):
    def __init__(self, map_view):
        threading.Thread.__init__(self)
        self.map_view = map_view

    def run(self):
        shadow = None
        building = None
        clock = pygame.time.Clock()
        while self.map_view.game_on:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    pos = pygame.mouse.get_pos()
                    if shadow is not None:
                        shadow.rect.center = pos
                        shadow.update()
                        self.map_view.place_building(building, (shadow.rect.left, shadow.rect.top))
                        shadow = None
                    else:
                        clicked_sprites = [s for s in self.map_view.buildings_panel_sprites if s.rect.collidepoint(pos)]
                        if len(clicked_sprites) == 1:
                            building = self.map_view.check_if_can_afford(clicked_sprites[0])
                            if self.map_view.can_afford_on_building:
                                shadow = Building(building.name, building.id, building.resources_cost,
                                                  building.texture, self.map_view.background.get_size(), pos)
                                shadow.image.fill(RED)
                        if self.map_view.left_arrow_buildings_panel.collidepoint(pos):
                            self.map_view.buildings_panel.scroll_building_panel_left()
                        if self.map_view.right_arrow_buildings_panel.collidepoint(pos):
                            self.map_view.buildings_panel.scroll_building_panel_right()
                        clicked_nav_arrows = [s for s in self.map_view.navigation_arrows_sprites if s.rect.collidepoint(pos)]
                        if len(clicked_nav_arrows) == 1:
                            self.map_view.switch_game_tile(clicked_nav_arrows[0])
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                    if shadow is not None:
                        shadow = None

            pos = pygame.mouse.get_pos()
            # self.map_view.mes("FPS: " + str(FPS), PURPLE, 0, 0)
            self.map_view.background.blit(self.map_view.game_screen, (0, 0))
            if shadow is not None:
                shadow.rect.center = pos
                shadow.update()
                if self.map_view.is_building_position_valid(shadow):
                    shadow.image.fill(GREEN)
                else:
                    shadow.image.fill(RED)
                self.map_view.background.blit(shadow.image, (shadow.rect.left, shadow.rect.top))
            if shadow is None:
                for sprite in self.map_view.buildings_panel_sprites:
                    if sprite.rect.collidepoint(pos):
                        self.map_view.draw_message_with_wrapping(str(sprite.resources_cost), GREEN,
                                                                 pos[0], pos[1],
                                                                 self.map_view.background)
            pygame.display.flip()
            clock.tick(FPS)
