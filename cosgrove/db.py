from peewee import *

database = MySQLDatabase('cosgrove', **{'user': 'root'})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database


class Slides(BaseModel):
    title = CharField(max_length=100, null=True)

    class Meta:
        db_table = 'slides'


class Products(BaseModel):
    big_image = CharField(max_length=2083)
    description = CharField(max_length=255)
    link = CharField(max_length=2083)
    price = DecimalField()
    screenshots = CharField(max_length=2083, null=True)
    thumb = CharField(max_length=2083)
    title = CharField(max_length=100)

    class Meta:
        db_table = 'products'

class Projects(BaseModel):
    big_image = CharField(max_length=2083)
    description = TextField()
    link = CharField(max_length=2083)
    screenshots = CharField(max_length=2083, null=True)
    thumb = CharField(max_length=2083)
    title = CharField(max_length=100)
    video_link = CharField(max_length=2083, null=True)

    class Meta:
        db_table = 'projects'


def execute(fn):
    '''cleanly execute mysql queries'''
    def wrap(*args, **kwargs):
        q = fn(*args, **kwargs)
        db_res = q.execute()
        caller = fn.__name__
        if 'report' in caller:
            column = kwargs.get('c')
            key = caller.split('_')[1]
            res = {}
            if column:
                res[key] = [{r.id: getattr(r, column)} for r in db_res]
            else:
                res[key] = [r._data for r in db_res]

            return res

        return {'status': 'query executed'}

    return wrap


@execute
def create_slide(**kwargs):
    return Slides.insert(**kwargs)


@execute
def report_slides():
    return Slides.select()


@execute
def update_slide(**kwargs):
    '''
     Update slide

    kwargs = {
        "title": string,
        "updated": {
            "title": string
        }
    }
    '''
    slide = Slides.get(Slides.title == kwargs.get('title'))
    if not slide:
        raise Exception({'error': 'slide does not exist'})

    return Slides.update(**kwargs.get('updated')).where(Slides.id == slide.id)


@execute
def delete_slide(**kwargs):
    '''
     Delete slide

    kwargs = {
        "title": string
    }
    '''
    slide = Slides.get(Slides.title == kwargs.get('title'))
    if not slide:
        raise Exception({'error': 'slide does not exist'})

    return Slides.delete().where(Slides.id == slide.id)


@execute
def create_project(**kwargs):
    '''
    kwargs = {
        "title": string,
        "description": string,
        "link": string,
        "thumb": string,
        "big_image": string,
        "video_link": string                  (optional),
        "screenshots": comma-separated string (optional)
    }
    '''
    return Projects.insert(**kwargs)


@execute
def report_projects():
    '''
     Report all projects
    '''
    return Projects.select()


@execute
def update_project(**kwargs):
    '''
     Update project information

    kwargs = {
        "title": string,
        "updated": {
            "column": string
            ...
        }
    }
    '''
    project = Projects.get(Projects.title == kwargs.get('title'))
    if not project:
        raise Exception({'error': 'project does not exist'})

    return Projects.update(**kwargs.get('updated')).where(Projects.id == project.id)

@execute
def delete_project(**kwargs):
    '''
     Delete project

    kwargs = {
        "title": string
    }
    '''
    project = Projects.get(Projects.title == kwargs.get('title'))
    if not project:
        raise Exception({'error': 'product does not exist'})

    return Projects.delete().where(Projects.id==project.id)


@execute
def create_product(**kwargs):
    '''
    kwargs = {
        "title": string,
        "description": string,
        "link": string,
        "price": float,
        "thumb": string,
        "big_image": string,
        "screenshots": comma-separated string (optional),
        "video_link": string                  (optional)
    }
    '''
    return Products.insert(**kwargs)


@execute
def report_products():
    return Products.select()


@execute
def update_product(**kwargs):
    '''
     Update product information

    kwargs = {
        "title": string,
        "updated": {
            "column": string
            ...
        }
    }
    '''
    product = Products.get(Products.title == kwargs.get('title'))
    if not product:
        raise Exception({'error': 'product does not exist'})

    return Products.update(**kwargs.get('updated')).where(Products.id == product.id)

@execute
def delete_product(**kwargs):
    '''
     Delete product

    kwargs = {
        "title": string
    }
    '''
    product = Products.get(Products.title == kwargs.get('title'))
    if not product:
        raise Exception({'error': 'product does not exist'})

    return Products.delete().where(Products.id==product.id)
