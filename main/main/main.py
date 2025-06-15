import pygame
import random
import os
import sys
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Game constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
TITLE = "Epic Adventure RPG"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Fonts
font_small = pygame.font.SysFont('Arial', 18)
font_medium = pygame.font.SysFont('Arial', 24)
font_large = pygame.font.SysFont('Arial', 36)
font_title = pygame.font.SysFont('Arial', 48)

# Load images (placeholder paths - you'll need actual image files)
def load_image(name, scale=1):
    try:
        image = pygame.image.load(f"assets/images/{name}.png").convert_alpha()
        if scale != 1:
            new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)
        return image
    except:
        # Create a placeholder surface if image not found
        surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.rect(surf, (random.randint(0, 255), (0, 0, 50, 50)))
        pygame.draw.rect(surf, BLACK, (0, 0, 50, 50), 2)
        text = font_small.render(name[:3], True, BLACK)
        surf.blit(text, (25 - text.get_width()//2, 25 - text.get_height()//2))
        return surf

# Load sounds (placeholder paths)
def load_sound(name):
    try:
        return mixer.Sound(f"assets/sounds/{name}.mp3")
    except:
        print(f"Sound {name} not found!")
        return None

# Game assets
class Assets:
    def __init__(self):
        # Backgrounds
        self.main_menu_bg = load_image("assets/images/main.png")
        self.forest_bg = load_image("assets/images/forest_bg.png")
        self.town_bg = load_image("assets/images/town_bg.png")
        self.cave_bg = load_image("assets/images/cave_bg.png")
        self.castle_bg = load_image("assets/images/castle_bg.png")
        
        # Character sprites
        self.player_img = load_image("assets/images/player.png", 0.5)
        self.goblin_img = load_image("assets/images/goblin.png", 0.5)
        self.wolf_img = load_image("assets/images/wolf.png", 0.5)
        self.bandit_img = load_image("assets/images/bandit.png", 0.5)
        self.orc_img = load_image("assets/images/orc.png", 0.5)
        self.dragon_img = load_image("assets/images/dragon.png", 0.5)
        
        # Item icons
        self.sword_icon = load_image("assets/images/sword_icon.png", 0.5)
        self.armor_icon = load_image("assets/images/armor_icon.png", 0.5)
        self.potion_icon = load_image("assets/images/potion_icon.png", 0.5)
        self.misc_icon = load_image("assets/images/misc_icon.png", 0.5)
        self.gold_icon = load_image("assets/images/gold_icon.png", 0.5)
        
        # UI elements
        self.button_img = load_image("assets/images/button.png", 0.5)
        self.button_hover_img = load_image("assets/images/button.png", 0.5)
        
        # Sounds
        self.battle_music = load_sound("assets/sounds/battle.mp3")
        self.town_music = load_sound("assets/sounds/town.mp3")
        self.explore_music = load_sound("assets/sounds/exsplore.mp3")
        self.menu_music = load_sound("assets/sounds/menu.mp3")
        self.attack_sound = load_sound("assets/sounds/attack.mp3")
        self.heal_sound = load_sound("assets/sounds/heal.mp3")
        self.level_up_sound = load_sound("assets/sounds/level_up.mp3")
        self.victory_sound = load_sound("assets/sounds/victory.mp3")
        self.defeat_sound = load_sound("assets/sounds/defeat.mp3")
assets = Assets()
class Button:
    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=GREEN):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)
        
        text_surf = font_medium.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False
class Item:
    def __init__(self, name, item_type, stat, value, icon=None):
        self.name = name
        self.type = item_type  # weapon, armor, potion, misc
        self.stat = stat  # attack for weapon, defense for armor, heal for potion
        self.value = value  # gold value
        self.icon = icon or self.get_default_icon()
        
    def get_default_icon(self):
        if self.type == "weapon":
            return assets.sword_icon
        elif self.type == "armor":
            return assets.armor_icon
        elif self.type == "potion":
            return assets.potion_icon
        else:
            return assets.misc_icon
            
    def draw(self, surface, x, y, selected=False):
        # Draw item icon
        surface.blit(self.icon, (x, y))
        
        # Draw selection highlight
        if selected:
            pygame.draw.rect(surface, YELLOW, (x-2, y-2, self.icon.get_width()+4, self.icon.get_height()+4), 2)
        
        # Draw item info
        info_y = y + self.icon.get_height() + 5
        name_text = font_small.render(self.name, True, WHITE)
        surface.blit(name_text, (x, info_y))
        
        if self.type == "weapon":
            stat_text = font_small.render(f"ATK +{self.stat}", True, WHITE)
        elif self.type == "armor":
            stat_text = font_small.render(f"DEF +{self.stat}", True, WHITE)
        elif self.type == "potion":
            stat_text = font_small.render(f"HEAL +{self.stat}", True, WHITE)
        else:
            stat_text = font_small.render("", True, WHITE)
            
        surface.blit(stat_text, (x, info_y + 20))
        
        value_text = font_small.render(f"{self.value}g", True, GOLD)
        surface.blit(value_text, (x, info_y + 40))

# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.exp = 0
        self.exp_to_level = 100
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.defense = 5
        self.gold = 50
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.location = "Starting Forest"
        self.image = assets.player_img
        self.locations_unlocked = ["Starting Forest", "Greenfield Town"]
        
        # Starting items
        wooden_sword = Item("Wooden Sword", "weapon", 2, 5, assets.sword_icon)
        self.add_item(wooden_sword)
        self.equip_item(wooden_sword)
        
    def add_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_level:
            self.level_up()
            
    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_level
        self.exp_to_level = int(self.exp_to_level * 1.5)
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 5
        self.defense += 3
        
        if assets.level_up_sound:
            assets.level_up_sound.play()
        
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        return actual_damage
        
    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
        if assets.heal_sound:
            assets.heal_sound.play()
        
    def is_alive(self):
        return self.hp > 0
        
    def equip_item(self, item):
        if item.type == "weapon":
            if self.equipped_weapon:
                self.unequip_item(self.equipped_weapon)
            self.equipped_weapon = item
            self.attack += item.stat
        elif item.type == "armor":
            if self.equipped_armor:
                self.unequip_item(self.equipped_armor)
            self.equipped_armor = item
            self.defense += item.stat
        
    def unequip_item(self, item):
        if item.type == "weapon" and self.equipped_weapon == item:
            self.attack -= item.stat
            self.equipped_weapon = None
        elif item.type == "armor" and self.equipped_armor == item:
            self.defense -= item.stat
            self.equipped_armor = None
        
    def add_item(self, item):
        self.inventory.append(item)
        
    def use_item(self, item):
        if item.type == "potion":
            self.heal(item.stat)
            self.inventory.remove(item)
            return True
        return False
        
    def can_travel_to(self, location):
        return location in self.locations_unlocked
        
    def unlock_location(self, location):
        if location not in self.locations_unlocked:
            self.locations_unlocked.append(location)
            return True
        return False

# Enemy class
class Enemy:
    def __init__(self, name, level, hp, attack, defense, exp_reward, gold_reward, image, boss=False):
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.loot_table = []
        self.image = image
        self.boss = boss
        
    def add_loot(self, item, chance):
        self.loot_table.append((item, chance))
        
    def generate_loot(self):
        loot = []
        for item, chance in self.loot_table:
            if random.random() < chance:
                loot.append(item)
        return loot
        
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        return actual_damage
        
    def is_alive(self):
        return self.hp > 0

# Game state class
class GameState:
    MAIN_MENU = 0
    PLAYING = 1
    COMBAT = 2
    INVENTORY = 3
    SHOP = 4
    GAME_OVER = 5
    VICTORY = 6
    TRAVEL = 7

# Create enemies
def create_enemies():
    enemies = []
    
    # Regular enemies
    goblin = Enemy("Goblin", 1, 30, 8, 2, 25, 10, assets.goblin_img)
    goblin.add_loot(Item("Rusty Dagger", "weapon", 3, 15, assets.sword_icon), 0.4)
    goblin.add_loot(Item("Goblin Ear", "misc", 0, 5, assets.misc_icon), 0.8)
    enemies.append(goblin)
    
    wolf = Enemy("Wild Wolf", 1, 40, 12, 1, 30, 15, assets.wolf_img)
    wolf.add_loot(Item("Wolf Fang", "misc", 0, 10, assets.misc_icon), 0.7)
    wolf.add_loot(Item("Wolf Pelt", "misc", 0, 20, assets.misc_icon), 0.5)
    enemies.append(wolf)
    
    bandit = Enemy("Bandit", 2, 50, 15, 5, 45, 25, assets.bandit_img)
    bandit.add_loot(Item("Short Sword", "weapon", 5, 30, assets.sword_icon), 0.3)
    bandit.add_loot(Item("Leather Armor", "armor", 4, 40, assets.armor_icon), 0.2)
    bandit.add_loot(Item("Small Health Potion", "potion", 20, 15, assets.potion_icon), 0.4)
    enemies.append(bandit)
    
    orc = Enemy("Orc Warrior", 3, 80, 20, 8, 70, 40, assets.orc_img)
    orc.add_loot(Item("Orcish Axe", "weapon", 8, 60, assets.sword_icon), 0.4)
    orc.add_loot(Item("Orc Tusk", "misc", 0, 30, assets.misc_icon), 0.9)
    orc.add_loot(Item("Medium Health Potion", "potion", 35, 25, assets.potion_icon), 0.3)
    enemies.append(orc)
    
    # Boss enemies
    dragon = Enemy("Ancient Dragon", 10, 300, 40, 20, 500, 200, assets.dragon_img, True)
    dragon.add_loot(Item("Dragon Scale Armor", "armor", 25, 300, assets.armor_icon), 1.0)
    dragon.add_loot(Item("Dragonbone Sword", "weapon", 30, 400, assets.sword_icon), 1.0)
    dragon.add_loot(Item("Large Health Potion", "potion", 60, 40, assets.potion_icon), 0.8)
    enemies.append(dragon)
    
    return enemies

