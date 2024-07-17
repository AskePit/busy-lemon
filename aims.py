from dataclasses import dataclass

from utils import IdPool

TAB = '    '

class Aim:
    name: str
    id: int

    children: list['Aim']
    parent: 'Aim'

    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None

    def attach(self, child) -> 'Aim':
        child.parent = self
        self.children.append(child)
        return child

    def setParent(self, parent):
        parent.attach(self)
        
    def printInTree(self, identationLevel):
        space = TAB*identationLevel

        res = f'{space}{self.name}'

        if len(self.children) > 0:
            res += ' [\n'
            for child in self.children:
                res += child.printInTree(identationLevel + 1)
            res += f'{space}]'

        res += '\n'
        
        return res

class AimsTree:
    root: Aim
    idPool: IdPool

    def __init__(self) -> None:
        self.idPool = IdPool()
        self.root = Aim('root')
        self.root.id = IdPool.yieldId()

    def __str__(self) -> str:
        return self.root.printInTree(0)

def main():
    aims = AimsTree()
    root = aims.root

    career = root.attach(Aim('career'))
    hobbies = root.attach(Aim('hobbies'))
    family = root.attach(Aim('family'))
    health = root.attach(Aim('health'))

    work = career.attach(Aim('work'))
    programming = career.attach(Aim('programming'))
    gamedev = career.attach(Aim('gamedev'))
    careerBranding = career.attach(Aim('career branding'))

    company = work.attach(Aim('company'))
    office = work.attach(Aim('office'))

    cpp = programming.attach(Aim('c++'))
    rust = programming.attach(Aim('rust'))
    architecture = programming.attach(Aim('architecture'))
    algorithms = programming.attach(Aim('algorithms'))
    
    math = gamedev.attach(Aim('math'))
    ue5 = gamedev.attach(Aim('ue5'))
    godot = gamedev.attach(Aim('godot'))
    render = gamedev.attach(Aim('render'))

    openSource = careerBranding.attach(Aim('open source'))
    articles = careerBranding.attach(Aim('articles'))

    projects = hobbies.attach(Aim('projects'))
    games = hobbies.attach(Aim('games'))
    guitar = hobbies.attach(Aim('guitar'))
    soldering = hobbies.attach(Aim('soldering'))

    passbook = projects.attach(Aim('passbook'))
    cashbook = projects.attach(Aim('cashbook'))
    busyLemon = projects.attach(Aim('busy-lemon'))
    tPipe = projects.attach(Aim('t-pipe'))
    chest = projects.attach(Aim('chest'))
    pyrk = projects.attach(Aim('pyrk'))

    ironAge = games.attach(Aim('iron age'))
    slug = games.attach(Aim('slug'))
    tarot = games.attach(Aim('tarot'))
    cards = games.attach(Aim('cards'))

    togetherTime = family.attach(Aim('together time'))
    documents = family.attach(Aim('documents'))
    todos = family.attach(Aim('todos'))
    betterLife = family.attach(Aim('better life'))

    diet = health.attach(Aim('diet'))
    sport = health.attach(Aim('sport'))

    print(aims)


if __name__ == "__main__":
    main()