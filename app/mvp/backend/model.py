from ext import db


# User model 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(),nullable=False)
    password = db.Column(db.Text(),nullable=False)
    isteacher = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"User {self.username}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
        db.session.commit()


# Sign model
class Sign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(50), nullable=False)
    mono_code_characters = db.Column(db.String(10), nullable=False)
    predictive_label = db.Column(db.String(50))

    def __repr__(self):
        return f"Sign {self.language} - {self.mono_code_characters}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, language, mono_code_characters, predictive_label):
        self.language = language
        self.mono_code_characters = mono_code_characters
        self.predictive_label = predictive_label
        db.session.commit()


# Activity model
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sign_id = db.Column(db.Integer, db.ForeignKey('sign.id'), nullable=False)
    result = db.Column(db.Numeric(5, 2), nullable=False)  # Success rate
    timetaken = db.Column(db.Numeric(6, 2))  # Time taken to perform the sign
    hint_used = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"Activity {self.id} - Student {self.student_id} Sign {self.sign_id}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, result, timetaken, hint_used):
        self.result = result
        self.timetaken = timetaken
        self.hint_used = hint_used
        db.session.commit()

# Performance History model
class PerformanceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sign_id = db.Column(db.Integer, db.ForeignKey('sign.id'), nullable=False)
    mastery_level = db.Column(db.Numeric(5, 2))  # Mastery level
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"PerformanceHistory {self.id} - Student {self.student_id} Sign {self.sign_id}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, mastery_level):
        self.mastery_level = mastery_level
        db.session.commit()

# Student-Sign Mastery model
class StudentSignMastery(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    sign_id = db.Column(db.Integer, db.ForeignKey('sign.id'), primary_key=True)
    current_mastery_level = db.Column(db.Numeric(5, 2))  # Current mastery level
    last_updated = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f"Mastery Student {self.student_id} Sign {self.sign_id}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, current_mastery_level):
        self.current_mastery_level = current_mastery_level
        db.session.commit()

