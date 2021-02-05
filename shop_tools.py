import time
import crafting_steps as cs

TURN_ON_TIME = 3
TURN_OFF_TIME = 3
TURN_ON_STEP = .1
TURN_OFF_STEP = .1
LOADING_TIME = 3
LOADING_STEP = .1


class ShopTool:
    """Super class for all other tools.

    Defines the following attributes:
        name
        brand
        price
        foot_print
        needed_power
        weight
        is_repaired
        is_being_used
        is_cleaned
        is_on
        __loading_time
        __loading_step

    Defines the following properties:
        loading_time -- the number of steps it takes to load a piece of wood into the tool
        loading_step -- the time each step takes to complete.


    Defines the following methods:
        _is_step_acceptable()
        _initialize_tool()
        use() -- this is overridden by each subclass
        """
    def __init__(self, name, **kwargs):
        self.name = name
        self.brand = kwargs.get('brand')
        self.price = kwargs.get('price')
        self.foot_print = kwargs.get('foot_print')
        self.needed_power = kwargs.get('needed_power')
        self.weight = kwargs.get('weight')
        self.is_repaired = True
        self.is_being_used = False
        self.is_cleaned = True
        self.is_on = False
        self.__loading_time = LOADING_TIME
        self.__loading_step = LOADING_STEP

    @property
    def loading_time(self):
        return self.__loading_time

    @property
    def loading_step(self):
        return self.__loading_step

    def _is_step_acceptable(self, step):
        """Returns true if <step> is in [acceptable_steps]."""
        if any((isinstance(step, Step) for Step in self.acceptable_steps)):
            return True
        else:
            raise InvalidStepError(f"The {self.name.title()} doesn't know how to perform {step.name}")

    def _initilize_tool(self, init_string, total_init_time, init_step):
        """Display the initialization routine for the tool.
        <init_string> <total_init_time> and <init_step> are all defined by the calling subclass
        <init_string> is the string which will be displayed
        <total_init_time> is the number of steps it takes to initialize the tool
        <init_step> is the time each step takes to complete"""
        print(init_string, end='')
        for i in range(total_init_time):
            print('.', end='')
            time.sleep(init_step)
        print('DONE')

    def use(self):
        pass


class PoweredShopTool(ShopTool):
    """The super class for all ShopTools which need electricity to work.
    Defines the following methods:
        turn_on()
        turn_off()
    """
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def turn_on(self):
        """Turn on the tool if it is not already on"""
        print(f'Turning on {self.name.title()}', end='')
        for i in range(TURN_ON_TIME):
            print('.', end='')
            time.sleep(TURN_ON_STEP)
        print('DONE')
        self.is_on = True

    def turn_off(self):
        """Turn off the tool"""
        print(f'Turning off {self.name.title()}', end='')
        for i in range(TURN_OFF_TIME):
            print('.', end='')
            time.sleep(TURN_OFF_STEP)
        self.is_on = False
        print('DONE')

    def use(self):
        """Check for on-ness. If it is on, Do nothing. If it isn't, turn it on"""
        if not self.is_on:
            self.turn_on()
        else:
            print(f'{self.name.title()} is already on.')


class BandSaw(PoweredShopTool):
    """A powered tool for cutting thick pieces of wood.
    Defines the following attributes:
        max_piece_height
        acceptable_steps

    Defines the following methods:
        use()
        cut_wood()
    """

    def __init__(self, **kwargs):
        self.name = 'band saw'
        self.max_piece_height = kwargs.get('max_piece_height')
        self.acceptable_steps = [cs.CuttingStep]
        super().__init__(self.name, **kwargs)

    def use(self, step):
        if self._is_step_acceptable(step):
            super().use()
            self.cut_wood(step)
            super().turn_off()

    def cut_wood(self, step):
        """Not to be called directly. Call use() instead.
        This method merely calls the perform() method for whatever <step> is passed to it"""
        step.perform()


class DrillPress(PoweredShopTool):
    """A powered tool for drilling holes in things.
        Defines the following attributes:
            max_piece_height
            acceptable_steps
            __loading_time. see ShopTool for description
            __loading_step. see ShopTool for description

        Defines the following properties:
            loading_time
            loading_step

        Defines the following methods:
            use()
            secure_workpiece()
            drill()
        """
    def __init__(self, **kwargs):
        self.name = 'drill press'
        super().__init__(self.name, **kwargs)
        self.max_piece_height = kwargs.get('max_piece_height')
        self.acceptable_steps = [cs.DrillingStep]
        self.__loading_time = 2
        self.__loading_step = .1

    @property
    def loading_time(self):
        return self.__loading_time

    @property
    def loading_step(self):
        return self.__loading_step

    def drill(self, step):
        """Not to be called directly. Call use() instead.
        This method merely calls the perform() method for whatever <step> is passed to it"""
        step.perform()

    def use(self, step):
        if self._is_step_acceptable(step):
            self.secure_workpiece()
            super().use()
            super().turn_off()

    def secure_workpiece(self):
        """Not to be called directly. Call use() instead.
        This method merely calls the perform() method for whatever <step> is passed to it"""
        super()._initilize_tool('Securing work piece', self.loading_time, self.loading_step)


