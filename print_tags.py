items = open("items.txt", 'r')
for item in items.readlines():
    if "spawn_egg" in item:
        print("item:" + item.strip())


# for item_name in ["brass", "electrum", "gold", "iron", "neptunium", "prismarine", "andesite_alloy", "stratus", "zinc", "ambrosium", "amethyst", "diamond", "emerald", "lapis", "quartz", "skyjade", "source_gem", "zanite"]:
#     print(f"""
# <create:scrap_{item_name}_extra_large>, 
# <create:scrap_{item_name}_large>, 
# <create:scrap_{item_name}_medium>, 
# <create:scrap_{item_name}_small>, 
# <create:scrap_{item_name}_tiny>, 
# """)