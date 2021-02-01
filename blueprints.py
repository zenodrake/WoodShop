from collections import namedtuple
import crafting_steps as cs

DEFAULT_NUM_LEGS = 4

class Blueprint:

    def __init__(self, name, design):
        self.name = name
        self.steps = design.steps
        self.req_tools = design.req_tools
        self._calculate_turning_steps()
        self._calculate_assembly_time()

    def _calculate_assembly_time(self):
        self.assembly_time = 0
        for step in self.steps:
            self.assembly_time += step.time_to_complete

    def _calculate_turning_steps(self):
        if hasattr(self, 'num_legs'):
            for i in range(self.num_legs):
                self.steps.insert(0, cs.TurningStep())


class ChairBlueprint(Blueprint):
    def __init__(self, design, **kwargs):
        self.name = 'chair'
        num_legs = kwargs.get('num_legs')

        if num_legs:
            self.num_legs = num_legs
        else:
            self.num_legs = DEFAULT_NUM_LEGS
        super().__init__(self.name, design)


class CushionedChairBlueprint(ChairBlueprint):
    def __init__(self, design, **kwargs):
        super().__init__(design, **kwargs)
        self.name = 'cushioned chair'
        self.cushioned = True


class BedBlueprint(Blueprint):
    def __init__(self, design, **kwargs):
        self.name = 'bed'
        super().__init__(self.name, design, **kwargs)


class CuttingBoardBlueprint(Blueprint):
    def __init__(self, design, **kwargs):
        self.name = 'cutting board'
        super().__init__(self.name, design, **kwargs)


class DeskBlueprint(Blueprint):
    def __init__(self, design, **kwargs):
        self.name = 'desk'
        super().__init__(self.name, design, **kwargs)


class DrawerBlueprint(Blueprint):
    def __init__(self, design, **kwargs):
        self.name = 'drawer'
        super().__init__(self.name, design, **kwargs)


class SofaBlueprint(Blueprint):
    def __init__(self, design, **kwargs):
        self.name = 'sofa'
        super().__init__(self.name, design, **kwargs)


class TableBlueprint(Blueprint):
    def __init__(self, design, **kwargs):
        self.name = 'table'
        num_legs = kwargs.get('num_legs')

        if num_legs:
            self.num_legs = num_legs
        else:
            self.num_legs = DEFAULT_NUM_LEGS
        super().__init__(self.name, design, **kwargs)


class UnknownItemError(KeyError):
    def __init__(self, item_name):
        super().__init__(f'An object of name "{item_name}" does not exist in the Encyclopedia')


class WoodObjectEncyclopedia:
    """This class stores all the information about creating furniture
    This information takes the form of a namedtuple called Furniture
    which stores the class--called constructor--the steps to craft, and required tools for assembly
    """
    __name = 'Encyclopedia of Wood'
    Design = namedtuple('Design', 'constructor steps req_tools')

    # chairs, desks, and tables, even though they require the Lathe, do not get passed a TurningStep as that is handled
    # by the Blueprint parent class based on the number of legs passed to the constructor
    __item_dict = {
        'chair': Design(ChairBlueprint, [cs.SandingStep(), cs.GluingStep(), cs.FasteningStep()], ['Lathe', 'Sander']),
        'cushioned chair': Design(CushionedChairBlueprint,
                                  [cs.SandingStep(), cs.GluingStep(), cs.FasteningStep(), cs.PaddingStep()],
                                  ['Lathe', 'Sander', 'Padder']),
        'desk': Design(DeskBlueprint, [cs.CuttingStep(), cs.PlaningStep(), cs.JointingStep(), cs.SandingStep(), cs.FasteningStep()],
                       ['Lathe', 'Planer', 'Jointer', 'Sander']),
        'table': Design(TableBlueprint, [cs.TurningStep(), cs.JointingStep(), cs.PlaningStep(),
                                         cs.GluingStep(), cs.FasteningStep(), cs.SandingStep()]
                        , ['Lathe', 'Jointer', 'Planer', 'Sander']),
        'drawer': Design(DrawerBlueprint, [cs.JointingStep(), cs.PlaningStep(), cs.SandingStep, cs.GluingStep()],
                         ['Sander', 'Jointer', 'Planer']),
        'bed': Design(BedBlueprint, [cs.JointingStep(), cs.PlaningStep(), cs.PaddingStep(), cs.FasteningStep()],
                      ['Jointer', 'Planer', 'Padder']),
        'sofa': Design(SofaBlueprint, [cs.JointingStep(), cs.PlaningStep(), cs.PaddingStep(), cs.FasteningStep()]
                       , ['Jointer', 'Planer', 'Padder']),
        'cutting board': Design(CuttingBoardBlueprint, [cs.JointingStep(), cs.PlaningStep(),
                                                        cs.SandingStep(), cs.GluingStep()],
                                ['Sander', 'Jointer', 'Planer'])
    }

    @staticmethod
    def get_blueprint(item_name):
        design = WoodObjectEncyclopedia.__item_dict.get(item_name)

        if not design:
            raise UnknownItemError(item_name)
        return design.constructor(design)


if __name__ == '__main__':
    requests = ['chair', 'table', 'cutting board', 'desk', 'bed', 'sofa']
    blueprints = []
    for req in requests:
        blueprints.append(WoodObjectEncyclopedia.get_blueprint(req))


    for bp in blueprints:
        print(bp.name, bp.assembly_time, bp.steps)