class DustCollector(PoweredShopTool):
    """A powered tool for collecting dust. Not sure how to implement it as yet, but if it is attached to another tool
    then the sawdust generated by that tool will go into the DustCollector instead onto the floor.
    Will be important when it comes time for the Worker to clean up"""
    def __init__(self, **kwargs):
        self.name = 'dust collector'
        self.acceptable_steps = []
        super().__init__(self.name, **kwargs)


class Jointer(PoweredShopTool):
    """A powered tool for making parallel two narrow sides of a board.
        Defines the following attributes:
            max_piece_width
            acceptable_steps

        Defines the following methods:
            use()
            load_workpiece()
            joint_wood()
    """
    def __init__(self, **kwargs):
        self.name = 'jointer'
        self.acceptable_steps = [cs.JointingStep]
        self.max_piece_width = kwargs.get('max_piece_width')
        super().__init__(self.name, **kwargs)

    def use(self, step):
        if self._is_step_acceptable(step):
            self.load_work_piece()
            super().use()
            self.joint_wood(step)
            super().turn_off()

    def joint_wood(self, step):
        """Not to be called directly. Call use() instead.
        This method merely calls the perform() method for whatever <step> is passed to it"""
        step.perform()

    def load_workpiece(self):
        """Not to be called directly. Call use() instead.
        This method merely calls the perform() method for whatever <step> is passed to it"""
        super()._initilize_tool('Loading work piece', self.loading_time, self.loading_step)


class Lathe(PoweredShopTool):
    """A powered tool for making cylinders and cylindrical things.
        Defines the following attributes:
            max_piece_length
            max_speed
            min_speed
            acceptable_steps
            __loading_time. see ShopTool for description
            __loading_step. see ShopTool for description

        Defines the following properties:
            loading_time
            loading_step

        Defines the following methods:
            use()
            turn_wood()
            load_workpiece()
        """
    def __init__(self, **kwargs):
        self.name = 'lathe'
        self.max_piece_length = kwargs.get('max_piece_length')
        self.max_speed = kwargs.get('max_speed')
        self.min_speed = kwargs.get('min_speed')
        self.acceptable_steps = [cs.TurningStep]
        super().__init__(self.name, **kwargs)
        self.__loading_time = 4
        self.__loading_step = .1

    @property
    def loading_time(self):
        return self.__loading_time

    @property
    def loading_step(self):
        return self.__loading_step

    def use(self, step):
        if self._is_step_acceptable(step):
            self.load_work_piece()
            super().use()
            self.turn_wood(step)
            super().turn_off()

    def turn_wood(self, step):
        """Not to be called directly. Call use() instead.
        This method merely calls the perform() method for whatever <step> is passed to it"""
        step.perform()

    def load_workpiece(self):
        """Not to be called directly. Call use() instead.
        This method merely calls the perform() method for whatever <step> is passed to it"""
        super()._initilize_tool('Loading work piece', self.loading_time, self.loading_step)


class Padder(PoweredShopTool):
    """A powered tool for adding cushioning to things.
        Defines the following attributes:
            max_piece_height
            acceptable_steps

        Defines the following methods:
            use()
            add_padding()
        """
    def __init__(self, **kwargs):
        self.name = 'padder'
        self.acceptable_steps = [cs.PaddingStep]
        super().__init__(self.name, **kwargs)

    def use(self, step):
        if self._is_step_acceptable(step):
            super().use()
            self.add_padding(step)

    def add_padding(self, step):
        """Not to be called directly. Call use() instead.
        This method merely calls the perform() method for whatever <step> is passed to it"""
        super()._initilize_tool('Affixing part', self.loading_time, self.loading_step)
        super()._initilize_tool('Loading padding', self.loading_time, self.loading_step)
        step.perform()


class Planer(PoweredShopTool):
    """A powered tool for making parallel the two broad sides of a board.
        Defines the following attributes:
            max_piece_height
            acceptable_steps

        Defines the following methods:
            use()
            plane_wood()
        """
    def __init__(self, **kwargs):
        self.name = 'planer'
        self.acceptable_steps = [cs.PlaningStep]
        super().__init__(self.name, **kwargs)

    def use(self, step):
        if self._is_step_acceptable(step):
            super().use()
            self.plane_wood(step)

    def plane_wood(self, step):
        """Not to be called directly. Call use() instead.
        This method merely calls the perform() method for whatever <step> is passed to it"""
        super()._initilize_tool('Feeding board', self.loading_time, self.loading_sep)
        step.perform()


