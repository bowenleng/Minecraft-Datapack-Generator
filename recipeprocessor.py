tag_file = open("item-tags.txt")
tags = {}
for line in tag_file.readlines():
    sep = line.index('>')
    if (sep == -1 or sep == len(line)): continue
    tag_id = line[1:sep].strip()
    
    contents = line[sep + 1:].strip().split(',')
    if tag_id not in tags:
        tags[tag_id] = []
        
    for item in contents:
        item = item.strip()
        if (len(item) == 0): continue
        if (':' in item):
            tags[tag_id].append(item)
tag_file.close()

def placing_items_in_list(filename):
    items = []
    file = open(filename, 'r')
    for item in file.readlines():
        sep = item.index(':')
        if sep == -1: continue
        cat = item[0:sep]
        namespace = item[sep+1:].strip()

        if ':' in namespace:
            if cat == "tag" and namespace in tags:
                items += tags[namespace]
            elif cat == "item":
                items.append(namespace)
    file.close()
    return items

def amt_processing(item, chnc_mult=1, amt_mult=1):
    if '[' in item:
        split = item.index('[')
        item = item[split+1:]
    if ']' in item:
        split = item.index(']')
        item = item[0:split]

    end = item.index('>')
    start = item.index('<')
    other = item[:start].strip() + 'i' + item[end+1:].strip()
    item_ind = other.index('i')

    size = len(other)

    p_ind = size
    a_ind = size
    if '%' in other:
        p_ind = other.index('%')
    
    if '*' in other:
        a_ind = other.index('*')

    chance = 1.0
    amt = 1

    if p_ind != size:
        try:
            if p_ind < item_ind:
                if a_ind < p_ind:
                    val = other[a_ind+1:p_ind].strip()
                else:
                    val = other[item_ind+1:p_ind].strip()
            else:
                if a_ind > p_ind:
                    val = other[p_ind+1:a_ind].strip()
                else:
                    val = other[p_ind:item_ind].strip()
            chance = float(val)
        except:
            print(val, a_ind, p_ind, item_ind)
            print(f"Chance cannot be processed for {item}")
    
    if a_ind != size:
        try:
            if a_ind < item_ind:
                if p_ind < a_ind:
                    val = other[p_ind+1:a_ind].strip()
                else:
                    val = other[0:a_ind].strip()
            else:
                if p_ind > a_ind:
                    val = other[a_ind+1:p_ind].strip()
                else:
                    val = other[a_ind:].strip()
            amt = int(val)
        except:
            print(val, a_ind, p_ind, item_ind)
            print(f"Amount cannot be processed for {item} with the format {other}")
    
    chance *= chnc_mult
    amt *= amt_mult
    return chance, amt

def key_property_processing(item):
    end = item.index('>')
    start = item.index('<')
    chance, amt = amt_processing(item)

    ing = item[start+1:end].strip()
    return [ing, amt, chance]

def item_property_processing(item, chnc_mult=1, amt_mult=1):
    end = item.index('>')
    start = item.index('<')
    chance, amt = amt_processing(item, chnc_mult, amt_mult)

    ing = item[start+1:end].strip()
    sep = ing.index(':')
    cat = ing[0:sep]
    item_id = ing[sep+1:]
    if cat == "item":
        return [[item_id], amt, chance]
    elif cat == "tag":
        if item_id in tags and tags[item_id] == 0:
            return [tags[item_id], amt, chance]
    return []

def gen_process(recipes, namespace, ings, basic_items, removed_items, amt=1, chance=1):
    if namespace in basic_items or (namespace in recipes and len(recipes[namespace]) > len(ings)): return True

    ndict = {}
    change = True
    for ing in ings:
        ing_data = item_property_processing(ing, chance, 1/amt)
        if len(ing_data) == 3:
            itemids = ing_data[0]
            for itemid in itemids:
                if (itemid in removed_items): continue
                if (itemid == namespace):
                    change = False
                    break
                if (itemid in ndict):
                    ndict[itemid][0] += ing_data[1]
                    ndict[itemid][1] += ing_data[2]
                else:
                    ndict[itemid] = ing_data[1:]
        if not change and namespace in recipes: break
    if change: recipes[namespace] = ndict
    return False

removed_items = placing_items_in_list("removed_items.txt")
basic_items = placing_items_in_list("basic_items.txt")

recipes = {}

rev_aether = open("reversed_aether.txt", 'r')
for rec in rev_aether.readlines():
    if len(rec) == 0: continue
    if ',' not in rec: continue
    parts = rec.strip().split(',')
    out = key_property_processing(parts[0])
    if len(out) != 3: continue

    unref = out[0]
    sep = unref.index(':')
    cat = unref[0:sep]
    namespace = unref[sep+1:]
    if cat == "item":
        gen_process(recipes, namespace, parts[1:], basic_items, removed_items, out[1], out[2])
    elif cat == "tag":
        for item in tags[namespace]:
            gen_process(recipes, item, parts[1:], basic_items, removed_items, out[1], out[2])
rev_aether.close()

rev_create = open("reversed_create.txt", 'r')
for rec in rev_create.readlines():
    if len(rec) == 0: continue
    if "," not in rec: parts = [rec[1:-1]]
    parts = rec.strip()[1:-1].split(",")

    if len(parts) < 2: continue
    outs = parts[1].strip().split(',')
    if len(outs) > 1: continue
    unpro_out = outs[0].strip()
    out = key_property_processing(unpro_out)
    if len(out) != 3: continue

    unref = out[0]
    sep = unref.index(':')
    cat = unref[0:sep]
    namespace = unref[sep+1:]
    ings = parts[0].split(',')
    if cat == "item":
        gen_process(recipes, namespace, ings, basic_items, removed_items, out[1], out[2])
    elif cat == "tag" and namespace in tags:
        for item in tags[namespace]:
            gen_process(recipes, item, ings, basic_items, removed_items, out[1], out[2])

