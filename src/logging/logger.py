import logging
import os
import sys
import datetime

dir = f"{datetime.datetime.now().strftime('%D_%m_%Y__%H_%M_%S ')}.log"

os.makedirs('Logs',exist_ok=True)
file = os.path.join('Logs',dir,dir)

os.makedirs(os.path.dirname(file),exist_ok=True)



logging.basicConfig(
    level=logging.INFO,
    filename=file,
    format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    datefmt='%Y_%m_%d %H:%M:%S'
)

my_logger = logging.getLogger("<<<PROJECT>>>")




