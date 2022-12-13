import datetime
from .models import History

def decor(func):
    def create(user, udsMetaObj, orderObj = False ):
        typeAction,fond = func()
        date = datetime.datetime.now()
        uds = str(udsMetaObj.uniq_id)
        history = History.objects.create(date = date, typeAction = typeAction,
                                            udsMeta = uds, my_user = user, order = orderObj, fond = fond)
        history.save()
    return create
        
    

