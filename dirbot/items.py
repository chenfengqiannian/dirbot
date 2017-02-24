from scrapy.item import Item, Field


class Website(Item):
    didian=Field()
    name = Field()

    phone=Field()
    title=Field()

