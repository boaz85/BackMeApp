class Item(object):

    def __init__(self, order, slug, display=None, value=None, **kwargs):
        if not isinstance(slug, (str, unicode)):
            raise TypeError('item slug should be a string or unicode, not %s' % slug.__class__.__name__)
        #if display is not None and not isinstance(display, (str, unicode)):
        #    raise TypeError('item slug should be a string or unicode, not %s' % display.__class__.__name__)
        if not isinstance(order, int):
            raise TypeError('item order should be an integer, not %s' % order.__class__.__name__)
        super(Item, self).__init__()
        self.value = value
        self.slug = slug
        self.display = slug if display is None else display
        self.order = order
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.display

    def __repr__(self):
        return '<enum.Item: %s>' % self.display

    def __eq__(self, other):
        if isinstance(other, Item):
            return type(self) == type(other) and self.order == other.order
        if isinstance(other, (int, str, unicode)):
            try:
                return self.order == int(other)
            except ValueError:
                return False
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __get__(self, instance, owner):
        return self.order


class Enumeration(object):
    @classmethod
    def from_value(cls, value):
        for attr in cls.get_items():
            if attr.value == value:
                return attr

    @classmethod
    def from_slug(cls, slug):
        for attr in cls.get_items():
            if attr.slug == slug:
                return attr

    @classmethod
    def from_order(cls, order):
        for attr in cls.get_items():
            if attr.order == order:
                return attr

    @classmethod
    def from_attribute(cls, name, value):
        for attr in cls.get_items():
            try:
                if getattr(attr, name)==value:
                    return attr
            except AttributeError:
                pass


    @classmethod
    def get_items(cls, order_by='order'):
        values = []
        for c in cls.__mro__:
            values += c.__dict__.values()
        items = filter(lambda attr: isinstance(attr, Item), values)
        items.sort(lambda x, y: cmp(getattr(x, order_by), getattr(y, order_by)))
        return items

    @classmethod
    def get_choices(cls, order_by='order'):
        return [(item.order, unicode(item.display)) for item in cls.get_items(order_by)]

    @classmethod
    def get_value(cls, order):
        return cls.from_order(order).value

    @classmethod
    def get_slug(cls, order):
        return cls.from_order(order).slug

    @classmethod
    def get_name(cls, order):
        for attr in cls.get_items():
            if attr.order == order:
                return attr.display if attr.display else attr.slug
