import pygame
from settings import WIDTH, HEIGHT, FPS
from player import Player
from utils import load_tileset, draw_map
from dialogue import DialogueBox  # Importa el cuadro de diálogo
from pytmx import load_pygame
from utils import load_story_from_json
from turtles import Turtle
import random
from crab import Crab  # Importa la clase Crab
from utils import  draw_score
import time
from power import Power  # Importa la clase Power
from utils import  draw_powerup_info
from zorro import Fox
from egg import Egg
import math
import json
from utils import mostrar_letrero_personalizado
from buttons import Button
from enemy import Enemy
from utils import draw_image, draw_map_from_tmx, check_collision,check_collision_power
from utils import init_objects
from utils import generate_random_turtle,generate_random_fox,generate_random_enemy
from settings import WIDTH, HEIGHT, FPS
import os
import sys
from gif import GifBackground
import subprocess
import pygame_menu