import datetime
from .models import History

def decor(func):
    def create(user, udsMetaObj, orderObj = False ):
        typeAction = func()
        date = datetime.datetime.now()
        print(typeAction)
        statistic = History.objects.create(date = date, typeAction = typeAction,
                                            udsMeta = udsMetaObj, my_user = user, order = orderObj)
        statistic.save()
    return create
        
    # @classmethod
    # def update(cls, user, udsMetaObj = None, orderObj = None):
    #     typeAction = "update"
    #     date = datetime.datetime.now()
    #     statistic = Statistic.objects.create(date = date, typeAction = typeAction,
    #                                          udsMeta = udsMetaObj, my_user = user, order = orderObj)
    #     statistic.save()
    

@decor
def arr():
    return "save"
