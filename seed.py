from models import User, db, Post, Tag, PostTag
from app import app

db.drop_all()
db.create_all()

# Make some users
missa = User(first_name="Missa", last_name="Butler", image_url="https://64.media.tumblr.com/ded3638160a352b70fc1040996afee9e/219c89ddc2320737-8b/s1280x1920/13769638b2981e7fe7983da23c38a407b9c177dc.pnj")
opi = User(first_name="Opi", last_name="Prime", image_url="https://www.thesprucepets.com/thmb/jIEvS_jxy1-M4oLqk6w1ZqfXfWU=/1500x0/filters:no_upscale():strip_icc()/facts-about-tuxedo-cats-554704-hero-6fcf332fd5ee4d93aecc4bcd3657396c.jpg")
scott = User(first_name="Scott", last_name="Butler", image_url="data:image/jpeg;base64,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")

db.session.add_all([missa, opi, scott])

db.session.commit()

#make some posts
new_post1 = Post(title="Hi", content="My name is optimus prime", user_id=2)
new_post2= Post(title="Palword", content="Palword is fun i made a gun", user_id=3)
new_post3 = Post(title="Yummy", content="This cake recipe is awesome", user_id=1)

db.session.add_all([new_post1, new_post2, new_post3])
db.session.commit()


#make some tags
video_games = Tag(name="video games")
food = Tag(name="food")
cats = Tag(name="cats")

db.session.add_all([video_games, food, cats])
db.session.commit()

