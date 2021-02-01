from blueprints import WoodObjectEncyclopedia


class Worker:
    def __init__(self, name):
        self.name = name
        self.known_blueprints = {}
        self.skills = []
        self.enc = WoodObjectEncyclopedia()
        self.active_job = None
        self.current_tool = None
        self.partial_jobs = []

    def craft(self, item, **kwargs):
        """Craft the item if the blueprint for it is known and the necessary skills are known.
        Return UnknownBlueprintError otherwise.
        This method returns an WoodObject
        """
        blueprint = self.known_blueprints.get(item)
        if blueprint:
            return blueprint(**kwargs)
        else:
            raise UnknownBlueprintError(item)

    def learn_blueprint(self, blueprint):
        new_blueprint = self.enc.get_item(blueprint)
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


if __name__ == '__main__':
    w = Worker('Miles Head')

    try:
        w.learn_blueprint('Chair')
    except UnknownBlueprintError as e:
        print(e)



    w.craft('Chair')