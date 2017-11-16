import datetime
import os
import uuid


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    now = datetime.datetime.now()
    return os.path.join('tires', 'pictures', now.strftime('%Y'), now.strftime('%m'), filename)