# Create items
def create_items():
    items = []
    
    # Weapons
    items.append(Item("Wooden Sword", "weapon", 2, 10, assets.sword_icon))
    items.append(Item("Iron Sword", "weapon", 5, 30, assets.sword_icon))
    items.append(Item("Steel Sword", "weapon", 8, 60, assets.sword_icon))
    items.append(Item("Silver Sword", "weapon", 12, 100, assets.sword_icon))
    items.append(Item("Dragonbone Sword", "weapon", 30, 400, assets.sword_icon))
    
    # Armor
    items.append(Item("Leather Vest", "armor", 3, 20, assets.armor_icon))
    items.append(Item("Chainmail", "armor", 7, 50, assets.armor_icon))
    items.append(Item("Plate Armor", "armor", 12, 100, assets.armor_icon))
    items.append(Item("Silver Armor", "armor", 18, 200, assets.armor_icon))
    items.append(Item("Dragon Scale Armor", "armor", 25, 300, assets.armor_icon))
    
    # Potions
    items.append(Item("Small Health Potion", "potion", 20, 15, assets.potion_icon))
    items.append(Item("Medium Health Potion", "potion", 35, 25, assets.potion_icon))
    items.append(Item("Large Health Potion", "potion", 60, 40, assets.potion_icon))
    items.append(Item("Elixir of Life", "potion", 100, 100, assets.potion_icon))
    
    # Misc
    items.append(Item("Ancient Key", "misc", 0, 0, assets.misc_icon))
    
    return items

