from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def is_authenticated(self):
        """
        Retorna True a menos que el usuario no tenga
        permitido autenticarse por algun motivo.
        """
        return True

    @property
    def is_active(self):
        """
        Retorna True para los usuarios a menos que esten
        inactivos, por ejemplo porque fueron banneados.
        """
        return True

    @property
    def is_anonymous(self):
        """
        Devuelve True solo a los usuarios que no se
        supone que puedan loguearse en el sistema.
        """
        return False

    def get_id(self):
        return str(self.id)


    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)