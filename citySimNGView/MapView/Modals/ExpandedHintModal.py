from MapView.CustomSprites.ContainerSprite import ContainerSprite
from MapView.Consts import BUILDINGS_PANEL_TEXTURE
from MapView.Utils import draw_text_with_wrapping, draw_text, \
    draw_text_with_wrapping_and_centering
from MapView.Consts import GREEN
from MapView.Items.Button import Button
from CreatorView.RelativePaths import relative_textures_path
import pygame

HINT_MODAL_X = 0.05
HINT_MODAL_Y = 0.05
HINT_MODAL_WIDTH = 0.5
HINT_MODAL_HEIGHT = 0.5
BUTTON_WIDTH = 0.1
BUTTON_HEIGHT = 0.1

RIGHT_ARROW_X = 0.7
LEFT_ARROW_X = 0.3
ARROW_Y = 0.9
ARROW_BUTTON_WIDTH = 0.1
ARROW_BUTTON_HEIGHT = 0.1


class ExpandedHintModal(ContainerSprite):
    def __init__(self, pos_x, pos_y, width, height, hints, game_board,
                 close_modal, id):
        ContainerSprite.__init__(self, pos_x, pos_y, width, height,
                                 BUILDINGS_PANEL_TEXTURE, "Hints modal",
                                 game_board)
        self.hints = hints
        self.curr_page = 1
        self.pages = {}
        self.buttons_sprites = pygame.sprite.Group()
        self.create_buttons(close_modal)
        self.id = id

        self.parse_message()

    def draw(self):
        self.clean()
        self.surface.blit(self.pages[self.curr_page], (0,0))
        self.surface.blit(self.right_arrow.image,
                          (self.right_arrow.rect[0] - self.pos_x,
                           self.right_arrow.rect[1] - self.pos_y))
        self.surface.blit(self.left_arrow.image,
                          (self.left_arrow.rect[0] - self.pos_x,
                           self.left_arrow.rect[1] - self.pos_y))
        self.surface.blit(self.close_button.image,
                          (self.close_button.rect[0] - self.pos_x,
                           self.close_button.rect[1] - self.pos_y))
        draw_text_with_wrapping_and_centering(
            self.left_arrow.pos_x + self.left_arrow.width - self.pos_x,
            ARROW_Y * self.height,
            self.right_arrow.pos_x - self.pos_x,
            "{}/{}".format(self.curr_page, self.last_page),
            self.surface, GREEN)
        self.blit_surface.blit(self.surface, self.rect)

    def create_page(self, surface, words, msg_split=False):
        print self.right_arrow.pos_y
        remaining_words = draw_text_with_wrapping(
            0, BUTTON_HEIGHT * self.height, self.width, words, GREEN,
            surface, 25, max_pos_y=self.right_arrow.rect[1] - self.pos_y,
            msg_split=msg_split)[3]
        return remaining_words

    def parse_message(self):
        self.pages[self.curr_page] = pygame.Surface.copy(self.image)
        remaining_words = self.create_page(self.pages[self.curr_page], self.hints)

        while remaining_words:
            self.curr_page += 1
            self.pages[self.curr_page] = pygame.Surface.copy(self.image)
            remaining_words = self.create_page(self.pages[self.curr_page], remaining_words,
                                               True)

        self.last_page = self.curr_page
        self.curr_page = 1

    def create_buttons(self, close_modal):
        self.close_button = Button(
            self.pos_x + self.width - BUTTON_WIDTH * self.width,  self.pos_y,
            BUTTON_WIDTH * self.width, BUTTON_HEIGHT * self.height,
            relative_textures_path + 'new\\delete.png', close_modal,
            self.blit_surface, "Close")
        self.buttons_sprites.add(self.close_button)

        self.create_scrolling_arrows()

    def create_scrolling_arrows(self):
        self.right_arrow = Button(RIGHT_ARROW_X * self.width + self.pos_x,
                                  ARROW_Y * self.height + self.pos_y,
                                  ARROW_BUTTON_WIDTH * self.width,
                                  ARROW_BUTTON_HEIGHT * self.height,
                                  relative_textures_path + "RightArrow.png",
                                  self.scroll_modal_right,
                                  self,
                                  "Go to the next page")

        self.left_arrow = Button(self.pos_x + LEFT_ARROW_X * self.width,
                                 self.pos_y + ARROW_Y * self.height,
                                 ARROW_BUTTON_WIDTH * self.width,
                                 ARROW_BUTTON_HEIGHT * self.height,
                                 relative_textures_path + "LeftArrow.png",
                                 self.scroll_modal_left,
                                 self,
                                 "Go to the previous page")
        self.buttons_sprites.add(self.right_arrow, self.left_arrow)

    def scroll_modal_left(self):
        if self.curr_page > 1:
            self.curr_page -= 1

    def scroll_modal_right(self):
        if self.curr_page < self.last_page:
            self.curr_page += 1