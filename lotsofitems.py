from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Category, Base, Item, User
create_engine('postgresql://sonam:password@localhost/catalog')

#BINDIND DB
Base.metadata.bind=engine

DBSession = sessionmaker(bind=engine)
sesssion = DBSession()

# Dummy User
user1 = User(name="John Tyler", email="johntyler!12@gmail.com", image="https://tse1.mm.bing.net/th?id=OIP.IZLLSP-RG2LYdFvM_Pl1mQHaHa&pid=Api&P=0&w=300&h=300")
session.add(user1)
session.commit()

category1= Category(name="string", user_id = 1)
session.add(category1)
session.commit()

item1 = Item(name="Soccer", user_id =1, description="The object of the game of soccer, also known in some countries as football, is to drive a soccer ball into the opposing team's goal in order to score a point.")

session.add(item1)
session.commit()

item2 = Item(name="Baseball", user_id=1,  description="Baseball is a bat-and-ball game played between two opposing teams who take turns batting and fielding. The game proceeds when a player on the fielding team, called the pitcher, throws a ball which a player on the batting team tries to hit with a bat.", category=category1)

session.add(item2)
session.commit()

item3 = Item(name="Basketball", user_id=1, description="Basketball is a team sport in which two teams, most commonly of five players each, opposing one another on a rectangular court. ", category=category1)

session.add(item3)
session.commit()

# Items for category 2
category2 = Category(name="string1", user_id=1)

session.add(category2)
session.commit()

item1 = Item(name="Rock Climbing", user_id=1, description="Rock climbing is a sport in which participants climb up, down or across natural rock formations or artificial rock walls. The goal is to reach the summit of a formation or the endpoint of a usually pre-defined route without falling. ", category=category2)

session.add(item1)
session.commit()

item2 = Item(name="Sketing", user_id=1,  description="Ice skating is the self-propulsion of a person across a sheet of ice, using metal-bladed ice skates to glide on the ice surface. ", category=category2)

session.add(item2)
session.commit()

item3 = Item(name="Hockey", user_id=1, description="Hockey is a sport in which two teams play against each other by trying to manoeuvre a ball or a puck into the opponent's goal using a hockey stick.", category=category2)

session.add(item3)
session.commit()

# Items for category3
category3 = Category(name="string3", user_id=1)

session.add(category3)
session.commit()

item1 = Item(name="Snowboarding", user_id=1, description="Snowboarding is a recreational activity and Winter Olympic and Paralympic sport that involves descending a snow-covered slope while standing on a snowboard attached to a rider's feet.", category=category3)

session.add(item1)
session.commit()

item2 = Item(name="Cricket", user_id=1, description="Cricket is a bat-and-ball game played between two teams of eleven players on a field at the centre of which is a 20-metre (22-yard) pitch with a wicket at each end, each comprising two bails balanced on three stumps.", category=category3)

session.add(item2)
session.commit()

item3 = Item(name="Foosball", user_id=1, description="A table game resembling soccer in which the ball is moved by manipulating rods to which small figures of players are attached", category=category3)

session.add(item3)
session.commit()

# Items for category4
category4 = Category(name="string4", user_id=1)

session.add(category4)
session.commit()


categories = session.query(Category).all()
for category in categories:
    print "Category: " + category.name

