from twython import Twython

variable = "variable1"
variable2 = "0"
variable3 = "1"
message = "Test variable: %s / Test2: %s / Test3: %s" % (variable, variable2, variable3)
print(message)

C_KEY = ''
C_SECRET = ''
A_TOKEN = ''
A_SECRET = 'E'

twitter = Twython(C_KEY, C_SECRET, A_TOKEN, A_SECRET)
photo = open('MyPic.jpg', 'rb')
response = twitter.upload_media(media=photo)
twitter.update_status(status='-test-Checkout this cool image!', media_ids=[response['media_id']])

#api.update_status(status=message)
