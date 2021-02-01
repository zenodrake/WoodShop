class Skill:
    def __init__(self, name):
        self.name = name

    def utilize(self):
        pass


class Clean(Skill):
    def __init__(self):
        super().__init__('Clean Up')

    def __call__(self, item):
        self.clean(item)

    def clean(self, item):
        print(f'Now cleaning {item}')
        print(f'{item} is now clean')


class Repair(Skill):
    def __init__(self):
        super().__init__('Repair')

    def __call__(self, broken_item):
        self.repair(broken_item)

    def repair(self, item):
        print(f'Now repairing {item}')
        print(f'{item} is now repaired')
