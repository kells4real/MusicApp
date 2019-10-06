AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

Dk0z+91ypOkuoCrVwSgV2DN0S+I6ZMP/dXSypM6R
AKIAZ7FXQZWOB2FJNBP2

#Resize pics
import io
from django.core.files.storage import default_storage as storage


def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    img_read = storage.open(self.image.name, 'r')
    img = Image.open(img_read)

    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        in_mem_file = io.BytesIO()
        img.save(in_mem_file, format='JPEG')
        img_write = storage.open(self.image.name, 'w+')
        img_write.write(in_mem_file.getvalue())
        img_write.close()

    img_read.close()
	
	
	#CORSConfiguration
	<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
   <CORSRule>
        <AllowedOrigin>*</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <AllowedMethod>POST</AllowedMethod>
        <AllowedMethod>PUT</AllowedMethod>
        <AllowedHeader>*</AllowedHeader>
    </CORSRule>
</CORSConfiguration>


Secret_Access_Key = 'C6PKEUeqh0grT94rCvRTYV9YDaBXX+oXHrVgrXsT'

Access_Key_Id = 'AKIAZ7FXQZWOP2BQOIMC'


#Postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
pip install postgres