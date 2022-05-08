from boto3 import Session
import string
import random


ACCESS_KEY = "################"
SECRET_KEY = "##############"
REGION_NAME = "#############"
BUCKET_NAME = "##############"

def download_link(file : str):

    ses = Session(aws_access_key_id=ACCESS_KEY,
              aws_secret_access_key=SECRET_KEY,
              region_name=REGION_NAME)

    key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
    file = file
    content_type = 'zip'
    s3 = ses.resource('s3')

    s3.Bucket(BUCKET_NAME).put_object(Key=key, Body=open(file, 'rb'), ContentType=content_type)
    client = ses.client('s3')
    url = client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': BUCKET_NAME,
            'Key': key,
        },
       ExpiresIn=3600
         )
    return url
