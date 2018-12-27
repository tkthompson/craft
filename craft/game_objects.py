import re as regex
import json
import datetime
import os

"""
Returns string formatted as formatted as [string]
"""
def bracketize(string):
    return "[" + str(string) + "]"

"""
Returns a formatted time string of current time
show_ms: whether the timestamp should show milliseconds {date/time}.milliseconds
is_filename: gives date and time
 - false yields [hh:mm:ss]
 - true yields yyyy-mm-dd_hh-mm-ss
"""
def getFormattedTime(show_ms = True, is_filename = False):
    current_time = str(datetime.datetime.now())
    if is_filename:
        current_time = regex.sub(":", "-", current_time)
        current_time = regex.sub(" ", "_", current_time)
    else:
        temp = current_time.split(" ")
        current_time = bracketize(temp[1])
    if show_ms:
        return current_time
    else:
        return regex.sub("\.\d+", "", current_time)

# Logging class for user logs
class GameLogger:
    def __init__(self, log_name):
        self.log_name = "logs/game/" + getFormattedTime(show_ms = False, is_filename = True) + "_" + log_name
        self.flair = ""

    """
    Changes flair and returns updated flair string.  Returns current value if no args given
    """
    def Flair(self, function = "add", flair = [""]):
        if function == "new":
            self.flair = ""
            for i in flair:
                if i:
                    self.flair += bracketize(i)
        elif function == "add":
                for i in flair:
                    if i:
                        self.flair += bracketize(i)
        elif function == "del":
            temp = ""
            for i in flair:
                temp = "\[" + i + "\]"
                self.flair = regex.sub(temp, "", self.flair)
        return self.flair

    def msg(self, message, show_ms = False, flair = ""):
        prefix = getFormattedTime(show_ms = show_ms) + flair + ": "
        with open(self.log_name, "a") as f:
            f.write(prefix + message + "\n")

"""
Ensures all required tags are in tags input
"""

def checkTagInput(input):
    if input == None:
        return False
    required_tags_file = open("required_tags.txt")
    required_tags = required_tags_file.readlines()
    output = True
    newline = r"\n"
    for i in required_tags:
        i = regex.sub(newline, "", i)
        if i in input:
            continue
        else:
            print("Required tag \"{0}\" missing!\n".format(i))
            output = False
            break
    required_tags_file.close()
    return output

"""
Superclass for any object the player can interact with, including Items, NPCs, Animals, etc
"""
class _Interactable:

    def __init__(self, name, description, verbs, tags):
        self.name = name
        self.description = description
        self.verbs = verbs
        self.tags = tags

    """
    Puts the object in a dictionary format
    """
    def dictify(self):
        return {"name":self.name, "description":self.description, "verbs":self.verbs, "tags":self.tags}

    """
    Outputs a json file named "filename" to the /obj directory
    Used to store objects for later use
    """
    def jsonify(self, filename):
        try:
            json.dump(self.dictify(), open("obj/" + filename, "w"), indent=4)
            return True
        except:
            print("An error occurred while attempting to write \"{}\"".format(filename))
            return False
    

# Superclass for all items (objects usable in crafting interface)
class Item(_Interactable):
    def __init__(self, value = None, file = None):
        try:
            if not (file == None):
                import_data = json.load(open(file, "r"))
                super().__init__(import_data.get("name", None), import_data.get("description", None), import_data.get("verbs", None), import_data.get("tags", None))
                self.value = import_data.get("value", None)
        except IOError:
            print("File \"{}\" not found.".format(file))
        finally:
            super().__init__(None, None, None, None)
            self.value = None

    def dictify(self):
        output = super().dictify()
        output["value"] = self.value
        return output

# Class to hold item recipes
class Recipe:
    def __init(self, file == None):
        recipe = json.load(open(file + ".json", "r"))
        self.name = recipe.get("name", None)
        self.ingredients = recipe.get("ingredients", [])
    
    def createNew(self):
        self.name = input("Recipe name (internal id): ")
        running = True
        iteration = 1
        while(running):
            print("Criteria for ingredient {}".format(iteration))
            itemName = input("The name of the item (enter \"any\" if irrelevant): ")
            playerInput = input("Does the item have any necessary tags? ")
            if not regex.match(r"[yY]",playerInput):
                self.ingredients.append({"item_name":itemName})
            else:
                i = 0
                tagName = []
                criteria = []
                while regex.match(r"[yY]",playerInput):
                    tagName[i] = input("Tag name: ")
                    criteria[i] = input("Criterion (>,<,>=,<=,=)(#): ")
                    criterion.replace(" ","")
                    i += 1
                self.ingredients.append({"item_name":itemName, "tag":tagName, "criterion":criterion})
                

class Inventory:
    def __init__(self, file = None, *args):
        if not file == None:
            data = json.load(open("obj/inv/" + file, "r"))
            self.inventory = data.get("items", [])
        else:
            self.inventory = []
        if not args == None:
            for item in args:
                self.inventory.append(item)

    def addInventory(self, *args):
        for inventory in args:
            for item in inventory:
                self.inventory.append(item)

class Actor(_Interactable, Inventory):
    def __init__(self, file, inventory_file = None):
        import_data = json.load(open("obj/actor/" + file, "r"))
        _Interactable.__init__(import_data.get("name", None), import_data.get("description", None), import_data.get("verbs", None), import_data.get("tags", None))
        Inventory.__init__(file = inventory_file)
        self.health = import_data.get("health", 0)
        
class Player:
    
    def __init__(self, file):
        save = json.load(open(file, "r"))
        self.name = save.get("name", "")
        self.xp = save.get("xp", 0)
        self.skill = int(self.xp / 100)
        self.health = save.get("health", 1)
        self.inventory = save.get("inventory", {})