import time


class Step:
    """The base class for all steps. Defines one method perform()"""
    def __init__(self, name, step_type, **kwargs):
        self.name = name
        self.step_type = step_type
        self.INITIATION_TIME = 2
        self.__is_completed = False

    def perform(self):
        print(f'Initiating {self.name.lower()}....', end='')
        # for i in range(1, self.INITIATION_TIME):
        #     print(i, end='...')
        #     time.sleep(1)
        # print()
        time.sleep(self.INITIATION_TIME)
        print('DONE')
        print(self.name.title(), end='...')
        for i in range(1, self.time_to_complete+1):
            print(i, end='...')
            time.sleep(1)

        print(f'{self.name} completed!')
        self.set_completed()

    @property
    def is_completed(self):
        return self.__is_completed

    def set_completed(self):
        self.__is_completed = True

    def __repr__(self):
        return self.name


class GenerationStep(Step):
    def __init__(self, name, **kwargs):
        self.name = name
        self.step_type = 'generation'
        super().__init__(self.name, self.step_type, **kwargs)


class AlterationStep(Step):
    def __init__(self, name, **kwargs):
        self.name = name
        self.step_type = 'alteration'
        super().__init__(self.name, self.step_type, **kwargs)


class AssemblyStep(Step):
    def __init__(self, name, **kwargs):
        self.name = name
        self.step_type = 'assembly'
        super().__init__(self.name, self.step_type, **kwargs)


class CuttingStep(GenerationStep):
    """The ripping of a board into narrower sections or the cutting of boards into shorter sections.
    Also applies to using the scroll saw to cut out intricate shapes"""
    def __init__(self):
        self.name = 'Cutting'
        self.time_to_complete = 3
        super().__init__(self.name)


class DrillingStep(AlterationStep):
    """Drilling holes in things to prepare them for fastening together"""
    def __init__(self):
        self.name = 'Drilling'
        self.time_to_complete = 2
        super.__init__(self.name)


class FasteningStep(AssemblyStep):
    """The screwing or nailing of two pieces of wood together. Separate and distinct from Gluing, but can be used in
    combination"""
    def __init__(self):
        self.name = 'Fastening'
        self.time_to_complete = 3
        super().__init__(self.name)


class GluingStep(AssemblyStep):
    """Attaching one piece of wood to another by chemical means. Can be used in conjunction with Gluing or used
    separately"""
    def __init__(self):
        self.name = 'Gluing'
        self.time_to_complete = 3
        self.time_to_dry = 3
        super().__init__(self.name)

    def perform(self):
        super().perform()
        print('Waiting for glue to dry and set up...')
        for i in range(1, self.time_to_dry+1):
            print(i, end='...')
            time.sleep(1)
        print('\nGlue is dry!')


class JointingStep(AlterationStep):
    """Smoothing out and making parallel the two narrow sides of a board.
    Useful when making desks, table, cutting boards, drawers, and sofas"""
    def __init__(self):
        self.name = 'Jointing'
        self.time_to_complete = 4
        super().__init__(self.name)


class PaddingStep(AlterationStep):
    """Used in the Sofa and Chair and Bed to make things comfortable"""
    def __init__(self):
        self.name = 'Padding'
        self.time_to_complete = 5
        super().__init__(self.name)


class PlaningStep(AlterationStep):
    """Smoothing out and making parallel the two broad sides of a board.
    Useful when making desks, tables, cutting boards
    """
    def __init__(self):
        self.name = 'Planing'
        self.time_to_complete = 4
        super().__init__(self.name)


class RoutingStep(AlterationStep):
    """Rounding over corners and making inlays and stuff"""
    def __init__(self):
        self.name = 'Routing'
        self.time_to_complete = 3
        super().__init__(self.name)


class SandingStep(AlterationStep):
    """Removing rough edges and making the exposed, viewable faces presentable. Used by most 'finished' goods"""
    def __init__(self):
        self.name = 'Sanding'
        self.time_to_complete = 3
        super().__init__(self.name)


class StainingStep(AlterationStep):
    """Prettifying the wood. Also protects it from the elements and from food stains and such like"""
    def __init__(self):
        self.name = 'Staining'
        self.time_to_complete = 5
        super().__init__(self.name)


class TurningStep(GenerationStep):
    """Turning things like bed posts, chair legs, table legs, desk legs, and generally anything which is cylindrical"""
    def __init__(self):
        self.name = 'Turning'
        self.time_to_complete = 7
        super().__init__(self.name)


class StepError(Exception):
    """Not sure how this will be used but I have it here in case I think of a reason"""
    def __init__(self, *args):
        super().__init__(*args)


if __name__ == '__main__':
    glueing = GluingStep()
    glueing.perform()

    staining = StainingStep()
    staining.perform()