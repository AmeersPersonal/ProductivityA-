
from user import User

from google.calendeder.googleCalender import Calender
def main():
    user = User('ameert', 'atayeh55@gmail.com')
    cal = Calender(user=user)
    cal.send_event({})

main()
