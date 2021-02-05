from shop_tools import ShopCatalog


class Business:
    """
    A class which does a thing
        Defines the following attributes:
            name
            equipment
            workers

        Defines the following properties:

        Defines the following methods:
    """

    def __init__(self, name):
        self.name = name
        self.owner = ''
        self.equipment = {}
        self.workers = []
        self.__owner_possessive = ''
        self.__set_possesive(self.owner)

    def __set_possessive(self, word):
        if word.endswith('s'):
            self.__owner_possessive = self.owner + "'"
        else:
            self.__owner_possessive = self.owner + "'s"

    def open(self):
        print(f'{self.__owner_possessive} {self.name} is now open!')

    def close(self):
        print(f'The {self.name} is now closed!')

    def set_name(self, name):
        self.name = name

    def set_owner(self, owner):
        self.owner = owner

    def buy_equipment(self, equipment):
        # self.equipment.append(equipment)
        self.equipment.update({equipment.name: equipment})
        print(f'{self.name} is now the proud owner of a {equipment.name}')

    def hire_worker(self, worker):
        self.workers.append(worker)
        worker.assign_to_business(self)

    def lookup_tool_by_step(self, step):
        return self.equipment.get(step.name)


class WoodShop(Business):
    """
    A class which does a thing
        Defines the following attributes:
            catalog

        Defines the following properties:

        Defines the following methods:
            lookup_tool_by_step()
    """
    def __init__(self):
        self.name = 'Woodshop'
        self.catalog = ShopCatalog()
        super().__init__(self.name)

    def lookup_tool_by_step(self, step):
        if step.name == 'Turning':
            return self.equipment.get('lathe')
        if step.name == 'Drilling':
            pass
