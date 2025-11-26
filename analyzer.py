import os

def can_be_int(val):
    try:
        int(val)
        return True
    except:
        return False
    
def can_be_float(val):
    try:
        float(val)
        return True
    except:
        return False

def user_input_int(name, skip='s'):
    action = "skip"
    if skip == 'q': action = "exit"

    val = input(f"Input the {name} value or press {skip} to {action}: ")
    while not can_be_int(val):
        if val == skip: return skip
        print(f"Invalid input, {name} has to be an integer")
        val = input(f"Please try again or press {skip} to {action}: ")
    if val == skip: return skip
    return int(val)

def user_input_pos_int(name, skip='s'):
    action = "skip"
    if skip == 'q': action = "exit"

    val = input(f"Input the {name} value or press {skip} to {action}: ")
    while not can_be_int(val) or int(val) < 0:
        if val == skip: return skip
        print(f"Invalid input, {name} has to be a positive integer")
        val = input(f"Please try again or press {skip} to {action}: ")
    if val == skip: return skip
    return int(val)

def user_input_ranged_pos_int(name, skip='s', upper=int(2 ** 31 - 1)):
    action = "skip"
    if skip == 'q': action = "exit"

    val = input(f"Input the {name} value or press {skip} to {action}: ")
    while not can_be_int(val) or int(val) < 0 or int(val) > upper:
        if val == skip: return skip
        print(f"Invalid input, {name} has to be a positive integer below {upper}")
        val = input(f"Please try again or press {skip} to {action}: ")
    if val == skip: return skip
    return int(val)

def user_input_float(name, skip='s'):
    action = "skip"
    if skip == 'q': action = "exit"

    val = input(f"Input the {name} value or press {skip} to {action}: ")
    while not can_be_float(val):
        if val == skip: return skip
        print(f"Invalid input, {name} has to be a float")
        val = input(f"Please try again or press {skip} to {action}: ")
    if val == skip: return skip
    return float(val)

def user_input_ranged_float(name, skip='s', lower=float("-inf"), upper=float("inf")):
    action = "skip"
    if skip == 'q': action = "exit"

    val = input(f"Input the {name} value or press {skip} to {action}: ")
    while not can_be_float(val) or float(val) < lower or float(val) > upper:
        if val == skip: return skip
        print(f"Invalid input, {name} has to be a float between {lower} and {upper}")
        val = input(f"Please try again or press {skip} to {action}: ")
    if val == skip: return skip
    return float(val)

def write_file(dir, nameid, prop):
    filename = dir + "/" + nameid.strip() + ".json"
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except:
            return
    created_file = open(filename, 'w')
    created_file.write(str(prop).lower().replace("'", '"'))
    created_file.close()

def write_tag_file(filename, vals):
    file = open(f"resources/data/mca/tags/item/{filename}.json", 'w')
    prop = {
        "replalce": False,
        "values": vals
    }
    file.write(str(prop).lower().replace("'", '"'))
    file.close()

def temperature_item(modid, nameid):
    cold_res = user_input_ranged_float("cold resistance", lower=0)
    if cold_res == 's': return True
    heat_res = user_input_ranged_float("heat_resistance", lower=0)
    if heat_res == 's': return True
    temperature = user_input_float("temperature")
    if temperature == 's': return True
    thermal = user_input_ranged_float("thermal resistance", lower=0)
    if thermal == 's': return True

    dir = "./resources/data/" + modid + "/legendarysurvivaloverhaul/temperature/items"
    prop = {
        "cold_resistance": cold_res,
        "heat_resistance": heat_res,
        "temperature": temperature,
        "thermal_resistance": thermal
    }
    write_file(dir, nameid, prop)
    return False

####### Section 1: Food Analysis #######
# Section 1 Functions
def thirst_food(modid, nameid):
    has_effects = input("Would you like to input any effects? (y for yes) ").lower()
    effects = []
    while has_effects[0] == 'y':
        amplifier = user_input_pos_int("amplifier", 'q')
        if amplifier == 'q': break

        chance = user_input_ranged_float("chance", 'q', 0, 1)
        if chance == 'q': break

        duration = user_input_pos_int("duration", 'q')
        if chance == 'q': break

        effectname = input("Input the id of the effect you would like to implement or press q to exit")
        if effectname == 'q': break

        effect = {
            "amplifier": amplifier,
            "chance": chance,
            "duration": duration,
            "effect": effectname
        }
        effects.append(effect)
        has_effects = input("Would you like to input another effect (press y if so): ").lower()

    hydration = user_input_int("hydration")
    if hydration == 's': return True

    saturation = user_input_ranged_float("saturation", lower=0)
    if saturation == 's': return True

    dir = "./resources/data/" + modid + "/legendarysurvivaloverhaul/thirst/consumables"
    prop = [
        {
            "effects": effects,
            "hydration": hydration,
            "properties": [],
            "saturation": saturation
        }
    ]
    write_file(dir, nameid, prop)
    return False

