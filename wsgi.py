from dotenv import load_dotenv

from checkin import create_app

load_dotenv('.env')
app = create_app('production')
