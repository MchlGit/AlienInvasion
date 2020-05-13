import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen() 

    def _check_events(self):
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN: 
                self._key_updown_events(event, True)
            elif event.type == pygame.KEYUP: 
                self._key_updown_events(event, False)

    def _create_fleet(self):
        ''' Create the fleet of aliens!'''
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        ship_height = self.ship.rect.height

        available_width = self.settings.screen_width - (2 * alien_width)
        # it is 2 * alien_width because need to take into account the empty space beside alien
        num_aliens = available_width // (2 * alien_width) 

        available_height = self.settings.screen_height - (3 * alien_height + ship_height) 
        num_rows = available_height // (2 * alien_height)

        # Make alien fleet
        for row_number in range(num_rows):
            for alien_number in range(num_aliens): 
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
            new_alien = Alien(self)
            alien_width, alien_height = new_alien.rect.size
            new_alien.x = alien_width + 2 * alien_width * alien_number
            new_alien.rect.x = int(new_alien.x)
            new_alien.rect.y = alien_height + 2 * alien_height * row_number
            self.aliens.add(new_alien)

    def _update_bullets(self): 
        '''Update position of bullets and get rid of old bullets.'''
        # Update bullet positions
        self.bullets.update()
        for bullet in self.bullets.copy(): 
            if bullet.rect.bottom <= 0: 
                self.bullets.remove(bullet)

    def _key_updown_events(self, event, isKeyDown=True):
        ''' handles key up and key down events '''
        if event.key == pygame.K_RIGHT: 
            # Move the ship to the right. 
            self.ship.moving_right = isKeyDown
        elif event.key == pygame.K_LEFT: 
            # Move the ship to the left. 
            self.ship.moving_left = isKeyDown
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE: 
            self._fire_bullet()

    def _fire_bullet(self):
        ''' Create a new bullet and add it to the bullets group.'''
        if(len(self.bullets) < self.settings.bullets_allowed):
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites(): 
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Make the most recently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