def temperature_food(modid, nameid):
    duration = user_input_pos_int("duration")
    if duration == 's': return True

    temperature = user_input_int("temperature")
    if temperature == 's': return True

    group_input = input("Please enter the group (f for food, d for drink, b for both): ").lower()[0]
    if group_input == 'f': 
        prop = [
            {
                "duration": duration,
                "group": "FOOD",
                "temperature_level": temperature
            }
        ]
    elif group_input == 'd':
        prop = [
            {
                "duration": duration,
                "group": "DRINK",
                "temperature_level": temperature
            }
        ]
    elif group_input == 'b':
        prop = [
            {
                "duration": duration,
                "group": "FOOD",
                "temperature_level": temperature
            },
            {
                "duration": duration,
                "group": "DRINK",
                "temperature_level": temperature
            }
        ]
    else: return True
    
    dir = "./resources/data/" + modid + "/legendarysurvivaloverhaul/temperature/consumables"
    write_file(dir, nameid, prop)
    return False

def damage_food(modid, nameid):
    heal_charge = user_input_pos_int("healing charge")
    heal_time = user_input_pos_int("healing time")
    heal_val = user_input_ranged_float("healing value", lower=0)
    amplifier = user_input_pos_int("amplifier")
    duration = user_input_pos_int("duration")
    dir = "./resources/data/" + modid + "/legendarysurvivaloverhaul/body_damage/consumables"
    prop = {
        "healing_charges": heal_charge,
        "healing_time": heal_time,
        "healing_value": heal_val,
        "recovery_effect_amplifier": amplifier,
        "recovery_effect_duration": duration
    }
    write_file(dir, nameid, prop)
    return False

# Section 1 Code
def categorize_food():
    file = open("food.txt", 'r')

    confect = []
    gluten = []
    lactose = []

    for item in file.readlines():
        if item.index(':') == -1: continue
        print("\n\n", '-' * 32)
        print("Item name:", item)
        mca_class = input("MCA classification (c for confectionary, g for gluten, l for lactose): ")
        if 'c' in mca_class: confect.append(item)
        if 'g' in mca_class: gluten.append(item)
        if 'l' in mca_class: lactose.append(item)
    
    write_tag_file("confectionaries", confect)
    write_tag_file("gluten", gluten)
    write_tag_file("lactose", lactose)


def analyze_food():
    file = open("food.txt", 'r')

    for item in file.readlines():
        if item.index(':') == -1: continue
        print("\n\n", '-' * 32)
        print("Item name:", item)

        parts = item.split(':')
        modid = parts[0]
        nameid = parts[1]

        # code written in order skip unecessary analysis
        if (modid in ["artifacts","beachparty","brewinandchewin","camping","create","curios","decorative_blocks","farmersdelight","farmersrespite","hardcore_torches","legendarysurvivaloverhaul","rusticdelight","supplementaries","vinery","wildernature"]):
            continue

        print("There are three categories of food, damage(d), temperature(t), and thirst(h)")
        category = input("Please enter the category of food you would like to do: ").lower()
        if category == 's': continue
        if 'h' in category:
            print("\nThirst Characteristics:")
            if thirst_food(modid, nameid):
                print(f"Skipping all characterisitcs for {item}")
                continue
        if 't' in category:
            print("\nTemperature Characteristics:")
            if temperature_food(modid, nameid):
                print(f"Skipping all characterisitcs for {item}")
                continue
        if 'd' in category:
            print("\nDamage Characteristics")
            if damage_food(modid, nameid):
                print(f"Skipping all characterisitcs for {item}")
                continue
    file.close()

####### Section 2: Biome Analysis #######
# Section 2 Code
def analyze_biomes():
    file = open("biomes.txt", 'r')
    for biome in file.readlines():
        if biome.index(':') == -1: continue
        print('-' * 32)
        print("\n\nBiome name:", biome)
        parts = biome.strip().split(':')
        modid = parts[0]
        nameid = parts[1]
        dry_in = input("Please enter if the biome is dry or not (t for is dry) or press s to skip: ").lower()[0]
        is_dry = False
        if dry_in == 's': continue
        elif dry_in == 't': is_dry = True
        temperature = user_input_float("temperature")
        if temperature == 's':
            print(f"Skipping all characterisitcs for {biome}")
            continue
        
        dir = "./resources/data/" + modid + "/legendarysurvivaloverhaul/temperature/biomes"
        prop = {
            "is_dry": is_dry,
            "temperature": temperature
        }
        write_file(dir, nameid, prop)


