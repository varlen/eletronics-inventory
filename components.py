componentsFile = open("./Componentes.csv")

components = []
types = []

# example partslist
BIG_MUFF = """4 BJT 2N5088
4 DI 1N4148
3 Pot B100K
4 C 1uF
4 C 100nF
3 C 470pF
1 C 4nF
1 C 10nF
5 R 10K
3 R 100K
3 R 470K
2 R 39K
2 R 150
2 R 15K
1 R 47K
1 R 100
1 R 3K3
1 R 1K
1 R 22K
"""

INTRO = """# Components Database v0.1

    This program keeps track of electronic parts. Run it with a Python interactive shell.
    Call showHelp() for usage examples.
"""
print(INTRO)

def showHelp():
    
    HELP = """Usage examples:

    1) Generate shoplist for example project:
    >> show(partslist(from_text(BIG_MUFF)))

    2) Query how many components of a given type are available:
    >> howMany('R','47K')
    """
    print(HELP)

class PartsList():
    def __init__(self,have,buy):
        self.have = have
        self.buy = buy

    def __str__(self):
        pl = """:: HAVE 👍  ::
"""
        have_strs = [ quantity + " - " + part + " " + value for part,value,quantity in self.have ]
        pl += "\n".join(have_strs)
        pl += """

:: SHOP 💸  ::
"""
        buy_strs = [ quantity + " - " + part + " " + value  for part,value,quantity in self.buy ]
        pl += "\n".join(buy_strs)
        pl += "\n\n"
        return pl

class Component(object):
    def __init__(self,theType,value,description,quantity):
        self.type = theType.strip()
        self.value = value.strip()
        self.description = description.strip()
        self.quantity = quantity.strip()

    def __str__(self):
        if int(self.quantity) == 1:
            qualifier = " disponível"
        else:
            qualifier = " disponíveis"
        return self.type + " (" + self.value + ") " + self.description + " - " + self.quantity + qualifier


for index, line in enumerate(componentsFile):
    if index == 0:
        # skip header
        continue
    componentData = line.strip().split(";")
    component = Component(componentData[0],componentData[3], componentData[1], componentData[2])
    components.append(component)
    if not componentData[0] in types:
        types.append(component.type)

def allTypes():
    types.sort()
    print(", ".join(types))

def ofType(theType):
    selected = [ x for x in components if x.type == theType ]
    return selected

def howMany(theType, theValue = ""):
    selected = [ int(x.quantity) for x in components if x.type == theType and x.value.startswith(theValue) ]
    return sum(selected)

def show(obj):
    if type(obj) is PartsList:
        print(obj)
    elif type(obj) is list:
        [ print(x) for x in obj ]
    else:
        print("Can't show this")

def partslist(the_list_of_parts_values_quants):
    have = []
    buy = []
    for part,value,quantity in the_list_of_parts_values_quants:
        currentQuantity = howMany(part,value)
        required = int(quantity)
        if currentQuantity < required:
            how_many_missing = required - currentQuantity
            buy.append((part,value,str(how_many_missing)))
        else:
            have.append((part,value,quantity))
    return PartsList(have,buy)

def from_text(partslist_text):
    requirements = []
    if type(partslist_text) is str:
        partslist_text = partslist_text.split("\n")
    for line in partslist_text:
        line_data = line.strip().split(" ")
        quantity = line_data[0]
        if quantity.isnumeric():
            part = line_data[1]
            value = line_data[2]
            requirements.append((part, value, quantity))
    return requirements
