import threading
import pygame
from Building import Building
from Consts import RED, LEFT, RIGHT, FPS, GREEN
from Utils import draw_text_with_wrapping


class UserEventHandlerThread(threading.Thread):
    def __init__(self, map_view):
        threading.Thread.__init__(self)
        self.map_view = map_view

    def run(self):
        shadow = None
        building = None
        clock = pygame.time.Clock()
        clicked_button = None

        while self.map_view.game_on:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:

                    # if we have selected building after clicking left button we try to place it
                    if shadow is not None:
                        shadow.rect.center = pos
                        shadow.update()
                        self.map_view.place_building(building, (shadow.rect.left, shadow.rect.top))
                        shadow = None
                    else:
                        # check if building sprite in buildings panel has been clicked
                        clicked_sprites = [s for s in self.map_view.buildings_panel_sprites if s.rect.collidepoint(pos)]
                        if len(clicked_sprites) == 1:
                            building = self.map_view.check_if_can_afford(clicked_sprites[0])
                            if self.map_view.can_afford_on_building:
                                shadow = Building(building.name, building.id, building.texture, building.resources_cost,
                                                  building.consumes, building.produces,
                                                  self.map_view.background.get_size(), pos)
                                shadow.image.fill(RED)

                        # check if some building sprite in map has been clicked
                        clicked_buildings = [b for b in self.map_view.buildings_sprites if b.rect.collidepoint(pos)]
                        if len(clicked_buildings) == 1:
                            self.map_view.get_building_state(clicked_buildings[0])
                            self.map_view.info_panel.curr_building = clicked_buildings[0]

                        if self.map_view.del_button_sprite is not None and self.map_view.del_button_sprite.rect.collidepoint(pos):
                            clicked_button = self.map_view.del_button_sprite
                            clicked_button.click_button(self.map_view, self.map_view.info_panel.curr_building)

                        if self.map_view.info_panel.stop_production_button is not None and \
                           self.map_view.info_panel.stop_production_button.rect.collidepoint(pos):
                            clicked_button = self.map_view.info_panel.stop_production_button
                            clicked_button.click_button(self.map_view, self.map_view.info_panel.curr_building)

                        if self.map_view.left_arrow_buildings_panel.rect.collidepoint(pos):
                            clicked_button = self.map_view.left_arrow_buildings_panel
                            clicked_button.click_button(self.map_view)
                        if self.map_view.right_arrow_buildings_panel.rect.collidepoint(pos):
                            clicked_button = self.map_view.right_arrow_buildings_panel
                            clicked_button.click_button(self.map_view)
                        if self.map_view.resources_panel.left_arrow.rect.collidepoint(pos):
                            clicked_button = self.map_view.resources_panel.left_arrow
                            clicked_button.click_button(self.map_view)
                        if self.map_view.resources_panel.right_arrow.rect.collidepoint(pos):
                            clicked_button = self.map_view.resources_panel.right_arrow
                            clicked_button.click_button(self.map_view)
                        clicked_nav_arrows = [s for s in self.map_view.navigation_arrows_sprites if s.rect.collidepoint(pos)]
                        if len(clicked_nav_arrows) == 1:
                            clicked_button = clicked_nav_arrows[0]
                            clicked_button.click_button(self.map_view, clicked_nav_arrows[0])

                if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                    if clicked_button is not None:
                        clicked_button.release_button(self.map_view)
                        clicked_button = None

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                    if shadow is not None:
                        shadow = None

            pos = pygame.mouse.get_pos()
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
                        draw_text_with_wrapping(pos[0], pos[1], self.map_view.width, str(sprite.resources_cost), GREEN,
                                                self.map_view.background)
            pygame.display.flip()
            clock.tick(FPS)
