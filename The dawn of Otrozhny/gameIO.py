# Used this for serialization 
# and deserialization of files in the game
import pickle
import levelData
import entities
import os
from functools import lru_cache
import pygame
PATH_ROOT = os.getcwd()
MAPS_PATH = os.path.join(PATH_ROOT, "Maps")

def list_maps():
    map_names = []
    if not os.path.exists(MAPS_PATH):
        os.mkdir(MAPS_PATH)
        return map_names
    for files in os.listdir(MAPS_PATH):
        #[-4] to remove extension and just get the map name
        map_names.append( (os.path.join(MAPS_PATH, files), files[-4] ))
    return map_names



def get_files_paths_from_folder(folder, *folders):
    file_paths = []
    curPath = os.path.join(PATH_ROOT, folder, *folders)
    if not os.path.exists(curPath):
        return None 
    for file in os.listdir(curPath):
        file_paths.append(os.path.join(curPath, file))
    return file_paths


def load_level(level_path):
    with open(level_path, "rb") as level:
        level_data = pickle.load(level)
        levelData.Level.load(level_data)

def load_level_object(level_path):
    with open(level_path, "rb") as level:
        level_data = pickle.load(level)
        return level_data

def save_level(level_name, level):
    pickle.dump(level, open( os.path.join(MAPS_PATH, str(level_name) + ".map"), "wb"))

# The lru cache caches the results of the function
# so I dont need to create a new surface object
# everytime
@lru_cache(maxsize=256)
def get_sprite(sprite_pack: str, sprite_position: int):
    
    filenames_list = get_files_paths_from_folder("Assets", sprite_pack, "Sprites")
    if filenames_list != None:
        
        for pos, path in enumerate(sorted(filenames_list)):
            if pos == sprite_position:
                img = pygame.image.load(path).convert_alpha()
                img.set_colorkey((152, 0, 136))
                return img
        img = pygame.image.load(filenames_list[0]).convert_alpha()
        img.set_colorkey((152, 0, 136))
        return img
    return None


def get_audio(sprite_pack, state):
    import random
    filenames_list = get_files_paths_from_folder("Assets", sprite_pack, str(state))
    if filenames_list == None:
        return None
    audioIndex = random.randint(0, len(filenames_list)-1)
    audioObj = pygame.mixer.Sound(filenames_list[audioIndex])
    return audioObj

@lru_cache(maxsize=8)
def get_cached_audio(folder_name, sub_folder):
    filenames_list = get_files_paths_from_folder("Assets", folder_name, sub_folder)
    if filenames_list == None:
        return None
    audioObj = pygame.mixer.Sound(filenames_list[0])
    return audioObj