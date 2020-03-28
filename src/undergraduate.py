class Undergraduate:
    def __init__(self, name):
        self._hp = 5
        self._score = 0
        self._name = name
        self._total_score = 0

    @property
    def hp(self):
        return self._hp

    @property
    def score(self):
        return self._score

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def damage(self):
        self._hp = self._hp - 1

    def plus_score(self, value):
        self._score = self._score + value

    @hp.setter
    def hp(self, value):
        self._hp = value

    @property
    def total_score(self):
        return self._total_score

    @total_score.setter
    def total_score(self, value):
        self._total_score = value
