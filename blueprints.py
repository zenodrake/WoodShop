from collections import namedtuple
import crafting_steps as cs
from wood_objects import RoundLeg, SquareLeg, Board

DEFAULT_NUM_LEGS = 4


class Blueprint:
    """Base class for all blueprints.
        Defines the following attributes:
            name
            steps
            req_tools -- the ShopTools necessary to successfully complete the blueprint
            req_parts -- the FurnitureComponents necessary to successfully complete the blueprint

        Defines the following methods:
            _calculate_assembly_time()
            _calculate_turning_steps()
            show_remaining_steps()

    """

    def __init__(self, name, design, **kwargs):
        self.name = name
        self.steps = design.steps
        self.req_tools = design.req_tools
        self.req_parts = design.req_parts
        self._calculate_turning_steps()
        self._calculate_assembly_time()

    def _calculate_assembly_time(self):
        """Add together all the times of each of the steps to arrive at the total length of time to fully complete"""
        self.assembly_time = 0
        for step in self.steps:
            self.assembly_time += step.time_to_complete

    def _calculate_turning_steps(self):
        """Based on the number of legs, calculate how many turning steps are necessary.
        Won't break if passed a negative number of steps, but it doesn't make a lot of sense"""
        if hasattr(self, 'num_legs'):
            for i in range(self.num_legs):
                self.steps.insert(0, cs.TurningStep())

    def show_remaining_steps(self):
        """Print out the steps left to be completed"""
        print('Steps left to complete: ')
        for s in (filter(lambda e: not e.is_completed, self.steps)):
            print(s, end=', ')


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
    """Used to signify when an item which doesn't exist in the WoodObjectEncylopedia is requested"""
    def __init__(self, item_name):
        super().__init__(f'An object of name "{item_name}" does not exist in the Encyclopedia')


class WoodObjectEncyclopedia:
    """This class stores all the information about creating furniture
    This information takes the form of a namedtuple called Furniture
    which stores the class--called constructor--the steps to craft, and required tools for assembly

        Defines the following attributes:
            __name
            Design, a namedtuple
            __item_dict

        Defines the following methods:
            get_item(), a static method
    """
    __name = 'Encyclopedia of Wood'
    Design = namedtuple('Design', 'constructor steps req_tools req_parts')

    # chairs, desks, and tables, even though they require the Lathe, get passed neither TurningSteps nor Legs as those
    # are handled by the Blueprint parent class based on the number of legs passed to the constructor
    __item_dict = {
        'chair': Design(
            ChairBlueprint,
            [cs.SandingStep(), cs.GluingStep(), cs.FasteningStep()],
            ['Lathe', 'Sander'],
            [Board, Board, Board, Board]
        ),
        'cushioned chair': Design(
            CushionedChairBlueprint,
            [cs.SandingStep(), cs.GluingStep(), cs.FasteningStep(), cs.PaddingStep()],
            ['Lathe', 'Sander', 'Padder'],
            [Board, Board, Board, Board]
        ),
        'desk': Design(
            DeskBlueprint,
            [cs.CuttingStep(), cs.PlaningStep(), cs.JointingStep(), cs.SandingStep(), cs.FasteningStep()],
            ['Lathe', 'Planer', 'Jointer', 'Sander'],
            [Board, Board]
        ),
        'table': Design(
            TableBlueprint,
            [cs.TurningStep(), cs.JointingStep(), cs.PlaningStep(),
             cs.GluingStep(), cs.FasteningStep(), cs.SandingStep()],
            ['Lathe', 'Jointer', 'Planer', 'Sander'],
            []
        ),
        'drawer': Design(
            DrawerBlueprint,
            [cs.JointingStep(), cs.PlaningStep(), cs.SandingStep, cs.GluingStep()],
            ['Sander', 'Jointer', 'Planer'],
            []
        ),
        'bed': Design(
            BedBlueprint,
            [cs.JointingStep(), cs.PlaningStep(), cs.PaddingStep(), cs.FasteningStep()],
            ['Jointer', 'Planer', 'Padder'],
            []
        ),
        'sofa': Design(
            SofaBlueprint,
            [cs.JointingStep(), cs.PlaningStep(), cs.PaddingStep(), cs.FasteningStep()],
            ['Jointer', 'Planer', 'Padder'],
            []
        ),
        'cutting board': Design(
            CuttingBoardBlueprint,
            [cs.JointingStep(), cs.PlaningStep(), cs.SandingStep(), cs.GluingStep()],
            ['Sander', 'Jointer', 'Planer'],
            []
        )
    }

    @staticmethod
    def get_blueprint(item_name):
        """Return a concrete implementation of a Blueprint based on <item_name>"""
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