####### Section 3: Armor Analysis #######
# Section 3 Functions
def damage_armor(modid, nameid):
    body_res = user_input_ranged_float("body resistance", lower=0)
    if body_res == 's': return True
    chest_res = user_input_ranged_float("chest resistance", lower=0)
    if chest_res == 's': return True
    feet_res = user_input_ranged_float("feet resistance", lower=0)
    if feet_res == 's': return True
    head_res = user_input_ranged_float("head resistance", lower=0)
    if head_res == 's': return True
    larm_res = user_input_ranged_float("left arm resistance", lower=0)
    if larm_res == 's': return True
    leg_res = user_input_ranged_float("leg resistance", lower=0)
    if leg_res == 's': return True
    rarm_res = user_input_ranged_float("right arm resistance", lower=0)
    if rarm_res == 's': return True
    
    dir = "./resources/data/" + modid + "/legendarysurvivaloverhaul/body_damage/items"
    prop = {
        "body_resistance": body_res,
        "chest_resistance": chest_res,
        "feet_resistance": feet_res,
        "head_resistance": head_res,
        "left_arm_resistance": larm_res,
        "legs_resistance": leg_res,
        "right_arm_resistance": rarm_res
    }
    write_file(dir, nameid, prop)
    return False

# Section 3 Code
def analyze_armor():
    file = open("armor.txt", 'r')
    for armor in file.readlines():
        if armor.index(':') == -1: continue
        print("\n\n", '-' * 32)
        print("Armor piece name:", armor)
        parts = armor.strip().split(':')
        modid = parts[0]
        nameid = parts[1]
        if (temperature_item(modid, nameid)):
            print(f"Skipping all characterisitcs for {armor}")
            continue
        if (damage_armor(modid, nameid)):
            print(f"Skipping all characterisitcs for {armor}")
            continue

####### Section 4: Block Analysis #######
# Section 4 Functions
def temperature_block(modid, nameid):
    cont = input("Would you like to define a property for the block (y for yes)? ").lower()[0]
    if cont == 's': return True
    vals = []
    while cont == 'y':
        cont_prop = input("Would you like to define the specific properties (y for yes)? ").lower()[0]
        if cont_prop == 's': return True
        properties = {}
        while cont_prop == 'y':
            key = input("Please enter the key for your property: ")
            value = input("Please enter the value for your property: ")
            properties[key] = value
            cont_prop = input("Would you like to define another specific property (y for yes)? ").lower()[0]
            if cont_prop == 's': return True
        
        temperature = user_input_float("temperature")
        if temperature == 's': return True
        vals.append({
            "properties": properties,
            "temperature": temperature
        })
        cont = input("Would you like to define another property for the block (y for yes)? ").lower()[0]
        vals.append(properties)
        if cont == 's': return True
    
    dir = "./resources/data/" + modid + "/legendarysurvivaloverhaul/temperature/blocks"
    write_file(dir, nameid, vals)
    return False

def thirst_block(modid, nameid):
    has_effects = input("Would you like to input any effects? (y for yes) ").lower()
    effects = []
    while has_effects[0] == 'y':
        amplifier = user_input_pos_int("amplifier", 'q')
        if amplifier == 'q': break

        chance = user_input_ranged_float("chance", 'q', 0, 1)
        if chance == 'q': break

        duration = user_input_pos_int("duration", 'q')
        if chance == 'q': break

        effectname = input("Input the id of the effect you would like to implement or press q to exit")
        if effectname == 'q': break

        effect = {
            "amplifier": amplifier,
            "chance": chance,
            "duration": duration,
            "effect": effectname
        }
        effects.append(effect)
        has_effects = input("Would you like to input another effect (press y if so): ").lower()

    hydration = user_input_int("hydration")
    if hydration == 's': return True

    saturation = user_input_ranged_float("saturation", lower=0)
    if saturation == 's': return True

    dir = "./resources/data/" + modid + "/legendarysurvivaloverhaul/thirst/blocks"
    prop = [
        {
            "effects": effects,
            "hydration": hydration,
            "properties": [],
            "saturation": saturation
        }
    ]
    write_file(dir, nameid, prop)
    return False

