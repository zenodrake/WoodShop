from blueprints import WoodObjectEncyclopedia


class Worker:
    """
    The class which represents the player of this little program
        Defines the following attributes:
            name
            known_blueprints
            skills
            enc
            business
            active_job
            current_tool
            partial_jobs
            inventory

        Defines the following properties:


        Defines the following methods:
            assign_to_business()
            make_item()
            prepare_item()
            prepare_items()
            craft()
            assemble()
            learn_blueprints()
            learn_skill()
            use_tool()
            show_known_blueprints()
            show_skills()
    """

    def __init__(self, name):
        self.name = name
        self.known_blueprints = {}
        self.skills = []
        self.enc = WoodObjectEncyclopedia()
        self.business = None
        self.active_job = None
        self.current_tool = None
        self.partial_jobs = []
        self.inventory = []

    def assign_to_business(self, business):
        self.business = business

    def make_item(self, using_blueprint):
        """Perform the necessary GenerationSteps necessary to create a Part. Step of crafting something.
        This method returns a Furniture Component
        """
        if not self.business:
            raise InvalidBusinessError("I'm not employed by any business")

        # necessary_tools = using_blueprint.req_tools
        # steps = (filter(lambda s: s.step_type == 'generation', using_blueprint.steps))

        for step in (filter(lambda s: s.step_type == 'generation', using_blueprint.steps)):
            tool = self.business.lookup_tool_by_step(step)
            part = tool.use(step)
            self.inventory.append(part)

    def prepare_item(self, item):
        """Perform the necessary AlterationSteps to make the Parts ready for assembly"""
        pass

    def prepare_items(self, items):
        """Just like prepare_item() but for more than one"""
        for item in items:
            self.prepare_item(item)

    def craft(self, item: str):
        """Do all the steps to fully create an completed piece of furniture"""
        blueprint = self.known_blueprints.get(item)
        if blueprint:
            self.make_item(blueprint)
        else:
            raise UnknownBlueprintError(item)
        self.prepare_items(item)
        self.assemble(item)

    def assemble(self, item):
        """Look at our inventory and if we have the parts necessary for the required item
        perform the necessary AssemblySteps to build it."""
        pass

    def learn_blueprint(self, blueprint):
        new_blueprint = self.enc.get_blueprint(blueprint)
        self.known_blueprints.update({blueprint: new_blueprint})

    def learn_skill(self, skill):
        self.skills.append(skill)

    def use_tool(self, tool_name):
        pass

    def show_known_blueprints(self):
        print('These are the things what I know how to make')
        for bp in self.known_blueprints.keys():
            print(bp)

    def show_skills(self):
        print('These are the skills I know')
        for skill in self.skills:
            print(skill)


class UnknownBlueprintError(Exception):
    def __init__(self, blueprint):
        super().__init__(f"I don't know how to craft a {blueprint}")


class InvalidBusinessError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


if __name__ == '__main__':
    import business
    import shop_tools

    lathe = shop_tools.Lathe()
    planer = shop_tools.Planer()
    table_saw = shop_tools.TableSaw()
    tools = [lathe, planer, table_saw]

    ws = business.WoodShop()
    ws.set_name("Miles Head's")




    for tool in tools:
        ws.buy_equipment(tool)

    print(ws.equipment)

    w = Worker('Miles Head')
    ws.hire_worker(w)

    try:
        w.learn_blueprint('chair')
        w.craft('chair')
    except UnknownBlueprintError as e:
        print(e)

