

class Unit:
    def __init__(self, label, **kwargs):
        self.label = label
        self.raw_label = kwargs.pop('raw_label', None)

    def __call__(self):
        return self.label

    def __repr__(self):
        reprstr = f'Unit: {self.label}'
        return reprstr

    @property
    def raw_label(self):
        label = self._raw_label
        if label is None:
            label = self.label
        return label

    @raw_label.setter
    def raw_label(self, label):
        self._raw_label = label
