import pygame
import random
import os
import sys
import json
import time
from pygame import mixer
from enum import Enum

# Initialize pygame
pygame.init()
mixer.init()

# Game constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
TITLE = "Epic Adventure RPG: Enhanced Edition"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (100, 100, 100)
SILVER = (210, 180, 140)

town_screen = pygame.image.load("assets/images/town_bg.png")
explore_screen = pygame.image.load("assets/images/explore.png")

# Weather colors
RAIN_COLOR = (100, 100, 150, 100)
SNOW_COLOR = (200, 200, 255, 150)
SANDSTORM_COLOR = (210, 180, 140, 120)

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Fonts
font_small = pygame.font.SysFont('Arial', 18)
font_medium = pygame.font.SysFont('Arial', 24)
font_large = pygame.font.SysFont('Arial', 36)
font_title = pygame.font.SysFont('Arial', 48)

# Weather types
class Weather(Enum):
    CLEAR = 0
    RAIN = 1
    SNOW = 2
    SANDSTORM = 3

# Time of day
class TimeOfDay(Enum):
    DAWN = 0
    DAY = 1
    DUSK = 2
    NIGHT = 3

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
    QUEST = 8
    CRAFTING = 9
    SKILLS = 10
    MINIGAME = 11
    DIALOGUE = 12
    MAP = 13

