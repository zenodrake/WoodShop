from shop_tools import ShopCatalog

class Business:
    def __init__(self, name):
        self.name = name
        self.equipment = {}
        self.workers = []

    def open(self):
        print('Business is now open!')

    def close(self):
        print('Business is now closed!')

    def set_name(self, name):
        self.name = name + ' ' + self.name

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
    def __init__(self):
        self.name = 'Woodshop'
        self.catalog = ShopCatalog()
        super().__init__(self.name)

    def lookup_tool_by_step(self, step):
        if step.name == 'Turning':
            return self.equipment.get('lathe')
        if step.name == 'Drilling':
            pass