class Router(PoweredShopTool):
    """A powered tool for rounding off edges or hollowing out part of a thing.
        Defines the following attributes:
            max_piece_height
            acceptable_steps

        Defines the following methods:
            use()
            route_wood()
        """
    def __init__(self, **kwargs):
        self.name = 'router'
        self.acceptable_steps = [cs.RoutingStep]
        super().__init__(self.name, **kwargs)

    def use(self, step):
        if self._is_step_acceptable(step):
            super().use()
            self.route_wood(step)
            super().turn_off()

    def route_wood(self, step):
        """Not to be called directly. Call use() instead.
        This method merely calls the perform() method for whatever <step> is passed to it"""
        step.perform()


class Sander(PoweredShopTool):
    """A powered tool for sanding and making smooth things.
        Defines the following attributes:
            max_piece_height
            acceptable_steps

        Defines the following methods:
            use()
            sand_wood()
        """
    def __init__(self, **kwargs):
        self.name = 'sander'
        self.acceptable_steps = [cs.SandingStep]
        super().__init__(self.name, **kwargs)

    def use(self, step):
        if self._is_step_acceptable(step):
            super().use()
            self.sand_wood(step)
            super().turn_off()

    def sand_wood(self, step):
        """Not to be called directly. Call use() instead.
        This method merely calls the perform() method for whatever <step> is passed to it"""
        step.perform()


class ScrollSaw(PoweredShopTool):
    """A powered tool for cutting intricate shapes in things.
        Defines the following attributes:
            max_piece_height
            acceptable_steps

        Defines the following methods:
            use()
            cut_wood()
        """
    def __init__(self, **kwargs):
        self.name = 'scroll saw'
        self.acceptable_steps = [cs.CuttingStep]
        super().__init__(self.name, **kwargs)

    def use(self, step):
        if self._is_step_acceptable(step):
            super().use()
            self.cut_wood(step)
            super().turn_off()

    def cut_wood(self, step):
        """Not to be called directly. Call use() instead.
        This method merely calls the perform() method for whatever <step> is passed to it"""
        step.perform()


class TableSaw(PoweredShopTool):
    """A powered tool for cutting boards either lengthwise or widthwise.
        Defines the following attributes:
            max_piece_height
            acceptable_steps

        Defines the following methods:
            use()
            cut_wood()
        """
    def __init__(self, **kwargs):
        self.name = 'table saw'
        self.acceptable_steps = [cs.CuttingStep]
        super().__init__(self.name, **kwargs)

    def use(self, step):
        if self._is_step_acceptable(step):
            super().use()
            self.cut_wood(step)
            super().turn_off()

    def cut_wood(self, step):
        """Not to be called directly. Call use() instead.
        This method merely calls the perform() method for whatever <step> is passed to it"""
        step.perform()


class WorkBench(ShopTool):
    """An unpowered tool primarily for assembling FurnitureComponents but also Gluing, Sanding, and Fastening.
        Defines the following attributes:
            max_piece_height
            acceptable_steps

        Defines the following methods:
            use()
            clamp_piece()
        """
    def __init__(self, **kwargs):
        self.name = 'work bench'
        self.acceptable_steps = [cs.GluingStep, cs.SandingStep, cs.FasteningStep]
        super().__init__(self.name, **kwargs)

    def use(self, step):
        if self._is_step_acceptable(step):
            self.clamp_piece()
            super().use()
            step.perform()

    def clamp_piece(self):
        """Not to be called directly. Call use() instead.
        This method merely calls the perform() method for whatever <step> is passed to it"""
        super()._initilize_tool('Clamping workpiece in place', self.loading_time, self.loading_step)


class InvalidStepError(Exception):
    """Used to indicate when a step passed to a ShopTool is not in its acceptable_steps attribute"""
    pass


# thinking this might function similar to the WoodObjectEncyclopedia, in that it would be our Factory for creating
# shop tools
class ShopCatalog:
    def __init__(self):
        pass



if __name__ == '__main__':
    import blueprints

    tool = DrillPress()
    tool = WorkBench()

    desk = blueprints.WoodObjectEncyclopedia.get_blueprint('desk')
    for s in desk.steps:
        try:
            tool.use(s)
        except InvalidStepError as e:
            print(f'Skipping {s.name} as the {tool.name} cannot handle it')