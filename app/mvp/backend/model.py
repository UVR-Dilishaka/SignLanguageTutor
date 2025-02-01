from ext import db

"""
class Recipie:
    id: int primary key
    title: str
    description: str(text)

"""


class Recipie(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(),nullable=False)
    description = db.Column(db.Text(),nullable=False)


    def __repr__(self):
        return f"Recipie {self.title}"

    def save(self):
        db.session.add(self)
        db.session.commit()
    

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self,title,description):
        self.title = title
        self.description = description  
        db.session.commit()

     
#user model
class User(db.Model):

    """
    class User:
    id: int primary key 
    username: str
    email: str
    password: str
    """

    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(),nullable=False)
    email = db.Column(db.String(),nullable=False)
    password = db.Column(db.Text(),nullable=False)

    def __repr__(self):
        return f"User {self.username}"

    def save(self):
        db.session.add(self)
        db.session.commit()
    

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password
        db.session.commit()

  



