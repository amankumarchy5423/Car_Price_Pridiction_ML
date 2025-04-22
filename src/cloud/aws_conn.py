import boto3
import os,sys
from dotenv import load_dotenv
load_dotenv()

from src.logging.logger import my_logger
from src.exception.project_exception import MyException

aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_Key')
aws_dz = os.getenv("REGION")




class s3client:
    s3_client = None
    s3_resources = None

    def __init__(self,region_name= aws_dz):
        try:
            self.region = region_name

            if s3client.s3_client == None or s3client.s3_resources == None:
                aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
                aws_secret_key = os.getenv('AWS_SECRET_ACCESS_Key')

                if aws_access_key == None or aws_secret_key == None:
                    MyException("enviroment variable is not load proper",sys)

                s3client.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                    region_name=self.region
                )
                s3client.s3_resources = boto3.resource('s3',
                                              aws_access_key_id = aws_access_key,
                                              aws_secret_access_key = aws_secret_key,
                                              region_name = self.region)
                
            self.s3_resources = s3client.s3_resources
            self.s3_client = s3client.s3_client
        except Exception as e:
            my_logger.error(f"Error in s3client class: {str(e)}")
            MyException(e,sys)





