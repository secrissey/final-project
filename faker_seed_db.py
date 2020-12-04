from faker import Faker 

# Creation of faker profile helper function
def getProfile():
    fake = Faker()
    return fake.profile()

    # Gather Data and place inside of Datbase
    import os
    from catsapp_api.models import Member
    from catsapp_api import db

def seedData():
    for seed_num in range(10):
        data = getProfile()
        print(data['name'])
        member = Member(data['name'], data['email'] )

        db.session.add(member)
        db.session.commit()

seedData()



    