rev_create.close()

rev_mc = open("reversed_minecraft.txt", 'r')
for rec in rev_mc.readlines():
    if len(rec) == 0: continue
    if ',' not in rec: continue
    delim = rec.index(',')
    unpro_out = rec[0:delim].strip()
    out = item_property_processing(unpro_out)
    if len(out) != 3: continue

    namespaces = out[0]
    for namespace in namespaces:
        ings_str = rec[delim+1:].strip()
        if '[' in ings_str:
            ings_str = ings_str[1:].strip()
        if ']' in ings_str:
            ings_str = ings_str[:-1].strip()

        ings = ings_str.split(',')
        gen_process(recipes, namespace, ings, basic_items, removed_items, out[1], out[2])
rev_mc.close()

# test
temp_out = open("temp_out.txt", 'w')
for rec in recipes:
    temp_out.write(rec+ " - ")
    for ing in recipes[rec]:
        temp_out.write(ing + str(recipes[rec][ing]) + ", ")
    temp_out.write("\n")
temp_out.close()

for rec in recipes:
    recdict = recipes[rec]
    vals = list(recdict)
    if len(vals) == 0: continue
    item = vals.pop()
    stat_vals = []
    while len(stat_vals) < len(vals):
        if len(vals) == 0: break
        if (item in recipes) and (item not in basic_items):
            a_mult = recdict[item][0]
            p_mult = recdict[item][1]
            for val in recipes[item]:
                val = val.strip()
                if val == item: break
                dat = recipes[item][val]
                if val in recdict:
                    recdict[val][1] += dat[1] * p_mult
                    recdict[val][0] += dat[0] * a_mult + int(recdict[val][1])
                    recdict[val][1] %= 1
                else:
                    recdict[val] = [dat[0] * a_mult + int(dat[1] * p_mult), dat[1] * p_mult % 1]
                    if val not in vals: vals.append(val)
            del recdict[item]
        else:
            if item in stat_vals:
                item = vals.pop()
                continue

            vals.append(item)
            stat_vals.append(item)
        item = vals.pop()

itemfile = open("items.txt", 'r')
items = []
for line in itemfile.readlines():
    items.append(line.strip())
itemfile.close()

for rec in recipes:
    tbdeleted = []
    added = {}
    for item in recipes[rec]:
        vals = recipes[rec][item]
        if item in tags["c:storage_blocks"] and vals[0] < 1:
            sep = item.index(':')
            namespace = item[sep+1:]
            cat = 'm' # <c:ingots> and <c:gems>
            if "crate" in namespace or "bundle" in namespace:
                cat = 'v' # <c:foods/vegetable> and <c:foods/fruit>
            chopped = namespace.replace("_block", '').replace("_crate", '').replace("_bundle", '')
            if cat == 'm':
                app_items = tags["c:ingots"] + tags["c:gems"]
            elif cat == 'v':
                app_items = tags["c:foods/vegetable"] + tags["c:foods/fruit"]
            else:
                break

            for i in app_items:
                if chopped in i:
                    mult = 9
                    if i in ["create:cardboard_block", "ars_nouveau:source_gem_block", "ars_nouveau:magebloom_block", "minecraft:amethyst_block", "minecraft:quartz_block"]:
                        mult = 4
                    if i in rec:
                        rec[i][1] += vals[1] * mult
                        rec[i][0] += vals[0] * mult + int(val[i][1])
                        rec[i][1] %= 1
                    else:
                        added[i] = [vals[0] * mult, vals[1] * mult]
                    break
            tbdeleted.append(item)

    for item in tbdeleted:
        del recipes[rec][item]

for rec in recipes:
    tbdeleted = []
    added = {}
    for item in recipes[rec]:
        vals = recipes[rec][item]
        if (item in tags["c:ingots"] or item in tags["c:gems"]) and vals[0] < 1:
            sep = item.index(':')
            namespace = item[sep+1:]

            for i in tags["c:nuggets"]:
                if chopped in i:
                    if i in rec:
                        rec[i][0] += vals[0] * 9
                        rec[i][1] += vals[1] * 9
                    else:
                        added[i] = [vals[0] * 9, vals[1] * 9]
                    break
            tbdeleted.append(item)

    for item in tbdeleted:
        del recipes[rec][item]


skipped = placing_items_in_list("skipped.txt")

outfile = open("refined_recipes.txt", 'w')
itemfile = open("items.txt", 'r')
tot_items = itemfile.readlines()
tot_items.sort()
for line in tot_items:
    line = line.strip()
    if (line in skipped) or (line in basic_items) or (line in removed_items): continue
    outfile.write("item:" + line + " - ")
    if line in recipes:
        ings = recipes[line]
        for item in ings:
            amt = ings[item][0]
            chnc = ings[item][1]
            if (len(ings[item]) == 0): continue
            if amt == 0 or chnc == 0: continue
            ln = item
            if amt != 1:
                ln += " * " + str(int(amt + int(chnc)))
            if chnc % 1 != 0:
                ln += " % " + str(round((chnc * 100) % 100, 6))
            outfile.write(ln + ", ")
    outfile.write('\n')
outfile.close()
