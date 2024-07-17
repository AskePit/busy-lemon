class IdPool:
    nextIdentifier: int
    freedIdentifiers: list[int]

    def __init__(self) -> None:
        self.nextIdentifier = 0
        self.freedIdentifiers = []

    def yieldId(self) -> int:
        if len(self.freedIdentifiers) > 0:
            identifier = self.freedIdentifiers[-1]
            self.freedIdentifiers.pop()
            return identifier
        else:
            self.nextIdentifier += 1
            return self.nextIdentifier

    def freeId(self, identifier: int):
        if not self.isIdFree(identifier):
            self.freedIdentifiers.append(identifier)

    def isIdFree(self, identifier: int) -> bool:
        return identifier >= self.nextIdentifier or identifier in self.freedIdentifiers