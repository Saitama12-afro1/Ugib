import datetime
from .models import History

def decor(func):
    def create(user, udsMetaObj, orderObj = False ):
        typeAction = func()
        date = datetime.datetime.now()
        uds = str(udsMetaObj.uniq_id) + " " + udsMetaObj.stor_person
        history = History.objects.create(date = date, typeAction = typeAction,
                                            udsMeta = uds, my_user = user, order = orderObj)
        history.save()
    return create
        
    

