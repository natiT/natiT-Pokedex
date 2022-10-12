class pokemon(object):
    def __init__(self, id, name, types, abilities, species, stats, flavortext):
        self.id = id
        self.name = name
        self.types = types
        self.abilities = abilities
        self.species = species
        self.stats = stats
        self.flavortext = flavortext


class api_output(object):
    def __init__(self, id, name, stats):
        self.id = id
        self.name = name
        self.stats = stats
