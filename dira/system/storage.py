from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from datetime import datetime

class ImageStorage(FileSystemStorage): 
    from django.conf import settings 
    def __init__(self, location=settings.MEDIA_ROOT,   base_url=settings.MEDIA_URL): 
    #  initialize the 
        super(ImageStorage, self).__init__(location, base_url)
        #  rewrite _save methods 
        def _save(self, name): 
            import os, time, random
            ext = os.path.splitext(name)[1]
            d = os.path.dirname(name)
            fn = time.strftime('%Y%m%d%H%M%S')+random.randint(0,100) 
            name = os.path.join(d, fn + ext)
            return super(ImageStorage, self)._save(name)