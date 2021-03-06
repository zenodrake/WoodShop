from abc import ABC, abstractmethod
from collections import namedtuple
import crafting_steps as cs
import shop_tools as st


class WoodObject(ABC):
    """
    Base class for all WoodObjects
        Defines the following attributes:
            name
            is_planed
            is_jointed
            is_routed
            is_sanded

        Defines the following properties:

        Defines the following methods:
            set_planed()
            set_sanded()
            sed_jointed()
            set_routed()
    """
    def __init__(self, name):
        self.name = name
        self.is_planed = False
        self.is_jointed = False
        self.is_routed = False
        self.is_sanded = False

    def set_planed(self):
        self.is_planed = True

    def set_sanded(self):
        self.is_sanded = True

    def set_jointed(self):
        self.is_jointed = True

    def set_routed(self):
        self.is_routed = True


class FurnitureComponent(WoodObject):
    def __init__(self, name):
        self.name = name
        super().__init__(self.name)


class RoundLeg(FurnitureComponent):
    def __init__(self):
        self.name = 'Round leg'
        super().__init__(self.name)


class SquareLeg(FurnitureComponent):
    def __init__(self):
        self.name = 'Square leg'
        super().__init__(self.name)


class Board(FurnitureComponent):
    def __init__(self):
        self.name = 'Board'
        super().__init__(self.name)


class CompletedWoodObject(WoodObject):
    """
    A class which does a thing
        Defines the following attributes:
            req_parts
            __is_completed

        Defines the following properties:
            is_completed

        Defines the following methods:
    """
    def __init__(self, name):
        self.name = name
        super().__init__(self.name)
        self.req_parts = []
        self.__is_completed = False

    @property
    def is_completed(self):
        return self.__is_completed

    @abstractmethod
    def use(self):
        pass


class Bed(CompletedWoodObject):
    """
    A class which does a thing
        Defines the following attributes:
            length
            width
            height

        Defines the following properties:

        Defines the following methods:
            _set_defaults()
    """
    def __init__(self, furniture, **kwargs):
        self.name = 'Bed'
        super().__init__(self.name, furniture)
        self.length = kwargs.get('length')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self._set_defaults()

    def _set_defaults(self):
        if not self.length:
            self.length = 2

        if not self.width:
            self.width = 1.5

        if not self.height:
            self.height = .5

    def use(self):
        print('You are now asleep')


class Chair(CompletedWoodObject):
    """
    A class which does a thing
        Defines the following attributes:
            name
            cushioned
            __num_legs
            max_weight
            weight

        Defines the following properties:
            num_legs

        Defines the following methods:
    """
    WEIGHT_LIMIT_PER_LEG = 100
    WEIGHT_PER_LEG = 1
    WEIGHT_OF_SEAT = 2
    WEIGHT_OF_BACK = 1

    def __init__(self, blueprint, **kwargs):
        self.name = 'Chair'
        self.cushioned = False
        super().__init__(self.name)
        self.__num_legs = blueprint.num_legs

        if self.__num_legs is None:
            self._num_legs = 4
        elif self.__num_legs < -1:
            raise InvalidLegNumber("Chairs must have at least -1 legs. Don't ask")

        self.max_weight = self.__num_legs * self.WEIGHT_LIMIT_PER_LEG
        self.weight = self.WEIGHT_OF_SEAT + self.WEIGHT_OF_BACK + self.WEIGHT_PER_LEG * self.__num_legs

    @property
    def num_legs(self):
        return self.__num_legs

    @num_legs.setter
    def num_legs(self, v):
        if v < -1:
            raise InvalidLegNumber("Chairs must have at least -1 legs. Don't ask")

        if v < self.__num_legs:
            print(f'You hack off {self._num_legs - v} legs until the chair looks right')
        elif v > self.__num_legs:
            print(f'Casting about, you find some spare legs just standing (ha!) around and affix them to the chair')

        self.__num_legs = v

    def use(self):
        if self.cushioned:
            addendum = 'It is comfy. '
        else:
            addendum = ''
        if self._num_legs == -1:
            print('You hear a distant sound of something falling over...')
            print("Anyway, you're now sitting in the chair.", addendum)
        elif self._num_legs == 0:
            print(f"You are now sitting in the {self.name}.", addendum, "Everything seems taller...")
        elif self._num_legs == 1:
            print(f"You are now sitting in the {self.name}.", addendum, "It's rather unsteady")
        elif self._num_legs == 2:
            print(f"You are now sitting in the {self.name}.", addendum, "It's a bit wobbly")
        else:
            print(f"You are now sitting in the {self.name}.", addendum)