def damage_block(modid, nameid):
    print("The below are the body part ids:")
    print("0 = head\n1 = right arm\n2 = left arm\n3 = chest\n4 = right leg\n5 = right foot\n6 = left leg\n7 = left foot")
    body_parts = []
    partid = user_input_pos_int("body part (as a string of integers with each digit representing a part")
    if partid == 's': return True
    while partid != 0:
        body_part = "HEAD"
        if partid % 10 == 1: body_part = "RIGHT_ARM"
        elif partid % 10 == 2: body_part = "LEFT_ARM"
        elif partid % 10 == 3: body_part = "CHEST"
        elif partid % 10 == 4: body_part = "RIGHT_LEG"
        elif partid % 10 == 5: body_part = "RIGHT_FOOT"
        elif partid % 10 == 6: body_part = "LEFT_LEG"
        elif partid % 10 == 7: body_part = "LEFT_FOOT"
        body_parts.append(body_part)
        partid //= 10

    print("The below are damage distribution ids:")
    print("0 = none\n1 = one of each part\n2 = all parts")
    dmg_id = user_input_ranged_pos_int("damage distribution(0-2 inclusive)", upper=2)
    if dmg_id == 's': return True
    dmg_dist = "NONE"
    if dmg_id == 1: dmg_dist = "ONE_OF"
    elif dmg_id == 2: dmg_dist = "ALL"

    dir = "./resources/data/" + modid + "/legendarysurvivaloverhaul/body_damage/damage_sources"
    prop = {
        "body_parts": body_parts,
        "damage_distribution": dmg_dist
    }
    write_file(dir, modid + '.' + nameid, prop)
    return False

# Section 4 Code
def analyze_blocks():
    file = open("block.txt", 'r')
    for block in file.readlines():
        if block.index(':') == -1: continue
        print("\n\n", '-' * 32)
        print("Block name:", block)
        parts = block.strip().split(':')
        modid = parts[0]
        nameid = parts[1]
        print("There are three categories of blocks, damage(d), temperature(t), and thirst(h)")
        category = input("Please enter the category of block you would like to do: ").lower()
        if 's' in category: continue
        if 'd' in category:
            print("\nDamage Characteristics:")
            if damage_block(modid, nameid):
                print(f"Skipping all characterisitcs for {block}")
                continue
        if 't' in category:
            print("\nTemperature Characteristics:")
            if temperature_block(modid, nameid):
                print(f"Skipping all characterisitcs for {block}")
                continue
        if 'h' in category:
            print("\nThirst Characteristics:")
            if thirst_block(modid, nameid):
                print(f"Skipping all characterisitcs for {block}")
                continue
    
####### Section 5: Miscellaneous Item Analysis #######
# Section 5 Functions
def fuel_item(modid, nameid):
    duration = user_input_pos_int("duration")
    if duration == 's': return True

    typein = input("Please input the type (h for heating, c for cooling): ").lower()[0]
    if typein == 'h': therm_type = "HEATING"
    elif typein == 'c': therm_type = "COOLING"
    else: return True

    dir = "./resources/data/" + modid + "/legendarysurvivaloverhaul/temperature/fuel_items"
    prop = [
        {
            "duration": duration,
            "thermal_type": therm_type
        }
    ]
    write_file(dir, nameid, prop)
    return False

# Section 5 Code
def analyze_items():
    file = open("items.txt", 'r')
    for item in file.readlines():
        if item.index(':') == -1: continue
        print("\n\n", '-' * 32)
        print("Item name:", item)
        parts = item.strip().split(':')
        modid = parts[0]
        nameid = parts[1]
        print("There are two categories of items, basic (b) and fuel (f)")
        category = input("Please enter the category of item you would like to do: ").lower()
        if 's' in category: continue
        if 'b' in category:
            print("\nTemperature Characteristics:")
            if temperature_item(modid, nameid):
                print(f"Skipping all characterisitcs for {item}")
                continue
        if 'f' in category:
            print("\nFuel Characteristics")
            if fuel_item(modid, nameid):
                print(f"Skipping all characterisitcs for {item}")
                continue

# main code
def main():
    print("There are 5 sections available, each corresponding to a category that is analyzed")
    print("They are:")
    print("0 = food (category)\n1 = food (analysis)\n2 = biome\n3 = armor\n4 = block\n5 = items")
    val = user_input_ranged_pos_int("category", upper=5)
    if val == 's': return
    if val == 0: categorize_food()
    elif val == 1: analyze_food()
    elif val == 2: analyze_biomes()
    elif val == 3: analyze_armor()
    elif val == 4: analyze_blocks()
    elif val == 5: analyze_items()

if __name__ == "__main__":
    main()