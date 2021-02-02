import time
import crafting_steps as cs

TURN_ON_TIME = 3
TURN_OFF_TIME = 3
TURN_ON_STEP = .1
TURN_OFF_STEP = .1
LOADING_TIME = 3
LOADING_STEP = .1


class ShopTool:
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
        if any((isinstance(step, Step) for Step in self.acceptable_steps)):
            return True
        else:
            raise InvalidStepError(f"The {self.name.title()} doesn't know how to perform {step.name}")

    def _initilize(self, init_string, total_init_time, init_step):
        print(init_string, end='')
        for i in range(total_init_time):
            print('.', end='')
            time.sleep(init_step)
        print('DONE')

    def use(self):
        pass


class PoweredShopTool(ShopTool):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def turn_on(self):
        print(f'Turning on {self.name.title()}', end='')
        for i in range(TURN_ON_TIME):
            print('.', end='')
            time.sleep(TURN_ON_STEP)
        print('DONE')
        self.is_on = True

    def turn_off(self):
        print(f'Turning off {self.name.title()}', end='')
        for i in range(TURN_OFF_TIME):
            print('.', end='')
            time.sleep(TURN_OFF_STEP)
        self.is_on = False
        print('DONE')

    def use(self):
        if not self.is_on:
            self.turn_on()
        else:
            print(f'{self.name.title()} is already on.')


class BandSaw(PoweredShopTool):
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
        step.perform()


class DrillPress(PoweredShopTool):
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

    def use(self, step):
        if self._is_step_acceptable(step):
            self.secure_workpiece()
            super().use()
            super().turn_off()

    def secure_workpiece(self):
        super()._initilize('Securing work piece', self.loading_time, self.loading_step)


class DustCollector(PoweredShopTool):
    def __init__(self, **kwargs):
        self.name = 'dust collector'
        self.acceptable_steps = []
        super().__init__(self.name, **kwargs)


class Jointer(PoweredShopTool):
    def __init__(self, **kwargs):
        self.name = 'jointer'
        self.acceptable_steps = [cs.JointingStep]
        super().__init__(self.name, **kwargs)

    def use(self, step):
        if self._is_step_acceptable(step):
            self.load_work_piece()
            super().use()
            self.joint_wood(step)
            super().turn_off()

    def joint_wood(self, step):
        step.perform()

    def load_work_piece(self):
        super()._initilize('Loading work piece', self.loading_time, self.loading_step)


class Lathe(PoweredShopTool):
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
        step.perform()

    def load_work_piece(self):
        super()._initilize('Loading work piece', self.loading_time, self.loading_step)


class Padder(PoweredShopTool):
    def __init__(self, **kwargs):
        self.name = 'padder'
        self.acceptable_steps = [cs.PaddingStep]
        super().__init__(self.name, **kwargs)

    def use(self, step):
        if self._is_step_acceptable(step):
            super().use()
            self.add_padding(step)

    def add_padding(self, step):
        super()._initilize('Affixing part', self.loading_time, self.loading_step)
        super()._initilize('Loading padding', self.loading_time, self.loading_step)
        step.perform()


class Planer(PoweredShopTool):
    def __init__(self, **kwargs):
        self.name = 'planer'
        self.acceptable_steps = [cs.PlaningStep]
        super().__init__(self.name, **kwargs)

    def use(self, step):
        if self._is_step_acceptable(step):
            super().use()
            self.plane_wood(step)

    def plane_wood(self, step):
        super()._initilize('Feeding board', self.loading_time, self.loading_sep)
        step.perform()


class Router(PoweredShopTool):
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
        step.perform()


class Sander(PoweredShopTool):
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
        step.perform()


class ScrollSaw(PoweredShopTool):
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
        step.perform()


class TableSaw(PoweredShopTool):
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
        step.perform()


class WorkBench(ShopTool):
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
        super()._initilize('Clamping workpiece in place', self.loading_time, self.loading_step)


class InvalidStepError(Exception):
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