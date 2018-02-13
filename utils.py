class AttrDict(dict):
    """
    以访问属性的方式访问字典
    """

    def __getattr__(self, item):
        if item in self:
            return self[item]
        else:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__, item))

    def __setattr__(self, key, value):
        self[key] = value
    
    def copy(self):
        return AttrDict(super(AttrDict, self).copy())


from pygame.colordict import THECOLORS

ConfigDict = AttrDict
colors = AttrDict(THECOLORS)
