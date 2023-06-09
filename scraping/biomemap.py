# Dict which maps biome id to type
# scraped from TheRedEngineer's biome detector:
#   http://www.theredengineer.com/biome-detector.html
# uses pre-1.13 biome id's, but also some post. 
# Not accurate to modern versions of the game.
BIOMES = {
    37: 'badlands',
    39: 'badlands_plateau',
    16: 'beach',
    27: 'birch_forest',
    28: 'birch_forest_hills',
    46: 'cold_ocean',
    29: 'dark_forest',
    157: 'dark_forest_hills',
    49: 'deep_cold_ocean',
    50: 'deep_frozen_ocean',
    48: 'deep_lukewarm_ocean',
    24: 'deep_ocean',
    47: 'deep_warm_ocean',
    2: 'desert',
    17: 'desert_hills',
    130: 'desert_lakes',
    43: 'end_barrens',
    42: 'end_highlands',
    41: 'end_midlands',
    165: 'eroded_badlands',
    132: 'flower_forest',
    4: 'forest',
    10: 'frozen_ocean',
    11: 'frozen_river',
    160: 'giant_spruce_taiga',
    161: 'giant_spruce_taiga_hills',
    32: 'giant_tree_taiga',
    33: 'giant_tree_taiga_hills',
    131: 'gravelly_mountains',
    140: 'ice_spikes',
    21: 'jungle',
    23: 'jungle_edge',
    22: 'jungle_hills',
    45: 'lukewarm_ocean',
    167: 'modified_badlands_plateau',
    162: 'modified_gravelly_mountains',
    149: 'modified_jungle',
    151: 'modified_jungle_edge',
    166: 'modified_wooded_badlands_plateau',
    3: 'mountains',
    20: 'mountain_edge',
    14: 'mushroom_fields',
    15: 'mushroom_field_shore',
    8: 'nether',
    0: 'ocean',
    1: 'plains',
    7: 'river',
    35: 'savanna',
    36: 'savanna_plateau',
    163: 'shattered_savanna',
    164: 'shattered_savanna_plateau',
    40: 'small_end_islands',
    26: 'snowy_beach',
    13: 'snowy_mountains',
    30: 'snowy_taiga',
    31: 'snowy_taiga_hills',
    158: 'snowy_taiga_mountains',
    12: 'snowy_tundra',
    25: 'stone_shore',
    129: 'sunflower_plains',
    6: 'swamp',
    134: 'swamp_hills',
    5: 'taiga',
    19: 'taiga_hills',
    133: 'taiga_mountains',
    155: 'tall_birch_forest',
    156: 'tall_birch_hills',
    9: 'the_end',
    127: 'the_void',
    44: 'warm_ocean',
    38: 'wooded_badlands_plateau',
    18: 'wooded_hills',
    34: 'wooded_mountains',
}

def names_from_ids(ids):
    """
    Takes the int array ids and returns a new array of the same size
    containing the biomes names as a strings
    """
    names = []
    for num in ids:
        names.append(BIOMES[num])

    return names
    