def load_image(name, scale=1):
    try:
        # Remove .png if it was accidentally included in the name
        if name.endswith('.png'):
            name = name[:-4]
        image = pygame.image.load(f"assets/images/{name}.png").convert_alpha()
        if scale != 1:
            new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)
        return image
    except FileNotFoundError:
        # Create a placeholder surface if image not found
        print(f"Image not found: assets/images/{name}.png - creating placeholder")
        surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pygame.draw.rect(surf, color, (0, 0, 50, 50))
        pygame.draw.rect(surf, BLACK, (0, 0, 50, 50), 2)
        text = font_small.render(name[:3], True, BLACK)
        surf.blit(text, (25 - text.get_width()//2, 25 - text.get_height()//2))
        return surf

def load_sound(name):
    try:
        if name.endswith('.mp3'):
            name = name[:-4]
        return mixer.Sound(f"assets/sounds/{name}.mp3")
    except:
        print(f"Sound {name} not found! Using silent sound")
        # Return a silent sound
        return mixer.Sound(buffer=bytearray(44))

# Game assets
class Assets:
    def __init__(self):
        # Backgrounds
        self.main_menu_bg = load_image("main_menu_bg.png")
        self.forest_bg = load_image("forest_bg.png")
        self.town_bg = load_image("town_bg.png")
        self.cave_bg = load_image("cave_bg.png")
        self.castle_bg = load_image("castle_bg.png")
        self.desert_bg = load_image("desert_bg.png")
        self.swamp_bg = load_image("swamp_bg.png")
        self.beach_bg = load_image("beach_bg.png")
        self.mountain_bg = load_image("mountain_bg.png")
        self.map_bg = load_image("world_map.png")
        
        # Character sprites
        self.player_img = load_image("Player.png", 0.5)
        self.goblin_img = load_image("goblin.png", 0.5)
        self.wolf_img = load_image("wolf.png", 0.5)
        self.bandit_img = load_image("bandit.png", 0.5)
        self.orc_img = load_image("orc.png", 0.5)
        self.dragon_img = load_image("dragon.png", 0.5)
        self.skeleton_img = load_image("skeleton.png", 0.5)
        self.spider_img = load_image("spider.png", 0.5)
        self.merchant_img = load_image("merchant.png", 0.5)
        self.blacksmith_img = load_image("blacksmith.png", 0.5)
        self.quest_giver_img = load_image("quest_giver.png", 0.5)
        
        # Item icons
        self.sword_icon = load_image("sword_icon.png", 0.5)
        self.armor_icon = load_image("armor_icon.png", 0.5)
        self.potion_icon = load_image("potion_icon.png", 0.5)
        self.misc_icon = load_image("misc_icon.png", 0.5)
        self.gold_icon = load_image("gold_icon.png", 0.5)
        self.herb_icon = load_image("herb_icon.png", 0.5)
        self.ore_icon = load_image("ore_icon.png", 0.5)
        self.scroll_icon = load_image("scroll_icon.png", 0.5)
        self.key_icon = load_image("key_icon.png", 0.5)
        
        # UI elements
        self.button_img = load_image("button.png", 0.5)
        self.button_hover_img = load_image("button.png", 0.5)
        self.quest_icon = load_image("quest_icon.png", 0.5)
        self.skill_icon = load_image("skill_icon.png", 0.5)
        self.crafting_icon = load_image("crafting_icon.png", 0.5)
        
        # Weather effects
        self.rain_img = load_image("rain.png", 0.5)
        self.snow_img = load_image("snow.png", 0.5)
        
        # Sounds
        self.battle_music = "assets/sounds/battle.mp3"
        self.town_music = "assets/sounds/town.mp3"
        self.explore_music = "assets/sounds/explore.mp3"
        self.menu_music = "assets/sounds/menu.mp3"
        self.rain_sound = load_sound("rain.mp3")
        self.snow_sound = load_sound("snow.mp3")
        self.wind_sound = load_sound("wind.mp3")
        self.attack_sound = load_sound("attack.mp3")
        self.heal_sound = load_sound("heal.mp3")
        self.level_up_sound = load_sound("level_up.mp3")
        self.victory_sound = load_sound("victory.mp3")
        self.defeat_sound = load_sound("defeat.mp3")
        self.crafting_sound = load_sound("crafting.mp3")
        self.quest_complete_sound = load_sound("quest_complete.mp3")
        
assets = Assets()

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=GREEN, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)
        
        text_surf = font_medium.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

# Item class
class Item:
    def __init__(self, name, item_type, stat, value, icon=None, description="", craftable=False, materials=None):
        self.name = name
        self.type = item_type  # weapon, armor, potion, misc, material, recipe
        self.stat = stat  # attack for weapon, defense for armor, heal for potion
        self.value = value  # gold value
        self.icon = icon or self.get_default_icon()
        self.description = description or f"A {item_type} called {name}"
        self.craftable = craftable
        self.materials = materials or []
        
    def get_default_icon(self):
        if self.type == "weapon":
            return assets.sword_icon
        elif self.type == "armor":
            return assets.armor_icon
        elif self.type == "potion":
            return assets.potion_icon
        elif self.type == "material":
            return assets.herb_icon
        elif self.type == "recipe":
            return assets.scroll_icon
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

# Quest class
class Quest:
    def __init__(self, title, description, objective, reward_exp, reward_gold, reward_items=None, required_item=None, required_kills=None):
        self.title = title
        self.description = description
        self.objective = objective
        self.reward_exp = reward_exp
        self.reward_gold = reward_gold
        self.reward_items = reward_items or []
        self.required_item = required_item  # (item_name, quantity)
        self.required_kills = required_kills  # {enemy_name: quantity}
        self.completed = False
        self.turned_in = False
        self.current_kills = {}
        
        if required_kills:
            for enemy in required_kills:
                self.current_kills[enemy] = 0
    
    def update_kill(self, enemy_name):
        if self.required_kills and enemy_name in self.required_kills:
            self.current_kills[enemy_name] += 1
            return self.check_completion()
        return False
    
    def check_completion(self):
        if self.completed:
            return True
            
        # Check item requirement
        item_complete = True
        if self.required_item:
            item_complete = False
        
        # Check kill requirements
        kill_complete = True
        if self.required_kills:
            for enemy, quantity in self.required_kills.items():
                if self.current_kills.get(enemy, 0) < quantity:
                    kill_complete = False
                    break
        
        self.completed = item_complete and kill_complete
        return self.completed

# Skill class
class Skill:
    def __init__(self, name, description, max_level, stat_effects, required_level=1, parent_skill=None):
        self.name = name
        self.description = description
        self.max_level = max_level
        self.current_level = 0
        self.stat_effects = stat_effects  # {"attack": 2, "defense": 1}
        self.required_level = required_level
        self.parent_skill = parent_skill
        self.unlocked = False
    
    def can_upgrade(self, player_level):
        if self.current_level >= self.max_level:
            return False
        if self.parent_skill and self.parent_skill.current_level < self.parent_skill.max_level:
            return False
        return player_level >= self.required_level
    
    def upgrade(self):
        if self.current_level < self.max_level:
            self.current_level += 1
            return self.stat_effects
        return {}

# Crafting Recipe class
class CraftingRecipe:
    def __init__(self, name, result_item, materials_required, skill_required=None, skill_level=0):
        self.name = name
        self.result_item = result_item
        self.materials_required = materials_required  # {item_name: quantity}
        self.skill_required = skill_required
        self.skill_level = skill_level
    
    def can_craft(self, player_inventory, player_skills=None):
        # Check materials
        for item_name, quantity in self.materials_required.items():
            item_count = sum(1 for item in player_inventory if item.name == item_name)
            if item_count < quantity:
                return False
        
        # Check skill if required
        if self.skill_required and player_skills:
            skill = next((s for s in player_skills if s.name == self.skill_required), None)
            if not skill or skill.current_level < self.skill_level:
                return False
                
        return True

# Player class with new features
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
        self.quests = []
        self.active_quests = []
        self.completed_quests = []
        self.skills = []
        self.reputation = 0  # -100 to 100 scale
        self.play_time = 0  # in seconds
        self.game_start_time = time.time()
        self.weather_resistance = 0  # Reduces weather effects
        self.weather = Weather.CLEAR
        self.time_of_day = TimeOfDay.DAY
        self.day_count = 1
        
        # Initialize skills
        self.init_skills()
        
        # Starting items
        wooden_sword = Item("Wooden Sword", "weapon", 2, 5, assets.sword_icon, "A basic wooden training sword")
        leather_armor = Item("Leather Vest", "armor", 3, 20, assets.armor_icon, "Simple leather armor offering minimal protection")
        health_potion = Item("Small Health Potion", "potion", 20, 15, assets.potion_icon, "Restores a small amount of health")
        
        self.add_item(wooden_sword)
        self.add_item(leather_armor)
        self.add_item(health_potion)
        self.equip_item(wooden_sword)
        self.equip_item(leather_armor)
    
    def init_skills(self):
        # Combat skills
        sword_mastery = Skill("Sword Mastery", "Increases attack with swords", 5, {"attack": 2})
        heavy_armor = Skill("Heavy Armor", "Increases defense with heavy armor", 5, {"defense": 3})
        dual_wielding = Skill("Dual Wielding", "Allows wielding two one-handed weapons", 1, {}, 5, sword_mastery)
        
        # Crafting skills
        blacksmithing = Skill("Blacksmithing", "Allows crafting better weapons and armor", 5, {})
        alchemy = Skill("Alchemy", "Allows crafting better potions", 5, {})
        
        # Exploration skills
        survival = Skill("Survival", "Reduces weather effects and increases exploration rewards", 5, {"weather_resistance": 5})
        
        self.skills = [sword_mastery, heavy_armor, dual_wielding, blacksmithing, alchemy, survival]
    
    def update(self):
        # Update play time
        self.play_time = time.time() - self.game_start_time
        
        # Update time of day (cycles every 10 minutes of real time)
        time_segment = (self.play_time % 600) / 600  # 10 minutes = 600 seconds
        if time_segment < 0.1:
            self.time_of_day = TimeOfDay.DAWN
        elif time_segment < 0.4:
            self.time_of_day = TimeOfDay.DAY
        elif time_segment < 0.5:
            self.time_of_day = TimeOfDay.DUSK
        else:
            self.time_of_day = TimeOfDay.NIGHT
            self.day_count = int(self.play_time // 600) + 1
        
        # Random weather changes (10% chance every 10 seconds)
        if random.random() < 0.1 and int(self.play_time) % 10 == 0:
            weather_roll = random.random()
            if weather_roll < 0.6:
                self.weather = Weather.CLEAR
            elif weather_roll < 0.8:
                self.weather = Weather.RAIN
            elif weather_roll < 0.95:
                self.weather = Weather.SNOW
            else:
                self.weather = Weather.SANDSTORM
    
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
        self.attack += 2  # Base increase, skills will add more
        self.defense += 1  # Base increase, skills will add more
        
        if assets.level_up_sound:
            assets.level_up_sound.play()
        
    def take_damage(self, damage):
        # Weather can affect combat
        weather_multiplier = 1.0
        if self.weather == Weather.RAIN:
            weather_multiplier = 0.9  # Rain makes combat slightly easier
        elif self.weather == Weather.SANDSTORM:
            weather_multiplier = 1.2  # Sandstorm makes combat harder
        
        actual_damage = max(1, (damage - self.defense) * weather_multiplier)
        self.hp -= actual_damage
        return actual_damage
        
    def is_alive(self):
        return self.hp > 0
        
    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
        if assets.heal_sound:
            assets.heal_sound.play()
        
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
    
    def add_quest(self, quest):
        if quest not in self.quests and quest not in self.active_quests and quest not in self.completed_quests:
            self.quests.append(quest)
            return True
        return False
    
    def start_quest(self, quest):
        if quest in self.quests:
            self.quests.remove(quest)
            self.active_quests.append(quest)
            return True
        return False
    
    def complete_quest(self, quest):
        if quest in self.active_quests and quest.completed:
            self.active_quests.remove(quest)
            self.completed_quests.append(quest)
            
            # Give rewards
            self.add_exp(quest.reward_exp)
            self.gold += quest.reward_gold
            for item in quest.reward_items:
                self.add_item(item)
            
            # Reputation gain
            self.reputation = min(100, self.reputation + 5)
            
            if assets.quest_complete_sound:
                assets.quest_complete_sound.play()
            
            return True
        return False
    
    def upgrade_skill(self, skill_name):
        skill = next((s for s in self.skills if s.name == skill_name), None)
        if skill and skill.can_upgrade(self.level):
            stat_increases = skill.upgrade()
            
            # Apply stat increases
            for stat, value in stat_increases.items():
                if stat == "attack":
                    self.attack += value
                elif stat == "defense":
                    self.defense += value
                elif stat == "weather_resistance":
                    self.weather_resistance += value
            
            return True
        return False
    
    def save_game(self, filename="savegame.json"):
        save_data = {
            "name": self.name,
            "level": self.level,
            "exp": self.exp,
            "exp_to_level": self.exp_to_level,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack,
            "defense": self.defense,
            "gold": self.gold,
            "inventory": [{"name": item.name, "type": item.type, "stat": item.stat, 
                          "value": item.value, "description": item.description} 
                         for item in self.inventory],
            "equipped_weapon": self.equipped_weapon.name if self.equipped_weapon else None,
            "equipped_armor": self.equipped_armor.name if self.equipped_armor else None,
            "location": self.location,
            "locations_unlocked": self.locations_unlocked,
            "quests": [{
                "title": q.title,
                "description": q.description,
                "objective": q.objective,
                "reward_exp": q.reward_exp,
                "reward_gold": q.reward_gold,
                "reward_items": [{"name": i.name, "type": i.type, "stat": i.stat, 
                                 "value": i.value, "description": i.description} 
                                for i in q.reward_items],
                "required_item": q.required_item,
                "required_kills": q.required_kills,
                "completed": q.completed,
                "turned_in": q.turned_in,
                "current_kills": q.current_kills
            } for q in self.quests + self.active_quests + self.completed_quests],
            "skills": [{
                "name": s.name,
                "description": s.description,
                "max_level": s.max_level,
                "current_level": s.current_level,
                "stat_effects": s.stat_effects,
                "required_level": s.required_level,
                "parent_skill": s.parent_skill.name if s.parent_skill else None
            } for s in self.skills],
            "reputation": self.reputation,
            "play_time": self.play_time,
            "day_count": self.day_count
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(save_data, f, indent=4)
            return True
        except:
            return False
    
    @classmethod
    def load_game(cls, filename="savegame.json"):
        try:
            with open(filename, 'r') as f:
                save_data = json.load(f)
            
            player = cls(save_data["name"])
            player.level = save_data["level"]
            player.exp = save_data["exp"]
            player.exp_to_level = save_data["exp_to_level"]
            player.hp = save_data["hp"]
            player.max_hp = save_data["max_hp"]
            player.attack = save_data["attack"]
            player.defense = save_data["defense"]
            player.gold = save_data["gold"]
            player.location = save_data["location"]
            player.locations_unlocked = save_data["locations_unlocked"]
            player.reputation = save_data["reputation"]
            player.play_time = save_data["play_time"]
            player.day_count = save_data["day_count"]
            
            # Rebuild inventory
            player.inventory = []
            for item_data in save_data["inventory"]:
                item = Item(
                    item_data["name"],
                    item_data["type"],
                    item_data["stat"],
                    item_data["value"],
                    description=item_data["description"]
                )
                player.inventory.append(item)
            
            # Rebuild equipped items
            if save_data["equipped_weapon"]:
                weapon = next((i for i in player.inventory if i.name == save_data["equipped_weapon"]), None)
                if weapon:
                    player.equip_item(weapon)
            
            if save_data["equipped_armor"]:
                armor = next((i for i in player.inventory if i.name == save_data["equipped_armor"]), None)
                if armor:
                    player.equip_item(armor)
            
            # Rebuild quests
            player.quests = []
            player.active_quests = []
            player.completed_quests = []
            
            for quest_data in save_data["quests"]:
                reward_items = []
                for item_data in quest_data["reward_items"]:
                    item = Item(
                        item_data["name"],
                        item_data["type"],
                        item_data["stat"],
                        item_data["value"],
                        description=item_data["description"]
                    )
                    reward_items.append(item)
                
                quest = Quest(
                    quest_data["title"],
                    quest_data["description"],
                    quest_data["objective"],
                    quest_data["reward_exp"],
                    quest_data["reward_gold"],
                    reward_items,
                    quest_data["required_item"],
                    quest_data["required_kills"]
                )
                quest.completed = quest_data["completed"]
                quest.turned_in = quest_data["turned_in"]
                quest.current_kills = quest_data["current_kills"]
                
                if not quest.turned_in:
                    if quest.completed:
                        player.active_quests.append(quest)
                    else:
                        player.quests.append(quest)
                else:
                    player.completed_quests.append(quest)
            
            # Rebuild skills
            player.skills = []
            for skill_data in save_data["skills"]:
                skill = Skill(
                    skill_data["name"],
                    skill_data["description"],
                    skill_data["max_level"],
                    skill_data["stat_effects"],
                    skill_data["required_level"]
                )
                skill.current_level = skill_data["current_level"]
                player.skills.append(skill)
            
            # Rebuild skill parent relationships
            for skill_data in save_data["skills"]:
                if skill_data["parent_skill"]:
                    child = next(s for s in player.skills if s.name == skill_data["name"])
                    parent = next(s for s in player.skills if s.name == skill_data["parent_skill"])
                    child.parent_skill = parent
            
            player.game_start_time = time.time() - player.play_time
            return player
        except:
            return None

# Enemy class with weather effects
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
        self.weather_effects = {
            Weather.RAIN: {"attack_multiplier": 0.9, "defense_multiplier": 1.0},
            Weather.SNOW: {"attack_multiplier": 1.0, "defense_multiplier": 1.1},
            Weather.SANDSTORM: {"attack_multiplier": 1.1, "defense_multiplier": 0.9},
            Weather.CLEAR: {"attack_multiplier": 1.0, "defense_multiplier": 1.0}
        }
        
    def add_loot(self, item, chance):
        self.loot_table.append((item, chance))
        
    def generate_loot(self):
        loot = []
        for item, chance in self.loot_table:
            if random.random() < chance:
                loot.append(item)
        return loot
        
    def take_damage(self, damage, weather):
        # Apply weather effects
        weather_effect = self.weather_effects.get(weather, self.weather_effects[Weather.CLEAR])
        actual_defense = self.defense * weather_effect["defense_multiplier"]
        actual_damage = max(1, damage - actual_defense)
        self.hp -= actual_damage
        return actual_damage
        
    def is_alive(self):
        return self.hp > 0
    
    def get_attack_power(self, weather):
        weather_effect = self.weather_effects.get(weather, self.weather_effects[Weather.CLEAR])
        return self.attack * weather_effect["attack_multiplier"]

# Create enemies with more variety
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
    
    skeleton = Enemy("Skeleton Warrior", 4, 60, 25, 10, 80, 50, assets.skeleton_img)
    skeleton.add_loot(Item("Bone Fragments", "misc", 0, 20, assets.misc_icon), 0.8)
    skeleton.add_loot(Item("Ancient Sword", "weapon", 10, 80, assets.sword_icon), 0.2)
    enemies.append(skeleton)
    
    giant_spider = Enemy("Giant Spider", 5, 100, 18, 5, 90, 60, assets.spider_img)
    giant_spider.add_loot(Item("Spider Silk", "material", 0, 40, assets.misc_icon), 0.7)
    giant_spider.add_loot(Item("Spider Venom", "material", 0, 60, assets.misc_icon), 0.4)
    enemies.append(giant_spider)
    
    # Boss enemies
    dragon = Enemy("Ancient Dragon", 10, 300, 40, 20, 500, 200, assets.dragon_img, True)
    dragon.add_loot(Item("Dragon Scale Armor", "armor", 25, 300, assets.armor_icon), 1.0)
    dragon.add_loot(Item("Dragonbone Sword", "weapon", 30, 400, assets.sword_icon), 1.0)
    dragon.add_loot(Item("Large Health Potion", "potion", 60, 40, assets.potion_icon), 0.8)
    enemies.append(dragon)
    
    return enemies

# Create items with more variety and crafting materials
def create_items():
    items = []
    
    # Weapons
    items.append(Item("Wooden Sword", "weapon", 2, 10, assets.sword_icon, "A basic wooden training sword"))
    items.append(Item("Iron Sword", "weapon", 5, 30, assets.sword_icon, "A standard iron sword"))
    items.append(Item("Steel Sword", "weapon", 8, 60, assets.sword_icon, "A well-made steel sword"))
    items.append(Item("Silver Sword", "weapon", 12, 100, assets.sword_icon, "A sword made of silver, effective against undead"))
    items.append(Item("Dragonbone Sword", "weapon", 30, 400, assets.sword_icon, "A powerful sword made from dragon bones"))
    
    # Armor
    items.append(Item("Leather Vest", "armor", 3, 20, assets.armor_icon, "Simple leather armor offering minimal protection"))
    items.append(Item("Chainmail", "armor", 7, 50, assets.armor_icon, "Flexible chainmail armor"))
    items.append(Item("Plate Armor", "armor", 12, 100, assets.armor_icon, "Heavy plate armor offering excellent protection"))
    items.append(Item("Silver Armor", "armor", 18, 200, assets.armor_icon, "Armor made of silver, effective against undead"))
    items.append(Item("Dragon Scale Armor", "armor", 25, 300, assets.armor_icon, "Armor made from dragon scales"))
    
    # Potions
    items.append(Item("Small Health Potion", "potion", 20, 15, assets.potion_icon, "Restores a small amount of health"))
    items.append(Item("Medium Health Potion", "potion", 35, 25, assets.potion_icon, "Restores a moderate amount of health"))
    items.append(Item("Large Health Potion", "potion", 60, 40, assets.potion_icon, "Restores a large amount of health"))
    items.append(Item("Elixir of Life", "potion", 100, 100, assets.potion_icon, "Fully restores health"))
    
    # Materials
    items.append(Item("Herbs", "material", 0, 5, assets.herb_icon, "Common herbs used in potion making"))
    items.append(Item("Rare Herbs", "material", 0, 15, assets.herb_icon, "Rare herbs used in advanced potions"))
    items.append(Item("Iron Ore", "material", 0, 10, assets.ore_icon, "Iron ore that can be smelted"))
    items.append(Item("Silver Ore", "material", 0, 30, assets.ore_icon, "Silver ore that can be smelted"))
    items.append(Item("Dragon Scales", "material", 0, 100, assets.misc_icon, "Rare scales from a dragon"))
    items.append(Item("Spider Silk", "material", 0, 40, assets.misc_icon, "Strong silk from giant spiders"))
    
    # Recipes
    items.append(Item("Health Potion Recipe", "recipe", 0, 50, assets.scroll_icon, 
                     "Teaches how to craft health potions", True, {"Herbs": 3}))
    items.append(Item("Iron Sword Recipe", "recipe", 0, 80, assets.scroll_icon, 
                     "Teaches how to craft iron swords", True, {"Iron Ore": 2}))
    
    # Misc
    items.append(Item("Ancient Key", "misc", 0, 0, assets.key_icon, "An ancient key to unlock hidden areas"))
    items.append(Item("Treasure Map", "misc", 0, 50, assets.misc_icon, "A map leading to hidden treasure"))
    
    return items

# Create quests
def create_quests():
    quests = []
    
    # Starting quest
    starting_quest = Quest(
        "Goblin Menace",
        "The local goblins have been causing trouble. Thin their numbers.",
        "Defeat 5 Goblins",
        100,
        50,
        [Item("Iron Sword", "weapon", 5, 30, assets.sword_icon)],
        None,
        {"Goblin": 5}
    )
    quests.append(starting_quest)
    
    # Collection quest
    herb_quest = Quest(
        "Herbalist's Request",
        "The town herbalist needs rare herbs for medicine.",
        "Collect 10 Herbs",
        150,
        75,
        [Item("Medium Health Potion", "potion", 35, 25, assets.potion_icon)],
        ("Herbs", 10)
    )
    quests.append(herb_quest)
    
    # Boss quest
    dragon_quest = Quest(
        "Dragon Slayer",
        "The ancient dragon threatens the kingdom. Slay the beast!",
        "Defeat the Ancient Dragon",
        500,
        200,
        [
            Item("Dragon Scale Armor", "armor", 25, 300, assets.armor_icon),
            Item("Dragonbone Sword", "weapon", 30, 400, assets.sword_icon)
        ],
        None,
        {"Ancient Dragon": 1}
    )
    quests.append(dragon_quest)
    
    return quests

# Create crafting recipes
def create_crafting_recipes():
    recipes = []
    
    # Potions
    recipes.append(CraftingRecipe(
        "Small Health Potion",
        Item("Small Health Potion", "potion", 20, 15, assets.potion_icon),
        {"Herbs": 3}
    ))
    
    recipes.append(CraftingRecipe(
        "Medium Health Potion",
        Item("Medium Health Potion", "potion", 35, 25, assets.potion_icon),
        {"Rare Herbs": 2, "Herbs": 5},
        "Alchemy",
        2
    ))
    
    # Weapons
    recipes.append(CraftingRecipe(
        "Iron Sword",
        Item("Iron Sword", "weapon", 5, 30, assets.sword_icon),
        {"Iron Ore": 2},
        "Blacksmithing",
        1
    ))
    
    recipes.append(CraftingRecipe(
        "Steel Sword",
        Item("Steel Sword", "weapon", 8, 60, assets.sword_icon),
        {"Iron Ore": 5},
        "Blacksmithing",
        3
    ))
    
    return recipes

# NPC class
class NPC:
    def __init__(self, name, image, dialogue, quests=None, shop_items=None, is_merchant=False, is_quest_giver=False):
        self.name = name
        self.image = image
        self.dialogue = dialogue
        self.quests = quests or []
        self.shop_items = shop_items or []
        self.is_merchant = is_merchant
        self.is_quest_giver = is_quest_giver
    
    def interact(self, player):
        # This would open a dialogue screen with options based on NPC type
        options = ["Talk"]
        
        if self.is_merchant:
            options.append("Shop")
        if self.is_quest_giver and self.quests:
            options.append("Quests")
        
        selected_option = show_dialogue_options(self.name, self.dialogue, options)
        
        if selected_option == "Shop" and self.is_merchant:
            # Open shop with this NPC's items
            pass
        elif selected_option == "Quests" and self.is_quest_giver:
            # Show available quests
            pass
    
    def give_quest(self, player, quest):
        if quest in self.quests:
            player.add_quest(quest)
            return True
        return False

# Dialogue system
def show_dialogue(npc_name, text):
    # Create a dialogue box
    dialogue_box = pygame.Surface((800, 200), pygame.SRCALPHA)
    dialogue_box.fill((0, 0, 0, 200))
    pygame.draw.rect(dialogue_box, WHITE, (0, 0, 800, 200), 2)
    
    # Draw NPC name
    name_text = font_medium.render(npc_name, True, YELLOW)
    dialogue_box.blit(name_text, (20, 20))
    
    # Draw dialogue text (wrapped)
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        if font_small.size(test_line)[0] < 760:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    
    if current_line:
        lines.append(current_line)
    
    for i, line in enumerate(lines):
        line_text = font_small.render(line, True, WHITE)
        dialogue_box.blit(line_text, (20, 60 + i * 30))
    
    # Draw to screen
    screen.blit(dialogue_box, (SCREEN_WIDTH//2 - 400, SCREEN_HEIGHT - 220))
    
    # Draw continue prompt
    continue_text = font_small.render("Press any key to continue...", True, WHITE)
    screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, SCREEN_HEIGHT - 30))
    
    pygame.display.flip()
    
    # Wait for key press
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def show_dialogue_options(npc_name, text, options):
    selected_option = 0
    
    while True:
        # Create a dialogue box
        dialogue_box = pygame.Surface((800, 200 + len(options) * 50), pygame.SRCALPHA)
        dialogue_box.fill((0, 0, 0, 200))
        pygame.draw.rect(dialogue_box, WHITE, (0, 0, 800, 200 + len(options) * 50), 2)
        
        # Draw NPC name
        name_text = font_medium.render(npc_name, True, YELLOW)
        dialogue_box.blit(name_text, (20, 20))
        
        # Draw dialogue text
        dialogue_text = font_small.render(text, True, WHITE)
        dialogue_box.blit(dialogue_text, (20, 60))
        
        # Draw options
        for i, option in enumerate(options):
            color = YELLOW if i == selected_option else WHITE
            option_text = font_medium.render(option, True, color)
            dialogue_box.blit(option_text, (50, 150 + i * 50))
        
        # Draw to screen
        screen.blit(dialogue_box, (SCREEN_WIDTH//2 - 400, SCREEN_HEIGHT - 220 - len(options) * 50))
        
        pygame.display.flip()
        
        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = max(0, selected_option - 1)
                elif event.key == pygame.K_DOWN:
                    selected_option = min(len(options) - 1, selected_option + 1)
                elif event.key == pygame.K_RETURN:
                    return options[selected_option]
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                option_y_start = SCREEN_HEIGHT - 220 - len(options) * 50 + 150
                
                for i in range(len(options)):
                    option_rect = pygame.Rect(SCREEN_WIDTH//2 - 400 + 50, option_y_start + i * 50, 
                                            700, 40)
                    if option_rect.collidepoint(mouse_pos):
                        return options[i]

# Weather effects
def draw_weather_effect(weather):
    if weather == Weather.RAIN:
        # Create rain effect
        rain_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        rain_surface.fill(RAIN_COLOR)
        
        # Draw rain drops
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.line(rain_surface, (200, 200, 255), (x, y), (x - 10, y + 20), 1)
        
        screen.blit(rain_surface, (0, 0))
        
        # Play rain sound
        if assets.rain_sound and not mixer.Channel(1).get_busy():
            mixer.Channel(1).play(assets.rain_sound, loops=-1)
    
    elif weather == Weather.SNOW:
        # Create snow effect
        snow_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        snow_surface.fill(SNOW_COLOR)
        
        # Draw snow flakes
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.circle(snow_surface, WHITE, (x, y), random.randint(1, 3))
        
        screen.blit(snow_surface, (0, 0))
        
        # Play snow sound
        if assets.snow_sound and not mixer.Channel(1).get_busy():
            mixer.Channel(1).play(assets.snow_sound, loops=-1)
    
    elif weather == Weather.SANDSTORM:
        # Create sandstorm effect
        sand_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        sand_surface.fill(SANDSTORM_COLOR)
        
        # Draw sand particles
        for _ in range(150):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.circle(sand_surface, (210, 180, 140), (x, y), random.randint(1, 2))
        
        screen.blit(sand_surface, (0, 0))
        
        # Play wind sound
        if assets.wind_sound and not mixer.Channel(1).get_busy():
            mixer.Channel(1).play(assets.wind_sound, loops=-1)
    
    else:
        # Clear weather - stop any weather sounds
        mixer.Channel(1).stop()

# Time of day effects
def draw_time_effect(time_of_day):
    time_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    
    if time_of_day == TimeOfDay.DAWN:
        time_surface.fill((255, 200, 150, 50))
    elif time_of_day == TimeOfDay.DUSK:
        time_surface.fill((100, 50, 150, 70))
    elif time_of_day == TimeOfDay.NIGHT:
        time_surface.fill((0, 0, 100, 120))
    
    if time_of_day != TimeOfDay.DAY:
        screen.blit(time_surface, (0, 0))

# Mini-game: Fishing
def fishing_minigame(player):
    result = None
    progress = 0
    fish_rect = pygame.Rect(SCREEN_WIDTH//2 - 25, 400, 50, 20)
    catch_zone = pygame.Rect(SCREEN_WIDTH//2 - 100, 300, 200, 100)
    fish_speed = 3
    direction = 1  # 1 for right, -1 for left
    
    # Create buttons
    cast_btn = Button(SCREEN_WIDTH//2 - 100, 600, 200, 50, "Cast Line")
    back_btn = Button(50, 50, 100, 50, "Back")
    
    while result is None:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cast_btn.is_clicked(mouse_pos, event) and progress == 0:
                    progress = 1  # Fishing in progress
                    cast_btn.text = "Reel In!"
                elif cast_btn.is_clicked(mouse_pos, event) and progress == 1:
                    # Check if fish is in catch zone
                    if catch_zone.contains(fish_rect):
                        # Successful catch
                        fish_type = random.choice(["Small Fish", "Medium Fish", "Large Fish", "Rare Fish"])
                        gold_earned = random.randint(10, 50)
                        player.gold += gold_earned
                        show_message(f"Caught a {fish_type}! Earned {gold_earned} gold!")
                    else:
                        show_message("The fish got away!")
                    
                    progress = 0
                    cast_btn.text = "Cast Line"
                    fish_rect.x = SCREEN_WIDTH//2 - 25
                
                if back_btn.is_clicked(mouse_pos, event):
                    return
        
        # Update fishing progress
        if progress == 1:
            # Move fish
            fish_rect.x += fish_speed * direction
            
            # Change direction if at edge
            if fish_rect.right > SCREEN_WIDTH:
                direction = -1
            elif fish_rect.left < 0:
                direction = 1
            
            # Randomly change speed
            if random.random() < 0.02:
                fish_speed = random.randint(2, 5)
        
        # Draw fishing screen
        screen.fill(BLUE)
        
        # Draw water
        pygame.draw.rect(screen, (0, 100, 200), (0, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT//2))
        
        # Draw fishing interface
        pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH//2 - 150, 200, 300, 300), 2)
        pygame.draw.rect(screen, (0, 0, 0, 50), catch_zone)
        
        # Draw fish
        pygame.draw.ellipse(screen, ORANGE, fish_rect)
        
        # Draw buttons
        if progress == 0:
            cast_btn.draw(screen)
        else:
            # Draw reel button only when fish is in catch zone
            if catch_zone.contains(fish_rect):
                cast_btn.color = GREEN
                cast_btn.hover_color = YELLOW
                cast_btn.draw(screen)
            else:
                cast_btn.color = RED
                cast_btn.hover_color = ORANGE
                cast_btn.draw(screen)
        
        back_btn.draw(screen)
        
        # Draw instructions
        if progress == 0:
            instr_text = font_medium.render("Cast your line to start fishing!", True, WHITE)
        else:
            instr_text = font_medium.render("Reel in when the fish is in the dark area!", True, WHITE)
        
        screen.blit(instr_text, (SCREEN_WIDTH//2 - instr_text.get_width()//2, 150))
        
        pygame.display.flip()
        clock.tick(FPS)

# Mini-game: Lockpicking
def lockpicking_minigame(player):
    result = None
    difficulty = min(max(player.level // 2, 1), 10)  # Scale with player level
    pick_position = 0
    tension = 0
    lock_positions = [random.randint(10, 90) for _ in range(difficulty)]
    current_lock = 0
    pick_speed = 2
    
    # Create buttons
    back_btn = Button(50, 50, 100, 50, "Back")
    
    while result is None:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Apply tension
                    tension = 1
                    
                    # Check if pick is in correct position
                    if abs(pick_position - lock_positions[current_lock]) < 5:
                        current_lock += 1
                        if current_lock >= len(lock_positions):
                            # Lock opened
                            gold_earned = random.randint(20, 100)
                            player.gold += gold_earned
                            show_message(f"Lock picked! Found {gold_earned} gold!")
                            return
                    else:
                        # Failed - reset progress
                        current_lock = 0
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    tension = 0
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.is_clicked(mouse_pos, event):
                    return
        
        # Move pick with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pick_position = max(0, pick_position - pick_speed)
        if keys[pygame.K_RIGHT]:
            pick_position = min(100, pick_position + pick_speed)
        
        # Draw lockpicking screen
        screen.fill(BLACK)
        
        # Draw lock
        pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH//2 - 150, 200, 300, 100), 2)
        
        # Draw pins
        for i in range(difficulty):
            pin_height = 30 if i >= current_lock else 10
            pygame.draw.rect(screen, GOLD, 
                            (SCREEN_WIDTH//2 - 120 + i * (240 // difficulty), 
                             200, 
                             10, 
                             pin_height))
        
        # Draw pick
        pick_x = SCREEN_WIDTH//2 - 120 + pick_position * 2.4
        pygame.draw.polygon(screen, SILVER, 
                           [(pick_x, 350), (pick_x - 10, 370), (pick_x + 10, 370)])
        
        # Draw tension wrench
        if tension:
            pygame.draw.rect(screen, SILVER, (SCREEN_WIDTH//2 - 10, 340, 20, 10))
        
        # Draw instructions
        instr_text = font_medium.render("Use LEFT/RIGHT to move pick, SPACE to apply tension", True, WHITE)
        screen.blit(instr_text, (SCREEN_WIDTH//2 - instr_text.get_width()//2, 400))
        
        diff_text = font_small.render(f"Difficulty: {difficulty}/10", True, WHITE)
        screen.blit(diff_text, (SCREEN_WIDTH//2 - diff_text.get_width()//2, 450))
        
        back_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

# Crafting screen
def crafting_screen(player, recipes):
    selected_recipe = None
    can_craft = False
    
    # Create buttons
    craft_btn = Button(700, 600, 150, 50, "Craft")
    back_btn = Button(850, 600, 150, 50, "Back")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check recipe selection
                for i, recipe in enumerate(recipes):
                    col = i % 5
                    row = i // 5
                    item_rect = pygame.Rect(50 + col * 110, 150 + row * 110, 100, 100)
                    if item_rect.collidepoint(mouse_pos):
                        selected_recipe = recipe
                        can_craft = recipe.can_craft(player.inventory, player.skills)
                
                # Check button clicks
                if back_btn.is_clicked(mouse_pos, event):
                    return
                
                if selected_recipe and craft_btn.is_clicked(mouse_pos, event) and can_craft:
                    # Remove materials
                    for mat_name, quantity in selected_recipe.materials_required.items():
                        for _ in range(quantity):
                            item_to_remove = next((i for i in player.inventory if i.name == mat_name), None)
                            if item_to_remove:
                                player.inventory.remove(item_to_remove)
                    
                    # Add crafted item
                    player.add_item(selected_recipe.result_item)
                    
                    if assets.crafting_sound:
                        assets.crafting_sound.play()
                    
                    show_message(f"Crafted {selected_recipe.result_item.name}!")
                    selected_recipe = None
        
        # Update button hover states
        back_btn.check_hover(mouse_pos)
        if selected_recipe and can_craft:
            craft_btn.check_hover(mouse_pos)
        
        # Draw crafting screen
        screen.fill(BLACK)
        
        # Draw background
        screen.blit(assets.town_bg, (0, 0))
        
        # Draw title
        title_text = font_large.render("Crafting", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        
        # Draw recipes
        for i, recipe in enumerate(recipes):
            col = i % 5
            row = i // 5
            x = 50 + col * 110
            y = 150 + row * 110
            
            # Draw recipe result icon
            recipe.result_item.draw(screen, x, y, selected_recipe == recipe)
            
            # Draw indicator if can't craft
            if not recipe.can_craft(player.inventory, player.skills):
                pygame.draw.rect(screen, (255, 0, 0, 100), (x, y, 100, 100))
        
        # Draw selected recipe info
        if selected_recipe:
            info_text = [
                f"Name: {selected_recipe.result_item.name}",
                f"Type: {selected_recipe.result_item.type.capitalize()}",
                f"Materials Required:"
            ]
            
            # Add materials
            for mat, qty in selected_recipe.materials_required.items():
                info_text.append(f" - {mat}: {qty}")
            
            # Add skill requirement if needed
            if selected_recipe.skill_required:
                info_text.append(f"Requires: {selected_recipe.skill_required} (Level {selected_recipe.skill_level})")
            
            # Draw info
            for i, text in enumerate(info_text):
                text_surf = font_small.render(text, True, WHITE)
                screen.blit(text_surf, (700, 150 + i * 25))
            
            # Draw craft button if possible
            if can_craft:
                craft_btn.draw(screen)
        
        back_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

# Skills screen
def skills_screen(player):
    selected_skill = None
    
    # Create buttons
    upgrade_btn = Button(700, 600, 150, 50, "Upgrade")
    back_btn = Button(850, 600, 150, 50, "Back")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check skill selection
                for i, skill in enumerate(player.skills):
                    col = i % 3
                    row = i // 3
                    skill_rect = pygame.Rect(50 + col * 300, 150 + row * 100, 280, 80)
                    if skill_rect.collidepoint(mouse_pos):
                        selected_skill = skill
                
                # Check button clicks
                if back_btn.is_clicked(mouse_pos, event):
                    return
                
                if selected_skill and upgrade_btn.is_clicked(mouse_pos, event):
                    if player.upgrade_skill(selected_skill.name):
                        show_message(f"{selected_skill.name} upgraded to level {selected_skill.current_level}!")
                    else:
                        show_message("Cannot upgrade this skill!")
        
        # Update button hover states
        back_btn.check_hover(mouse_pos)
        if selected_skill and selected_skill.can_upgrade(player.level):
            upgrade_btn.check_hover(mouse_pos)
        
        # Draw skills screen
        screen.fill(BLACK)
        
        # Draw background
        screen.blit(assets.town_bg, (0, 0))
        
        # Draw title
        title_text = font_large.render("Skills", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        
        # Draw skill points
        points_text = font_medium.render(f"Available Skill Points: {player.level - sum(s.current_level for s in player.skills)}", True, WHITE)
        screen.blit(points_text, (50, 100))
        
        # Draw skills
        for i, skill in enumerate(player.skills):
            col = i % 3
            row = i // 3
            x = 50 + col * 300
            y = 150 + row * 100
            
            # Draw skill box
            color = YELLOW if selected_skill == skill else BLUE
            pygame.draw.rect(screen, color, (x, y, 280, 80), border_radius=5)
            pygame.draw.rect(screen, BLACK, (x, y, 280, 80), 2, border_radius=5)
            
            # Draw skill name and level
            name_text = font_medium.render(f"{skill.name} (Lvl {skill.current_level}/{skill.max_level})", True, BLACK)
            screen.blit(name_text, (x + 10, y + 10))
            
            # Draw skill description
            desc_text = font_small.render(skill.description, True, BLACK)
            screen.blit(desc_text, (x + 10, y + 35))
            
            # Draw requirements if not unlocked
            if not skill.can_upgrade(player.level):
                req_text = font_small.render(f"Req: Lvl {skill.required_level}", True, RED)
                screen.blit(req_text, (x + 10, y + 55))
        
        # Draw selected skill info
        if selected_skill:
            info_text = [
                f"Name: {selected_skill.name}",
                f"Level: {selected_skill.current_level}/{selected_skill.max_level}",
                f"Description: {selected_skill.description}",
                f"Effects:"
            ]
            
            # Add effects
            for stat, value in selected_skill.stat_effects.items():
                info_text.append(f" - {stat.capitalize()}: +{value * selected_skill.current_level}")
            
            # Add requirements
            if selected_skill.parent_skill:
                info_text.append(f"Requires: {selected_skill.parent_skill.name} (Max Level)")
            
            info_text.append(f"Player Level Required: {selected_skill.required_level}")
            
            # Draw info
            for i, text in enumerate(info_text):
                text_surf = font_small.render(text, True, WHITE)
                screen.blit(text_surf, (700, 150 + i * 25))
            
            # Draw upgrade button if possible
            if selected_skill.can_upgrade(player.level):
                upgrade_btn.draw(screen)
        
        back_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

# Quest screen
def quest_screen(player):
    selected_quest = None
    show_active = True  # Toggle between active and available quests
    
    # Create buttons
    toggle_btn = Button(50, 100, 200, 50, "Show Available" if show_active else "Show Active")
    accept_btn = Button(700, 600, 150, 50, "Accept")
    complete_btn = Button(700, 600, 150, 50, "Complete")
    back_btn = Button(850, 600, 150, 50, "Back")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check quest selection
                quest_list = player.active_quests if show_active else player.quests
                for i, quest in enumerate(quest_list):
                    quest_rect = pygame.Rect(50, 170 + i * 100, 600, 80)
                    if quest_rect.collidepoint(mouse_pos):
                        selected_quest = quest
                
                # Check button clicks
                if back_btn.is_clicked(mouse_pos, event):
                    return
                
                if toggle_btn.is_clicked(mouse_pos, event):
                    show_active = not show_active
                    toggle_btn.text = "Show Available" if show_active else "Show Active"
                    selected_quest = None
                
                if selected_quest:
                    if show_active and complete_btn.is_clicked(mouse_pos, event):
                        if selected_quest.completed:
                            player.complete_quest(selected_quest)
                            selected_quest = None
                    elif not show_active and accept_btn.is_clicked(mouse_pos, event):
                        player.start_quest(selected_quest)
                        selected_quest = None
                        show_active = True
                        toggle_btn.text = "Show Available"
        
        # Update button hover states
        back_btn.check_hover(mouse_pos)
        toggle_btn.check_hover(mouse_pos)
        
        if selected_quest:
            if show_active:
                complete_btn.check_hover(mouse_pos)
            else:
                accept_btn.check_hover(mouse_pos)
        
        # Draw quest screen
        screen.fill(BLACK)
        
        # Draw background
        screen.blit(assets.town_bg, (0, 0))
        
        # Draw title
        title_text = font_large.render("Active Quests" if show_active else "Available Quests", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        
        # Draw toggle button
        toggle_btn.draw(screen)
        
        # Draw quests
        quest_list = player.active_quests if show_active else player.quests
        for i, quest in enumerate(quest_list):
            # Draw quest box
            color = YELLOW if selected_quest == quest else BLUE
            pygame.draw.rect(screen, color, (50, 170 + i * 100, 600, 80), border_radius=5)
            pygame.draw.rect(screen, BLACK, (50, 170 + i * 100, 600, 80), 2, border_radius=5)
            
            # Draw quest info
            title_text = font_medium.render(quest.title, True, BLACK)
            screen.blit(title_text, (70, 180 + i * 100))
            
            status_text = font_small.render("(Completed)" if quest.completed else "(In Progress)", True, BLACK)
            screen.blit(status_text, (70, 210 + i * 100))
            
            objective_text = font_small.render(f"Objective: {quest.objective}", True, BLACK)
            screen.blit(objective_text, (70, 230 + i * 100))
        
        # Draw selected quest info
        if selected_quest:
            info_text = [
                f"Title: {selected_quest.title}",
                f"Description: {selected_quest.description}",
                f"Objective: {selected_quest.objective}",
                f"Reward: {selected_quest.reward_exp} EXP, {selected_quest.reward_gold} gold"
            ]
            
            # Add reward items
            if selected_quest.reward_items:
                info_text.append("Reward Items:")
                for item in selected_quest.reward_items:
                    info_text.append(f" - {item.name}")
            
            # Add progress for active quests
            if show_active and selected_quest.required_kills:
                info_text.append("Progress:")
                for enemy, quantity in selected_quest.required_kills.items():
                    current = selected_quest.current_kills.get(enemy, 0)
                    info_text.append(f" - {enemy}: {current}/{quantity}")
            
            # Draw info
            for i, text in enumerate(info_text):
                text_surf = font_small.render(text, True, WHITE)
                screen.blit(text_surf, (700, 150 + i * 25))
            
            # Draw appropriate action button
            if show_active:
                if selected_quest.completed:
                    complete_btn.draw(screen)
            else:
                accept_btn.draw(screen)
        
        back_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

# Map screen
def map_screen(player):
    # Create buttons
    back_btn = Button(50, 50, 100, 50, "Back")
    
    # Location markers
    locations = [
        {"name": "Starting Forest", "pos": (200, 400), "unlocked": True},
        {"name": "Greenfield Town", "pos": (300, 350), "unlocked": True},
        {"name": "Dark Cave", "pos": (400, 450), "unlocked": "Dark Cave" in player.locations_unlocked},
        {"name": "Mountain Pass", "pos": (500, 300), "unlocked": "Mountain Pass" in player.locations_unlocked},
        {"name": "Dragon's Keep", "pos": (600, 200), "unlocked": "Dragon's Keep" in player.locations_unlocked},
    ]
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.is_clicked(mouse_pos, event):
                    return
                
                # Check if clicking on a location
                for loc in locations:
                    marker_rect = pygame.Rect(loc["pos"][0] - 10, loc["pos"][1] - 10, 20, 20)
                    if marker_rect.collidepoint(mouse_pos) and loc["unlocked"]:
                        player.location = loc["name"]
                        return
        
        # Draw map screen
        screen.fill(BLACK)
        
        # Draw map background
        screen.blit(assets.map_bg, (0, 0))
        
        # Draw title
        title_text = font_large.render("World Map", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        
        # Draw current location
        loc_text = font_medium.render(f"Current Location: {player.location}", True, WHITE)
        screen.blit(loc_text, (SCREEN_WIDTH//2 - loc_text.get_width()//2, 100))
        
        # Draw location markers
        for loc in locations:
            if loc["unlocked"]:
                color = YELLOW if loc["name"] == player.location else GREEN
                pygame.draw.circle(screen, color, loc["pos"], 10)
                
                # Draw location name
                name_text = font_small.render(loc["name"], True, WHITE)
                screen.blit(name_text, (loc["pos"][0] - name_text.get_width()//2, loc["pos"][1] + 15))
            else:
                pygame.draw.circle(screen, RED, loc["pos"], 10)
                pygame.draw.line(screen, BLACK, (loc["pos"][0] - 7, loc["pos"][1] - 7), 
                                 (loc["pos"][0] + 7, loc["pos"][1] + 7), 2)
                pygame.draw.line(screen, BLACK, (loc["pos"][0] + 7, loc["pos"][1] - 7), 
                                 (loc["pos"][0] - 7, loc["pos"][1] + 7), 2)
        
        # Draw connections between locations
        pygame.draw.line(screen, WHITE, (200, 400), (300, 350), 2)  # Forest to Town
        pygame.draw.line(screen, WHITE, (300, 350), (400, 450), 2)  # Town to Cave
        pygame.draw.line(screen, WHITE, (300, 350), (500, 300), 2)  # Town to Mountain
        pygame.draw.line(screen, WHITE, (500, 300), (600, 200), 2)  # Mountain to Dragon
        
        back_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

# Show message popup
def show_message(message, duration=2):
    popup = pygame.Surface((600, 100), pygame.SRCALPHA)
    popup.fill((0, 0, 0, 200))
    pygame.draw.rect(popup, WHITE, (0, 0, 600, 100), 2)
    
    # Split message into multiple lines if needed
    words = message.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        if font_medium.size(test_line)[0] < 580:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    
    if current_line:
        lines.append(current_line)
    
    # Draw message lines
    for i, line in enumerate(lines):
        line_text = font_medium.render(line, True, WHITE)
        popup.blit(line_text, (300 - line_text.get_width()//2, 30 + i * 30))
    
    start_time = pygame.time.get_ticks()
    
    while pygame.time.get_ticks() - start_time < duration * 1000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.blit(popup, (SCREEN_WIDTH//2 - 300, SCREEN_HEIGHT//2 - 50))
        pygame.display.flip()
        clock.tick(FPS)

# Main menu with save/load options
def main_menu():
    # Create buttons
    start_btn = Button(SCREEN_WIDTH//2 - 100, 250, 200, 50, "New Game")
    load_btn = Button(SCREEN_WIDTH//2 - 100, 325, 200, 50, "Load Game")
    quit_btn = Button(SCREEN_WIDTH//2 - 100, 400, 200, 50, "Quit")
    
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
                    return "new"
                elif load_btn.is_clicked(mouse_pos, event):
                    loaded_player = Player.load_game()
                    if loaded_player:
                        # Stop menu music
                        if assets.menu_music:
                            mixer.music.stop()
                        return loaded_player
                    else:
                        show_message("No save game found or error loading!", 2)
                elif quit_btn.is_clicked(mouse_pos, event):
                    pygame.quit()
                    sys.exit()
        
        # Update button hover states
        start_btn.check_hover(mouse_pos)
        load_btn.check_hover(mouse_pos)
        quit_btn.check_hover(mouse_pos)
        
        # Draw main menu
        screen.fill(BLACK)
        screen.blit(assets.main_menu_bg, (0, 0))
        
        # Draw title
        title_text = font_title.render("EPIC ADVENTURE RPG", True, GOLD)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
        
        # Draw version
        version_text = font_small.render("Enhanced Edition", True, WHITE)
        screen.blit(version_text, (SCREEN_WIDTH//2 - version_text.get_width()//2, 170))
        
        # Draw buttons
        start_btn.draw(screen)
        load_btn.draw(screen)
        quit_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

def town_screen(player, npcs):
    # Create buttons
    explore_btn = Button(SCREEN_WIDTH//2 - 100, 300, 200, 50, "Explore")
    quests_btn = Button(SCREEN_WIDTH//2 - 100, 375, 200, 50, "Quests")
    skills_btn = Button(SCREEN_WIDTH//2 - 100, 450, 200, 50, "Skills")
    craft_btn = Button(SCREEN_WIDTH//2 - 100, 525, 200, 50, "Crafting")
    map_btn = Button(SCREEN_WIDTH//2 - 100, 600, 200, 50, "Map")
    
    # NPC buttons
    npc_btns = []
    for i, npc in enumerate(npcs):
        npc_btns.append(Button(50, 150 + i * 100, 200, 80, npc.name))
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if explore_btn.is_clicked(mouse_pos, event):
                    return "explore"
                elif quests_btn.is_clicked(mouse_pos, event):
                    quest_screen(player)
                elif skills_btn.is_clicked(mouse_pos, event):
                    skills_screen(player)
                elif craft_btn.is_clicked(mouse_pos, event):
                    crafting_screen(player, create_crafting_recipes())
                elif map_btn.is_clicked(mouse_pos, event):
                    map_screen(player)
                
                # Check NPC interactions
                for i, btn in enumerate(npc_btns):
                    if btn.is_clicked(mouse_pos, event):
                        npcs[i].interact(player)
        
        # Update button hover states
        explore_btn.check_hover(mouse_pos)
        quests_btn.check_hover(mouse_pos)
        skills_btn.check_hover(mouse_pos)
        craft_btn.check_hover(mouse_pos)
        map_btn.check_hover(mouse_pos)
        for btn in npc_btns:
            btn.check_hover(mouse_pos)
        
        # Draw town screen
        screen.fill(BLACK)
        screen.blit(assets.town_bg, (0, 0))
        
        # Draw title
        title_text = font_large.render(f"{player.location}", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        
        # Draw player info
        info_text = [
            f"Name: {player.name}",
            f"Level: {player.level}",
            f"HP: {player.hp}/{player.max_hp}",
            f"Gold: {player.gold}",
            f"Day: {player.day_count}"
        ]
        
        for i, text in enumerate(info_text):
            text_surf = font_small.render(text, True, WHITE)
            screen.blit(text_surf, (SCREEN_WIDTH - 200, 50 + i * 30))
        
        # Draw buttons
        explore_btn.draw(screen)
        quests_btn.draw(screen)
        skills_btn.draw(screen)
        craft_btn.draw(screen)
        map_btn.draw(screen)
        
        # Draw NPCs
        for i, btn in enumerate(npc_btns):
            btn.draw(screen)
            screen.blit(npcs[i].image, (270, 150 + i * 100))
        
        pygame.display.flip()
        clock.tick(FPS)

def explore_screen(player, enemies, crafting_recipes):
    # Create buttons
    town_btn = Button(50, 50, 100, 50, "Town")
    hunt_btn = Button(SCREEN_WIDTH//2 - 100, 300, 200, 50, "Hunt Enemies")
    gather_btn = Button(SCREEN_WIDTH//2 - 100, 375, 200, 50, "Gather Materials")
    fish_btn = Button(SCREEN_WIDTH//2 - 100, 450, 200, 50, "Fishing Mini-game")
    lockpick_btn = Button(SCREEN_WIDTH//2 - 100, 525, 200, 50, "Lockpicking Mini-game")
    
    # Weather and time effects
    weather_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    time_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if town_btn.is_clicked(mouse_pos, event):
                    player.location = "Greenfield Town"
                    return
                elif hunt_btn.is_clicked(mouse_pos, event):
                    # Random enemy encounter
                    enemy = random.choice(enemies)
                    
                    # Scale enemy level to player level
                    enemy.level = max(1, player.level + random.randint(-1, 2))
                    enemy.hp = enemy.max_hp = 30 * enemy.level
                    enemy.attack = 8 * enemy.level
                    enemy.defense = 2 * enemy.level
                    enemy.exp_reward = 25 * enemy.level
                    enemy.gold_reward = 10 * enemy.level
                    
                    combat_result = combat_screen(player, enemy)
                    
                    if combat_result == "victory":
                        # Add exp and gold
                        player.add_exp(enemy.exp_reward)
                        player.gold += enemy.gold_reward
                        
                        # Check for loot
                        loot = enemy.generate_loot()
                        if loot:
                            for item in loot:
                                player.add_item(item)
                            show_message(f"Found {', '.join(i.name for i in loot)}!", 2)
                        
                        # Update quests
                        for quest in player.active_quests:
                            if not quest.completed:
                                if quest.update_kill(enemy.name):
                                    show_message(f"Quest progress: {quest.title}", 2)
                    
                    elif combat_result == "flee":
                        show_message("You escaped safely!", 1)
                    else:
                        show_message("You were defeated!", 2)
                        player.hp = player.max_hp // 2  # Heal to half after defeat
                        player.location = "Greenfield Town"  # Return to town
                        return
                
                elif gather_btn.is_clicked(mouse_pos, event):
                    # Gather random materials
                    materials = [
                        Item("Herbs", "material", 0, 5, assets.herb_icon),
                        Item("Iron Ore", "material", 0, 10, assets.ore_icon),
                        Item("Rare Herbs", "material", 0, 15, assets.herb_icon)
                    ]
                    
                    found = random.choice(materials)
                    player.add_item(found)
                    show_message(f"Found {found.name}!", 1)
                
                elif fish_btn.is_clicked(mouse_pos, event):
                    fishing_minigame(player)
                
                elif lockpick_btn.is_clicked(mouse_pos, event):
                    lockpicking_minigame(player)
        
        # Update button hover states
        town_btn.check_hover(mouse_pos)
        hunt_btn.check_hover(mouse_pos)
        gather_btn.check_hover(mouse_pos)
        fish_btn.check_hover(mouse_pos)
        lockpick_btn.check_hover(mouse_pos)
        
        # Draw explore screen
        screen.fill(BLACK)
        
        # Draw appropriate background based on location
        if "Forest" in player.location:
            screen.blit(assets.forest_bg, (0, 0))
        elif "Cave" in player.location:
            screen.blit(assets.cave_bg, (0, 0))
        elif "Mountain" in player.location:
            screen.blit(assets.mountain_bg, (0, 0))
        else:
            screen.blit(assets.explore_screen, (0, 0))
        
        # Draw weather and time effects
        draw_weather_effect(player.weather)
        draw_time_effect(player.time_of_day)
        
        # Draw title
        title_text = font_large.render(f"{player.location}", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        
        # Draw player info
        info_text = [
            f"Name: {player.name}",
            f"Level: {player.level}",
            f"HP: {player.hp}/{player.max_hp}",
            f"Gold: {player.gold}",
            f"Weather: {player.weather.name.lower().capitalize()}",
            f"Time: {player.time_of_day.name.lower().capitalize()}"
        ]
        
        for i, text in enumerate(info_text):
            text_surf = font_small.render(text, True, WHITE)
            screen.blit(text_surf, (SCREEN_WIDTH - 200, 50 + i * 30))
        
        # Draw buttons
        town_btn.draw(screen)
        hunt_btn.draw(screen)
        gather_btn.draw(screen)
        fish_btn.draw(screen)
        lockpick_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

def combat_screen(player, enemy):
    # Combat states
    PLAYER_TURN = 0
    ENEMY_TURN = 1
    VICTORY = 2
    DEFEAT = 3
    FLEE = 4
    
    combat_state = PLAYER_TURN
    
    # Create buttons
    attack_btn = Button(100, 600, 150, 50, "Attack")
    defend_btn = Button(300, 600, 150, 50, "Defend")
    item_btn = Button(500, 600, 150, 50, "Items")
    flee_btn = Button(700, 600, 150, 50, "Flee")
    
    # Combat log
    log = []
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if combat_state == PLAYER_TURN:
                    if attack_btn.is_clicked(mouse_pos, event):
                        # Player attack
                        damage = max(1, player.attack - enemy.defense // 2)
                        enemy.take_damage(damage, player.weather)
                        log.append(f"You hit {enemy.name} for {damage} damage!")
                        
                        if not enemy.is_alive():
                            combat_state = VICTORY
                            log.append(f"You defeated {enemy.name}!")
                        else:
                            combat_state = ENEMY_TURN
                    
                    elif defend_btn.is_clicked(mouse_pos, event):
                        # Player defend (reduces next damage)
                        log.append("You brace for the enemy's attack!")
                        # TODO: Implement defend mechanic
                        combat_state = ENEMY_TURN
                    
                    elif item_btn.is_clicked(mouse_pos, event):
                        # Use item
                        potions = [i for i in player.inventory if i.type == "potion"]
                        if potions:
                            potion = potions[0]  # Use first potion
                            player.use_item(potion)
                            log.append(f"You used {potion.name} and healed {potion.stat} HP!")
                        else:
                            log.append("You have no potions!")
                        combat_state = ENEMY_TURN
                    
                    elif flee_btn.is_clicked(mouse_pos, event):
                        # Attempt to flee
                        if random.random() < 0.7:  # 70% chance to flee
                            combat_state = FLEE
                        else:
                            log.append("You failed to escape!")
                            combat_state = ENEMY_TURN
        
        # Enemy turn
        if combat_state == ENEMY_TURN:
            if enemy.is_alive():
                damage = max(1, enemy.get_attack_power(player.weather) - player.defense // 2)
                player.take_damage(damage)
                log.append(f"{enemy.name} hits you for {damage} damage!")
                
                if not player.is_alive():
                    combat_state = DEFEAT
                    log.append("You were defeated!")
                else:
                    combat_state = PLAYER_TURN
            else:
                combat_state = VICTORY
        
        # Update button hover states
        if combat_state == PLAYER_TURN:
            attack_btn.check_hover(mouse_pos)
            defend_btn.check_hover(mouse_pos)
            item_btn.check_hover(mouse_pos)
            flee_btn.check_hover(mouse_pos)
        
        # Draw combat screen
        screen.fill(BLACK)
        
        # Draw background based on weather
        if player.weather == Weather.RAIN:
            screen.fill((50, 50, 100))
        elif player.weather == Weather.SNOW:
            screen.fill((200, 200, 255))
        elif player.weather == Weather.SANDSTORM:
            screen.fill((210, 180, 140))
        else:
            screen.fill((100, 150, 100))
        
        # Draw combatants
        screen.blit(player.image, (200, 200))
        screen.blit(enemy.image, (600, 200))
        
        # Draw health bars
        # Player health
        pygame.draw.rect(screen, RED, (200, 180, 100, 10))
        pygame.draw.rect(screen, GREEN, (200, 180, 100 * (player.hp / player.max_hp), 10))
        
        # Enemy health
        pygame.draw.rect(screen, RED, (600, 180, 100, 10))
        pygame.draw.rect(screen, GREEN, (600, 180, 100 * (enemy.hp / enemy.max_hp), 10))
        
        # Draw names and levels
        player_text = font_small.render(f"{player.name} Lv.{player.level}", True, WHITE)
        enemy_text = font_small.render(f"{enemy.name} Lv.{enemy.level}", True, WHITE)
        screen.blit(player_text, (200, 150))
        screen.blit(enemy_text, (600, 150))
        
        # Draw combat log
        log_surface = pygame.Surface((600, 150), pygame.SRCALPHA)
        log_surface.fill((0, 0, 0, 150))
        
        for i, message in enumerate(log[-5:]):  # Show last 5 messages
            text = font_small.render(message, True, WHITE)
            log_surface.blit(text, (10, 10 + i * 30))
        
        screen.blit(log_surface, (SCREEN_WIDTH//2 - 300, 400))
        
        # Draw buttons if player's turn
        if combat_state == PLAYER_TURN:
            attack_btn.draw(screen)
            defend_btn.draw(screen)
            item_btn.draw(screen)
            flee_btn.draw(screen)
        
        # Check combat resolution
        if combat_state == VICTORY:
            pygame.display.flip()
            pygame.time.delay(1000)
            return "victory"
        elif combat_state == DEFEAT:
            pygame.display.flip()
            pygame.time.delay(1000)
            return "defeat"
        elif combat_state == FLEE:
            pygame.display.flip()
            pygame.time.delay(1000)
            return "flee"
        
        pygame.display.flip()
        clock.tick(FPS)

# Main game function
def main():
    # Show main menu
    menu_result = main_menu()
    
    if menu_result == "new":
        # Initialize new game
        enemies = create_enemies()
        quests = create_quests()
        crafting_recipes = create_crafting_recipes()
        
        # Create NPCs
        npcs = [
            NPC("Blacksmith", assets.blacksmith_img, 
                "I can craft weapons and armor for you.", 
                shop_items=[i for i in create_items() if i.type in ["weapon", "armor"]], 
                is_merchant=True),
            NPC("Herbalist", assets.merchant_img, 
                "I have potions and herbs for sale.", 
                shop_items=[i for i in create_items() if i.type in ["potion", "material"]], 
                is_merchant=True),
            NPC("Quest Giver", assets.quest_giver_img, 
                "I have tasks for brave adventurers like you.", 
                quests=quests, 
                is_quest_giver=True)
        ]
        
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
        
        # Add starting quest
        player.add_quest(quests[0])
    else:
        # Loaded game
        player = menu_result
        enemies = create_enemies()
        quests = create_quests()
        crafting_recipes = create_crafting_recipes()
        npcs = [
            NPC("Blacksmith", assets.blacksmith_img, 
                "I can craft weapons and armor for you.", 
                shop_items=[i for i in create_items() if i.type in ["weapon", "armor"]], 
                is_merchant=True),
            NPC("Herbalist", assets.merchant_img, 
                "I have potions and herbs for sale.", 
                shop_items=[i for i in create_items() if i.type in ["potion", "material"]], 
                is_merchant=True),
            NPC("Quest Giver", assets.quest_giver_img, 
                "I have tasks for brave adventurers like you.", 
                quests=quests, 
                is_quest_giver=True)
        ]
    
    # Play explore music
    if assets.explore_music:
        mixer.music.load(assets.explore_music)
        mixer.music.play(-1)
    
    # Main game loop
    running = True
    while running:
        player.update()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Game logic based on location
        if player.location == "Greenfield Town":
            town_screen(player, npcs)
        else:
            explore_screen(player, enemies, crafting_recipes)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()