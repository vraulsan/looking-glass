from dotenv import load_dotenv
import os

load_dotenv()

## Example jumpserver, please edit and add yours
jumpserver1 = {}
jumpserver1['address'] = ('jumpserver1.earth.com', 22)
jumpserver1['usern'] = os.getenv('USERN')
jumpserver1['passw'] = os.getenv('PASSW')

## Example routers, please edit and add yours
routers_list = [
  dict(address=('saturn01-r1', 22),
    usern=os.getenv('USERN'),
    passw=os.getenv('PASSW'),
    type='IOS-XR',
    asn='65534',
    location='Saturn',
    jumpserver=jumpserver1
  ),
  dict(address=('mars01-r1', 22),
    usern=os.getenv('USERN'),
    passw=os.getenv('PASSW'),
    type='JunOS',
    asn='65533',
    location='Mars',
    jumpserver=jumpserver1
  ),
  dict(address=('earth01-r1', 22),
    usern=os.getenv('USERN'),
    passw=os.getenv('PASSW'),
    type='JunOS',
    asn='65532',
    location='Mars',
    jumpserver=False
  )
]