# Combat system
def combat_screen(player, enemy):
    state = GameState.COMBAT
    combat_over = False
    result = None  # True = win, False = lose, None = fled
    
    # Combat buttons
    attack_btn = Button(50, 600, 150, 50, "Attack")
    item_btn = Button(225, 600, 150, 50, "Use Item")
    flee_btn = Button(400, 600, 150, 50, "Flee")
    
    # Combat log
    combat_log = []
    combat_log.append(f"Encountered {enemy.name}!")
    
    # Scale enemy based on player level if not a boss
    if not enemy.boss:
        enemy.level = player.level
        enemy.hp = enemy.max_hp * player.level
        enemy.attack += (player.level - 1) * 2
        enemy.defense += (player.level - 1)
        enemy.exp_reward *= player.level
        enemy.gold_reward *= player.level
    
    while not combat_over:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Handle button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if attack_btn.is_clicked(mouse_pos, event):
                    # Player attack
                    damage = max(1, player.attack + random.randint(-2, 3))
                    enemy_damage = enemy.take_damage(damage)
                    combat_log.append(f"You hit {enemy.name} for {enemy_damage} damage!")
                    
                    if assets.attack_sound:
                        assets.attack_sound.play()
                    
                    # Check if enemy is dead
                    if not enemy.is_alive():
                        combat_log.append(f"You defeated {enemy.name}!")
                        player.add_exp(enemy.exp_reward)
                        player.gold += enemy.gold_reward
                        combat_log.append(f"Gained {enemy.exp_reward} EXP and {enemy.gold_reward} gold!")
                        
                        # Loot
                        loot = enemy.generate_loot()
                        for item in loot:
                            player.add_item(item)
                            combat_log.append(f"Got {item.name}!")
                        
                        result = True
                        combat_over = True
                        if assets.victory_sound:
                            assets.victory_sound.play()
                        break
                    
                    # Enemy attack
                    damage = max(1, enemy.attack + random.randint(-2, 2))
                    player_damage = player.take_damage(damage)
                    combat_log.append(f"{enemy.name} hits you for {player_damage} damage!")
                    
                    if assets.attack_sound:
                        assets.attack_sound.play()
                    
                    # Check if player is dead
                    if not player.is_alive():
                        combat_log.append("You were defeated!")
                        player.gold = max(0, player.gold - int(player.gold * 0.3))
                        player.hp = player.max_hp // 2
                        result = False
                        combat_over = True
                        if assets.defeat_sound:
                            assets.defeat_sound.play()
                        break
                        
                elif item_btn.is_clicked(mouse_pos, event):
                    # Open inventory to use item
                    state = GameState.INVENTORY
                    use_result = inventory_screen(player, True)
                    
                    if use_result is not None:  # Item was used
                        state = GameState.COMBAT
                        combat_log.append(use_result)
                        
                        # Enemy still gets a turn if player used item
                        damage = max(1, enemy.attack + random.randint(-2, 2))
                        player_damage = player.take_damage(damage)
                        combat_log.append(f"{enemy.name} hits you for {player_damage} damage!")
                        
                        if assets.attack_sound:
                            assets.attack_sound.play()
                            
                        # Check if player is dead
                        if not player.is_alive():
                            combat_log.append("You were defeated!")
                            player.gold = max(0, player.gold - int(player.gold * 0.3))
                            player.hp = player.max_hp // 2
                            result = False
                            combat_over = True
                            if assets.defeat_sound:
                                assets.defeat_sound.play()
                            break
                    
                elif flee_btn.is_clicked(mouse_pos, event):
                    # Try to flee
                    if random.random() < 0.5 or enemy.boss:  # Lower chance to flee from bosses
                        combat_log.append("You failed to flee!")
                        
                        # Enemy attack
                        damage = max(1, enemy.attack + random.randint(-2, 2))
                        player_damage = player.take_damage(damage)
                        combat_log.append(f"{enemy.name} hits you for {player_damage} damage!")
                        
                        if assets.attack_sound:
                            assets.attack_sound.play()
                            
                        # Check if player is dead
                        if not player.is_alive():
                            combat_log.append("You were defeated!")
                            player.gold = max(0, player.gold - int(player.gold * 0.3))
                            player.hp = player.max_hp // 2
                            result = False
                            combat_over = True
                            if assets.defeat_sound:
                                assets.defeat_sound.play()
                            break
                    else:
                        combat_log.append("You successfully fled!")
                        result = None
                        combat_over = True
        
        # Update button hover states
        attack_btn.check_hover(mouse_pos)
        item_btn.check_hover(mouse_pos)
        flee_btn.check_hover(mouse_pos)
        
        # Draw combat screen
        screen.fill(BLACK)
        
        # Draw background based on location
        if player.location == "Dark Cave":
            screen.blit(assets.cave_bg, (0, 0))
        elif player.location == "Dragon's Keep":
            screen.blit(assets.castle_bg, (0, 0))
        else:
            screen.blit(assets.forest_bg, (0, 0))
        
        # Draw combatants
        screen.blit(player.image, (150, 200))
        screen.blit(enemy.image, (600, 200))
        
        # Draw health bars
        # Player health
        pygame.draw.rect(screen, RED, (50, 150, 200, 20))
        pygame.draw.rect(screen, GREEN, (50, 150, 200 * (player.hp / player.max_hp), 20))
        player_health_text = font_medium.render(f"{player.hp}/{player.max_hp}", True, WHITE)
        screen.blit(player_health_text, (150 - player_health_text.get_width()//2, 150))
        
        # Enemy health
        pygame.draw.rect(screen, RED, (600, 150, 200, 20))
        pygame.draw.rect(screen, GREEN, (600, 150, 200 * (enemy.hp / enemy.max_hp), 20))
        enemy_health_text = font_medium.render(f"{enemy.hp}/{enemy.max_hp}", True, WHITE)
        screen.blit(enemy_health_text, (700 - enemy_health_text.get_width()//2, 150))
        
        # Draw names and levels
        player_text = font_medium.render(f"{player.name} (Lvl {player.level})", True, WHITE)
        enemy_text = font_medium.render(f"{enemy.name} (Lvl {enemy.level})", True, WHITE)
        screen.blit(player_text, (150 - player_text.get_width()//2, 120))
        screen.blit(enemy_text, (700 - enemy_text.get_width()//2, 120))
        
        if enemy.boss:
            boss_text = font_medium.render("BOSS", True, RED)
            screen.blit(boss_text, (700 - boss_text.get_width()//2, 90))
        
        # Draw combat log
        log_y = 400
        for i, message in enumerate(combat_log[-5:]):  # Show last 5 messages
            log_text = font_small.render(message, True, WHITE)
            screen.blit(log_text, (50, log_y + i * 30))
        
        # Draw buttons
        attack_btn.draw(screen)
        item_btn.draw(screen)
        flee_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    return result

# Inventory screen
def inventory_screen(player, combat_mode=False):
    state = GameState.INVENTORY
    selected_item = None
    result = None
    
    # Create buttons
    use_btn = Button(700, 600, 150, 50, "Use/Equip")
    equip_btn = Button(700, 600, 150, 50, "Equip")
    unequip_btn = Button(550, 600, 150, 50, "Unequip")
    back_btn = Button(850, 600, 150, 50, "Back")
    
    while state == GameState.INVENTORY:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check item selection
                for i, item in enumerate(player.inventory):
                    col = i % 5
                    row = i // 5
                    item_rect = pygame.Rect(50 + col * 110, 150 + row * 110, 100, 100)
                    if item_rect.collidepoint(mouse_pos):
                        selected_item = item
                
                # Check button clicks
                if back_btn.is_clicked(mouse_pos, event):
                    return result
                
                if selected_item:
                    if combat_mode:
                        if use_btn.is_clicked(mouse_pos, event):
                            if selected_item.type == "potion":
                                player.use_item(selected_item)
                                return f"Used {selected_item.name}!"
                            else:
                                return "You can't use that in combat!"
                    else:
                        if equip_btn.is_clicked(mouse_pos, event):
                            if selected_item.type in ["weapon", "armor"]:
                                player.equip_item(selected_item)
                        elif unequip_btn.is_clicked(mouse_pos, event):
                            if (player.equipped_weapon == selected_item) or (player.equipped_armor == selected_item):
                                player.unequip_item(selected_item)
        
        # Update button hover states
        back_btn.check_hover(mouse_pos)
        if combat_mode:
            use_btn.check_hover(mouse_pos)
        else:
            equip_btn.check_hover(mouse_pos)
            unequip_btn.check_hover(mouse_pos)
        
        # Draw inventory screen
        screen.fill(BLACK)
        
        # Draw background
        screen.blit(assets.town_bg, (0, 0))
        
        # Draw title
        title_text = font_large.render("Inventory", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        
        # Draw player stats
        stats_text = [
            f"Name: {player.name}",
            f"Level: {player.level}",
            f"EXP: {player.exp}/{player.exp_to_level}",
            f"HP: {player.hp}/{player.max_hp}",
            f"Attack: {player.attack}",
            f"Defense: {player.defense}",
            f"Gold: {player.gold}"
        ]
        
        for i, stat in enumerate(stats_text):
            stat_text = font_small.render(stat, True, WHITE)
            screen.blit(stat_text, (700, 150 + i * 25))
        
        # Draw equipped items
        equip_text = font_medium.render("Equipped:", True, WHITE)
        screen.blit(equip_text, (700, 350))
        
        weapon_text = font_small.render(f"Weapon: {player.equipped_weapon.name if player.equipped_weapon else 'None'}", True, WHITE)
        armor_text = font_small.render(f"Armor: {player.equipped_armor.name if player.equipped_armor else 'None'}", True, WHITE)
        screen.blit(weapon_text, (700, 380))
        screen.blit(armor_text, (700, 410))
        
        # Draw inventory items
        inv_text = font_medium.render("Inventory:", True, WHITE)
        screen.blit(inv_text, (50, 120))
        
        for i, item in enumerate(player.inventory):
            col = i % 5
            row = i // 5
            x = 50 + col * 110
            y = 150 + row * 110
            item.draw(screen, x, y, selected_item == item)
        
        # Draw buttons
        if combat_mode:
            use_btn.draw(screen)
        else:
            equip_btn.draw(screen)
            unequip_btn.draw(screen)
        back_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    return result

# Shop screen
def shop_screen(player):
    state = GameState.SHOP
    shop_items = create_items()
    selected_item = None
    sell_mode = False
    
    # Create buttons
    buy_btn = Button(550, 600, 150, 50, "Buy")
    sell_btn = Button(700, 600, 150, 50, "Sell")
    back_btn = Button(850, 600, 150, 50, "Back")
    confirm_btn = Button(700, 600, 150, 50, "Confirm")
    cancel_btn = Button(550, 600, 150, 50, "Cancel")
    
    while state == GameState.SHOP:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not sell_mode:
                    # Check item selection in shop
                    for i, item in enumerate(shop_items):
                        col = i % 5
                        row = i // 5
                        item_rect = pygame.Rect(50 + col * 110, 150 + row * 110, 100, 100)
                        if item_rect.collidepoint(mouse_pos):
                            selected_item = item
                else:
                    # Check item selection in player inventory
                    for i, item in enumerate(player.inventory):
                        col = i % 5
                        row = i // 5
                        item_rect = pygame.Rect(50 + col * 110, 150 + row * 110, 100, 100)
                        if item_rect.collidepoint(mouse_pos):
                            selected_item = item
                
                # Check button clicks
                if back_btn.is_clicked(mouse_pos, event):
                    return
                
                if not sell_mode:
                    if buy_btn.is_clicked(mouse_pos, event):
                        sell_mode = True
                        selected_item = None
                    elif sell_btn.is_clicked(mouse_pos, event):
                        sell_mode = True
                        selected_item = None
                    elif selected_item and confirm_btn.is_clicked(mouse_pos, event):
                        # Buy item
                        if player.gold >= selected_item.value:
                            player.gold -= selected_item.value
                            player.add_item(selected_item)
                            selected_item = None
                        else:
                            selected_item = None  # Can't afford
                else:
                    if cancel_btn.is_clicked(mouse_pos, event):
                        sell_mode = False
                        selected_item = None
                    elif selected_item and confirm_btn.is_clicked(mouse_pos, event):
                        # Sell item
                        # Check if item is equipped
                        if (player.equipped_weapon == selected_item) or (player.equipped_armor == selected_item):
                            selected_item = None  # Can't sell equipped items
                        else:
                            sell_price = selected_item.value // 2
                            player.gold += sell_price
                            player.inventory.remove(selected_item)
                            selected_item = None
        
        # Update button hover states
        back_btn.check_hover(mouse_pos)
        if sell_mode:
            cancel_btn.check_hover(mouse_pos)
            confirm_btn.check_hover(mouse_pos)
        else:
            buy_btn.check_hover(mouse_pos)
            sell_btn.check_hover(mouse_pos)
            if selected_item:
                confirm_btn.check_hover(mouse_pos)
        
        # Draw shop screen
        screen.fill(BLACK)
        
        # Draw background
        screen.blit(assets.town_bg, (0, 0))
        
        # Draw title
        title_text = font_large.render("Shop - Buy" if not sell_mode else "Shop - Sell", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        
        # Draw player gold
        gold_text = font_medium.render(f"Gold: {player.gold}", True, GOLD)
        screen.blit(gold_text, (700, 120))
        
        # Draw items
        if not sell_mode:
            # Shop items
            inv_text = font_medium.render("Shop Items:", True, WHITE)
            screen.blit(inv_text, (50, 120))
            
            for i, item in enumerate(shop_items):
                col = i % 5
                row = i // 5
                x = 50 + col * 110
                y = 150 + row * 110
                item.draw(screen, x, y, selected_item == item)
        else:
            # Player inventory
            inv_text = font_medium.render("Your Inventory:", True, WHITE)
            screen.blit(inv_text, (50, 120))
            
            for i, item in enumerate(player.inventory):
                col = i % 5
                row = i // 5
                x = 50 + col * 110
                y = 150 + row * 110
                item.draw(screen, x, y, selected_item == item)
        
        # Draw selected item info
        if selected_item:
            info_text = [
                f"Name: {selected_item.name}",
                f"Type: {selected_item.type.capitalize()}",
                f"Value: {selected_item.value}g" if not sell_mode else f"Sell Price: {selected_item.value//2}g"
            ]
            
            if selected_item.type == "weapon":
                info_text.append(f"Attack: +{selected_item.stat}")
            elif selected_item.type == "armor":
                info_text.append(f"Defense: +{selected_item.stat}")
            elif selected_item.type == "potion":
                info_text.append(f"Heal: +{selected_item.stat} HP")
            
            for i, text in enumerate(info_text):
                text_surf = font_small.render(text, True, WHITE)
                screen.blit(text_surf, (700, 150 + i * 25))
        
        # Draw buttons
        if sell_mode:
            cancel_btn.draw(screen)
            if selected_item:
                confirm_btn.draw(screen)
        else:
            buy_btn.draw(screen)
            sell_btn.draw(screen)
            if selected_item:
                confirm_btn.draw(screen)
        back_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

# Healer screen
def healer_screen(player):
    cost = 20 * player.level
    heal_amount = player.max_hp - player.hp
    
    # Create buttons
    heal_btn = Button(400, 400, 150, 50, f"Heal ({cost}g)")
    back_btn = Button(600, 400, 150, 50, "Back")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if heal_btn.is_clicked(mouse_pos, event):
                    if player.hp < player.max_hp:
                        if player.gold >= cost:
                            player.gold -= cost
                            player.heal(heal_amount)
                        else:
                            pass  # Not enough gold
                    else:
                        pass  # Already at full health
                elif back_btn.is_clicked(mouse_pos, event):
                    return
        
        # Update button hover states
        heal_btn.check_hover(mouse_pos)
        back_btn.check_hover(mouse_pos)
        
        # Draw healer screen
        screen.fill(BLACK)
        
        # Draw background
        screen.blit(assets.town_bg, (0, 0))
        
        # Draw title
        title_text = font_large.render("Temple of Healing", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
        
        # Draw player status
        status_text = [
            f"HP: {player.hp}/{player.max_hp}",
            f"Heal Amount: {heal_amount} HP",
            f"Cost: {cost} gold"
        ]
        
        for i, text in enumerate(status_text):
            text_surf = font_medium.render(text, True, WHITE)
            screen.blit(text_surf, (SCREEN_WIDTH//2 - text_surf.get_width()//2, 200 + i * 40))
        
        # Draw buttons
        if player.hp < player.max_hp and player.gold >= cost:
            heal_btn.draw(screen)
        back_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

# Travel screen
def travel_screen(player):
    locations = [
        ("Starting Forest", "A dense forest where your adventure begins"),
        ("Greenfield Town", "A peaceful town with shops and services"),
        ("Dark Cave", "A dangerous cave full of monsters"),
        ("Mountain Pass", "A treacherous path through the mountains"),
        ("Dragon's Keep", "The lair of the ancient dragon (BOSS)")
    ]
    
    # Create buttons for each location
    location_btns = []
    for i, (loc, desc) in enumerate(locations):
        if player.can_travel_to(loc) or i == 0:  # Always show starting location
            btn = Button(100, 150 + i * 100, 300, 80, loc)
            location_btns.append((btn, loc, desc))
    
    back_btn = Button(SCREEN_WIDTH//2 - 75, 650, 150, 50, "Back")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        selected_loc = None
        selected_desc = ""
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn, loc, desc in location_btns:
                    if btn.is_clicked(mouse_pos, event) and player.can_travel_to(loc):
                        player.location = loc
                        return
                
                if back_btn.is_clicked(mouse_pos, event):
                    return
        
        # Check hover for description
        for btn, loc, desc in location_btns:
            if btn.check_hover(mouse_pos) and player.can_travel_to(loc):
                selected_loc = loc
                selected_desc = desc
        
        # Draw travel screen
        screen.fill(BLACK)
        
        # Draw background
        screen.blit(assets.town_bg, (0, 0))
        
        # Draw title
        title_text = font_large.render("Travel", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        
        # Draw current location
        current_text = font_medium.render(f"Current Location: {player.location}", True, WHITE)
        screen.blit(current_text, (SCREEN_WIDTH//2 - current_text.get_width()//2, 100))
        
        # Draw location buttons
        for btn, loc, desc in location_btns:
            if player.can_travel_to(loc):
                btn.draw(screen)
            else:
                # Draw locked locations
                pygame.draw.rect(screen, (50, 50, 50), btn.rect, border_radius=5)
                pygame.draw.rect(screen, BLACK, btn.rect, 2, border_radius=5)
                lock_text = font_medium.render("Locked", True, WHITE)
                screen.blit(lock_text, (btn.rect.centerx - lock_text.get_width()//2, 
                                       btn.rect.centery - lock_text.get_height()//2))
        
        # Draw selected location description
        if selected_loc:
            desc_lines = [selected_desc[i:i+40] for i in range(0, len(selected_desc), 40)]
            for i, line in enumerate(desc_lines):
                desc_text = font_small.render(line, True, WHITE)
                screen.blit(desc_text, (500, 200 + i * 25))
        
        back_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

# Town screen
def town_screen(player):
    # Create buttons
    shop_btn = Button(300, 200, 200, 80, "Shop")
    heal_btn = Button(550, 200, 200, 80, "Temple")
    inventory_btn = Button(300, 350, 200, 80, "Inventory")
    status_btn = Button(550, 350, 200, 80, "Status")
    travel_btn = Button(300, 500, 200, 80, "Travel")
    leave_btn = Button(550, 500, 200, 80, "Leave Town")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shop_btn.is_clicked(mouse_pos, event):
                    shop_screen(player)
                elif heal_btn.is_clicked(mouse_pos, event):
                    healer_screen(player)
                elif inventory_btn.is_clicked(mouse_pos, event):
                    inventory_screen(player)
                elif status_btn.is_clicked(mouse_pos, event):
                    pass  # Status is shown in inventory
                elif travel_btn.is_clicked(mouse_pos, event):
                    travel_screen(player)
                elif leave_btn.is_clicked(mouse_pos, event):
                    return
        
        # Update button hover states
        shop_btn.check_hover(mouse_pos)
        heal_btn.check_hover(mouse_pos)
        inventory_btn.check_hover(mouse_pos)
        status_btn.check_hover(mouse_pos)
        travel_btn.check_hover(mouse_pos)
        leave_btn.check_hover(mouse_pos)
        
        # Draw town screen
        screen.fill(BLACK)
        
        # Draw background
        screen.blit(assets.town_bg, (0, 0))
        
        # Draw title
        title_text = font_large.render(f"Welcome to {player.location}", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        
        # Draw buttons
        shop_btn.draw(screen)
        heal_btn.draw(screen)
        inventory_btn.draw(screen)
        status_btn.draw(screen)
        travel_btn.draw(screen)
        leave_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

# Explore screen
def explore_screen(player, enemies):
    # Create buttons
    explore_btn = Button(300, 300, 200, 80, "Explore")
    town_btn = Button(550, 300, 200, 80, "Go to Town")
    inventory_btn = Button(300, 450, 200, 80, "Inventory")
    status_btn = Button(550, 450, 200, 80, "Status")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if explore_btn.is_clicked(mouse_pos, event):
                    # Random encounter
                    encounter_chance = random.random()
                    
                    if encounter_chance < 0.6:  # 60% chance for combat
                        # Boss encounter chance
                        if player.location == "Dragon's Keep" or (player.level >= 10 and random.random() < 0.2):
                            # Boss fight
                            boss = next(e for e in enemies if e.boss)
                            combat_result = combat_screen(player, boss)
                            
                            # If player defeated the boss, unlock new areas
                            if combat_result and player.location == "Dragon's Keep":
                                player.unlock_location("Mountain Pass")
                                player.unlock_location("Dark Cave")
                        else:
                            # Regular enemy
                            regular_enemies = [e for e in enemies if not e.boss]
                            enemy = random.choice(regular_enemies)
                            combat_screen(player, enemy)
                    elif encounter_chance < 0.8:  # 20% chance for treasure
                        gold_found = random.randint(10, 50) * player.level
                        player.gold += gold_found
                        
                        # Show treasure popup
                        show_message(f"Found treasure! Got {gold_found} gold!")
                        
                        # Chance to find item
                        if random.random() < 0.5:
                            items = create_items()
                            item = random.choice(items)
                            player.add_item(item)
                            show_message(f"Found {item.name}!")
                    else:  # 20% chance for nothing
                        show_message("Nothing interesting found...")
                        
                elif town_btn.is_clicked(mouse_pos, event):
                    town_screen(player)
                elif inventory_btn.is_clicked(mouse_pos, event):
                    inventory_screen(player)
                elif status_btn.is_clicked(mouse_pos, event):
                    pass  # Status is shown in inventory
        
        # Update button hover states
        explore_btn.check_hover(mouse_pos)
        town_btn.check_hover(mouse_pos)
        inventory_btn.check_hover(mouse_pos)
        status_btn.check_hover(mouse_pos)
        
        # Draw explore screen
        screen.fill(BLACK)
        
        # Draw background based on location
        if player.location == "Dark Cave":
            screen.blit(assets.cave_bg, (0, 0))
        elif player.location == "Dragon's Keep":
            screen.blit(assets.castle_bg, (0, 0))
        else:
            screen.blit(assets.forest_bg, (0, 0))
        
        # Draw title
        title_text = font_large.render(f"{player.location}", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        
        # Draw location description
        desc_text = ""
        if player.location == "Starting Forest":
            desc_text = "A dense forest where your adventure begins"
        elif player.location == "Greenfield Town":
            desc_text = "A peaceful town with shops and services"
        elif player.location == "Dark Cave":
            desc_text = "A dangerous cave full of monsters"
        elif player.location == "Mountain Pass":
            desc_text = "A treacherous path through the mountains"
        elif player.location == "Dragon's Keep":
            desc_text = "The lair of the ancient dragon (BOSS)"
        
        desc_surf = font_medium.render(desc_text, True, WHITE)
        screen.blit(desc_surf, (SCREEN_WIDTH//2 - desc_surf.get_width()//2, 100))
        
        # Draw buttons
        explore_btn.draw(screen)
        town_btn.draw(screen)
        inventory_btn.draw(screen)
        status_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

# Show message popup
def show_message(message, duration=2):
    popup = pygame.Surface((600, 100), pygame.SRCALPHA)
    popup.fill((0, 0, 0, 200))
    pygame.draw.rect(popup, WHITE, (0, 0, 600, 100), 2)
    
    message_text = font_medium.render(message, True, WHITE)
    popup.blit(message_text, (300 - message_text.get_width()//2, 50 - message_text.get_height()//2))
    
    start_time = pygame.time.get_ticks()
    
    while pygame.time.get_ticks() - start_time < duration * 1000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.blit(popup, (SCREEN_WIDTH//2 - 300, SCREEN_HEIGHT//2 - 50))
        pygame.display.flip()
        clock.tick(FPS)

# Main menu
def main_menu():
    # Create buttons
    start_btn = Button(SCREEN_WIDTH//2 - 100, 300, 200, 80, "Start Game")
    quit_btn = Button(SCREEN_WIDTH//2 - 100, 450, 200, 80, "Quit")
    
    # Play menu music
    if assets.menu_music:
        mixer.music.load(assets.menu_music)
        mixer.music.play(-1)  # Loop indefinitely
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.is_clicked(mouse_pos, event):
                    # Stop menu music
                    if assets.menu_music:
                        mixer.music.stop()
                    return True
                elif quit_btn.is_clicked(mouse_pos, event):
                    pygame.quit()
                    sys.exit()
        
        # Update button hover states
        start_btn.check_hover(mouse_pos)
        quit_btn.check_hover(mouse_pos)
        
        # Draw main menu
        screen.fill(BLACK)
        screen.blit(assets.main_menu_bg, (0, 0))
        
        # Draw title
        title_text = font_title.render("EPIC ADVENTURE RPG", True, GOLD)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
        
        # Draw buttons
        start_btn.draw(screen)
        quit_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

# Main game function
def main():
    # Show main menu
    if not main_menu():
        return
    
    # Initialize game
    enemies = create_enemies()
    
    # Get player name
    name = ""
    input_active = True
    name_prompt = font_large.render("Enter your name:", True, WHITE)
    name_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2, 300, 50)
    
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip():
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 20 and event.unicode.isalnum():
                        name += event.unicode
        
        # Draw name input screen
        screen.fill(BLACK)
        screen.blit(assets.main_menu_bg, (0, 0))
        
        screen.blit(name_prompt, (SCREEN_WIDTH//2 - name_prompt.get_width()//2, SCREEN_HEIGHT//2 - 100))
        
        pygame.draw.rect(screen, WHITE, name_rect, 2)
        name_surface = font_medium.render(name, True, WHITE)
        screen.blit(name_surface, (name_rect.x + 10, name_rect.y + 10))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    # Create player
    player = Player(name.strip())
    
    # Play explore music
    if assets.explore_music:
        mixer.music.load(assets.explore_music)
        mixer.music.play(-1)
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Game logic based on location
        if player.location == "Greenfield Town":
            town_screen(player)
        else:
            explore_screen(player, enemies)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()