class CushionedChair(Chair):
    """
    A class which does a thing
        Defines the following attributes:
            name
            cushioned

        Defines the following properties:

        Defines the following methods:
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'Cushioned Chair'
        self.cushioned = True


class CuttingBoard(CompletedWoodObject):
    """
    A class which does a thing
        Defines the following attributes:
            length
            width
            height

        Defines the following properties:

        Defines the following methods:
    """
    def __init__(self, furniture, **kwargs):
        self.name = 'Cutting Board'
        super().__init__(self.name, furniture)
        self.length = kwargs.get('length') or .30
        self.width = kwargs.get('width') or .20
        self.height = kwargs.get('height') or .5

    def use(self):
        print('You cut mightily')


class Desk(CompletedWoodObject):
    """
    A class which does a thing
        Defines the following attributes:
            length
            width
            height

        Defines the following properties:
            size
            area
            volume

        Defines the following methods:
            _set_defaults
    """
    def __init__(self, furniture, **kwargs):
        self.name = 'Desk'
        super().__init__(self.name, furniture)
        self.length = kwargs.get('length')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self._set_defaults()

    def _set_defaults(self):
        if not self.length:
            self.length = 2

        if not self.width:
            self.width = 1.5

        if not self.height:
            self.height = 1.2

    @property
    def size(self):
        return self.length, self.width, self.height

    @property
    def area(self):
        area = round(self.length * self.width, 2)
        return f'This {self.name} has an area of {area} square meters'

    @property
    def volume(self):
        v = round(self.length * self.width * self.height, 2)
        return f'This {self.name} is {v} cubic meters'

    def use(self):
        print(f'You are now using the {self.name} to write a thing')


class Drawer(CompletedWoodObject):
    """
    A class which does a thing
        Defines the following attributes:
            length
            width
            height
            _stored_items

        Defines the following properties:

        Defines the following methods:
            _set_defaults()
            __iter__()
            __get_item__()
            retrieve_item()
            retrieve_items()
            store_item()
            store_items()
    """
    def __init__(self, furniture, **kwargs):
        self.name = 'Drawer'
        super().__init__(self.name, furniture)
        self.length = kwargs.get('length')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self._stored_items = []
        self._set_defaults()

    def __getitem__(self, i):
        try:
            rtn_item = self._stored_items.pop(self._stored_items.index(i))
            return rtn_item
        except ValueError:
            raise UnstoredItemError(i, self.name)

    def __iter__(self):
        return self._stored_items.__iter__()

    def _set_defaults(self):
        if not self.length:
            self.length = 2

        if not self.width:
            self.width = 1.5

        if not self.height:
            self.height = 1.2

    def retrieve_item(self, item):
        return self.__getitem__(item)

    def retrieve_items(self, items):
        returned = []
        for item in items:
            try:
                rtn_item = self._stored_items.pop(self._stored_items.index(item))
                returned.append(rtn_item)
            except ValueError:
                raise UnstoredItemError(item, self.name)

    def store_item(self, item):
        self._stored_items.append(item)

    def store_items(self, items):
        for item in items:
            self.store_item(item)

    def use(self):
        print(f'You are now using the {self.name} to draw something')


class Sofa(CompletedWoodObject):
    """
        A class which does a thing
            Defines the following attributes:
                length
                width
                height

            Defines the following properties:

            Defines the following methods:

        """
    def __init__(self, furniture, **kwargs):
        self.name = 'Sofa'
        super().__init__(self.name, furniture)
        self.length = kwargs.get('length')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self._set_defaults()

    def _set_defaults(self):
        if not self.length:
            self.length = 2

        if not self.width:
            self.width = 1

        if not self.height:
            self.height = .25

    def use(self):
        print('You are now sitting down')


class Table(CompletedWoodObject):
    """
        A class which does a thing
            Defines the following attributes:
                length
                width
                height
                num_leaves

            Defines the following properties:
                size
                area
                volume

            Defines the following methods:

        """
    def __init__(self, furniture, **kwargs):
        self.name = 'Table'
        super().__init__(self.name, furniture)
        self.length = kwargs.get('length')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.num_leaves = kwargs.get('num_leaves')
        self._set_defaults()

    def _set_defaults(self):
        if not self.length:
            self.length = 2

        if not self.width:
            self.width = 1.5

        if not self.height:
            self.height = 1.2

        if not self.num_leaves:
            self.num_leaves = 0

    @property
    def size(self):
        return self.length, self.width, self.height

    @property
    def area(self):
        area = round(self.length * self.width, 2)
        return f'This {self.name} has an area of {area} square meters'

    @property
    def volume(self):
        v = round(self.length * self.width * self.height, 2)
        return f'This {self.name} is {v} cubic meters'

    def use(self):
        print(f'You are now using the {self.name} to defer doing something')


class UnstoredItemError(Exception):
    """Raised by the Drawer when something it isn't storing is asked to be retrieved"""
    def __init__(self, item, wood_object):
        super().__init__(f"There is no {item} in this {wood_object}")


class InvalidLegNumber(Exception):
    """Raised by Chairs when the number of legs isn't to their liking"""
    def __init__(self, *args):
        pass
        # super().__init__(*args)


if __name__ == '__main__':
    pass
