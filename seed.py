from app import *
from models import *

db.drop_all()
db.create_all()

u1 = User(first_name="Amber", last_name="Jool", img_url="https://pbs.twimg.com/profile_images/1340017723569438720/gsTAHx7F.jpg")
u2 = User(first_name="Jack", last_name="Sparrow", img_url="https://ohmy.disney.com/wp-content/uploads/2014/10/Q3-Jack-Sparrow.png")
u3 = User(first_name="Steve", last_name="MC", img_url="https://cdn.vox-cdn.com/thumbor/knQ8JkrNCLHYs4OxBpZoAeEEHpQ=/0x0:1100x774/1200x800/filters:focal(462x299:638x475)/cdn.vox-cdn.com/uploads/chorus_image/image/66810361/Minecraft-360.0.jpg")
u4 = User(first_name="Anastasia", last_name="Dream", img_url="https://static.onecms.io/wp-content/uploads/sites/20/2020/11/06/baby-panda-smithsonian1.jpg")
u5 = User(first_name="Alice", last_name="Red", img_url="https://www.cowboydatingexpert.com/wp-content/uploads/2019/09/Retro-cowgirl-in-jeans-jacket-in-countryside.jpg")

db.session.add_all([u1,u2,u3,u4,u5])
db.session.commit()

p1 = Post(title="First Post! Yay!", content="This is my first post and I can't wait to do more", created_at=datetime(2020, 6, 5, 7, 36), user_id=1)
p2 = Post(title="Captain Jack Sparrow, at your service", content="This is the day you will always remember as the day you almost caught captain Jack Sparrow", created_at=datetime(2020, 6, 8, 16, 15),user_id=2)
p3 = Post(title="Second Post! Yay!", content="Now I have 2 posts! It's amazing", created_at=datetime(2020, 7, 8, 10, 55), user_id=1)
p4 = Post(title="Third Post! Yay!", content="Now I have 3 posts! That's got to be a record or something!", created_at=datetime(2020, 7, 15, 20, 12), user_id=1)
p5 = Post(title="The Problem", content="The problem is not the proble. the problem is the way you think about the problem", created_at=datetime(2020, 10, 15, 17, 16), user_id=2)
p6 = Post(title="Heyo there!", content="Hello everyone and welcome to a new video where today I'll be showing you how to build the universe one to one scale in Minecraft. First you start with...", created_at=datetime(2020, 11, 17, 22, 15), user_id=3)
p7 = Post(title="my first post", content="hi. Im shy, but I want to post more", created_at=datetime(2021, 1, 30, 17, 44), user_id=4)
p8 = Post(title="Howdy partner", content="You look a little out of your comfort zone there, partner. Perhaps I can help by getting you a passy and a new daippy", created_at=datetime(2021, 3, 29, 19, 56), user_id=5)
p9 = Post(title="hi again", content="i wanna try to post more, but i don't know if i will be able to", user_id=4)

db.session.add_all([p1,p2,p3,p4,p5,p6,p7,p8,p9])
db.session.commit()