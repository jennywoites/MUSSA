from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True, unique=True)

    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    alumno = db.relationship("Alumno", back_populates="user")

    def __init__(self, username, password):
        self.username = username
        self.password = password

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
        return '<User %r>' % (self.username)
