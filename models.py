from app import db
# class Product_Table(db.Model):
#     __tablename__="Product_Table"
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     productName = db.Column(db.String(80), unique=True, nullable=False)
#     details = db.Column(db.String(120), nullable=False)
#     price = db.Column(db.Integer)

#--------------------------Create Table---------------------------------------
# db.create_all() ==> Crate Table
#--------------------------Add Rows-------------------------------------------
# >>> product1=Product_Table(productName='dellg5',details="laptop",price=15000)
# >>> product2=Product_Table(productName='lenovo',details="laptop2",price=20000)
# >>> db.session.add(product1)
# >>> db.session.add(product2)
# >>> db.session.commit()
#---------------------------Read Speific Rows ----------------------------------
# >>> product1_read=Product_Table.query.filter_by(id=3).first()
#product1_read.productName ===>
#product1_read.details ===>
#product1_read.price ===>
#--------------------------------------------------------------------------------
class Person(db.Model):
    __bind_key__='database1'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # Relation Person ----> Address 
    # addresses = db.relationship('Address', backref='person', lazy=True)#Retrive dynamic,Select,join 

class Address(db.Model):
    __bind_key__='database2'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    # person_id = db.Column(db.Integer, db.ForeignKey('person.id'),nullable=False)

class Address3(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    # person_id = db.Column(db.Integer, db.ForeignKey('person.id'),nullable=False)

#API --> Application Prgramming Interface
#GUI --> Graphical USers 














