SQLAlchemy 
Flask 
Installation of marshmallow etc 
Object serialization/deserialization using Marshmallow
Flask + marshmallow 
Flask SqlAlchemy 
RabbitMQ
Asynchronous jobs using Celery
Database migrations using Alembic
Formatting code using Black
-------------------
###SQLAlchemy 
#pip3 install sqlalchemy
#or windows from http://www.lfd.uci.edu/~gohlke/pythonlibs/#sqlalchemy (does not get installed)

#start cygwin sqld
#mysql -running daemon in cygwin
/usr/bin/mysqld_safe &
#shutting down
mysqladmin.exe -h 127.0.0.1 -u root   --connect-timeout=5 shutdown
#mysql admin #  default port 3306, 
mysql -u root    -h 127.0.0.1 
#few commands
show databases;
create database python;
use python;
show tables;
create table employes ( id INT, first_name VARCHAR(20), last_name VARCHAR(20), hire_date  DATE);
desc employes;
insert into employes values (3, "das", "das", '1999-03-30');
select * from employes; 
drop table employes;



##SQLAlchemy - Quick Tutorial 
https://www.bytefish.de/blog/first_steps_with_sqlalchemy/

# Install virtualenv
$ pip install virtualenv

$ virtualenv sqlalchemy
$ sqlalchemy\Scripts\activate

(sqlalchemy) PS $ pip install jupyter ipython sqlalchemy 
(sqlalchemy) PS $ ipython   
#advantage any code , copy it to the clipboard and then use ipythons paste 
>>> %paste

##Without any Model class 
#Database Urls - dialect+driver://username:password@host:port/database

#http://docs.sqlalchemy.org/en/latest/core/engines.html#engine-creation-api
from sqlalchemy import create_engine

# sqlite://<nohostname>/<path>
# where <path> is relative:
engine = create_engine('sqlite:///foo.db')
#for an absolute file path
#Unix/Mac - 4 initial slashes in total
engine = create_engine('sqlite:////absolute/path/to/foo.db')
#Windows
engine = create_engine('sqlite:///C:\\path\\to\\foo.db')
#Windows alternative using raw string
engine = create_engine(r'sqlite:///C:\path\to\foo.db')
#To use a SQLite :memory: database, specify an empty URL:
engine = create_engine('sqlite://')

#MySQL
# default
engine = create_engine('mysql://scott:tiger@localhost/foo')
# mysql-python
engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo')
# MySQL-connector-python
engine = create_engine('mysql+mysqlconnector://scott:tiger@localhost/foo')
# OurSQL
engine = create_engine('mysql+oursql://scott:tiger@localhost/foo')

#Few importants  methods 
engine.scalar(statement, *multiparams, **params)
    Executes and returns the first column of the first row.
engine.execute(statement, *multiparams, **params)
    Executes the given construct and returns a ResultProxy.
engine.has_table(table_name, schema=None)
    Return True if the given backend has a table of the given name.
engine.table_names(schema=None, connection=None)
    Return a list of all table names available in the database.
engine.run_callable(callable_, *args, **kwargs)
    Given a callable object or function, execute it, 
    passing a Connection as the first argument
engine.raw_connection(_connection=None)
    Return a 'raw' DBAPI connection from the connection pool.



#execution 
#Option-1 : Transaction based commit 
with engine.begin() as conn:
    conn.execute("insert into table (x, y, z) values (1, 2, 3)")
    conn.execute("my_special_procedure(5)")
    
#OR directly - autocomitted 
#multiple 
engine.execute("INSERT INTO table (id, value) VALUES (?, ?)", (1, "v1"), (2, "v2"))
#single 
engine.execute("INSERT INTO table (id, value) VALUES (?, ?)",  1, "v1")
#with trx boundary 
def do_something(conn, x, y):
    conn.execute("some statement", {'x':x, 'y':y})

engine.transaction(do_something, 5, 10)


#Option-2: Get connection and execute 
conn = engine.connect()
#multiple 
conn.execute("INSERT INTO table (id, value) VALUES (?, ?)", (1, "v1"), (2, "v2"))
#single 
conn.execute("INSERT INTO table (id, value) VALUES (?, ?)",  1, "v1")

#with trx boundary call trans.rollback() or trans2.commit()
trans = conn.begin()   # transaction
conn.execute("insert into x (a, b) values (1, 2)")
trans.commit()         # actually commits
#or 
with conn.begin():
    conn.execute("insert into x (a, b) values (1, 2)")

#check below 
conn.begin_nested() 
    use a SAVEPOINT
conn.begin_twophase() 
    use a two phase /XID transaction

#Execute the given function within a transaction boundary.
def do_something(conn, x, y):
    conn.execute("some statement", {'x':x, 'y':y})
    
conn.transaction(do_something, 5, 10)


#DBAPI-agnostic way( without using ?) 
from sqlalchemy import text
t = text("SELECT * FROM users")
result = connection.execute(t)
#For SQL statements where a colon is required verbatim
t = text("SELECT * FROM users WHERE name='\:username'")
#with elaborate binding 
t = text("SELECT * FROM users WHERE id=:user_id").bindparams(user_id=7).\
        columns(id=Integer, name=String)
#or 
from sqlalchemy.sql import column
t = text("SELECT * FROM users WHERE id=:user_id").bindparams(user_id=7).columns(
                      column('id', Integer),
                      column('name', String)
                  )
for id, name in connection.execute(t):
    print(id, name)
    
#multiple bindparams 
t = text("SELECT id, name FROM user WHERE name=:name AND timestamp=:timestamp")\
        .bindparams(name='jack',
            timestamp=datetime.datetime(2012, 10, 8, 15, 12, 5))
#or 
from sqlalchemy import bindparam
t=text("SELECT id, name FROM user WHERE name=:name AND timestamp=:timestamp").bindparams(
                bindparam('name', value='jack', type_=String),
                bindparam('timestamp', type_=DateTime)
            )    

#with Proc 
t = text("EXEC my_procedural_thing()").execution_options(autocommit=True)
result = connection.execute(t)
conn.close()   
        
#Example 
from sqlalchemy import create_engine
engine = create_engine('sqlite:///sample.db')
engine.execute("create table emp(id int, name varchar(10))")
engine.execute("insert into emp values (1,'xxxx')")
results = engine.execute("select * from emp")
rows = list(results)  #force 



##With Model
#uses the declarative extensions of SQLAlchemy. 
#declarative_base is a factory function, that returns a base class (actually a metaclass), 
#and the entities are going to inherit from it. 

#Once the definition of the class is done, 
#the Table and mapper will be generated automatically. 
#Only define explicitly table name, primary keys and relationships.

#create the Base class:

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

'''
A one to many relationship places a foreign key on the child table(Child class) 
referencing the parent(Parent). 
relationship() is then specified on the parent(Parent class), 
as referencing a collection of items represented by the child:

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    
To establish a bidirectional relationship in one-to-many, 
where the 'reverse' side is a many to one, 
use  backref option on a Parent relationship() eg 
Child.parent would created on Child to access parent 
children = relationship("Child", backref="parent")


'''

'''
Many to Many adds an association table between two classes. 
There is no need to delete from this table manually, it is handled automatically
The association table is indicated by the secondary argument to relationship() of Parent class . 

association_table = Table('association', Base.metadata,
    Column('left_id', Integer, ForeignKey('left.id')),
    Column('right_id', Integer, ForeignKey('right.id'))
)

class Parent(Base):
    __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    children = relationship("Child",secondary=association_table)

class Child(Base):
    __tablename__ = 'right'
    id = Column(Integer, primary_key=True)
    
For a bidirectional relationship, 
both sides of the relationship contain a collection, Use backref on Parent realtionship()
Child.parents would created on Child to access parents 
children = relationship("Child",secondary=association_table, backref="parents")

'''

'''
sqlalchemy.orm.relationship(argument, secondary=None, primaryjoin=None, 
        secondaryjoin=None, foreign_keys=None, uselist=None, order_by=False, 
        backref=None, back_populates=None, post_update=False, cascade=False, 
        extension=None, viewonly=False, lazy='select', collection_class=None, 
        passive_deletes=False, passive_updates=True, remote_side=None, 
        enable_typechecks=True, join_depth=None, comparator_factory=None, 
        single_parent=False, innerjoin=False, distinct_target_key=None, 
        doc=None, active_history=False, cascade_backrefs=True, 
        load_on_pending=False, bake_queries=True, _local_remote_pairs=None, 
        query_class=None, info=None)
    Provide a relationship between two mapped classes
sqlalchemy.orm.backref(name, **kwargs)
    Create a back reference with explicit keyword arguments, 
    which are the same arguments one can send to relationship().
    Note name attribute would be created Other objects 

lazy types 
    lazy='dynamic' 
        Valid for a one-to-many or many-to-many relationship, 
        as 'children' would be Python collection for these relations 
        However with this, 'children' is a Query object in place of a collection 
        and filter() criterion may be applied as well as limits and offsets, either explicitly or via array slices
    lazy='noload'   
        A 'noload' relationship never loads from the database
        children would be empty          
    lazy='select'
        By default, all inter-object relationships are lazy loading ie load upon attribute access
    lazy='raise'
        lazy='select' causes  N plus one problem
        for any  N objects loaded, accessing their lazy-loaded attributes means 
        there will be N+1 SELECT statements emitted
        This options would make children empty and if somebody accesses children, would raise Exception
    lazy="joined"
        Eager loading in the ORM
        This form of loading applies a JOIN to the given SELECT statement 
        so that related rows are loaded in the same result set. 
    lazy='subquery' 
        Emits a second SELECT statement for each relationship to be loaded, 
        across all result objects at once
        Advantages compared to 'joined'
        it allows the original query to proceed without changing it at all
        it allows for many collections to be eagerly loaded without producing a single query that has many JOINs in it, which can be even less efficient
    lazy='selectin' 
        Emits a second (or more) SELECT statement 
        which assembles the primary key identifiers of the parent objects 
        into an IN clause, so that all members of related collections / scalar references are loaded at once by primary key
        In general, 'selectin' loading is probably superior to 'subquery' eager loading in most ways
        
'''


from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref



#Bidirectional One to Many : One Image, Many Comment 
#Here Parent = Image , Child = Comment , 
#Parent gets 'children=relationship('Child', backref='parent'), children is Python collection
#Child gets foreign key 'parent_id = Column(Integer, ForeignKey('parent.id'))'


#Bidirectional Many to Many relation with association table 
#Here Parent = Image , Child = Tag , association table = tags 
#Parent gets 'children = relationship("Child",secondary=association_table, backref='parent'), children is Python collection
#Child gets nothing 



tags = Table('tag_image', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id')),    #tags = table name of Tag 
    Column('image_id', Integer, ForeignKey('images.id')) #images = Table name of Image 
)

class Image(Base):
    __tablename__ = 'images'
    id          =   Column(Integer, primary_key=True)
    uuid        =   Column(String(36), unique=True, nullable=False)
    likes       =   Column(Integer, default=0)
    created_at  =   Column(DateTime, default=datetime.utcnow)
    tags        =   relationship('Tag', secondary=tags, backref = backref('images', lazy='dynamic'))
    comments    =   relationship('Comment', backref='image', lazy='dynamic')
    def __repr__(self):
        str_created_at = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return "<Image (uuid='%s', likes='%d', created_at=%s)>" % (self.uuid, self.likes, str_created_at)

class Tag(Base):
    __tablename__ = 'tags'
    id      =   Column(Integer, primary_key=True)
    name    =   Column(String(255), unique=True, nullable=False)
    def __repr__(self):
        return "<Tag (name='%s')>" % (self.name)

class Comment(Base):
    __tablename__ = 'comments'
    id          =   Column(Integer, primary_key=True)
    text        =   Column(String(2000))
    image_id    =   Column(Integer, ForeignKey('images.id'))
    def __repr__(self):
        return "<Comment (text='%s')>" % (self.text)


##Connecting and Creating the Schema

from sqlalchemy import create_engine

#for sqlite hack 
from sqlalchemy import event
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
    

engine = create_engine('sqlite:///:memory:', echo=True)
#generates the Schema:
Base.metadata.create_all(engine)


#With echo=True for the engine, below SQL would be generated :
CREATE TABLE tags (
        id INTEGER NOT NULL,
        name VARCHAR(255) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (name)
)
COMMIT

CREATE TABLE images (
        id INTEGER NOT NULL,
        uuid VARCHAR(36) NOT NULL,
        likes INTEGER,
        created_at DATETIME,
        PRIMARY KEY (id),
        UNIQUE (uuid)
)
COMMIT

CREATE TABLE tag_image (
        tag_id INTEGER,
        image_id INTEGER,
        FOREIGN KEY(tag_id) REFERENCES tags (id),
        FOREIGN KEY(image_id) REFERENCES images (id)
)
COMMIT

CREATE TABLE comments (
        id INTEGER NOT NULL,
        text VARCHAR(2000),
        image_id INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(image_id) REFERENCES images (id)
)
COMMIT


##Handling Sessions to DB 

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

#Note attributes are accessed as Class.attribute_var 
#Instance is created like Class(attribute_var=value,...)
#.id are automatically created 
#On to Many, Image to comments , comments  is python collection 
#Many to Many , Image to tags, tags is python collection 

##Insert
tag_cool = Tag(name='cool')
tag_car = Tag(name='car')
tag_animal = Tag(name='animal')

comment_rhino = Comment(text='Rhinoceros, often abbreviated as rhino, is a group of five extant species of odd-toed ungulates in the family Rhinocerotidae.')

image_car = Image(uuid='uuid_car', tags=[tag_car, tag_cool], \
    created_at=(datetime.utcnow() - timedelta(days=1)))
image_another_car = Image(uuid='uuid_anothercar', tags=[tag_car])
image_rhino = Image(uuid='uuid_rhino', tags=[tag_animal], comments=[comment_rhino])


#add the records and commit the work:
session.add(tag_cool)
session.add(tag_car)
session.add(tag_animal)
session.add(comment_rhino)
session.add(image_car)
session.add(image_another_car)
session.add(image_rhino)
session.commit()


#The generated SQL appears in the command prompt:
BEGIN
INSERT INTO tags (name) VALUES (?)('cool',)
INSERT INTO tags (name) VALUES (?)('car',)
INSERT INTO tags (name) VALUES (?)('animal',)
INSERT INTO images (uuid, likes, created_at) VALUES (?, ?, ?)('uuid_car', 0, '2014-12-20 19:16:19.822000')
INSERT INTO images (uuid, likes, created_at) VALUES (?, ?, ?)('uuid_anothercar', 0, '2014-12-21 19:16:19.828000')
INSERT INTO images (uuid, likes, created_at) VALUES (?, ?, ?)('uuid_rhino', 0, '2014-12-21 19:16:19.829000')
INSERT INTO tag_image (tag_id, image_id) VALUES (?, ?)((2, 1), (1, 1), (3, 3), (2, 2))
INSERT INTO comments (text, image_id) VALUES (?, ?)('Rhinoceros, often abbreviated as rhino, is a group of five extant species of odd-toed ungulates in the family Rhinocerotidae.', 3)
COMMIT


##Update
# Find the image with the given uuid:
image_to_update = session.query(Image).filter(Image.uuid == 'uuid_rhino').first()
# Increase the number of upvotes:
image_to_update.likes = image_to_update.likes + 1
# And commit the work:
session.commit()


#The generated SQL appears in the command prompt:
SELECT images.id AS images_id, images.uuid AS images_uuid, images.likes AS images_likes, images.created_at AS images_created_at
        FROM imagesWHERE images.uuid = ? LIMIT ? OFFSET ? ('uuid_rhino', 1, 0)
UPDATE images SET likes=? WHERE images.id = ? (1, 3)
COMMIT


##Delete
session.delete(image_rhino)
session.commit()

#The generated SQL appears in the command prompt:
#comments of an image do not get deleted once the image is deleted. 
#orphaned tags are not deleted
SELECT images.id AS images_id, images.uuid AS images_uuid, images.likes AS images_likes, images.created_at AS images_created_at
    FROM images WHERE images.id = ? (3,)
SELECT comments.id AS comments_id, comments.text AS comments_text, comments.image_id AS comments_image_id
    FROM comments WHERE ? = comments.image_id (3,)
sqlalchemy.engine.base.Engine SELECT tags.id AS tags_id, tags.name AS tags_name 
    FROM tags, tag_image WHERE ? = tag_image.image_id AND tags.id = tag_image.tag_id (3,)
DELETE FROM tag_image WHERE tag_image.tag_id = ? AND tag_image.image_id = ? (3, 3)
UPDATE comments SET image_id=? WHERE comments.id = ? (None, 1)
DELETE FROM images WHERE images.id = ? (3,)
COMMIT (1,)


#If you want the comments to be deleted, 
#when the parent image is deleted, then add a cascade = "all,delete" to the relationship declaration:
comments = relationship('Comment', cascade = "all,delete", backref='image', lazy='dynamic')



##Queries
#http://docs.sqlalchemy.org/en/latest/orm/query.html
#To force query, use .all(), .count(), .one() etc actions 
#.filter() etc returns another query 

# Get a list of tags:
for name in session.query(Tag.name).order_by(Tag.name):
    print(name)

# How many tags do we have?
session.query(Tag).count()

# Get all images created yesterday:
session.query(Image) \
    .filter(Image.created_at < datetime.utcnow().date()) \
    .all()

# Get all images, that belong to the tag 'car' or 'animal', using a subselect:
session.query(Image) \
    .filter(Image.tags.any(Tag.name.in_(['car', 'animal']))) \
    .all()

# This can also be expressed with a join:
session.query(Image) \
    .join(Tag, Image.tags) \
    .filter(Tag.name.in_(['car', 'animal'])) \
    .all()

# Play around with functions:
from sqlalchemy.sql import func, desc

max_date = session.query(func.max(Image.created_at))
session.query(Image).filter(Image.created_at == max_date).first()

# Get a list of tags with the number of images:
q = session.query(Tag, func.count(Tag.name)) \
    .outerjoin(Image, Tag.images) \
    .group_by(Tag.name) \
    .order_by(desc(func.count(Tag.name))) \
    .all()

for tag, count in q:
    print 'Tag "%s" has %d images.' % (tag.name, count) 

# Get images created in the last two hours and zero likes so far:
session.query(Image) \
    .join(Tag, Image.tags) \
    .filter(Image.created_at > (datetime.utcnow() - timedelta(hours=2))) \
    .filter(Image.likes == 0) \
    .all()


###Quick Flask 
#http://flask.palletsprojects.com/en/1.1.x/deploying/#deployment


##Flask 
jinja2 core filter 
    https://jinja.palletsprojects.com/en/2.10.x/templates/#list-of-builtin-filters
Jinja2 Test 
    https://jinja.palletsprojects.com/en/2.10.x/templates/#builtin-tests

#First code 
from flask import Flask

app = Flask(__name__)

@app.route("/")#http://127.0.0.1:5000/
def home():
    return """
        <html><body>
        <h1 id="some" class="some">Hello there!!</h1>
        <h1 id="some2" class="some">Welcome</h1>
        </body></html>
    """
#OR  
# from flask import Response
# r = Response(response="<a>ok</a>", status=200, mimetype="application/xml")
# r.headers["Content-Type"] = "text/xml; charset=utf-8"
# return r  

if __name__ == '__main__':
    app.run()    
  

#BeautifulSoup 
from bs4 import BeautifulSoup
import requests

r  = requests.get("http://127.0.0.1:5000/")
data = r.text
soup = BeautifulSoup(data, 'html.parser')
soup.html.body.h1.name  #only first
soup.html.body.h1.attrs  #only first 
soup.html.body.h1.text  #only first
soup.find_all('h1') 
for e in soup.find_all('h1') :
    print(e.attrs['id'])  #e.text, e['id']

soup.select("html body h1")  
soup.select("h1#some")
soup.select("h1.some")



#flask code 
from flask import Flask, request, jsonify, render_template, make_response 
import json , os 

app = Flask(__name__)

'''
#to xml or json based on template 
template = render_template('somefile.xml', values=values)
r = make_response(template)
r.headers['Content-Type'] = 'application/xml'
r.status_code = 200 
return r 
'''
@app.route("/env", methods=['GET','POST'])#http://127.0.0.1:5000/env
def env():
    if request.method == 'POST':
        envp = request.form.get('envp', 'all').upper()
        env_dict = os.environ
        if os.environ.get(envp, "notfound") != "notfound":
            env_dict = { envp : os.environ.get(envp,"notfound") }
        return render_template("env.html", 
            envs=env_dict)
    else:
        return """
            <html><body>
            <form action="/env" method="post">
              Put Variable name :<br>
              <input type="text" name="envp" value="ALL">
              <br><br>
              <input type="submit" value="Submit">
            </form> 
            </body></html>
        """
        

#templates/env.html 
<html>
<body>
<table border="1">
<tr><th>Key</th><th>Value</th></tr>
{% if envs.items() %}  {# can put jinja test eg var is defined #}
{% for k,v in envs.items() %}
<tr>
<td>{{ k }}</td>
<td>{{ v }}</td>
</tr>
{% endfor %}
{% endif %}
</table>
</body>
</html>



##More example 

from flask import jsonify, Response    
@app.route("/helloj")               # http://localhost:5000/helloj?name=das&format=xml
@app.route("/helloj/<string:name>") # http://localhost:5000/helloj/das #REST param 
def helloj(name="Unknown"):
        db = [ {"name": "ABC", "age": 20}, 
          {"name": "das", "age": 100}]
        fname = request.args.get("name", name)
        format = request.args.get("format", "json")
        age = None 
        for emp in db:
            if fname == emp['name']:
                age = emp['age']
        if format == "json":
            if age:
                obj = {"name": fname, "age": age}
                resp = jsonify(obj)
                resp.status_code = 200
            else:
                error = {"details": "Name is not found"}
                resp = jsonify(error)
                resp.status_code = 500
        else:   #http://localhost:5000/helloj?name=das&format=xml
            data = '''<?xml version="1.0"?>
                      <data><name>%s</name><age>%s</age></data>''' % (fname, age)
            resp = Response(response=data, status=200, mimetype="application/xml")
            resp.headers['Content-Type'] = "text/xml; charset=utf-8"
        return resp 
    
    
'''
import requests as r 
res = r.get("http://localhost:5000/helloj")
res.json() 
'''   


##Example DB 
from sqlalchemy import * 
from flask import jsonify, g
DATABASE = "people.db"
def get_db():
    db = getattr(g, '_database', None)  #do import g, g is global object in FLASK
    if db is None:
        db = g._database = create_engine("sqlite:///"+DATABASE)
    return db     
    
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        pass #db.close()
        
        
def getage(name):
    eg = get_db()
    q = eg.execute("select age from people where name = ?" ,name)
    return q.fetchone()[0]

@app.route("/json", methods=['POST'])   # http://localhost:5000/json with jsondata
def js():
    user = dict(username='nobody', age="nonefound")
    if 'Content-Type' in request.headers and request.headers['Content-Type'].lower() == 'application/json':
        user['username'] = request.json.get("username", "nobody")
    try:
        user['age'] = getage(user['username'])
    except:
        pass
    resp = jsonify(user)
    resp.status_code = 200
    return resp  
    
'''
headers = {'Content-Type': 'application/json'}
import json
import requests as r 
obj = {'username' : 'das'}
res = r.post("http://localhost:5000/json", data=json.dumps(obj),headers=headers)
res.json() 
''' 
#Some data creation 
from sqlalchemy import * 
DATABASE = "people.db"
db = create_engine("sqlite:///"+DATABASE)
db.execute("""create table if not exists people (name string, age int)""")
db.execute("""insert into people values(?,?)""", ["das", 20])

q = db.execute("select age from people where name=?", "das")
q.fetchone()




##Example Login 
from flask import session, redirect, url_for #NEW
app.secret_key = b"jhdkjhdkhshd"  #NEW

from functools import wraps
def auth_required(f):
    @wraps(f)
    def _inner(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))  #login is method name 
        return f(*args, **kwargs)
    return _inner

    
@app.route("/")
@auth_required  #NEW, should be inner 
def home():   # http://localhost:5000/
    return """
            <html><body>
                <h1 id="some" class="cl2">Hello there!!! </h1>
                <h1 id="some2" class="cl2">Welcome</h1>
            </body></html>
        """

def check_auth(user, password):
    return user == 'admin' and password == 'secret'
   
@app.route("/login", methods=['GET', 'POST'])  # http://localhost:5000/login
def login():  
    if request.method == 'POST':
        name = request.form.get('name', 'all')
        password = request.form.get('pass', 'all')
        if check_auth(name, password):
            session['username'] = name
            return redirect(url_for('home'))  #home is method name 
        else:
            return "<h1>Error</h1>"
    else:
        return """
                <html><body>
                <form action="/login" method="post">
                 Name: <br/>
                 <input type="text" name="name" value="" />
                 Password: <br/>
                 <input type="password" name="pass" value="" />
                 <br/><br/>
                 <input type="submit" value="Submit" />
                </form>
                </body></html>
            """
        
'''
s = r.Session()
cred = {'name': 'admin', 'pass': 'secret'}
r1 = s.post("http://127.0.0.1:5000/login", cred)
r2 = s.get("http://127.0.0.1:5000/")
r2.text   
'''        
        
##Example upload 
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET', 'POST']) #http://127.0.0.1:5000/upload
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file.filename:
            filename = secure_filename(file.filename) #normalizes the file path 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
    
from flask import send_from_directory
#mimetype: str

#as_attachment: bool, attachment_filename:str, mimetype: str
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)    
    
  
#with file upload and download 
files = {'file': open('copy.txt','rb')} #'file' same as form's name for type=file 
other_form_data = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}
r = requests.post("http://127.0.0.1:5000/upload", files=files, data=other_form_data)
r.request.url #'http://127.0.0.1:5000/download/copy.txt' , the redirected one 
r.status_code
r.headers.get('content-disposition') #'attachment; filename=copy.txt'
local_filename = r.headers.get('content-disposition').split("=")[-1]
with open(local_filename+".bak", 'wb') as f:
    f.write(r.content)

            
#for big file 
import shutil
with requests.get('http://127.0.0.1:5000/download/copy.txt', stream=True) as r:
    with open(local_filename+".bak2", 'wb') as f:
        shutil.copyfileobj(r.raw, f)           
            
            
       
#Packaging 
$ pip install virtualenv

$ mkdir myproject
$ cd myproject
$ virtualenv venv
New python executable in venv/bin/python
Installing setuptools, pip............done.

$ . venv/bin/activate
#or in windows 
$ venv\scripts\activate
$ pip install Click flask

$ deactivate
#Directory layout 
flaskr
    __init__.py
    quick_server.py 
    example.json 
    uploads\
    templates\ 
    static\ 
setup.py 
MANIFEST.in
.gitignore 

#exmample .gitignore
.gitignore

venv/

*.pyc
__pycache__/

dist/
build/
*.egg-info/

#Update 
#__init__.py 
from flask import Flask
app = Flask(__name__)
from . import quick_server  #should be last as routes module needs above app variable 

#quick_server.py 
#comment out below 
#app = Flask(__name__)
from flaskr import app

#update all reference to relative path is with app.root_path 
def server():
    import os.path 
    filename = os.path.join(app.root_path, 'example.json')
    with open(filename, "rt") as f:
        #...
        
DATABASE = os.path.join(app.root_path,'database.db')
UPLOAD_FOLDER = os.path.join(app.root_path,'uploads')


#Basic Setup Script, file:setup.py 
from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    #Please keep in mind that you have to list subpackages explicitly. 
    #If you want setuptools to lookup the packages for you automatically
    #which py pkg to package, based on current dir 
    packages=find_packages(),
    include_package_data=True,  # checks  MANIFEST.in
    zip_safe=False, #setuptools to install your project as a directory rather than as a zipfile
    install_requires=[
        'flask',
    ],
)
#or 
install_requires=[
    'Flask>=0.2',
    'SQLAlchemy>=0.6',
    'BrokenPackage>=0.7,<=1.0'
]

#MANIFEST.in
#This tells Python to copy everything in the static and templates directories, 
#and the schema.sql file, but to exclude all bytecode files
include flaskr/example.json
graft flaskr/static
graft flaskr/templates
graft flaskr/uploads
global-exclude *.pyc


#Install the Project
#This tells pip to find setup.py in the current directory and install it in editable or development mode. Editable mode means that as you make changes to your local code, you’ll only need to re-install if you change the metadata about the project, 
#such as its dependencies.
$ pip install -e .

$ pip list

#under venv , now go to any dir 
$ set FLASK_APP=flaskr  #set FLASK_ENV=development/production(don't set ENV)
#https://flask.palletsprojects.com/en/1.1.x/config/#environment-and-debug-features
#Setting FLASK_ENV to development will enable debug mode. 
#flask run will use the interactive debugger and reloader by default in debug mode. 
#To control this separately from the environment, use the FLASK_DEBUG flag.

$ flask run  #flask run --port 8000
#for flask <0.19,
$ set FLASK_APP=flaskr/__init__.py 
$ flask run
#or with gevent_server.py 
$ set FLASK_APP=gevent_server.py
$ flask run

##Deploy to Production
$ pip install wheel

$ python setup.py bdist_wheel
#You can find the file in dist/flaskr-1.0.0-py3-none-any.whl. 

#Copy this file to another machine, 
#set up a new virtualenv, then install the file with pip.

$ pip install flaskr-1.0.0-py3-none-any.whl

#Then run 
$ set FLASK_APP=flaskr
$ flask run 

##Deployement
#https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/

# For example to deploy via  Gevent 
pip install gevent 
#Gevent is a coroutine-based Python networking library 
#that uses greenlet to provide a high-level synchronous API on top of libev event loop:


#gevent_server.py
from gevent.pywsgi import WSGIServer
from flaskr import app

# http_server = WSGIServer(('localhost', 5000), app, keyfile='key.pem', certfile='cert.pem')
http_server = WSGIServer(('127.0.0.1', 5000), app)
http_server.serve_forever()

#With tornado 
$ pip install tornado

#code 
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from my_app import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
IOLoop.instance().start()


##SSL 
#to use adhoc certificates 
$ pip install pyopenssl
#then 
app.run(ssl_context='adhoc')
#or 
$ flask run --cert=adhoc

#to use Self-Signed Certificates
#http://slproweb.com/products/Win32OpenSSL.html
C:\cygwin64\bin\openssl.exe req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

#then 
app.run(ssl_context=('cert.pem', 'key.pem'))
#OR 
$ flask run --cert=cert.pem --key=key.pem

#To redirect http to https, use Flask-SSLify 
#that configures your Flask application to redirect all incoming requests to HTTPS.

#Using real certificates 
#https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
#eg one free CA , https://letsencrypt.org/getting-started/
#with nignx 
#https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04



###Flask in details 
#Check for many examples 
#https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

#hello.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

#To run 
$ export FLASK_APP=hello.py
$ flask run
 * Running on http://127.0.0.1:5000/

C:\path\to\app>set FLASK_APP=hello.py
PS C:\path\to\app> $env:FLASK_APP = "hello.py"
#OR 
$ export FLASK_APP=hello.py
$ python -m flask run
 * Running on http://127.0.0.1:5000/

#To bind to any local address 
flask run --host=0.0.0.0

#Debug Mode
$ export FLASK_ENV=development
$ flask run


##Routing

#Converter types:
string
	(default) accepts any text without a slash
int
	accepts positive integers
float
	accepts positive floating point values
path
    like string but also accepts slashes
uuid
    accepts UUID strings

#add variable sections , with <variable_name> or  <converter:variable_name>.

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)

#Define multiple rules for the same function. 
#This specifies that /users/ will be the URL for page one 
#and /users/page/N will be the URL for page N.
#/users/page/1 will be redirected to /users/
@app.route('/users/', defaults={'page': 1})
@app.route('/users/page/<int:page>')
def show_users(page):
    pass

#If your route handles GET and POST requests, 
#make sure the default route only handles GET, as redirects can’t preserve form data.
@app.route('/region/', defaults={'id': 1})
@app.route('/region/<int:id>', methods=['GET', 'POST'])
def region(id):
   pass

##Class based view 
class MyView(View):
    methods = ['GET']
    decorators = [superuser_required]

    def dispatch_request(self, name):
        return 'Hello %s!' % name

app.add_url_rule('/hello/<name>', view_func=MyView.as_view('myview'))

#OR Use view that dispatches request methods to the corresponding class methods
class CounterAPI(MethodView):
    def get(self):
        return session.get('counter', 0)

    def post(self):
        session['counter'] = session.get('counter', 0) + 1
        return 'OK'

app.add_url_rule('/counter', view_func=CounterAPI.as_view('counter'))

##Stream Helpers

from flask import stream_with_context, request, Response

@app.route('/stream')
def streamed_response():
    @stream_with_context
    def generate():
        yield 'Hello '
        yield request.args['name']
        yield '!'
    return Response(generate())

#OR 
from flask import stream_with_context, request, Response

@app.route('/stream')
def streamed_response():
    def generate():
        yield 'Hello '
        yield request.args['name']
        yield '!'
    return Response(stream_with_context(generate()))


    
    
##Unique URLs / Redirection Behavior

The following two rules differ in their use of a trailing slash.

@app.route('/projects/') #Flask redirects here even without a trailing slash
def projects():
    return 'The project page'

@app.route('/about') #Here flask does not redirects 
def about():
    return 'The about page'



##URL Building using url_for()

#It accepts the name of the function as its first argument 
#and any number of keyword arguments, each corresponding to a variable part of the URL rule. 

#Unknown variable parts are appended to the URL as query parameters.

#Example 
from flask import Flask, escape, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))

with app.test_request_context():
    print(url_for('index'))   # /
    print(url_for('login'))     # /login
    print(url_for('login', next='/')) # /login?next=/
    print(url_for('profile', username='John Doe')) # /user/John%20Doe
    print(url_for('profile', username='John Doe', q="2")) # /user/John%20Doe?q=2



##HTTP Methods
from flask import request

@app.route('/login', methods=['GET', 'POST']) #with GET, adds support for the HEAD method and handles HEAD requests according to the HTTP RFC
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

        
##Static Files
url_for('static', filename='style.css') #filesystem as static/style.css.


##Rendering Templates with jinja2 template 
#Jinja2 Has many tests, filters and functions

from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

#Flask checks 
#Case 1: a module:
/application.py
/templates
    /hello.html

#Case 2: a package:
/application
    /__init__.py
    /templates
        /hello.html

#hello.html
#can access to the request, session and g and get_flashed_messages() function.

<!doctype html>
<title>Hello from Flask</title>
{% if name %}
  <h1>Hello {{ name }}!</h1>
{% else %}
  <h1>Hello, World!</h1>
{% endif %}


#Automatic escaping is enabled
>>> from flask import Markup
>>> Markup('<strong>Hello %s!</strong>') % '<blink>hacker</blink>'
Markup(u'<strong>Hello &lt;blink&gt;hacker&lt;/blink&gt;!</strong>')
>>> Markup.escape('<blink>hacker</blink>')
Markup(u'&lt;blink&gt;hacker&lt;/blink&gt;')
>>> Markup('<em>Marked up</em> &raquo; HTML').striptags()
u'Marked up \xbb HTML'


##The Request Object
#To access parameters submitted in the URL (?key=value)
searchword = request.args.get('key', '')

#For data transmitted in a POST or PUT request) ,use the form attribute
#Raises  KeyError if key does not exists and  a HTTP 400 Bad Request error page is shown 
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

    
    
##File Uploads
#Uploaded files are stored in memory or at a temporary location on the filesystem. 
from flask import request
from werkzeug.utils import secure_filename

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/' + secure_filename(f.filename))
    ...

    
    
##Cookies
#Reading cookies:

from flask import request

@app.route('/')
def index():
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.

#Storing cookies:

from flask import make_response

@app.route('/')
def index():
    resp = make_response(render_template(...))
    resp.set_cookie('username', 'the username')
    return resp

    
    
    
##Redirects and Errors
from flask import abort, redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()

#to customize the error page
from flask import render_template

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

    
    
##About Responses
#The return value from a view function is automatically converted into a response object 
1.If a response object of the correct type is returned it's directly returned 
  from the view.
2.If it’s a string, a response object is created with that data 
  and the default parameters.
3.If a tuple is returned the items in the tuple can provide extra information. 
  Such tuples have to be in the form (response, status, headers), 
  (response, headers) or (response, status)   
  where at least one item has to be in the tuple. 
  The status value will override the status code 
  and headers can be a list or dictionary of additional header values.
4.If none of that works, Flask will assume the return value is a 
  valid WSGI application and convert that into a response object.
5. use the make_response() function to get this response object 

@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


##APIs with JSON
#If you return a dict from a view, it will be converted to a JSON response.

@app.route("/me")
def me_api():
    user = get_current_user()
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }

#OR 
@app.route("/users")
def users_api():
    users = get_all_users()
    return jsonify([user.to_json() for user in users])

#Other methods 
flask.json.dumps(obj, app=None, **kwargs)
    Serialize obj to a JSON-formatted string.
flask.json.dump(obj, fp, app=None, **kwargs)
    Like dumps() but writes into a file object.
flask.json.loads(s, app=None, **kwargs)
    Deserialize an object from a JSON-formatted string s.
flask.json.load(fp, app=None, **kwargs)
    Like loads() but reads from a file object.

#also from Request class 
from flask import request

class flask.Request(environ, populate_request=True, shallow=False)
    get_data(cache=True, as_text=False, parse_form_data=False)
    get_json(force=False, silent=False, cache=True)
        Parse data as JSON.
        If the mimetype does not indicate JSON (application/json, see is_json()), 
        this returns None.
        If parsing fails, on_json_loading_failed() is called 
        and its return value is used as the return value.
    property headers
        The headers from the WSGI environ as immutable EnvironHeaders.
        use  get(key, default=None, type=None, as_bytes=False)
    property json
        The parsed JSON data if mimetype indicates JSON (application/json)
        Calls get_json() with default arguments.
    property data
        Calls get_data() with default arguments.
    
    
##Sessions
#This is implemented on top of cookies and signs the cookies cryptographically. 

from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)

# Set the secret key to some random bytes. 
#python -c 'import os; print(os.urandom(16))'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

    
    
##Message Flashing
#To flash a message use the flash() method, 
#to get hold of the messages ,use get_flashed_messages() in templates 

from flask import Flask, flash, redirect, render_template, \
     request, url_for

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'secret':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

#layout.html
<!doctype html>
<title>My Application</title>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul class=flashes>
    {% for message in messages %}
      <li>{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
{% block body %}{% endblock %}

#index.html
{% extends "layout.html" %}
{% block body %}
  <h1>Overview</h1>
  <p>Do you want to <a href="{{ url_for('login') }}">log in?</a>
{% endblock %}

#login.html 
{% extends "layout.html" %}
{% block body %}
  <h1>Login</h1>
  {% if error %}
    <p class=error><strong>Error:</strong> {{ error }}
  {% endif %}
  <form method=post>
    <dl>
      <dt>Username:
      <dd><input type=text name=username value="{{
          request.form.username }}">
      <dt>Password:
      <dd><input type=password name=password>
    </dl>
    <p><input type=submit value=Login>
  </form>
{% endblock %}

##Flashing With Categories
flash(u'Invalid password provided', 'error')

#Then in template 
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    <ul class=flashes>
    {% for category, message in messages %}
      <li class="{{ category }}">{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}

#OR with filtering 
{% with errors = get_flashed_messages(category_filter=["error"]) %}
{% if errors %}
<div class="alert-message block-message error">
  <a class="close" href="#">×</a>
  <ul>
    {%- for msg in errors %}
    <li>{{ msg }}</li>
    {% endfor -%}
  </ul>
</div>
{% endif %}
{% endwith %}


##Sending file 

flask.send_file(filename_or_fp, mimetype=None, as_attachment=False, 
        attachment_filename=None, add_etags=True, 
        cache_timeout=None, conditional=False, 
        last_modified=None)
    Sends the contents of a file to the client
        filename_or_fp – the filename of the file to send. 
            This is relative to the root_path if a relative path is specified. 
            Alternatively a file object might be provided in which case X-Sendfile might not work 
            and fall back to the traditional method. 
            Make sure that the file pointer is positioned at the start of data to send 
            before calling send_file().
        mimetype – the mimetype of the file if provided. 
            If a file path is given, auto detection happens as fallback, otherwise an error will be raised.
        as_attachment – set to True if you want to send this file 
            with a Content-Disposition: attachment header.
        attachment_filename – the filename for the attachment 
            if it differs from the file’s filename.
        add_etags – set to False to disable attaching of etags.
        conditional – set to True to enable conditional responses.
        cache_timeout – the timeout in seconds for the headers. When None (default), this value is set by get_send_file_max_age() of current_app.
        last_modified – set the Last-Modified header to this value, a datetime or timestamp. If a file was passed, this overrides its mtime.
flask.send_from_directory(directory, filename, **options)
    Send a file from a given directory with send_file(). 
    This is a secure way to quickly expose static files 
    from an upload folder or something similar.
    #Example 
    @app.route('/uploads/<path:filename>')
    def download_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                   filename, as_attachment=True)

##Application Globals - flask.g
#To share data that is valid for one request only from one function to another, 
#a global variable is not good enough because it would break in threaded environments. 
#Use flask.g , it is only valid for the active request 
#and that will return different values for each request. 

#methods 
'key' in g
iter(g)
g.get(name, default=None)
g.pop(name, default=<object object>)
g.setdefault(name, default=None)



##Configuration 
app.config 
    Works exactly like a dict 
    but provides ways to fill it from files or special dictionaries.

#yourconfig.cfg
#only uppercase keys are added to the config.
DEBUG = True
SECRET_KEY = 'development key'

#Then 
app.config.from_pyfile('yourconfig.cfg')
#or 
export YOURAPPLICATION_SETTINGS='/path/to/config/yourconfig.cfg'
app.config.from_envvar('YOURAPPLICATION_SETTINGS')
#ie  
app.config.from_pyfile(os.environ['YOURAPPLICATION_SETTINGS'])

#or 
app.config.from_object('yourapplication.default_config')
from yourapplication import default_config
app.config.from_object(default_config)
#Objects are usually either modules or classes. 
#loads only the uppercase attributes of the module/class. 

#or store directly 
app.config['IMAGE_STORE_TYPE'] = 'fs'
app.config['IMAGE_STORE_PATH'] = '/var/app/images'
app.config['IMAGE_STORE_BASE_URL'] = 'http://img.website.com'
image_store_config = app.config.get_namespace('IMAGE_STORE_')
#The resulting dictionary image_store_config would look like:
{
    'type': 'fs',
    'path': '/var/app/images',
    'base_url': 'http://img.website.com'
}
#or 
app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )


##Logging
#a logger is preconfigured  to use.
app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')



##Deployement
#https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/

# For example to deploy via  Gevent 
#Gevent is a coroutine-based Python networking library 
#that uses greenlet to provide a high-level synchronous API on top of libev event loop:

from gevent.wsgi import WSGIServer
from yourapplication import app

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()

#Twisted Web
#Twisted Web is the web server shipped with Twisted, a mature, 
#non-blocking event-driven networking library.
$ twistd -n web --port tcp:8080 --wsgi myproject.app


##Modular Applications with Blueprints
Blueprints in Flask are intended for these cases:
1.Factor an application into a set of blueprints. 
  This is ideal for larger applications; a project could instantiate an application object, initialize several extensions, and register a collection of blueprints.
2.Register a blueprint on an application at a URL prefix and/or subdomain. 
  Parameters in the URL prefix/subdomain become common view arguments
  (with defaults) across all view functions in the blueprint.
3.Register a blueprint multiple times on an application with different URL rules.
4.Provide template filters, static files, templates, 
 and other utilities through blueprints. 
 A blueprint does not have to implement applications or view functions.
5.Register a blueprint on an application for any of these cases 
  when initializing a Flask extension.

flask.Flask(import_name, static_url_path=None, 
    static_folder='static', static_host=None, host_matching=False, 
    subdomain_matching=False, template_folder='templates', 
    instance_path=None, instance_relative_config=False, 
    root_path=None)
flask.Blueprint(name, import_name, static_folder=None, static_url_path=None, 
        template_folder=None, url_prefix=None, subdomain=None, 
        url_defaults=None, root_path=None, 
        cli_group=<object object>)
    name – The name of the blueprint. Will be prepended to each endpoint name.
    import_name – The name of the blueprint package, usually __name__. This helps locate the root_path for the blueprint.
    static_folder – A folder with static files that should be served by the blueprint’s static route. The path is relative to the blueprint’s root path. Blueprint static files are disabled by default.
    static_url_path – The url to serve static files from. Defaults to static_folder. If the blueprint does not have a url_prefix, the app’s static route will take precedence, and the blueprint’s static files won’t be accessible.
    template_folder – A folder with templates that should be added to the app’s template search path. The path is relative to the blueprint’s root path. Blueprint templates are disabled by default. Blueprint templates have a lower precedence than those in the app’s templates folder.
    url_prefix – A path to prepend to all of the blueprint’s URLs, to make them distinct from the rest of the app’s routes.
    subdomain – A subdomain that blueprint routes will match on by default.
    url_defaults – A dict of default values that blueprint routes will receive by default.
    root_path – By default, the blueprint will automatically this based on import_name. In certain situations this automatic detection can fail, so the path can be specified manually instead.
    #Methods 
    add_app_template_filter(f, name=None)
    add_app_template_global(f, name=None)
    add_app_template_test(f, name=None)
    add_url_rule(rule, endpoint=None, view_func=None, **options)
    after_app_request(f)
    after_request(f)
    app_context_processor(f)
    app_errorhandler(code)
    app_template_filter(name=None)
    app_template_global(name=None)
    app_template_test(name=None)
    app_url_defaults(f)
    app_url_value_preprocessor(f)
    before_app_first_request(f)
    before_app_request(f)
    before_request(f)
    context_processor(f)
    endpoint(endpoint)
    errorhandler(code_or_exception)
    get_send_file_max_age(filename)
  
#Example : yourapplication.py 
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')
                        
# it will prefix the endpoint of the function with the name of the blueprint 
#which was given to the Blueprint constructor (in this case also simple_page). 
#The blueprint’s name does not modify the URL, only the endpoint.

@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)


##Blueprint - Registering Blueprints
from flask import Flask
from yourapplication.simple_page import simple_page

app = Flask(__name__)
app.register_blueprint(simple_page)

#below rules would be registered 
>>> app.url_map
Map([<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
 <Rule '/<page>' (HEAD, OPTIONS, GET) -> simple_page.show>,
 <Rule '/' (HEAD, OPTIONS, GET) -> simple_page.show>])

#or mount  at different locations:
app.register_blueprint(simple_page, url_prefix='/pages')

>>> app.url_map
Map([<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
 <Rule '/pages/<page>' (HEAD, OPTIONS, GET) -> simple_page.show>,
 <Rule '/pages/' (HEAD, OPTIONS, GET) -> simple_page.show>])

 
 
##Blueprint -  Resource Folder
#The folder is inferred from the second argument to Blueprint 
#which is usually __name__. 
#This argument specifies what logical Python module or package corresponds to the blueprint. 

#If it points to an actual Python package 
#that package (which is a folder on the filesystem) is the resource folder. 
#If it’s a module, the package the module is contained in will be the resource folder. 
>>> simple_page.root_path
'/Users/username/TestProject/yourapplication'

#To quickly open sources from this folder 
with simple_page.open_resource('static/style.css') as f:
    code = f.read()

##Blueprint - Static Files (relative to Resource folder or abs path can be given )
admin = Blueprint('admin', __name__, url_prefix="admin", static_folder='static')
#By default the rightmost part of the path is where it is exposed on the web. 
#or change via  static_url_path argument. 

#If the blueprint has the url_prefix admin 
#the static URL will be /admin/static.
#The endpoint is named blueprint_name.static
url_for('admin.static', filename='style.css')

#if the blueprint does not have a url_prefix,
#it is not possible to access the blueprint’s static folder. 


##Blueprint - Templates (relative to Resource folder or abs path can be given )
admin = Blueprint('admin', __name__, template_folder='templates')
#The template folder is added to the search path of templates 
#but with a lower priority than the actual application’s template folder. 
#That way you can easily override templates that a blueprint provides in the actual application. 

#To render the template 'admin/index.html' 
#then  create a file like this: yourapplication/admin/templates/admin/index.html. 
#use EXPLAIN_TEMPLATE_LOADING config variable to debug further 
yourpackage/
    blueprints/
        admin/
            templates/
                admin/
                    index.html
            __init__.py

##Blueprint - Building URLs
url_for('admin.index')

#if you are in a view function of a blueprint or a rendered template 
#and you want to link to another endpoint of the same blueprint
url_for('.index')


##Blueprint - Error Handlers
@simple_page.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html')

#Most errorhandlers will simply work as expected; 
#however, there is a caveat concerning handlers for 404 and 405 exceptions. 

#These errorhandlers are only invoked from an appropriate raise statement 
#or a call to abort in another of the blueprint’s view functions; 

#they are not invoked by, e.g., an invalid URL access. 
#This is because the blueprint does not “own” a certain URL space, 
#so the application instance has no way of knowing 
#which blueprint error handler it should run if given an invalid URL. 

#If you would like to execute different handling strategies 
#for these errors based on URL prefixes, 
#they may be defined at the application level using the request proxy object:

@app.errorhandler(404)
@app.errorhandler(405)
def _handle_api_error(ex):
    if request.path.startswith('/api/'):
        return jsonify_error(ex)
    else:
        return ex


###Flask - Tutorial 
/home/user/Projects/flask-tutorial
├── flaskr/
│   ├── __init__.py
│   ├── db.py
│   ├── schema.sql
│   ├── auth.py
│   ├── blog.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── blog/
│   │       ├── create.html
│   │       ├── index.html
│   │       └── update.html
│   └── static/
│       └── style.css
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   ├── test_auth.py
│   └── test_blog.py
├── venv/
├── setup.py
└── MANIFEST.in

#.gitignore

venv/

*.pyc
__pycache__/

instance/

.pytest_cache/
.coverage
htmlcov/

dist/
build/
*.egg-info/

#Python 3 comes bundled with the venv module to create virtual environment
$ mkdir myproject
$ cd myproject
$ python3 -m venv venv
#On Windows:
$ py -3 -m venv venv  #last one is directory name 

#Activate the environment
$ . venv/bin/activate
#On Windows:
> venv\Scripts\activate


#for Python2 
pip install virtualenv
python2 -m virtualenv venv
#On Windows:
> \Python27\Scripts\virtualenv.exe venv

#Install Flask 
$ pip install Flask



##Flask - Tutorial - Application Setup
#flaskr/__init__.py

import os

from flask import Flask

'''
Flask Arguments 
import_name 
    the name of the application package
static_url_path 
    can be used to specify a different path for the static files on the web. 
    Defaults to the name of the static_folder folder.
static_folder 
    the folder with static files that should be served at static_url_path. 
    Defaults to the 'static' folder in the root path of the application.
static_host 
    the host to use when adding the static route. 
    Defaults to None. 
    Required when using host_matching=True with a static_folder configured.
host_matching 
    set url_map.host_matching attribute. Defaults to False.
subdomain_matching 
    consider the subdomain relative to SERVER_NAME when matching routes. 
    Defaults to False.
template_folder 
    the folder that contains the templates that should be used by the application. 
    Defaults to 'templates' folder in the root path of the application.
instance_path 
    An alternative instance path for the application. 
    By default the folder 'instance' next to the package or module 
    is assumed to be the instance path.
instance_relative_config 
    if set to True relative filenames for loading the config 
    are assumed to be relative to the instance path 
    instead of the application root.
root_path 
    Flask by default will automatically calculate the path to the root 
    of the application. 
    if the package is a Python 3 namespace package 
    and needs to be manually defined.
'''

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists , default is 'instance' under flaskr 
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

#Run 
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ flask run

#For Windows cmd, use set instead of export:

> set FLASK_APP=flaskr
> set FLASK_ENV=development
> flask run

#For Windows PowerShell, use $env: instead of export:

> $env:FLASK_APP = "flaskr"
> $env:FLASK_ENV = "development"
> flask run



##Flask - Tutorial - Define and Access the Database
#flaskr/db.py

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

# g is a special object that is unique for each request. 
# It is used to store data that might be accessed by multiple functions during the request. 

#current_app is a special object that points to the Flask application 
#handling the request. 

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row #return rows that behave like dicts

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

#open_resource() opens a file relative to the flaskr package,
def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        


#click.command() defines a command line command called init-db 
#that calls the init_db function and shows a success message to the user. 
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    
   
# app.teardown_appcontext() tells Flask to call that function 
# when cleaning up after returning the response.

# app.cli.add_command() adds a new command that can be called 
# with the flask command.
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
   
#Update create_app to call db.init_app(app)
#flaskr/__init__.py

def create_app():
    app = ...
    # existing code omitted

    from . import db
    db.init_app(app)

    return app

    
#flaskr/schema.sql

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

#Initialize the Database File
$ flask init-db



##Flask - Tutorial - Blueprints and Views
#Flaskr will have two blueprints, one for authentication functions 
#and one for the blog posts functions. 

#flaskr/auth.py

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

#This creates a Blueprint named 'auth'.
#The url_prefix will be prepended to all the URLs associated with the blueprint.

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

    
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')
    
#bp.before_app_request() registers a function that runs before the view function,
#no matter what URL is requested. 
#load_logged_in_user checks if a user id is stored in the session 
#and gets that user’s data from the database, storing it on g.user, which lasts for the length of the request. If there is no user id, or if the id doesn’t exist, g.user will be None.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()



#for logout 
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#Creating, editing, and deleting blog posts will require a user to be logged in. 
#A decorator can be used to check this for each view it’s applied to.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
    
#Update below to Import and register the blueprint 
#flaskr/__init__.py

def create_app():
    app = ...
    # existing code omitted

    from . import auth
    app.register_blueprint(auth.bp)

    return app

##Flask - Tutorial - Templates

#g is automatically available in templates
#flaskr/templates/base.html

<!doctype html>
<title>{% block title %}{% endblock %} - Flaskr</title>
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<nav>
  <h1>Flaskr</h1>
  <ul>
    {% if g.user %}
      <li><span>{{ g.user['username'] }}</span>
      <li><a href="{{ url_for('auth.logout') }}">Log Out</a>
    {% else %}
      <li><a href="{{ url_for('auth.register') }}">Register</a>
      <li><a href="{{ url_for('auth.login') }}">Log In</a>
    {% endif %}
  </ul>
</nav>
<section class="content">
  <header>
    {% block header %}{% endblock %}
  </header>
  {% for message in get_flashed_messages() %}
    <div class="flash">{{ message }}</div>
  {% endfor %}
  {% block content %}{% endblock %}
</section>

#flaskr/templates/auth/register.html

{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}Register{% endblock %}</h1>
{% endblock %}

{% block content %}
  <form method="post">
    <label for="username">Username</label>
    <input name="username" id="username" required>
    <label for="password">Password</label>
    <input type="password" name="password" id="password" required>
    <input type="submit" value="Register">
  </form>
{% endblock %}

#flaskr/templates/auth/login.html

{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}Log In{% endblock %}</h1>
{% endblock %}

{% block content %}
  <form method="post">
    <label for="username">Username</label>
    <input name="username" id="username" required>
    <label for="password">Password</label>
    <input type="password" name="password" id="password" required>
    <input type="submit" value="Log In">
  </form>
{% endblock %}

#flaskr/static/style.css
html { font-family: sans-serif; background: #eee; padding: 1rem; }
body { max-width: 960px; margin: 0 auto; background: white; }
h1 { font-family: serif; color: #377ba8; margin: 1rem 0; }
a { color: #377ba8; }
hr { border: none; border-top: 1px solid lightgray; }
nav { background: lightgray; display: flex; align-items: center; padding: 0 0.5rem; }
nav h1 { flex: auto; margin: 0; }
nav h1 a { text-decoration: none; padding: 0.25rem 0.5rem; }
nav ul  { display: flex; list-style: none; margin: 0; padding: 0; }
nav ul li a, nav ul li span, header .action { display: block; padding: 0.5rem; }
.content { padding: 0 1rem 1rem; }
.content > header { border-bottom: 1px solid lightgray; display: flex; align-items: flex-end; }
.content > header h1 { flex: auto; margin: 1rem 0 0.25rem 0; }
.flash { margin: 1em 0; padding: 1em; background: #cae6f6; border: 1px solid #377ba8; }
.post > header { display: flex; align-items: flex-end; font-size: 0.85em; }
.post > header > div:first-of-type { flex: auto; }
.post > header h1 { font-size: 1.5em; margin-bottom: 0; }
.post .about { color: slategray; font-style: italic; }
.post .body { white-space: pre-line; }
.content:last-child { margin-bottom: 0; }
.content form { margin: 1em 0; display: flex; flex-direction: column; }
.content label { font-weight: bold; margin-bottom: 0.5em; }
.content input, .content textarea { margin-bottom: 1em; }
.content textarea { min-height: 12em; resize: vertical; }
input.danger { color: #cc2f2e; }
input[type=submit] { align-self: start; min-width: 10em; }

#test Application 
http://127.0.0.1:5000/auth/register


##Flask - Tutorial - Blog Blueprint

#the blog blueprint does not have a url_prefix. 
#So the index view will be at /, the create view at /create, and so on. 

#flaskr/blog.py

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)    
    
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
   
#Update to Import and register the blueprint 
#flaskr/__init__.py

def create_app():
    app = ...
    # existing code omitted

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app


#flaskr/templates/blog/index.html

{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}Posts{% endblock %}</h1>
  {% if g.user %}
    <a class="action" href="{{ url_for('blog.create') }}">New</a>
  {% endif %}
{% endblock %}

{% block content %}
  {% for post in posts %}
    <article class="post">
      <header>
        <div>
          <h1>{{ post['title'] }}</h1>
          <div class="about">by {{ post['username'] }} on {{ post['created'].strftime('%Y-%m-%d') }}</div>
        </div>
        {% if g.user['id'] == post['author_id'] %}
          <a class="action" href="{{ url_for('blog.update', id=post['id']) }}">Edit</a>
        {% endif %}
      </header>
      <p class="body">{{ post['body'] }}</p>
    </article>
    {% if not loop.last %}
      <hr>
    {% endif %}
  {% endfor %}
{% endblock %}

#flaskr/templates/blog/create.html

{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}New Post{% endblock %}</h1>
{% endblock %}

{% block content %}
  <form method="post">
    <label for="title">Title</label>
    <input name="title" id="title" value="{{ request.form['title'] }}" required>
    <label for="body">Body</label>
    <textarea name="body" id="body">{{ request.form['body'] }}</textarea>
    <input type="submit" value="Save">
  </form>
{% endblock %}


#flaskr/templates/blog/update.html

{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}Edit "{{ post['title'] }}"{% endblock %}</h1>
{% endblock %}

{% block content %}
  <form method="post">
    <label for="title">Title</label>
    <input name="title" id="title"
      value="{{ request.form['title'] or post['title'] }}" required>
    <label for="body">Body</label>
    <textarea name="body" id="body">{{ request.form['body'] or post['body'] }}</textarea>
    <input type="submit" value="Save">
  </form>
  <hr>
  <form action="{{ url_for('blog.delete', id=post['id']) }}" method="post">
    <input class="danger" type="submit" value="Delete" onclick="return confirm('Are you sure?');">
  </form>
{% endblock %}

##Flask - Tutorial - Make the Project Installable
#setup.py

from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)

#MANIFEST.in
#This tells Python to copy everything in the static and templates directories, 
#and the schema.sql file, but to exclude all bytecode files
include flaskr/schema.sql
graft flaskr/static
graft flaskr/templates
global-exclude *.pyc

.

#Install the Project
$ pip install -e .

$ pip list

Package        Version   Location
-------------- --------- ----------------------------------
click          6.7
Flask          1.0
flaskr         1.0.0     /home/user/Projects/flask-tutorial
itsdangerous   0.24
Jinja2         2.10
MarkupSafe     1.0
pip            9.0.3
setuptools     39.0.1
Werkzeug       0.14.1
wheel          0.30.0


##Flask - Tutorial - Test Coverage
$ pip install pytest coverage

#tests/data.sql

INSERT INTO user (username, password)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO post (title, body, author_id, created)
VALUES
  ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00');

#tests/conftest.py

import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

#Testing Factory
#tests/test_factory.py

from flaskr import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'

#Testing Database
#tests/test_db.py

import sqlite3

import pytest
from flaskr.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)

#The init-db command should call the init_db function and output a message.
def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called

#testing - Authentication
#tests/conftest.py

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)

#tests/test_auth.py

import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session

#testing - Blog
#tests/test_blog.py

import pytest
from flaskr.db import get_db


def test_index(client, auth):
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data

#A user must be logged in to access the create, update, and delete views. 
#The logged in user must be the author of the post to access update and delete, 
#otherwise a 403 Forbidden status is returned. 
#If a post with the given id doesn’t exist, update and delete should return 404 Not Found.

@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404

#The create and update views should render and return a 200 OK status 
#for a GET request. 
#When valid data is sent in a POST request, 
#create should insert the new post data into the database, 
#and update should modify the existing data. 
#Both pages should show an error message on invalid data.
tests/test_blog.py

def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title': 'created', 'body': ''})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': ''})

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'updated'


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post is None

#Running the Tests
#setup.cfg

[tool:pytest]
testpaths = tests

[coverage:run]
branch = True
source =
    flaskr

#To run the tests
$ pytest

========================= test session starts ==========================
platform linux -- Python 3.6.4, pytest-3.5.0, py-1.5.3, pluggy-0.6.0
rootdir: /home/user/Projects/flask-tutorial, inifile: setup.cfg
collected 23 items

tests/test_auth.py ........                                      [ 34%]
tests/test_blog.py ............                                  [ 86%]
tests/test_db.py ..                                              [ 95%]
tests/test_factory.py ..                                         [100%]

====================== 24 passed in 0.64 seconds =======================

$ coverage run -m pytest
$ coverage report

Name                 Stmts   Miss Branch BrPart  Cover
------------------------------------------------------
flaskr/__init__.py      21      0      2      0   100%
flaskr/auth.py          54      0     22      0   100%
flaskr/blog.py          54      0     16      0   100%
flaskr/db.py            24      0      4      0   100%
------------------------------------------------------
TOTAL                  153      0     44      0   100%


$ coverage html

This generates files in the htmlcov directory. Open htmlcov/index.html in your browser to see the report.

##Flask - Tutorial - Deploy to Production
$ pip install wheel

$ python setup.py bdist_wheel
#You can find the file in dist/flaskr-1.0.0-py3-none-any.whl. 

#Copy this file to another machine, 
#set up a new virtualenv, then install the file with pip.

$ pip install flaskr-1.0.0-py3-none-any.whl

#Then run 
$ export FLASK_APP=flaskr
$ flask init-db

#Configure the Secret Key
$ python -c 'import os; print(os.urandom(16))'
b'_5#y2L"F4Q8z\n\xec]/'

#Create the config.py file in the instance folder, 
#which the factory will read from if it exists. 
#Copy the generated value into it.
#venv/var/flaskr-instance/config.py

SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

#Run with a Production Server
$ pip install waitress

$ waitress-serve --call 'flaskr:create_app'

#Serving on http://0.0.0.0:8080




##Flask - Templates

#autoescaping is enabled for all templates ending in .html, .htm, .xml as well as .xhtml when using render_template().

#autoescaping is enabled for all strings when using render_template_string().

#a template has the ability to opt in/out autoescaping with the {% autoescape %} tag.

#The following global variables are available within Jinja2 templates by default:
config
    The current configuration object (flask.config)
request
    The current request object (flask.request). 
session
    The current session object (flask.session). 
g
    The request-bound object for global variables (flask.g). 
url_for()
    The flask.url_for() function.
get_flashed_messages()
    The flask.get_flashed_messages() function.

#Importing any template like below to access above 
{% from '_helpers.html' import my_macro with context %}

#Standard Filters

tojson()
    This function converts the given object into JSON representation. 
    This is for example very helpful if you try to generate JavaScript on the fly.
    <script type=text/javascript>
        doSomethingWith({{ user.username|tojson }});
    </script>
    It is also safe to use the output of |tojson in a single-quoted HTML attribute:
    <button onclick='doSomethingWith({{ user.username|tojson }})'>
        Click me
    </button>

#Controlling Autoescaping
#There are three ways to accomplish that:
1.In the Python code, wrap the HTML string in a Markup object before passing it to the template. This is in general the recommended way.
2.Inside the template, use the |safe filter to explicitly mark a string as safe HTML ({{ myvariable|safe }})
3.Temporarily disable the autoescape system altogether.

#To disable the autoescape system in templates
{% autoescape false %}
    <p>autoescaping is disabled here
    <p>{{ will_not_be_escaped }}
{% endautoescape %}

#Registering Filters
@app.template_filter('reverse')
def reverse_filter(s):
    return s[::-1]

#or 
def reverse_filter(s):
    return s[::-1]
app.jinja_env.filters['reverse'] = reverse_filter

#Usage 
{% for x in mylist | reverse %}
{% endfor %}



#Context Processors
#To inject new variables automatically into the context of a template, 
@app.context_processor
def inject_user():
    return dict(user=g.user)

#a context processor can also make functions available to templates 
@app.context_processor
def utility_processor():
    def format_price(amount, currency=u'€'):
        return u'{0:.2f}{1}'.format(amount, currency)
    return dict(format_price=format_price)

#Usage 
{{ format_price(0.33) }}

##Flask - Templates - Details 
{% ... %} for Statements, any python statement 
{{ ... }} for Expressions to print to the template output
{# ... #} for Comments not included in the template output

#use a dot (.) to access
{{ foo.bar }}
{{ foo['bar'] }}

#trim_blocks, the first newline after a template tag is removed automatically
#lstrip_blocks option can also be set to strip tabs and spaces from the beginning of a line to the start of a block.

##Base Template
#base.html
<!DOCTYPE html>
<html lang="en">
<head>
    {% block head %}
    <link rel="stylesheet" href="style.css" />
    <title>{% block title %}{% endblock %} - My Webpage</title>
    {% endblock %}
</head>
<body>
    <div id="content">{% block content %}{% endblock %}</div>
    <div id="footer">
        {% block footer %}
        &copy; Copyright 2008 by <a href="http://domain.invalid/">you</a>.
        {% endblock %}
    </div>
</body>
</html>

#Child Template
{% extends "base.html" %}
{% block title %}Index{% endblock %}
{% block head %}
    {{ super() }}
    <style type="text/css">
        .important { color: #336699; }
    </style>
{% endblock %}
{% block content %}
    <h1>Index</h1>
    <p class="important">
      Welcome to my awesome homepage.
    </p>
{% endblock %}

#to print a block multiple times,use the special self variable 
#and call the block with that name:

<title>{% block title %}{% endblock %}</title>
<h1>{{ self.title() }}</h1>
{% block body %}{% endblock %}

#to render the contents of the parent block by calling super
{% block sidebar %}
    <h3>Table Of Contents</h3>
    ...
    {{ super() }}
{% endblock %}

#Jinja2 allows you to put the name of the block after the end tag 
{% block sidebar %}
    {% block inner_sidebar %}
        ...
    {% endblock inner_sidebar %}
{% endblock sidebar %}

#Blocks can be nested for more complex layouts. 
#However, per default blocks may not access variables from outer scopes:
#This example would output empty <li> 
{% for item in seq %}
    <li>{% block loop_item %}{{ item }}{% endblock %}</li>
{% endfor %}

#So, explicitly specify that variables are available in a block 
#by setting the block to 'scoped' by adding the scoped modifier to a block declaration:
{% for item in seq %}
    <li>{% block loop_item scoped %}{{ item }}{% endblock %}</li>
{% endfor %}

##Template Objects
#If a template object was passed in the template context, 
#you can extend from that object as well
{% extends layout_template %}



##For
<h1>Members</h1>
<ul>
{% for user in users %}
  <li>{{ user.username|e }}</li>
{% endfor %}
</ul>

#or 
<dl>
{% for key, value in my_dict.items() %}
    <dt>{{ key|e }}</dt>
    <dd>{{ value|e }}</dd>
{% endfor %}
</dl>

#Inside of a for-loop block, you can access some special variables:
loop.index
	The current iteration of the loop. (1 indexed)
loop.index0
	The current iteration of the loop. (0 indexed)
loop.revindex
	The number of iterations from the end of the loop (1 indexed)
loop.revindex0
	The number of iterations from the end of the loop (0 indexed)
loop.first
	True if first iteration.
loop.last
	True if last iteration.
loop.length
	The number of items in the sequence.
loop.cycle
	A helper function to cycle between a list of sequences. 
loop.depth
	Indicates how deep in a recursive loop the rendering currently is. 
    Starts at level 1
loop.depth0
	Indicates how deep in a recursive loop the rendering currently
    is. Starts at level 0
loop.previtem
	The item from the previous iteration of the loop. 
    Undefined during the first iteration.
loop.nextitem
	The item from the following iteration of the loop. 
    Undefined during the last iteration.
loop.changed(*val)
	True if previously called with a different value (or not called at all).

#Within a for-loop, it’s possible to cycle among a list of strings/variables 
{% for row in rows %}
    <li class="{{ loop.cycle('odd', 'even') }}">{{ row }}</li>
{% endfor %}

#Unlike in Python, it’s not possible to break or continue in a loop. 
#You can, filter the sequence during iteration, which allows to skip items. 
{% for user in users if not user.hidden %}
    <li>{{ user.username|e }}</li>
{% endfor %}

#If no iteration took place because the sequence was empty 
#render a default block by using else:
<ul>
{% for user in users %}
    <li>{{ user.username|e }}</li>
{% else %}
    <li><em>no users found</em></li>
{% endfor %}
</ul>

#For loops recursively
# This is useful with recursive data such as sitemaps or RDFa. 

#The loop variable always refers to the closest (innermost) loop. 
#or rebind the variable loop  by writing {% set outer_loop = loop %} 
#after the loop that we want to use recursively. 
#Then, we can call it using {{ outer_loop(…) }}

<ul class="sitemap">
{%- for item in sitemap recursive %}
    <li><a href="{{ item.href|e }}">{{ item.title }}</a>
    {%- if item.children -%}
        <ul class="submenu">{{ loop(item.children) }}</ul>
    {%- endif %}</li>
{%- endfor %}
</ul>


#To check whether some value has changed since the last iteration 
#or will change in the next iteration, use previtem and nextitem:
{% for value in values %}
    {% if loop.previtem is defined and value > loop.previtem %}
        The value just increased!
    {% endif %}
    {{ value }}
    {% if loop.nextitem is defined and loop.nextitem > value %}
        The value will increase even more!
    {% endif %}
{% endfor %}

#OR whether the value changed at all, using changed is even easier:
{% for entry in entries %}
    {% if loop.changed(entry.category) %}
        <h2>{{ entry.category }}</h2>
    {% endif %}
    <p>{{ entry.message }}</p>
{% endfor %}



##If
#The if statement in Jinja is comparable with the Python if statement. 

{% if users %}
<ul>
{% for user in users %}
    <li>{{ user.username|e }}</li>
{% endfor %}
</ul>
{% endif %}

#For multiple branches
{% if kenny.sick %}
    Kenny is sick.
{% elif kenny.dead %}
    You killed Kenny!  You bastard!!!
{% else %}
    Kenny looks okay --- so far
{% endif %}


##Macros
#Macros are comparable with functions in regular programming languages. 
{% macro input(name, value='', type='text', size=20) -%}
    <input type="{{ type }}" name="{{ name }}" value="{{
        value|e }}" size="{{ size }}">
{%- endmacro %}

#If the macro was defined in a different template, import it first.
#If a macro name starts with an underscore, it’s not exported and can’t be imported.

#The macro can then be called like a function in the namespace:
<p>{{ input('username') }}</p>
<p>{{ input('password', type='password') }}</p>


#Inside macros, you have access to three special variables:
varargs
    If more positional arguments are passed to the macro 
    than accepted by the macro, 
    they end up in the special varargs variable as a list of values.
kwargs
    Like varargs but for keyword arguments. 
    All unconsumed keyword arguments are stored in this special variable.
caller
    If the macro was called from a call tag, 
    the caller is stored in this variable as a callable macro.

#The following attributes are available on a macro object:
name
    The name of the macro. {{ input.name }} will print input.
arguments
    A tuple of the names of arguments the macro accepts.
defaults
    A tuple of default values.
catch_kwargs
    This is true if the macro accepts extra keyword arguments 
    (i.e.: accesses the special kwargs variable).
catch_varargs
    This is true if the macro accepts extra positional arguments 
    (i.e.: accesses the special varargs variable).
caller
    This is true if the macro accesses the special caller variable 
    and may be called from a call tag.

#To pass a macro to another macro. 
{% macro render_dialog(title, class='dialog') -%}
    <div class="{{ class }}">
        <h2>{{ title }}</h2>
        <div class="contents">
            {{ caller() }}  #comes from below 
        </div>
    </div>
{%- endmacro %}

{% call render_dialog('Hello World') %}
    This is a simple dialog rendered by using a macro and
    a call block.
{% endcall %}

#To pass arguments back to the call block
{% macro dump_users(users) -%}
    <ul>
    {%- for user in users %}
        <li><p>{{ user.username|e }}</p>{{ caller(user) }}</li>
    {%- endfor %}
    </ul>
{%- endmacro %}

{% call(user) dump_users(list_of_user) %}
    <dl>
        <dl>Realname</dl>
        <dd>{{ user.realname|e }}</dd>
        <dl>Description</dl>
        <dd>{{ user.description }}</dd>
    </dl>
{% endcall %}

##Filters
#Use like below or with | for infline 
{% filter upper %}
    This text becomes uppercase
{% endfilter %}


##Assignments
#Assignments at top level (outside of blocks, macros or loops) 
#are exported from the template like top level macros 
#and can be imported by other templates.

{% set navigation = [('index.html', 'Index'), ('about.html', 'About')] %}
{% set key, value = call_something() %}

#it is not possible to set variables inside a block 
#and have them show up outside of it. 
#This also applies to loops. 
#The only exception to that rule are if statements which do not introduce a scope.

#As a result the following template is not going to do what you might expect:
{% set iterated = false %}
{% for item in seq %}
    {{ item }}
    {% set iterated = true %}
{% endfor %}
{% if not iterated %} did not iterate {% endif %}

#It is not possible with Jinja syntax to do this. 
#Instead use alternative constructs like the loop else block 
#or the special loop variable:
{% for item in seq %}
    {{ item }}
{% else %}
    did not iterate
{% endfor %}

#OR, more complex use cases can be handled using namespace objects 
#which allow propagating of changes across scopes:
{% set ns = namespace(found=false) %}
{% for item in items %}
    {% if item.check_something() %}
        {% set ns.found = true %}
    {% endif %}
    * {{ item.title }}
{% endfor %}
Found item having something: {{ ns.found }}

##Block Assignments
{% set navigation %}
    <li><a href="/">Index</a>
    <li><a href="/downloads">Downloads</a>
{% endset %}

#the block assignment supports filters.
{% set reply | wordwrap %}
    You wrote:
    {{ message }}
{% endset %}


##Include
#The include statement is useful to include a template 
#and return the rendered contents of that file into the current namespace:

#Included templates have access to the variables of the active context by default.
{% include 'header.html' %}
    Body
{% include 'footer.html' %}

#you can mark an include with ignore missing; 
#in which case Jinja will ignore the statement 
#if the template to be included does not exist. 

#When combined with with or without context, 
#it must be placed before the context visibility statement. 
{% include "sidebar.html" ignore missing %}
{% include "sidebar.html" ignore missing with context %}
{% include "sidebar.html" ignore missing without context %}

#You can also provide a list of templates that are checked for existence before inclusion. 
#The first template that exists will be included. 
#If ignore missing is given, it will fall back to rendering nothing if none of the templates exist, 
#otherwise it will raise an exception.
{% include ['page_detailed.html', 'page.html'] %}
{% include ['special_sidebar.html', 'sidebar.html'] ignore missing %}



##Import
#For  importing macros and top level variables 
#Macros and variables starting with one or more underscores are private and cannot be imported.

#forms.html
{% macro input(name, value='', type='text') -%}
    <input type="{{ type }}" value="{{ value|e }}" name="{{ name }}">
{%- endmacro %}

{%- macro textarea(name, value='', rows=10, cols=40) -%}
    <textarea name="{{ name }}" rows="{{ rows }}" cols="{{ cols
        }}">{{ value|e }}</textarea>
{%- endmacro %}

#Then use as 
{% import 'forms.html' as forms %}
<dl>
    <dt>Username</dt>
    <dd>{{ forms.input('username') }}</dd>
    <dt>Password</dt>
    <dd>{{ forms.input('password', type='password') }}</dd>
</dl>
<p>{{ forms.textarea('comment') }}</p>

#OR 
{% from 'forms.html' import input as input_field, textarea %}
<dl>
    <dt>Username</dt>
    <dd>{{ input_field('username') }}</dd>
    <dt>Password</dt>
    <dd>{{ input_field('password', type='password') }}</dd>
</dl>
<p>{{ textarea('comment') }}</p>


##Import Context Behavior
#By default, included templates are passed the current context 
#and imported templates are not. 

#or use below to get the context 
{% from 'forms.html' import input with context %}
{% include 'header.html' without context %}

#eg render_box.html is able to access box 
{% for box in boxes %}
    {% include "render_box.html" %}
{% endfor %}



##Literals
"Hello World"
'Hello'
42 , 42.23
['list', 'of', 'objects']:
    <ul>
    {% for href, caption in [('index.html', 'Index'), ('about.html', 'About'),
                             ('downloads.html', 'Downloads')] %}
        <li><a href="{{ href }}">{{ caption }}</a></li>
    {% endfor %}
    </ul>

('tuple', 'of', 'values'):
{'dict': 'of', 'key': 'and', 'value': 'pairs'}:
true , false
    Note these are lowercase 

##Math
+
    {{ 1 + 1 }} is 2.
-
    {{ 3 - 2 }} is 1.
/
    {{ 1 / 2 }} is {{ 0.5 }}.
//
    {{ 20 // 7 }} is 2.
%
{{ 11 % 7 }} is 4.
*
    {{ 2 * 2 }} would return 4. 
    {{ '=' * 80 }} would print a bar of 80 equal signs.
**
    {{ 2**3 }} would return 8.

==
    Compares two objects for equality.
!=
    Compares two objects for inequality.
>
    true if the left hand side is greater than the right hand side.
>=
    true if the left hand side is greater or equal to the right hand side.
<
    true if the left hand side is lower than the right hand side.
<=
    true if the left hand side is lower or equal to the right hand side.

and
    Return true if the left and the right operand are true.
or
    Return true if the left or the right operand are true.
not
    negate a statement (see below).
(expr)
    group an expression.
in
    Perform a sequence / mapping containment test. 
    Returns true if the left operand is contained in the right. 
    {{ 1 in [1, 2, 3] }} would, for example, return true.
is
    Performs a test.
|
    Applies a filter.
~
    Converts all operands into strings and concatenates them.
    {{ "Hello " ~ name ~ "!" }} would return  Hello John!.
()
    Call a callable: {{ post.render() }}. 
    {{ post.render(user, full=true) }}.
. , []
    Get an attribute of an object. 
<do something> if <something is true> else <do something else>
    if expressions. These are useful in some situations. 
    {% extends layout_template if layout_template is defined else 'master.html' %}
    {{ "[{}]".format(page.title) if page.title }}

Python Methods
    {{ page.title.capitalize() }}
    {{ f.bar() }}


##Expression Statement
{% import jinja2.ext.do  %}
    The 'do' aka expression-statement extension 
    adds a simple do tag to the template engine 
    that works like a variable expression but ignores the return value.
{% import jinja2.ext.loopcontrols %}
    This extension adds support for break and continue in loops. 
    After enabling, Jinja2 provides those two keywords which work exactly like 
    in Python.
{% import jinja2.ext.with_  %}
    This extension is now built-in and no longer does anything.


##Flask - Templates - functions 
range([start, ]stop[, step])
    Return a list containing an arithmetic progression of integers
lipsum(n=5, html=True, min=20, max=100)
    Generates some lorem ipsum for the template. 
    By default, five paragraphs of HTML are generated with each paragraph between 20 and 100 words. 
    If html is False, regular text is returned. 
dict(**items)
    A convenient alternative to dict literals. {'foo': 'bar'} is the same as dict(foo='bar').
class cycler(*items)
    The cycler allows you to cycle among values similar to how loop.cycle works.
    {% set row_class = cycler('odd', 'even') %}
   {{ row_class.next() }}
    A cycler has the following attributes and methods:
    reset()
        Resets the cycle to the first item.
    next()
        Goes one item ahead and returns the then-current item.
    current
        Returns the current item.
lipsum(n=5, html=True, min=20, max=100)
    Generates some lorem ipsum for the template.        
        

##Flask - Templates - tests 
#note first argument comes from LHS of is ie LHS is TEST => TEST(LHS) 
#any more arg, pass as function syntax 
callable(object)
    Return whether the object is callable (i.e., some kind of function). 
    Note that classes are callable, as are instances with a __call__() method.
defined(value)
    Return true if the variable is defined
divisibleby(value, num)
    Check if a variable is divisible by a number.
eq(a, b)
    Aliases:	==, equalto
escaped(value)
    Check if the value is escaped.
even(value)
    Return true if the variable is even.
ge(a, b)
    Aliases:	>=
gt(a, b)
    Aliases:	>, greaterthan
in(value, seq)
    Check if value is in seq.
    New in version 2.10.
iterable(value)
    Check if it's possible to iterate over an object.
le(a, b)
    Aliases:	<=
lower(value)
    Return true if the variable is lowercased.
lt(a, b)
    Aliases:	<, lessthan
mapping(value)
    Return true if the object is a mapping (dict etc.).
    New in version 2.6.
ne(a, b)
    Aliases:	!=
none(value)
    Return true if the variable is none.
number(value)
    Return true if the variable is a number.
odd(value)
    Return true if the variable is odd.
sameas(value, other)
    Check if an object points to the same memory address than another object:
sequence(value)
    Return true if the variable is a sequence. Sequences are variables that are iterable.
string(value)
    Return true if the object is a string.
undefined(value)
    Like defined() but the other way round.
upper(value)
    Return true if the variable is uppercased.
    

##Flask - Templates - filters  
abs(number)
    Return the absolute value of the argument.
attr(obj, name)
    Get an attribute of an object. foo|attr("bar") works like foo.bar 
    just that always an attribute is returned and items are not looked up.
batch(value, linecount, fill_with=None)
    A filter that batches items. 
    It works pretty much like slice just the other way round. 
    It returns a list of lists with the given number of items. 
    If you provide a second parameter this is used to fill up missing items. 
    <table>
    {%- for row in items|batch(3, '&nbsp;') %}
      <tr>
      {%- for column in row %}
        <td>{{ column }}</td>
      {%- endfor %}
      </tr>
    {%- endfor %}
    </table>
capitalize(s)
    Capitalize a value. The first character will be uppercase, all others lowercase.
center(value, width=80)
    Centers the value in a field of a given width.
default(value, default_value=u'', boolean=False)
    If the value is undefined it will return the passed default value, otherwise the value of the variable:
    {{ my_variable|default('my_variable is not defined') }}
    This will output the value of my_variable if the variable was defined, otherwise 'my_variable is not defined'. If you want to use default with variables that evaluate to false you have to set the second parameter to true:
    {{ ''|default('the string was empty', true) }}
    Aliases:	d
dictsort(value, case_sensitive=False, by='key', reverse=False)
    Sort a dict and yield (key, value) pairs. Because python dicts are unsorted you may want to use this function to order them by either key or value:
    {% for item in mydict|dictsort %}
        sort the dict by key, case insensitive
    {% for item in mydict|dictsort(reverse=true) %}
        sort the dict by key, case insensitive, reverse order
    {% for item in mydict|dictsort(true) %}
        sort the dict by key, case sensitive
    {% for item in mydict|dictsort(false, 'value') %}
        sort the dict by value, case insensitive
escape(s)
    Convert the characters &, <, >, ', and ” in string s to HTML-safe sequences. Use this if you need to display text that might contain such characters in HTML. Marks return value as markup string.
    Aliases:	e
filesizeformat(value, binary=False)
    Format the value like a 'human-readable' file size (i.e. 13 kB, 4.1 MB, 102 Bytes, etc). Per default decimal prefixes are used (Mega, Giga, etc.), if the second parameter is set to True the binary prefixes are used (Mebi, Gibi).
first(seq)
    Return the first item of a sequence.
float(value, default=0.0)
    Convert the value into a floating point number. If the conversion doesn't work it will return 0.0. You can override this default using the first parameter.
forceescape(value)
    Enforce HTML escaping. This will probably double escape variables.
format(value, *args, **kwargs)
    Apply python string formatting on an object:
    {{ "%s - %s"|format("Hello?", "Foo!") }}
        -> Hello? - Foo!
groupby(value, attribute)
    Group a sequence of objects by a common attribute.
    If you for example have a list of dicts or objects that represent persons with gender, first_name and last_name attributes and you want to group all users by genders you can do something like the following snippet:
    <ul>
    {% for group in persons|groupby('gender') %}
        <li>{{ group.grouper }}<ul>
        {% for person in group.list %}
            <li>{{ person.first_name }} {{ person.last_name }}</li>
        {% endfor %}</ul></li>
    {% endfor %}
    </ul>
    Additionally it's possible to use tuple unpacking for the grouper and list:
    <ul>
    {% for grouper, list in persons|groupby('gender') %}
        ...
    {% endfor %}
    </ul>
    As you can see the item we're grouping by is stored in the grouper attribute and the list contains all the objects that have this grouper in common.
    Changed in version 2.6: It's now possible to use dotted notation to group by the child attribute of another attribute.
indent(s, width=4, first=False, blank=False, indentfirst=None)
    Return a copy of the string with each line indented by 4 spaces. The first line and blank lines are not indented by default.
    Parameters:	
        width – Number of spaces to indent by.
        first – Don't skip indenting the first line.
        blank – Don't skip indenting empty lines.
    Changed in version 2.10: Blank lines are not indented by default.
    Rename the indentfirst argument to first.
int(value, default=0, base=10)
    Convert the value into an integer. If the conversion doesn't work it will return 0. You can override this default using the first parameter. You can also override the default base (10) in the second parameter, which handles input with prefixes such as 0b, 0o and 0x for bases 2, 8 and 16 respectively. The base is ignored for decimal numbers and non-string values.
join(value, d=u'', attribute=None)
    Return a string which is the concatenation of the strings in the sequence. The separator between elements is an empty string per default, you can define it with the optional parameter:
    {{ [1, 2, 3]|join('|') }}
        -> 1|2|3
    {{ [1, 2, 3]|join }}
        -> 123
    It is also possible to join certain attributes of an object:
    {{ users|join(', ', attribute='username') }}
    New in version 2.6: The attribute parameter was added.
last(seq)
    Return the last item of a sequence.
length(object)
    Return the number of items of a sequence or mapping.
    Aliases:	count
list(value)
    Convert the value into a list. If it was a string the returned list will be a list of characters.
lower(s)
    Convert a value to lowercase.
map()
    Applies a filter on a sequence of objects or looks up an attribute. 
    This is useful when dealing with lists of objects but you are really only interested in a certain value of it.
    The basic usage is mapping on an attribute. 
    Imagine you have a list of users but you are only interested in a list of usernames:
    Users on this page: {{ users|map(attribute='username')|join(', ') }}
    Alternatively you can let it invoke a filter by passing the name of the filter 
    and the arguments afterwards. A good example would be applying a text conversion filter on a sequence:
    Users on this page: {{ titles|map('lower')|join(', ') }}
max(value, case_sensitive=False, attribute=None)
    Return the largest item from the sequence.
    {{ [1, 2, 3]|max }}
        -> 3
    Parameters:	
        case_sensitive – Treat upper and lower case strings as distinct.
        attribute – Get the object with the max value of this attribute.
min(value, case_sensitive=False, attribute=None)
    Return the smallest item from the sequence.
    {{ [1, 2, 3]|min }}
        -> 1
    Parameters:	
        case_sensitive – Treat upper and lower case strings as distinct.
        attribute – Get the object with the max value of this attribute.
pprint(value, verbose=False)
    Pretty print a variable. Useful for debugging.
    With Jinja 1.2 onwards you can pass it a parameter. If this parameter is truthy the output will be more verbose (this requires pretty)
random(seq)
    Return a random item from the sequence.
reject()
    Filters a sequence of objects by applying a test to each object, and rejecting the objects with the test succeeding.
    If no test is specified, each object will be evaluated as a boolean.
    Example usage:
    {{ numbers|reject("odd") }}
    New in version 2.7.
rejectattr()
    Filters a sequence of objects by applying a test to the specified attribute of each object, and rejecting the objects with the test succeeding.
    If no test is specified, the attribute's value will be evaluated as a boolean.
    {{ users|rejectattr("is_active") }}
    {{ users|rejectattr("email", "none") }}
    New in version 2.7.
replace(s, old, new, count=None)
    Return a copy of the value with all occurrences of a substring replaced with a new one. The first argument is the substring that should be replaced, the second is the replacement string. If the optional third argument count is given, only the first count occurrences are replaced:
    {{ "Hello World"|replace("Hello", "Goodbye") }}
        -> Goodbye World
    {{ "aaaaargh"|replace("a", "d'oh, ", 2) }}
        -> d'oh, d'oh, aaargh
reverse(value)
    Reverse the object or return an iterator that iterates over it the other way round.
round(value, precision=0, method='common')
    Round the number to a given precision. The first parameter specifies the precision (default is 0), the second the rounding method:
        'common' rounds either up or down
        'ceil' always rounds up
        'floor' always rounds down
    If you don't specify a method 'common' is used.
    {{ 42.55|round }}
        -> 43.0
    {{ 42.55|round(1, 'floor') }}
        -> 42.5
    Note that even if rounded to 0 precision, a float is returned. If you need a real integer, pipe it through int:
    {{ 42.55|round|int }}
        -> 43
safe(value)
    Mark the value as safe which means that in an environment with automatic escaping enabled this variable will not be escaped.
select()
    Filters a sequence of objects by applying a test to each object, and only selecting the objects with the test succeeding.
    If no test is specified, each object will be evaluated as a boolean.
    Example usage:
    {{ numbers|select("odd") }}
    {{ numbers|select("odd") }}
    {{ numbers|select("divisibleby", 3) }}
    {{ numbers|select("lessthan", 42) }}
    {{ strings|select("equalto", "mystring") }}
    
selectattr()
    Filters a sequence of objects by applying a test to the specified attribute of each object, and only selecting the objects with the test succeeding.
    If no test is specified, the attribute's value will be evaluated as a boolean.
    Example usage:
    {{ users|selectattr("is_active") }}
    {{ users|selectattr("email", "none") }}
    New in version 2.7.
slice(value, slices, fill_with=None)
    Slice an iterator and return a list of lists containing those items. Useful if you want to create a div containing three ul tags that represent columns:
    <div class="columwrapper">
      {%- for column in items|slice(3) %}
        <ul class="column-{{ loop.index }}">
        {%- for item in column %}
          <li>{{ item }}</li>
        {%- endfor %}
        </ul>
      {%- endfor %}
    </div>
    If you pass it a second argument it's used to fill missing values on the last iteration.
sort(value, reverse=False, case_sensitive=False, attribute=None)
    Sort an iterable. Per default it sorts ascending, if you pass it true as first argument it will reverse the sorting.
    If the iterable is made of strings the third parameter can be used to control the case sensitiveness of the comparison which is disabled by default.
    {% for item in iterable|sort %}
        ...
    {% endfor %}
    It is also possible to sort by an attribute (for example to sort by the date of an object) by specifying the attribute parameter:
    {% for item in iterable|sort(attribute='date') %}
        ...
    {% endfor %}
    Changed in version 2.6: The attribute parameter was added.
string(object)
    Make a string unicode if it isn't already. That way a markup string is not converted back to unicode.
striptags(value)
    Strip SGML/XML tags and replace adjacent whitespace by one space.
sum(iterable, attribute=None, start=0)
    Returns the sum of a sequence of numbers plus the value of parameter 'start' (which defaults to 0). When the sequence is empty it returns start.
    It is also possible to sum up only certain attributes:
    Total: {{ items|sum(attribute='price') }}
    Changed in version 2.6: The attribute parameter was added to allow suming up over attributes. Also the start parameter was moved on to the right.
title(s)
    Return a titlecased version of the value. I.e. words will start with uppercase letters, all remaining characters are lowercase.
tojson(value, indent=None)
    Dumps a structure to JSON so that it's safe to use in <script> tags. It accepts the same arguments and returns a JSON string. Note that this is available in templates through the |tojson filter which will also mark the result as safe. Due to how this function escapes certain characters this is safe even if used outside of <script> tags.
    The following characters are escaped in strings:
        <
        >
        &
        '
    This makes it safe to embed such strings in any place in HTML with the notable exception of double quoted attributes. In that case single quote your attributes or HTML escape it in addition.
    The indent parameter can be used to enable pretty printing. Set it to the number of spaces that the structures should be indented with.
    Note that this filter is for use in HTML contexts only.
    New in version 2.9.
trim(value)
    Strip leading and trailing whitespace.
truncate(s, length=255, killwords=False, end='...', leeway=None)
    Return a truncated copy of the string. The length is specified with the first parameter which defaults to 255. If the second parameter is true the filter will cut the text at length. Otherwise it will discard the last word. If the text was in fact truncated it will append an ellipsis sign ("..."). If you want a different ellipsis sign than "..." you can specify it using the third parameter. Strings that only exceed the length by the tolerance margin given in the fourth parameter will not be truncated.
    {{ "foo bar baz qux"|truncate(9) }}
        -> "foo..."
    {{ "foo bar baz qux"|truncate(9, True) }}
        -> "foo ba..."
    {{ "foo bar baz qux"|truncate(11) }}
        -> "foo bar baz qux"
    {{ "foo bar baz qux"|truncate(11, False, '...', 0) }}
        -> "foo bar..."
    The default leeway on newer Jinja2 versions is 5 and was 0 before but can be reconfigured globally.
unique(value, case_sensitive=False, attribute=None)
    Returns a list of unique items from the the given iterable.
    {{ ['foo', 'bar', 'foobar', 'FooBar']|unique }}
        -> ['foo', 'bar', 'foobar']
    The unique items are yielded in the same order as their first occurrence in the iterable passed to the filter.
    Parameters:	
        case_sensitive – Treat upper and lower case strings as distinct.
        attribute – Filter objects with unique values for this attribute.
upper(s)
    Convert a value to uppercase.
urlencode(value)
    Escape strings for use in URLs (uses UTF-8 encoding). It accepts both dictionaries and regular strings as well as pairwise iterables.
    New in version 2.7.
urlize(value, trim_url_limit=None, nofollow=False, target=None, rel=None)
    Converts URLs in plain text into clickable links.
    If you pass the filter an additional integer it will shorten the urls to that number. Also a third argument exists that makes the urls “nofollow”:
    {{ mytext|urlize(40, true) }}
        links are shortened to 40 chars and defined with rel="nofollow"
    If target is specified, the target attribute will be added to the <a> tag:
    {{ mytext|urlize(40, target='_blank') }}
    Changed in version 2.8+: The target parameter was added.
wordcount(s)
    Count the words in that string.
wordwrap(s, width=79, break_long_words=True, wrapstring=None)
    Return a copy of the string passed to the filter wrapped after 79 characters. You can override this default using the first parameter. If you set the second parameter to false Jinja will not split words apart if they are longer than width. By default, the newlines will be the default newlines for the environment, but this can be changed using the wrapstring keyword argument.
    New in version 2.7: Added support for the wrapstring parameter.
xmlattr(d, autospace=True)
    Create an SGML/XML attribute string based on the items in a dict. All values that are neither none nor undefined are automatically escaped:
    <ul{{ {'class': 'my_list', 'missing': none,
            'id': 'list-%d'|format(variable)}|xmlattr }}>
    ...
    </ul>
    Results in something like this:
    <ul class="my_list" id="list-42">
    ...
    </ul>
    As you can see it automatically prepends a space in front of the item if the filter returned something unless the second parameter is false.
    
    
##check advanced jinja2 
#https://www.webforefront.com/django/createreusablejinjatemplates.html
    
Jinja template with {% block %} tags
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{% block title%}Default title{% endblock title %}</title>
    <meta name="description" content="{% block metadescription%}{% endblock metadescription %}">
    <meta name="keywords" content="{% block metakeywords%}{% endblock metakeywords %}">
   
Jinja template with {% extends %} and {% block %} tag

{% if user %}{% extends "base.html" %}{% else %}{% extends "signup_base.html" %}{% endif %}
{% block title %}Coffeehouse home page{% endblock %} 

Jinja templates use of super() with three reusable templates

# base.html template 
<p>{% block breadcrumb %}Home{% endblock %}</p>

# index.html template
{% extends "base.html" %} 
{% block breadcrumb %}Main{% endblock %} 

# detail.html template
{% extends "index.html" %} 
{% block breadcrumb %} {{super()}} : Detail {% endblock %} 

By default, the {% include %} tag expects the name of a template. For example, {% include "footer.html" %} inserts the contents of the footer.html template in the position of the template where it's declared. The {% include %} tag also makes the underlying template aware of variables. This meas the footer.html template can have variable definitions (e.g.{{year}}) and if the calling template has these variable definitions, the {% include %} tag automatically substitutes these values.

In addition, it's possible to provide a list of templates as a fall-back mechanism. 
For example, {% include ['special_sidebar.html', 'sidebar.html'] ignore missing %} 
tells Jinja to first attempt to locate the special_sidebar.html template 
and if it isn't found to attempt to locate the sidebar.html template, 
if neither template is found the last argument ignore missing tells Jinja 
to render nothing. Note the ignore missing argument can also be used 
in individual statements (e.g. {% include "footer.html" ignore missing %}, 
as well as lists). In addition, if the ignore missing statement is not used 
and Jinja can't find a matching template declared in {% include %} Jinja 
raises an exception.

Jinja {% macro %} definition and use of {% import %}

# base.html template 
{% macro coffeestore(name, id='', address='', city='San Diego', state='CA', email=None) -%}
    <a id="{{id}}"></a>
    <h4>{{name}}</h4>
    <p>{{address}} {{city}},{{state}}</p>
    {% if email %}<p><a href='mailto:{{email}}'>{{email}}</a></p>{% endif %}
{%- endmacro %}

# index.html template calls inherited macro directly
{% extends "base.html" %} 
{{coffeestore('Downtown',1,'Horton Plaza','San Diego','CA','downtown@coffeehouse.com')}}

# detail.html template with no extends, uses {% import %} to access macro in base.html
{% import 'base.html' as base %}
{{base.coffeestore('Downtown',1,'Horton Plaza','San Diego','CA','downtown@coffeehouse.com')}}

# otherdetail.html template with no extends, uses {% from import %} to access macro in base.html
{% from 'base.html' import coffeestore as mycoffeestoremacro %}
{{mycoffeestoremacro('Downtown',1,'Horton Plaza','San Diego','CA','downtown@coffeehouse.com')}}


Jinja {% call %} and {% macro %} use

# macro definition
{% macro contentlist(adcolumn_width=3,contentcolumn_width=6) -%}
   <div class="col-md-{{adcolumn_width}}">
    Sidebar ads
   </div>
   <div class="col-md-{{contentcolumn_width}}">
      {{ caller() }}
   </div>
   <div class="col-md-{{adcolumn_width}}">
    Sidebar ads
   </div>
{%- endmacro %}

# macro call/invocation
{% call contentlist() %} 
  <ul>
    <li>This is my list</li> 
  </ul>
{% endcall %}

# rendering
<div class="col-md-3">
    Sidebar ads
</div>
<div class="col-md-6">
  <ul>
    <li>This is my list</li> 
  </ul>
</div>
<div class="col-md-3">
    Sidebar ads
</div>


A more advanced scenario of the {% call %} tag with a {% macro %} is for the caller() statement to use references, a process that's more natural to data that's recursive in nature (i.e. a macro over a macro). 

Jinja {% call %} and {% macro %} recursive calls

# macro definition
{% macro contentlist(itemlist,adcolumn_width=3,contentcolumn_width=6) -%}
   <div class="col-md-{{adcolumn_width}}">
    Sidebar ads
   </div>
   <div class="col-md-{{contentcolumn_width}}">
     {% for item in itemlist %}
      {{ caller(item) }}
     {% endfor %}
   </div>
   <div class="col-md-{{adcolumn_width}}">
    Sidebar ads
   </div>
{%- endmacro %}

# variable definition
{% set coffeestores=[{'id':0,'name':'Corporate','address':'624 Broadway','city':'San Diego','state':'CA',
'email':'corporate@coffeehouse.com'},{'id':1,'name':'Downtown','address':'Horton Plaza','city':'San Diego',
'state':'CA','email':'downtown@coffeehouse.com'},{'id':2,'name':'Uptown','address':'1240 University Ave',
'city':'San Diego','state':'CA','email':'uptown@coffeehouse.com'},{'id':3,'name':'Midtown',
'address':'784 W Washington St','city':'San Diego','state':'CA','email':'midtown@coffeehouse.com'}] %}

# macro call/invocation
{% call(item) contentlist(coffeestores) %} 
    <a id="{{item.id}}"></a>
    <h4>{{item.name}}</h4>
    <p>{{item.address}} {{item.city}},{{item.state}}</p>
    {% if item.email %}<p><a href='mailto:{{item.email}}'>{{item.email}}</a></p>{% endif %}
{% endcall %}

# rendering
<div class="col-md-3">
    Sidebar ads
</div>
<div class="col-md-6">       
    <a id="0"></a>
    <h4>Corporate</h4>
    <p>624 Broadway San Diego,CA</p>
    <p><a href="mailto:corporate@coffeehouse.com">corporate@coffeehouse.com</a></p>
       
    <a id="1"></a>
    <h4>Downtown</h4>
    <p>Horton Plaza San Diego,CA</p>
    <p><a href="mailto:downtown@coffeehouse.com">downtown@coffeehouse.com</a></p>
       
    <a id="2"></a>
    <h4>Uptown</h4>
    <p>1240 University Ave San Diego,CA</p>
    <p><a href="mailto:uptown@coffeehouse.com">uptown@coffeehouse.com</a></p>
       
    <a id="3"></a>
    <h4>Midtown</h4>
    <p>784 W Washington St San Diego,CA</p>
    <p><a href="mailto:midtown@coffeehouse.com">midtown@coffeehouse.com</a></p>
</div>
<div class="col-md-3">
    Sidebar ads
</div>

The {% set %} statement lets you define variables in the context of Jinja templates. 
It's useful when you need to create variables for values that aren't exposed 
by a Django view method or when a variable is tied to a heavyweight operation. 
The following is a sample statement of this statement 
{% set drinkwithtax=drink.cost*1.07 %}. 
The scope of a variable defined in a {% set %} statement is from its declaration 
until the end of the template.

The {% set %} statement can also define content blocks. 
For example, the statement 
{% set advertisement %}<div class'banner'><img src=.....></div>{% endset %}, 
creates the variable advertisement with the content enclosed between {% set %} 
and {% endset %} which can later be reused in other parts of a template 
(e.g. {{advertisement}}).

#Example 
The joiner function lets you join a series of disparate sections and join them 
with a given separator, which defaults to a comma-space (", "). 
A characteristic of the joiner function is that it returns the separator string 
every time it's called, except the first time to give the correct appearance 
in case sections are dependent on a condition. 

{% set slash_joiner = joiner("/ ") %}
User: {% if username %} {{ slash_joiner() }}
    {{username}}
{% endif %}
{% if alias %} {{ slash_joiner() }}
    {{alias}}
{% endif %}
{% if nickname %} {{ slash_joiner() }}
    {{nickname}}
{% endif %}

# Output

# If all variables are defined
User: username / alias / nickname

# If only nickname is defined
User: nickname

# If only username and alias is defined 
User: username / alias 
# Etc, the joiner function avoids any unnecessary preceding slash 
# because it doesn't print anything the first time its called

###Installation of marshmallow etc 
pip install marshmallow flask-sqlalchemy marshmallow-sqlalchemy flask-marshmallow Celery alembic 

#black requires python3.6 to run, but can reformat any python code 
pip install black

###Object serialization/deserialization using Marshmallow
#marshmallow is an ORM/ODM/framework-agnostic library for converting complex datatypes, 
#such as objects, to and from native Python datatypes.

from datetime import date
from marshmallow import Schema, fields, pprint

class ArtistSchema(Schema):
    name = fields.Str()

class AlbumSchema(Schema):
    title = fields.Str()
    release_date = fields.Date()
    artist = fields.Nested(ArtistSchema())

bowie = dict(name='David Bowie')
album = dict(artist=bowie, title='Hunky Dory', release_date=date(1971, 12, 17))

schema = AlbumSchema()
result = schema.dump(album)
#result is nested dict 
#{'title': 'Hunky Dory', 'release_date': '1971-12-17', 'artist': {'name': 'David Bowie'}}
>>> schema.load(result)
{'title': 'Hunky Dory', 'release_date': datetime.date(1971, 12, 17), 'artist': {'name': 'David Bowie'}}

pprint(result, indent=2)
# { 'artist': {'name': 'David Bowie'},
#   'release_date': '1971-12-17',
#   'title': 'Hunky Dory'}
result = schema.dumps(album)
>>> result
'{"title": "Hunky Dory", "release_date": "1971-12-17", "artist": {"name": "David Bowie"}}'
>>> schema.loads(result)
{'title': 'Hunky Dory', 'release_date': datetime.date(1971, 12, 17), 'artist': {'name': 'David Bowie'}}


##Reference 
class marshmallow.fields.Field(*, default=<marshmallow.missing>, 
        missing=<marshmallow.missing>, data_key=None, attribute=None, 
        validate=None, required=False, allow_none=None, 
        load_only=False, dump_only=False, error_messages=None, **metadata)
Raw(Field):
    Field that applies no formatting or validation
Nested(nested, *, default=missing_, exclude=tuple(), only=None, **kwargs):
    Allows you to nest a :class:`Schema <marshmallow.Schema>`
    inside a field.
        user = fields.Nested(UserSchema)
        user2 = fields.Nested('UserSchema')  # Equivalent to above
        collaborators = fields.Nested(UserSchema, many=True, only=('id',))
        parent = fields.Nested('self')
        
Pluck(Nested):
    Allows you to replace nested data with one of the data's fields.
        from marshmallow import Schema, fields
        class ArtistSchema(Schema):
            id = fields.Int()
            name = fields.Str()
        class AlbumSchema(Schema):
            artist = fields.Pluck(ArtistSchema, 'id')
        in_data = {'artist': 42}
        loaded = AlbumSchema().load(in_data) # => {'artist': {'id': 42}}
        dumped = AlbumSchema().dump(loaded)  # => {'artist': 42}

List(cls_or_instance, **kwargs)
    A list field, composed with another `Field` class or instance.
    numbers = fields.List(fields.Float())

Tuple(tuple_fields, *args, **kwargs)
    A tuple field, composed of a fixed number of other `Field` classes or
    instances
    row = Tuple((fields.String(), fields.Integer(), fields.Float()))
String(value, attr, obj, **kwargs):
    A string field.
UUID(value, attr, obj, **kwargs):
    A UUID field
Integer(*, strict=False, as_string=False **kwargs):
    An integer field.
Float(*, allow_nan=False, as_string=False, **kwargs):
    A double as an IEEE-754 double precision string.
Decimal(places=None, rounding=None, *, allow_nan=False, as_string=False, **kwargs):
    A field that (de)serializes to the Python ``decimal.Decimal`` type.
Boolean(*, truthy=None, falsy=None, **kwargs):
    A boolean field.
DateTime(format=None, **kwargs):
    A formatted datetime string.
    Example: ``'2014-12-22T03:12:58.019077+00:00'``
    format: Either ``"rfc"`` (for RFC822), ``"iso"`` (for ISO8601),
        or a date format string. If `None`, defaults to "iso".
NaiveDateTime(format=None, *, timezone=None, **kwargs):
    A formatted naive datetime string.
AwareDateTime(format=None, *, default_timezone=None, **kwargs):
    A formatted aware datetime string.
Time(Field):
    ISO8601-formatted time string.
Date(DateTime):
    ISO8601-formatted date string.
TimeDelta(precision=SECONDS, **kwargs):
    A field that (de)serializes a :class:`datetime.timedelta` object 
    precision: Influences how the integer is interpreted during
        (de)serialization. Must be 'days', 'seconds', 'microseconds',
        'milliseconds', 'minutes', 'hours' or 'weeks'.
Dict(keys=None, values=None, **kwargs):
Url(String):
    A validated URL field. Validation occurs during both serialization and
    deserialization.
Email(String):
    A validated email field. Validation occurs during both serialization and
    deserialization.
Method(erialize=None, deserialize=None, **kwargs):
    A field that takes the value returned by a `Schema` method.
    serialize: The name of the Schema method from which
        to retrieve the value. The method must take an argument ``obj``
        (in addition to self) that is the object to be serialized.
    deserialize: Optional name of the Schema method for deserializing
        a value The method must take a single argument ``value``, which is the
        value to deserialize.
Function(serialize=None, deserialize=None, **kwargs):
    A field that takes the value returned by a function.
    callable serialize
    callable deserialize
Constant(constant, **kwargs):
    A field that (de)serializes to a preset constant.
# Aliases
URL = Url
Str = String
Bool = Boolean
Int = Integer



##Declaring Schemas
import datetime as dt


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return "<User(name={self.name!r})>".format(self=self)

#Then corresponding Schema 
from marshmallow import Schema, fields


class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()

#OR 
from marshmallow import Schema, fields

UserSchema = Schema.from_dict(
    {"name": fields.Str(), "email": fields.Email(), "created_at": fields.DateTime()}
)

#Then Serializing Objects or dumping 
from marshmallow import pprint

user = User(name="Monty", email="monty@python.org")
schema = UserSchema()
result = schema.dump(user)
pprint(result)
# {"name": "Monty",
#  "email": "monty@python.org",
#  "created_at": "2014-08-17T14:54:16.049594+00:00"}

json_result = schema.dumps(user)
pprint(json_result)
# '{"name": "Monty", "email": "monty@python.org", "created_at": "2014-08-17T14:54:16.049594+00:00"}'

#OR Filtering Output
summary_schema = UserSchema(only=("name", "email"))
summary_schema.dump(user)
# {"name": "Monty Python", "email": "monty@python.org"}

#Then Deserializing Objects ie Loading

from pprint import pprint

user_data = {
    "created_at": "2014-08-11T05:26:03.869245",
    "email": "ken@yahoo.com",
    "name": "Ken",
}
schema = UserSchema()
result = schema.load(user_data)
pprint(result)
# {'name': 'Ken',
#  'email': 'ken@yahoo.com',
#  'created_at': datetime.datetime(2014, 8, 11, 5, 26, 3, 869245)},

#To deserialize to an object, use @post_load 
from marshmallow import Schema, fields, post_load


class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

user_data = {"name": "Ronnie", "email": "ronnie@stones.com"}
schema = UserSchema()
result = schema.load(user_data)
print(result)  # => <User(name='Ronnie')>


#Handling Collections of Objects
#Set many=True when dealing with iterable collections of objects.

user1 = User(name="Mick", email="mick@stones.com")
user2 = User(name="Keith", email="keith@stones.com")
users = [user1, user2]
schema = UserSchema(many=True)
result = schema.dump(users)  # OR UserSchema().dump(users, many=True)
pprint(result)
# [{'name': u'Mick',
#   'email': u'mick@stones.com',
#   'created_at': '2014-08-17T14:58:57.600623+00:00'}
#  {'name': u'Keith',
#   'email': u'keith@stones.com',
#   'created_at': '2014-08-17T14:58:57.600623+00:00'}]



##Validation
#Validation occurs on deserialization but not on serialization.
class marshmallow.validate.OneOf(choices, labels=None, *, error=None)
    Validator which succeeds if value is a member of choices.
    Parameters
            choices (iterable) – A sequence of valid values.
            labels (iterable) – Optional sequence of labels to pair with the choices.
            error (str) – Error message to raise in case of a validation error. 
                Can be interpolated with {input}, {choices} and {labels}.
    options(valuegetter=<class 'str'>)
        Return a generator over the (value, label) pairs, 
        where value is a string associated with each choice. 
        This convenience method is useful to populate, for instance, 
        a form select field.
        Parameters
            valuegetter – Can be a callable or a string. 
            In the former case, it must be a one-argument callable 
            which returns the value of a choice. 
            In the latter case, the string specifies the name of an attribute 
            of the choice objects. 
            Defaults to str() or str().
class marshmallow.validate.ContainsOnly(choices, labels=None, *, error=None)
    Validator which succeeds if value is a sequence and each element in the 
    sequence is also in the sequence passed as choices. 
    Empty input is considered valid.
class marshmallow.validate.Email(*, error=None)
    Validate an email address.
    Parameters
        error (str) – Error message to raise in case of a validation error. 
            Can be interpolated with {input}.
class marshmallow.validate.Equal(comparable, *, error=None)
    Validator which succeeds if the value passed to it is equal to comparable.
    Parameters
            comparable – The object to compare to.
            error (str) – Error message to raise in case of a validation error. 
                Can be interpolated with {input} and {other}.
class marshmallow.validate.Length(min=None, max=None, *, error=None, equal=None)
    Validator which succeeds if the value passed to it has a length between a minimum and maximum. Uses len(), so it can work for strings, lists, or anything with length.
    Parameters
            min (int) – The minimum length. 
                If not provided, minimum length will not be checked.
            max (int) – The maximum length. 
                If not provided, maximum length will not be checked.
            equal (int) – The exact length. 
                If provided, maximum and minimum length will not be checked.
            error (str) – Error message to raise in case of a validation error. 
                Can be interpolated with {input}, {min} and {max}.
class marshmallow.validate.NoneOf(iterable, *, error=None)
    Validator which fails if value is a member of iterable.
    Parameters
            iterable (iterable) – A sequence of invalid values.
            error (str) – Error message to raise in case of a validation error. 
                Can be interpolated using {input} and {values}.
class marshmallow.validate.Predicate(method, *, error=None, **kwargs)
    Call the specified method of the value object. The validator succeeds if the invoked method returns an object that evaluates to True in a Boolean context. Any additional keyword argument will be passed to the method.
    Parameters
            method (str) – The name of the method to invoke.
            error (str) – Error message to raise in case of a validation error. 
                Can be interpolated with {input} and {method}.
            kwargs – Additional keyword arguments to pass to the method.
class marshmallow.validate.Range(min=None, max=None, *, min_inclusive=True, max_inclusive=True, error=None)
    Validator which succeeds if the value passed to it is within the specified range. If min is not specified, or is specified as None, no lower bound exists. If max is not specified, or is specified as None, no upper bound exists. The inclusivity of the bounds (if they exist) is configurable. If min_inclusive is not specified, or is specified as True, then the min bound is included in the range. If max_inclusive is not specified, or is specified as True, then the max bound is included in the range.
    Parameters
            min – The minimum value (lower bound). 
                If not provided, minimum value will not be checked.
            max – The maximum value (upper bound). 
                If not provided, maximum value will not be checked.
            error (str) – Error message to raise in case of a validation error. 
                Can be interpolated with {input}, {min} and {max}.
            min_inclusive (bool) – Whether the min bound is included in the range.
            max_inclusive (bool) – Whether the max bound is included in the range.
class marshmallow.validate.Regexp(regex, flags=0, *, error=None)
    Validator which succeeds if the value matches regex.
    Note
    Uses re.match, which searches for a match at the beginning of a string.
    Parameters
            regex – The regular expression string to use. 
                Can also be a compiled regular expression pattern.
            flags – The regexp flags to use, for example re.IGNORECASE. 
                Ignored if regex is not a string.
            error (str) – Error message to raise in case of a validation error. 
                Can be interpolated with {input} and {regex}.
class marshmallow.validate.URL(*, relative=False, schemes=None, require_tld=True, error=None)
    Validate a URL.
    Parameters
            relative (bool) – Whether to allow relative URLs.
            error (str) – Error message to raise in case of a validation error. 
                Can be interpolated with {input}.
            schemes (set) – Valid schemes. By default, http, https, ftp, and ftps are allowed.
            require_tld (bool) – Whether to reject non-FQDN hostnames.

#Schema.load()/Schema.loads() raises a ValidationError error 
#when invalid data are passed in. 
from marshmallow import ValidationError

try:
    result = UserSchema().load({"name": "John", "email": "foo"})
except ValidationError as err:
    print(err.messages)  # => {"email": ['"foo" is not a valid email address.']}
    print(err.valid_data)  # => {"name": "John"}

#When validating a collection, the errors dictionary will be keyed 
#on the indices of invalid items.

from pprint import pprint

from marshmallow import Schema, fields, ValidationError


class BandMemberSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email()


user_data = [
    {"email": "mick@stones.com", "name": "Mick"},
    {"email": "invalid", "name": "Invalid"},  # invalid email
    {"email": "keith@stones.com", "name": "Keith"},
    {"email": "charlie@stones.com"},  # missing "name"
]

try:
    BandMemberSchema(many=True).load(user_data)
except ValidationError as err:
    pprint(err.messages)
    # {1: {'email': ['Not a valid email address.']},
    #  3: {'name': ['Missing data for required field.']}}


#To perform additional validation for a field by passing the validate argument. 
#There are a number of built-in validators in the marshmallow.validate module.

#may also pass a collection (list, tuple, generator) of callables to validate.


from pprint import pprint

from marshmallow import Schema, fields, validate, ValidationError


class UserSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1))
    permission = fields.Str(validate=validate.OneOf(["read", "write", "admin"]))
    age = fields.Int(validate=validate.Range(min=18, max=40))


in_data = {"name": "", "permission": "invalid", "age": 71}
try:
    UserSchema().load(in_data)
except ValidationError as err:
    pprint(err.messages)
    # {'age': ['Must be greater than or equal to 18 and less than or equal to 40.'],
    #  'name': ['Shorter than minimum length 1.'],
    #  'permission': ['Must be one of: read, write, admin.']}

#OR implement your own validation functions.

from marshmallow import Schema, fields, ValidationError


def validate_quantity(n):
    if n < 0:
        raise ValidationError("Quantity must be greater than 0.")
    if n > 30:
        raise ValidationError("Quantity must not be greater than 30.")


class ItemSchema(Schema):
    quantity = fields.Integer(validate=validate_quantity)


in_data = {"quantity": 31}
try:
    result = ItemSchema().load(in_data)
except ValidationError as err:
    print(err.messages)  # => {'quantity': ['Quantity must not be greater than 30.']}

##Field Validators as instance Methods

from marshmallow import fields, Schema, validates, ValidationError


class ItemSchema(Schema):
    quantity = fields.Integer()

    @validates("quantity")
    def validate_quantity(self, value):
        if value < 0:
            raise ValidationError("Quantity must be greater than 0.")
        if value > 30:
            raise ValidationError("Quantity must not be greater than 30.")

            
            
##Required Fields
#Make a field required by passing required=True. 
#To customize the error message for required fields, 
#pass a dict with a required key as the error_messages argument for the field.

from pprint import pprint

from marshmallow import Schema, fields, ValidationError


class UserSchema(Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True, error_messages={"required": "Age is required."})
    city = fields.String(
        required=True,
        error_messages={"required": {"message": "City required", "code": 400}},
    )
    email = fields.Email()


try:
    result = UserSchema().load({"email": "foo@bar.com"})
except ValidationError as err:
    pprint(err.messages)
    # {'age': ['Age is required.'],
    # 'city': {'code': 400, 'message': 'City required'},
    # 'name': ['Missing data for required field.']}

    
    
##Partial Loading
#When using the same schema in multiple places, 
#you may only want to skip required validation by passing partial.

class UserSchema(Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True)


result = UserSchema().load({"age": 42}, partial=("name",))
# OR UserSchema(partial=('name',)).load({'age': 42})
print(result)  # => {'age': 42}


#OR ignore missing fields entirely by setting partial=True.

class UserSchema(Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True)


result = UserSchema().load({"age": 42}, partial=True)
# OR UserSchema(partial=True).load({'age': 42})
print(result)  # => {'age': 42}



##Specifying Defaults
class UserSchema(Schema):
    id = fields.UUID(missing=uuid.uuid1)
    birthdate = fields.DateTime(default=dt.datetime(2017, 9, 29))


UserSchema().load({})
# {'id': UUID('337d946c-32cd-11e8-b475-0022192ed31b')}
UserSchema().dump({})
# {'birthdate': '2017-09-29T00:00:00+00:00'}


##Handling Unknown Fields
#By default, load will raise a ValidationError 
#if it encounters a key with no matching Field in the schema.

#This behavior can be modified with the unknown option, 
    RAISE (default): raise a ValidationError if there are any unknown fields
    EXCLUDE: exclude unknown fields
    INCLUDE: accept and include the unknown fields

#For example 
from marshmallow import Schema, INCLUDE


class UserSchema(Schema):
    class Meta:
        unknown = INCLUDE

#at instantiation time,
schema = UserSchema(unknown=INCLUDE)

#or when calling load.
UserSchema().load(data, unknown=INCLUDE)


##Validation Without Deserialization
errors = UserSchema().validate({"name": "Ronnie", "email": "invalid-email"})
print(errors)  # {'email': ['Not a valid email address.']}



##Read-only/dump_only and Write-only/load_only Fields
# When loading, dump-only fields are considered unknown. 
# If the unknown option is set to INCLUDE, 
# values with keys corresponding to those fields are therefore loaded 
# with no validation.

class UserSchema(Schema):
    name = fields.Str()
    # password is "write-only"
    password = fields.Str(load_only=True)
    # created_at is "read-only"
    created_at = fields.DateTime(dump_only=True)

##Specifying Serialization/Deserialization Keys
#Schemas will (de)serialize an input dictionary from/to an output dictionary 
#whose keys are identical to the field names. 

#If you are consuming and producing data that does not match your schema, 
#specify the output keys via the data_key argument.

class UserSchema(Schema):
    name = fields.String()
    email = fields.Email(data_key="emailAddress")


s = UserSchema()

data = {"name": "Mike", "email": "foo@bar.com"}
result = s.dump(data)
# {'name': u'Mike',
# 'emailAddress': 'foo@bar.com'}

data = {"name": "Mike", "emailAddress": "foo@bar.com"}
result = s.load(data)
# {'name': u'Mike',
# 'email': 'foo@bar.com'}



##Implicit Field Creation
#Marshmallow will choose an appropriate field type based on the attribute's type.

#Note that name will be automatically formatted as a String 
#and created_at will be formatted as a DateTime.

class UserSchema(Schema):
    uppername = fields.Function(lambda obj: obj.name.upper())

    class Meta:
        fields = ("name", "email", "created_at", "uppername")

#OR The schema below is equivalent to above:

class UserSchema(Schema):
    uppername = fields.Function(lambda obj: obj.name.upper())

    class Meta:
        # No need to include 'uppername'
        additional = ("name", "email", "created_at")

        
        
##Ordering Output
#To maintain field ordering, set the ordered option to True. 

from collections import OrderedDict

from marshmallow import Schema, fields, pprint


class UserSchema(Schema):
    uppername = fields.Function(lambda obj: obj.name.upper())

    class Meta:
        fields = ("name", "email", "created_at", "uppername")
        ordered = True


u = User("Charlie", "charlie@stones.com")
schema = UserSchema()
result = schema.dump(u)
assert isinstance(result, OrderedDict)
# marshmallow's pprint function maintains order
pprint(result, indent=2)
# {
#   "name": "Charlie",
#   "email": "charlie@stones.com",
#   "created_at": "2014-10-30T08:27:48.515735+00:00",
#   "uppername": "CHARLIE"
# }




##Nesting Schemas
#Schemas can be nested to represent relationships between objects 
#(e.g. foreign key relationships). 

#For example, a Blog may have an author represented by a User object.

import datetime as dt


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()
        self.friends = []
        self.employer = None


class Blog:
    def __init__(self, title, author):
        self.title = title
        self.author = author  # A User object

#Then Use Nested Schema 
from marshmallow import Schema, fields, pprint


class UserSchema(Schema):
    name = fields.String()
    email = fields.Email()
    created_at = fields.DateTime()


class BlogSchema(Schema):
    title = fields.String()
    author = fields.Nested(UserSchema)

#The serialized blog will have the nested user representation.
user = User(name="Monty", email="monty@python.org")
blog = Blog(title="Something Completely Different", author=user)
result = BlogSchema().dump(blog)
pprint(result)
# {'title': u'Something Completely Different',
#  'author': {'name': u'Monty',
#             'email': u'monty@python.org',
#             'created_at': '2014-08-17T14:58:57.600623+00:00'}}



#If the field is a collection of nested objects, you must set many=True.
collaborators = fields.Nested(UserSchema, many=True)



##Specifying Which Fields to Nest
#You can explicitly specify which attributes of the nested objects 
#you want to serialize with the only argument.

class BlogSchema2(Schema):
    title = fields.String()
    author = fields.Nested(UserSchema, only=["email"])


schema = BlogSchema2()
result = schema.dump(blog)
pprint(result)
# {
#     'title': u'Something Completely Different',
#     'author': {'email': u'monty@python.org'}
# }



#OR represent the attributes of deeply nested objects using dot delimiters.

class SiteSchema(Schema):
    blog = fields.Nested(BlogSchema2)


schema = SiteSchema(only=["blog.author.email"])
result = schema.dump(site)
pprint(result)
# {
#     'blog': {
#         'author': {'email': u'monty@python.org'}
#     }
# }


#You can replace nested data with a single value 
#(or flat list of values if many=True) using the Pluck field.

class UserSchema(Schema):
    name = fields.String()
    email = fields.Email()
    friends = fields.Pluck("self", "name", many=True)


# ... create ``user`` ...
serialized_data = UserSchema().dump(user)
pprint(serialized_data)
# {
#     "name": "Steve",
#     "email": "steve@example.com",
#     "friends": ["Mike", "Joe"]
# }
deserialized_data = UserSchema().load(result)
pprint(deserialized_data)
# {
#     "name": "Steve",
#     "email": "steve@example.com",
#     "friends": [{"name": "Mike"}, {"name": "Joe"}]
# }


##Nest Schema - Partial Loading
#Nested schemas also inherit the partial parameter of the parent load call.

class UserSchemaStrict(Schema):
    name = fields.String(required=True)
    email = fields.Email()
    created_at = fields.DateTime(required=True)


class BlogSchemaStrict(Schema):
    title = fields.String(required=True)
    author = fields.Nested(UserSchemaStrict, required=True)


schema = BlogSchemaStrict()
blog = {"title": "Something Completely Different", "author": {}}
result = schema.load(blog, partial=True)
pprint(result)
# {'author': {}, 'title': 'Something Completely Different'}


#You can specify a subset of the fields to allow partial loading 
#using dot delimiters.

author = {"name": "Monty"}
blog = {"title": "Something Completely Different", "author": author}
result = schema.load(blog, partial=("title", "author.created_at"))
pprint(result)
# {'author': {'name': 'Monty'}, 'title': 'Something Completely Different'}



##Two-way Nesting
#If you have two objects that nest each other, 
#you can refer to a nested schema by its class name. 
#This allows you to nest Schemas that have not yet been defined.


class AuthorSchema(Schema):
    # Make sure to use the 'only' or 'exclude' params
    # to avoid infinite recursion
    books = fields.Nested("BookSchema", many=True, exclude=("author",))

    class Meta:
        fields = ("id", "name", "books")


class BookSchema(Schema):
    author = fields.Nested(AuthorSchema, only=("id", "name"))

    class Meta:
        fields = ("id", "title", "author")

from marshmallow import pprint
from mymodels import Author, Book

author = Author(name="William Faulkner")
book = Book(title="As I Lay Dying", author=author)
book_result = BookSchema().dump(book)
pprint(book_result, indent=2)
# {
#   "id": 124,
#   "title": "As I Lay Dying",
#   "author": {
#     "id": 8,
#     "name": "William Faulkner"
#   }
# }

author_result = AuthorSchema().dump(author)
pprint(author_result, indent=2)
# {
#   "id": 8,
#   "name": "William Faulkner",
#   "books": [
#     {
#       "id": 124,
#       "title": "As I Lay Dying"
#     }
#   ]
# }



#If you need to, you can also pass the full, module-qualified path to fields.Nested.
books = fields.Nested('path.to.BookSchema',
                      many=True, exclude=('author', ))

                      
                      
                      
##Nesting A Schema Within Itself
#If the object to be marshalled has a relationship to an object of the same type, 
#you can nest the Schema within itself by passing "self" (with quotes) 
#to the Nested constructor.

class UserSchema(Schema):
    name = fields.String()
    email = fields.Email()
    friends = fields.Nested("self", many=True)
    # Use the 'exclude' argument to avoid infinite recursion
    employer = fields.Nested("self", exclude=("employer",), default=None)


user = User("Steve", "steve@example.com")
user.friends.append(User("Mike", "mike@example.com"))
user.friends.append(User("Joe", "joe@example.com"))
user.employer = User("Dirk", "dirk@example.com")
result = UserSchema().dump(user)
pprint(result, indent=2)
# {
#     "name": "Steve",
#     "email": "steve@example.com",
#     "friends": [
#         {
#             "name": "Mike",
#             "email": "mike@example.com",
#             "friends": [],
#             "employer": null
#         },
#         {
#             "name": "Joe",
#             "email": "joe@example.com",
#             "friends": [],
#             "employer": null
#         }
#     ],
#     "employer": {
#         "name": "Dirk",
#         "email": "dirk@example.com",
#         "friends": []
#     }
# }




##Pre-processing and Post-processing Methods
#Data pre-processing and post-processing methods can be registered 
#using the pre_load, post_load, pre_dump, and post_dump decorators.

#the processing pipeline for deserialization is as follows:
    @pre_load(pass_many=True) methods
    @pre_load(pass_many=False) methods
    load(in_data, many) (validation and deserialization)
    @post_load(pass_many=True) methods
    @post_load(pass_many=False) methods

#for serialization is similar
    @pre_dump(pass_many=False) methods
    @pre_dump(pass_many=True) methods
    dump(obj, many) (serialization)
    @post_dump(pass_many=False) methods
    @post_dump(pass_many=True) methods

#Example 
from marshmallow import Schema, fields, pre_load


class UserSchema(Schema):
    name = fields.Str()
    slug = fields.Str()

    @pre_load
    def slugify_name(self, in_data, **kwargs):
        in_data["slug"] = in_data["slug"].lower().strip().replace(" ", "-")
        return in_data


schema = UserSchema()
result = schema.load({"name": "Steve", "slug": "Steve Loria "})
result["slug"]  # => 'steve-loria'

#By default, pre- and post-processing methods receive one object/datum at a time, 
#transparently handling the many parameter passed to the schema at runtime.

#In cases where your pre- and post-processing methods need to receive the input collection when many=True, 
#add pass_many=True to the method decorators. 
#The method will receive the input data (which may be a single datum or a collection) 
#and the boolean value of many.


#One common use case is to wrap data in a namespace 
#upon serialization and unwrap the data during deserialization.

from marshmallow import Schema, fields, pre_load, post_load, post_dump


class BaseSchema(Schema):
    # Custom options
    __envelope__ = {"single": None, "many": None}
    __model__ = User

    def get_envelope_key(self, many):
        """Helper to get the envelope key."""
        key = self.__envelope__["many"] if many else self.__envelope__["single"]
        assert key is not None, "Envelope key undefined"
        return key

    @pre_load(pass_many=True)
    def unwrap_envelope(self, data, many, **kwargs):
        key = self.get_envelope_key(many)
        return data[key]

    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many, **kwargs):
        key = self.get_envelope_key(many)
        return {key: data}

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


class UserSchema(BaseSchema):
    __envelope__ = {"single": "user", "many": "users"}
    __model__ = User
    name = fields.Str()
    email = fields.Email()


user_schema = UserSchema()

user = User("Mick", email="mick@stones.org")
user_data = user_schema.dump(user)
# {'user': {'email': 'mick@stones.org', 'name': 'Mick'}}

users = [
    User("Keith", email="keith@stones.org"),
    User("Charlie", email="charlie@stones.org"),
]
users_data = user_schema.dump(users, many=True)
# {'users': [{'email': 'keith@stones.org', 'name': 'Keith'},
#            {'email': 'charlie@stones.org', 'name': 'Charlie'}]}

user_objs = user_schema.load(users_data, many=True)
# [<User(name='Keith Richards')>, <User(name='Charlie Watts')>]



##Raising Errors in Pre-/Post-processor Methods
#Pre- and post-processing methods may raise a ValidationError. 
#By default, errors will be stored on the "_schema" key in the errors dictionary.

from marshmallow import Schema, fields, ValidationError, pre_load


class BandSchema(Schema):
    name = fields.Str()

    @pre_load
    def unwrap_envelope(self, data, **kwargs):
        if "data" not in data:
            raise ValidationError('Input data must have a "data" key.')
        return data["data"]


sch = BandSchema()
try:
    sch.load({"name": "The Band"})
except ValidationError as err:
    err.messages
# {'_schema': ['Input data must have a "data" key.']}


#If you want to store and error on a different key, 
#pass the key name as the second argument to ValidationError.

from marshmallow import Schema, fields, ValidationError, pre_load


class BandSchema(Schema):
    name = fields.Str()

    @pre_load
    def unwrap_envelope(self, data, **kwargs):
        if "data" not in data:
            raise ValidationError(
                'Input data must have a "data" key.', "_preprocessing"
            )
        return data["data"]


sch = BandSchema()
try:
    sch.load({"name": "The Band"})
except ValidationError as err:
    err.messages
# {'_preprocessing': ['Input data must have a "data" key.']}



#You may register multiple processor methods on a Schema.
# Keep in mind, however, that the invocation order of decorated methods 
#of the same type is not guaranteed. 

#If you need to guarantee order of processing steps, you should put them 
#in the same method.

from marshmallow import Schema, fields, pre_load

# YES
class MySchema(Schema):
    field_a = fields.Field()

    @pre_load
    def preprocess(self, data, **kwargs):
        step1_data = self.step1(data)
        step2_data = self.step2(step1_data)
        return step2_data

    def step1(self, data):
        do_step1(data)

    # Depends on step1
    def step2(self, data):
        do_step2(data)


# NO
class MySchema(Schema):
    field_a = fields.Field()

    @pre_load
    def step1(self, data, **kwargs):
        do_step1(data)

    # Depends on step1
    @pre_load
    def step2(self, data, **kwargs):
        do_step2(data)

        
        
##Schema-level Validation
#register schema-level validation functions for a Schema 
#using the marshmallow.validates_schema decorator.

# By default, schema-level validation errors will be stored on the 
#_schema key of the errors dictionary.

from marshmallow import Schema, fields, validates_schema, ValidationError


class NumberSchema(Schema):
    field_a = fields.Integer()
    field_b = fields.Integer()

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if data["field_b"] >= data["field_a"]:
            raise ValidationError("field_a must be greater than field_b")


schema = NumberSchema()
try:
    schema.load({"field_a": 1, "field_b": 2})
except ValidationError as err:
    err.messages["_schema"]
# => ["field_a must be greater than field_b"]



##Storing Errors on Specific Fields
#It is possible to report errors on fields and subfields using a dict.
#When multiple schema-leval validator return errors, 
#the error structures are merged together in the ValidationError raised 
#at the end of the validation.

from marshmallow import Schema, fields, validates_schema, ValidationError


class NumberSchema(Schema):
    field_a = fields.Integer()
    field_b = fields.Integer()
    field_c = fields.Integer()
    field_d = fields.Integer()

    @validates_schema
    def validate_lower_bound(self, data, **kwargs):
        errors = {}
        if data["field_b"] <= data["field_a"]:
            errors["field_b"] = ["field_b must be greater than field_a"]
        if data["field_c"] <= data["field_a"]:
            errors["field_c"] = ["field_c must be greater than field_a"]
        if errors:
            raise ValidationError(errors)

    @validates_schema
    def validate_upper_bound(self, data, **kwargs):
        errors = {}
        if data["field_b"] >= data["field_d"]:
            errors["field_b"] = ["field_b must be lower than field_d"]
        if data["field_c"] >= data["field_d"]:
            errors["field_c"] = ["field_c must be lower than field_d"]
        if errors:
            raise ValidationError(errors)


schema = NumberSchema()
try:
    schema.load({"field_a": 3, "field_b": 2, "field_c": 1, "field_d": 0})
except ValidationError as err:
    err.messages
# => {
#     'field_b': [
#         'field_b must be greater than field_a',
#         'field_b must be lower than field_d'
#     ],
#     'field_c': [
#         'field_c must be greater than field_a',
#         'field_c must be lower than field_d'
#     ]
#    }



##Using Original Input Data
#If you want to use the original, unprocessed input, 
#you can add pass_original=True to post_load or validates_schema.

from marshmallow import Schema, fields, post_load, ValidationError


class MySchema(Schema):
    foo = fields.Int()
    bar = fields.Int()

    @post_load(pass_original=True)
    def add_baz_to_bar(self, data, original_data, **kwargs):
        baz = original_data.get("baz")
        if baz:
            data["bar"] = data["bar"] + baz
        return data


schema = MySchema()
schema.load({"foo": 1, "bar": 2, "baz": 3})
# {'foo': 1, 'bar': 5}




##Overriding How Attributes Are Accessed
#By default, marshmallow uses utils.get_value to pull attributes 
#from various types of objects for serialization. 
#This will work for most use cases.

#However, if you want to specify how values are accessed from an object, 
#you can override the get_attribute method.

class UserDictSchema(Schema):
    name = fields.Str()
    email = fields.Email()

    # If we know we're only serializing dictionaries, we can
    # use dict.get for all input objects
    def get_attribute(self, obj, key, default):
        return obj.get(key, default)


##Using Context
#The context attribute of a Schema is a general-purpose store 
#for extra information that may be needed for (de)serialization. 
#It may be used in both Schema and Field methods.

schema = UserSchema()
# Make current HTTP request available to
# custom fields, schema methods, schema validators, etc.
schema.context["request"] = request
schema.dump(user)



##Custom Error Messages
#You can customize the error messages that dump and dumps uses 
#when raising a ValidationError. 
#You do this by overriding the error_messages class variable:

class MySchema(Schema):
    error_messages = {
        "unknown": "Custom unknown field error message.",
        "type": "Custom invalid type error message.",
    }

    
    
    
    
### Flask + marshmallow 
#adds additional features to marshmallow, 
#including URL and Hyperlinks fields 
#It also (optionally) integrates with Flask-SQLAlchemy.


##Create your app.

from flask import Flask
from flask_marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow(app)


#Write  models.

from your_orm import Model, Column, Integer, String, DateTime
from flask_marshmallow import Marshmallow as ma

class User(Model):
    email = Column(String)
    password = Column(String)
    date_created = Column(DateTime, auto_now_add=True)

    
#Define  output format with marshmallow.
class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("email", "date_created", "_links")

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        #first arg, string of view name 
        {"self": ma.URLFor("user_detail", id="<id>"), "collection": ma.URLFor("users")}
    )


user_schema = UserSchema()
users_schema = UserSchema(many=True)

#Output the data in views.
@app.route("/api/users/")
def users():
    all_users = User.all()
    return users_schema.dump(all_users)


@app.route("/api/users/<id>")
def user_detail(id):
    user = User.get(id)
    return user_schema.dump(user)


# {
#     "email": "fred@queen.com",
#     "date_created": "Fri, 25 Apr 2014 06:02:56 -0000",
#     "_links": {
#         "self": "/api/users/42",
#         "collection": "/api/users/"
#     }
# }



##With Flask-SQLAlchemy Integration
#initialize the SQLAlchemy and Marshmallow extensions, in that order.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"

# Order matters: Initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

#Declare your like normal.
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref="books")

#Generate marshmallow Schemas from models using ModelSchema or TableSchema.
class AuthorSchema(ma.ModelSchema):
    class Meta:
        model = Author


class BookSchema(ma.TableSchema):
    class Meta:
        table = Book.__table__

db.create_all()
author_schema = AuthorSchema()
book_schema = BookSchema()
author = Author(name="Chuck Paluhniuk")
book = Book(title="Fight Club", author=author)
db.session.add(author)
db.session.add(book)
db.session.commit()
author_schema.dump(author)
# {'id': 1, 'name': 'Chuck Paluhniuk', 'books': [1]}


#ModelSchema is nearly identical in API to marshmallow_sqlalchemy.ModelSchema 
#with the following exceptions:
1. By default, ModelSchema uses the scoped session created by Flask-SQLAlchemy.
2. ModelSchema subclasses flask_marshmallow.Schema, 
   so it includes the jsonify method.
   
#You can also use ma.HyperlinkRelated fields if you want relationships 
#to be represented by hyperlinks rather than primary keys.
class BookSchema(ma.ModelSchema):
    class Meta:
        model = Book
        
    #name of the  view used to generate the URL
    #If your models and views use the id attribute as a primary key, you're done; 
    #otherwise, you must specify the name of the attribute used as the primary key.
    author = ma.HyperlinkRelated("author_detail")

with app.test_request_context():
    print(book_schema.dump(book))
# {'id': 1, 'title': 'Fight Club', 'author': '/authors/1'}


#To represent a one-to-many relationship, 
#wrap the HyperlinkRelated instance in a marshmallow.fields.List field, like this:
class AuthorSchema(ma.ModelSchema):
    class Meta:
        model = Author

    books = ma.List(ma.HyperlinkRelated("book_detail"))

with app.test_request_context():
    print(author_schema.dump(author))
# {'id': 1, 'name': 'Chuck Paluhniuk', 'books': ['/books/1']}

##Reference 
class flask_marshmallow.fields.URLFor(endpoint, **kwargs)
    Field that outputs the URL for an endpoint.
    Acts identically to Flask's url_for function, 
    except that arguments can be pulled from the object to be serialized.
    Usage:
        url = URLFor('author_get', id='<id>')
        https_url = URLFor('author_get', id='<id>', _scheme='https', _external=True)
    Parameters
        endpoint (str) – Flask endpoint name.
        kwargs – Same keyword arguments as Flask's url_for, 
        except string arguments enclosed in < > will be interpreted 
        as attributes to pull from the object.

flask_marshmallow.fields.UrlFor
    alias of flask_marshmallow.fields.URLFor

class flask_marshmallow.fields.AbsoluteURLFor(endpoint, **kwargs)
    Field that outputs the absolute URL for an endpoint.

flask_marshmallow.fields.AbsoluteUrlFor
    alias of flask_marshmallow.fields.AbsoluteURLFor

class flask_marshmallow.fields.Hyperlinks(schema, **kwargs)
    Field that outputs a dictionary of hyperlinks, 
    given a dictionary schema with URLFor objects as values.
    Example:
    _links = Hyperlinks({
        'self': URLFor('author', id='<id>'),
        'collection': URLFor('author_list'),
    })
    URLFor objects can be nested within the dictionary.
    _links = Hyperlinks({
        'self': {
            'href': URLFor('book', id='<id>'),
            'title': 'book detail'
        }
    })


    
    
###Flask SqlAlchemy 

#yourapplication.py 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
        
#With csutom ctor 
class Foo(db.Model):
    # ...
    def __init__(**kwargs):
        super(Foo, self).__init__(**kwargs)
        # do custom stuff

#to create the tables and database:
from yourapplication import db
db.create_all()

#to create some users:
from yourapplication import User
admin = User(username='admin', email='admin@example.com')
guest = User(username='guest', email='guest@example.com')

#To save 
db.session.add(admin)
db.session.add(guest)
db.session.commit()

#Accessing the data 
>>> User.query.all()
[<User u'admin'>, <User u'guest'>]
>>> User.query.filter_by(username='admin').first()
<User u'admin'>




##Simple Relationships

from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category',
        backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name

#usage 
py = Category(name='Python')
Post(title='Hello Python!', body='Python is pretty cool', category=py)
p = Post(title='Snakes', body='Ssssssss')
py.posts.append(p)
db.session.add(py)

>>> py.posts
[<Post 'Hello Python!'>, <Post 'Snakes'>]

#eager loads 
from sqlalchemy.orm import joinedload
query = Category.query.options(joinedload('posts'))
for category in query:
    print category, category.posts
#<Category u'Python'> [<Post u'Hello Python!'>, <Post u'Snakes'>]

#to get a query object for that relationship
>>> Post.query.with_parent(py).filter(Post.title != 'Snakes').all()
[<Post 'Hello Python!'>]


##Introduction into Contexts
#to use more than one application or create the application dynamically in a function 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

#So how does SQLAlchemy come to know about your application? 
#You will have to setup an application context. 

#If you are working inside a Flask view function or a CLI command, 
#that automatically happens. 

#However, if you are working inside the interactive shell
from yourapp import create_app
app = create_app()
app.app_context().push()

#or 
def my_function():
    with app.app_context():
        user = db.User(...)
        db.session.add(user)
        db.session.commit()

#Some functions inside Flask-SQLAlchemy also accept optionally 
#the application to operate on:
from yourapp import db, create_app
db.create_all(app=create_app())



##Configuration Keys

SQLALCHEMY_DATABASE_URI
	The database URI that should be used for the connection. Examples:
    sqlite:////tmp/test.db
    mysql://username:password@server/db

SQLALCHEMY_BINDS
	A dictionary that maps bind keys to SQLAlchemy connection URIs. 

SQLALCHEMY_ECHO
	If set to True SQLAlchemy will log all the statements issued to stderr 
    which can be useful for debugging.

SQLALCHEMY_RECORD_QUERIES
	Can be used to explicitly disable or enable query recording. 
    Query recording automatically happens in debug or testing mode. 
    See get_debug_queries() for more information.
SQLALCHEMY_NATIVE_UNICODE
SQLALCHEMY_POOL_SIZE
SQLALCHEMY_POOL_TIMEOUT
SQLALCHEMY_POOL_RECYCLE
SQLALCHEMY_MAX_OVERFLOW
SQLALCHEMY_TRACK_MODIFICATIONS
SQLALCHEMY_ENGINE_OPTIONS


##Connection URI Format
dialect+driver://username:password@host:port/database

#Examples 
Postgres:
    postgresql://scott:tiger@localhost/mydatabase
MySQL:
    mysql://scott:tiger@localhost/mydatabase
Oracle:
    oracle://scott:tiger@127.0.0.1:1521/sidname
SQLite (note that platform path conventions apply):
    #Unix/Mac (note the four leading slashes)
    sqlite:////absolute/path/to/foo.db
    #Windows (note 3 leading forward slashes and backslash escapes)
    sqlite:///C:\\absolute\\path\\to\\foo.db
    #Windows (alternative using raw string)
    r'sqlite:///C:\absolute\path\to\foo.db'

    
##Using custom MetaData and naming conventions

from sqlalchemy import MetaData
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)


##Timeouts
#Certain database backends may impose different inactive connection timeouts, 
#which interferes with Flask-SQLAlchemy's connection pooling.
#eg By default, MariaDB is configured to have a 600 second timeout. 
#set SQLALCHEMY_POOL_RECYCLE to a value less than your backend's timeout.



##Declaring Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
#Example 
Integer
	an integer
String(size)
	a string with a maximum length (optional in some databases, e.g. PostgreSQL)
Text
	some longer unicode text
DateTime
	date and time expressed as Python datetime object.
Float
	stores floating point values
Boolean
	stores a boolean value
PickleType
	stores a pickled Python object
LargeBinary
	stores large arbitrary binary data
    
    
##One-to-Many Relationships
#can use strings to refer to classes that are not created yet 

class Person(db.Model): #One 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    #to have a one-to-one relationship you can pass uselist=False to relationship().
    addresses = db.relationship('Address', backref='person', lazy=True)
    #backref is a simple way to also declare a new property on the Address class.
    #ie my_address.person to get to the person at that address. 

class Address(db.Model): #Many 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
        nullable=False)


#other than lazy 
1.'select' / True (which is the default, but explicit is better than implicit) means that SQLAlchemy will load the data as necessary in one go using a standard select statement.
2.'joined' / False tells SQLAlchemy to load the relationship in the same query as the parent using a JOIN statement.
3.'subquery' works like 'joined' but instead SQLAlchemy will use a subquery.
4.'dynamic' is special and can be useful if you have many items and always want to apply additional SQL filters to them. Instead of loading the items SQLAlchemy will return another query object which you can further refine before loading the items. Note that this cannot be turned into a different loading strategy when querying so it's often a good idea to avoid using this in favor of lazy=True. A query object equivalent to a dynamic user.addresses relationship can be created using Address.query.with_parent(user) while still being able to use lazy or eager loading on the relationship itself as necessary.

#To define the lazy status for backrefs- use backref() function:
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    addresses = db.relationship('Address', lazy='select',
        backref=db.backref('person', lazy='joined'))

##Many-to-Many Relationships
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('pages', lazy=True))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)


##Inserting Records
from yourapp import User
me = User('admin', 'admin@example.com')
db.session.add(me)
db.session.commit()
>>> me.id
1

##Deleting Records
db.session.delete(me)
db.session.commit()

##Querying Records
peter = User.query.filter_by(username='peter').first()
>>> peter.id
2
>>> peter.email
u'peter@example.org'

missing = User.query.filter_by(username='missing').first()
>>> missing is None
True

>>> User.query.filter(User.email.endswith('@example.com')).all()
[<User u'admin'>, <User u'guest'>]

>>> User.query.order_by(User.username).all()
[<User u'admin'>, <User u'guest'>, <User u'peter'>]

>>> User.query.limit(1).all()
[<User u'admin'>]

>>> User.query.get(1)
<User u'admin'>

#Queries in Views
@app.route('/user/<username>')
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('show_user.html', user=user)

>>> User.query.filter_by(username=username).first_or_404(description='There is no data with {}'.format(username))



##Multiple Databases with Binds

SQLALCHEMY_DATABASE_URI = 'postgres://localhost/main'
SQLALCHEMY_BINDS = {
    'users':        'mysqldb://localhost/users',
    'appmeta':      'sqlite:////path/to/appmeta.db'
}

#Creating and Dropping Tables
db.create_all()
db.create_all(bind=['users'])
db.create_all(bind='appmeta')
db.drop_all(bind=None)

#Referring to Binds
class User(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)



##Example - Quotes API (Flask + SQLAlchemy)

import datetime

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from marshmallow import Schema, fields, ValidationError, pre_load

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/quotes.db"
db = SQLAlchemy(app)

# MODELS #
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(80))
    last = db.Column(db.String(80))


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref=db.backref("quotes", lazy="dynamic"))
    posted_at = db.Column(db.DateTime)


# SCHEMAS #
class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first = fields.Str()
    last = fields.Str()
    formatted_name = fields.Method("format_name", dump_only=True)

    def format_name(self, author):
        return "{}, {}".format(author.last, author.first)


# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")


class QuoteSchema(Schema):
    id = fields.Int(dump_only=True)
    author = fields.Nested(AuthorSchema, validate=must_not_be_blank)
    content = fields.Str(required=True, validate=must_not_be_blank)
    posted_at = fields.DateTime(dump_only=True)

    # Allow client to pass author's full name in request body
    # e.g. {"author': 'Tim Peters"} rather than {"first": "Tim", "last": "Peters"}
    @pre_load
    def process_author(self, data, **kwargs):
        author_name = data.get("author")
        if author_name:
            first, last = author_name.split(" ")
            author_dict = dict(first=first, last=last)
        else:
            author_dict = {}
        data["author"] = author_dict
        return data


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
quote_schema = QuoteSchema()
quotes_schema = QuoteSchema(many=True, only=("id", "content"))

# API #
@app.route("/authors")
def get_authors():
    authors = Author.query.all()
    # Serialize the queryset
    result = authors_schema.dump(authors)
    return {"authors": result}


@app.route("/authors/<int:pk>")
def get_author(pk):
    try:
        author = Author.query.get(pk)
    except IntegrityError:
        return {"message": "Author could not be found."}, 400
    author_result = author_schema.dump(author)
    quotes_result = quotes_schema.dump(author.quotes.all())
    return {"author": author_result, "quotes": quotes_result}


@app.route("/quotes/", methods=["GET"])
def get_quotes():
    quotes = Quote.query.all()
    result = quotes_schema.dump(quotes, many=True)
    return {"quotes": result}


@app.route("/quotes/<int:pk>")
def get_quote(pk):
    try:
        quote = Quote.query.get(pk)
    except IntegrityError:
        return {"message": "Quote could not be found."}, 400
    result = quote_schema.dump(quote)
    return {"quote": result}


@app.route("/quotes/", methods=["POST"])
def new_quote():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    try:
        data = quote_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422
    first, last = data["author"]["first"], data["author"]["last"]
    author = Author.query.filter_by(first=first, last=last).first()
    if author is None:
        # Create a new author
        author = Author(first=first, last=last)
        db.session.add(author)
    # Create new quote
    quote = Quote(
        content=data["content"], author=author, posted_at=datetime.datetime.utcnow()
    )
    db.session.add(quote)
    db.session.commit()
    result = quote_schema.dump(Quote.query.get(quote.id))
    return {"message": "Created new quote.", "quote": result}


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=5000)

#Run the app.
$ pip install flask flask-sqlalchemy
$ python examples/flask_example.py

$ pip install httpie
$ http POST :5000/quotes/ author="Tim Peters" content="Beautiful is better than ugly."
$ http POST :5000/quotes/ author="Tim Peters" content="Now is better than never."
$ http POST :5000/quotes/ author="Peter Hintjens" content="Simplicity is always better than functionality."

#invlid data 
$ http POST :5000/quotes/ content="I have no author"
{
    "author": [
        "Data not provided."
    ]
}

#Now we can GET a list of all the quotes.

$ http :5000/quotes/
{
    "quotes": [
        {
            "content": "Beautiful is better than ugly.",
            "id": 1
        },
        {
            "content": "Now is better than never.",
            "id": 2
        },
        {
            "content": "Simplicity is always better than functionality.",
            "id": 3
        }
    ]
}

#We can also GET the quotes for a single author.

$ http :5000/authors/1
{
    "author": {
        "first": "Tim",
        "formatted_name": "Peters, Tim",
        "id": 1,
        "last": "Peters"
    },
    "quotes": [
        {
            "content": "Beautiful is better than ugly.",
            "id": 1
        },
        {
            "content": "Now is better than never.",
            "id": 2
        }
    ]
}






###RabbitMQ
#RabbitMQ3.7.17 supports Erlang 22.0.x, 21.3.x, and 20.3.x release series.
#https://www.rabbitmq.com/which-erlang.html


1.Install Erlang/OTP,  otp_win64_22.0.exe with admin previledge(must)
2.Make Sure ERLANG_HOME is Set
3.Install RabbitMQ Server
  eg https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.7.17/rabbitmq-server-3.7.17.exe
4. Install, this would start RabbitMQ as windows service 
  
#Stopping a Node
rabbitmqctl.bat stop
rabbitmqctl.bat status

#Default User Access
#The broker creates a user guest with password guest. 
#Unconfigured clients will in general use these credentials. 

#Port Access
4369: epmd, a peer discovery service used by RabbitMQ nodes and CLI tools
5672, 5671: used by AMQP 0-9-1 and 1.0 clients without and with TLS
25672: used for inter-node and CLI tools communication (Erlang distribution server port) and is allocated from a dynamic range (limited to a single port by default, computed as AMQP port + 20000). Unless external connections on these ports are really necessary (e.g. the cluster uses federation or CLI tools are used on machines outside the subnet), these ports should not be publicly exposed. See networking guide for details.
35672-35682: used by CLI tools (Erlang distribution client ports) for communication with nodes and is allocated from a dynamic range (computed as server distribution port + 10000 through server distribution port + 10010). See networking guide for details.
15672: HTTP API clients, management UI and rabbitmqadmin (only if the management plugin is enabled)
61613, 61614: STOMP clients without and with TLS (only if the STOMP plugin is enabled)
1883, 8883: (MQTT clients without and with TLS, if the MQTT plugin is enabled
15674: STOMP-over-WebSockets clients (only if the Web STOMP plugin is enabled)
15675: MQTT-over-WebSockets clients (only if the Web MQTT plugin is enabled)



###Asynchronous jobs using Celery
#Celery is a task queue with batteries included. 
#It uses many Broker eg RabbitMQ

#Application
#tasks.py:

from celery import Celery

#The first argument to Celery is the name of the current module. 
app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y

#Start RabbitMQ service 
#Running the Celery worker server (would block)
#Note Windows not supported for Celery4.x, use celery==3.1.24
#or use single threaded (use linux for production)
$ celery -A tasks worker --loglevel=info --pool=solo
#or use eventlet 
$ pip install eventlet 
$ celery -A tasks worker --loglevel=info --pool=eventlet
#or 
set FORKED_BY_MULTIPROCESSING=1
celery -A tasks worker --loglevel=info

#In production you'll want to run the worker in the background as a daemon. 
#To do this you need to use the tools provided by your platform, 
#or something like supervisord (see Daemonization for more information).
$ celery worker --help
$ celery help

##Calling the task
#To call our task ,use the delay() method.
from tasks import add
add.delay(4, 4) #returns an AsyncResult

#Results are not enabled by default. 
#If you want to keep track of the tasks' states, 
#Celery needs to store or send the states somewhere. 

#There are several built-in result backends to choose from: SQLAlchemy/Django ORM, Memcached, Redis, RPC (RabbitMQ/AMQP), and – or you can define your own.

#For this example we use the rpc result backend using RabbitMQ
app = Celery('tasks', backend='rpc://', broker='pyamqp://')

#Or if you want to use Redis as the result backend
app = Celery('tasks', backend='redis://localhost', broker='pyamqp://')

#usage 
result = add.delay(4, 4)
>>> result.ready()
False
>>> result.get(timeout=1)
8

#In case the task raised an exception, get() will re-raise the exception
result.get(propagate=False)
result.traceback


##Configuration
#The default configuration should be good enough for most use cases
app.conf.task_serializer = 'json'

#or 
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Europe/Oslo',
    enable_utc=True,
)

#or 
app.config_from_object('celeryconfig')

#celeryconfig.py:

broker_url = 'pyamqp://'
result_backend = 'rpc://'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Oslo'
enable_utc = True

#To verify that your configuration file works properly 
$ python -m celeryconfig

#For examle, route a misbehaving task to a dedicated queue:
#celeryconfig.py:
task_routes = {
    'tasks.add': 'low-priority',
}

#Or instead of routing it you could rate limit the task instead, 
#so that only 10 tasks of this type can be processed in a minute (10/m):
task_annotations = {
    'tasks.add': {'rate_limit': '10/m'}
}

#OR 
$ celery -A tasks control rate_limit tasks.add 10/m



##Result_backend  configuration 
Database backend settings
    result_backend = 'db+scheme://user:password@host:port/dbname'
    #Examples:
    # sqlite (filename)
    result_backend = 'db+sqlite:///results.sqlite'
    # mysql
    result_backend = 'db+mysql://scott:tiger@localhost/foo'
    # postgresql
    result_backend = 'db+postgresql://scott:tiger@localhost/mydatabase'
    # oracle
    result_backend = 'db+oracle://scott:tiger@127.0.0.1:1521/sidname'
    #configuration 
    database_engine_options
        Default: {} (empty mapping).
        # echo enables verbose logging from SQLAlchemy.
        app.conf.database_engine_options = {'echo': True}

    database_table_names
        Default: {} (empty mapping).
        When SQLAlchemy is configured as the result backend, 
        Celery automatically creates two tables to store result meta-data for tasks. 
        This setting allows you to customize the table names:
        # use custom table names for the database result backend.
        database_table_names = {
            'task': 'myapp_taskmeta',
            'group': 'myapp_groupmeta',
        }


RPC Result Backend (RabbitMQ/QPid)
    result_backend = 'rpc://'
    The RPC result backend (rpc://) is special as it doesnt actually store 
    the states, but rather sends them as messages. 
    This is an important difference as it means that a result 
    can only be retrieved once, and only by the client that initiated the task. 
    Two different processes can't wait for the same result.
    The messages are transient (non-persistent) by default, 
    so the results will disappear if the broker restarts. You can configure the result backend to send persistent messages using the result_persistent setting.
    #configuration 
    result_persistent
        Default: Disabled by default (transient messages).
        If set to True, result messages will be persistent. 
        This means the messages won't be lost after a broker restart.
        Example configuration
        result_backend = 'rpc://'
        result_persistent = False
        #Please note: using this backend could trigger the raise of celery.backends.rpc.BacklogLimitExceeded 
        #if the task tombstone is too old.
        #E.g.
        for i in range(10000):
            r = debug_task.delay()
        print(r.state)  # this would raise celery.backends.rpc.BacklogLimitExceeded



##Using Celery in your Application
#Project layout:
proj/__init__.py
    /celery.py
    /tasks.py

#proj/celery.py
from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('proj',
             broker='amqp://',
             backend='amqp://',
             include=['proj.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()

#proj/tasks.py

from __future__ import absolute_import, unicode_literals
from .celery import app


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

#Starting the worker
#run the worker in the directory above proj
$ celery -A proj worker -l info --pool=solo

When the worker starts you should see a banner and some messages:

-------------- celery@halcyon.local v4.0 (latentcall)
---- **** -----
--- * ***  * -- [Configuration]
-- * - **** --- . broker:      amqp://guest@localhost:5672//
- ** ---------- . app:         __main__:0x1012d8590
- ** ---------- . concurrency: 8 (processes)
- ** ---------- . events:      OFF (enable -E to monitor this worker)
- ** ----------
- *** --- * --- [Queues]
-- ******* ---- . celery:      exchange:celery(direct) binding:celery
--- ***** -----

#The default concurrency number is the number of CPU's on that machine 
#(including cores), or pecify a custom number using the celery worker -c option. 
#Including the default prefork pool, Celery also supports using Eventlet, Gevent, and running in a single thread 

#Stopping the worker
#To stop the worker simply hit Control-c. 

#to run the worker in the background
#The daemonization scripts uses the celery multi command 
#to start one or more workers in the background:
$ celery multi start w1 -A proj -l info
celery multi v4.0.0 (latentcall)
> Starting nodes...
    > w1.halcyon.local: OK

#To restart it too:
$ celery  multi restart w1 -A proj -l info
celery multi v4.0.0 (latentcall)
> Stopping nodes...
    > w1.halcyon.local: TERM -> 64024
> Waiting for 1 node.....
    > w1.halcyon.local: OK
> Restarting node w1.halcyon.local: OK
celery multi v4.0.0 (latentcall)
> Stopping nodes...
    > w1.halcyon.local: TERM -> 64052

#or stop it:
$ celery multi stop w1 -A proj -l info

#The stop command is asynchronous
# OR do synchronous
$ celery multi stopwait w1 -A proj -l info

#By default it'll create pid and log files in the current directory, 
#to protect against multiple workers launching on top of each other 
#put these in a dedicated directory:
$ mkdir -p /var/run/celery
$ mkdir -p /var/log/celery
$ celery multi start w1 -A proj -l info --pidfile=/var/run/celery/%n.pid \
                                        --logfile=/var/log/celery/%n%I.log

#With the multi command you can start multiple workers, 
#with queue names 
$ celery multi start 10 -A proj -l info -Q:1-3 images,video -Q:4,5 data -Q default -L:4,5 debug

##Calling Tasks
add.delay(2, 2)
#Or 
add.apply_async((2, 2))

#or with options 
#eg the task will be sent to a queue named lopri 
#and the task will execute, at the earliest, 10 seconds after the message was sent.
>>> add.apply_async((2, 2), queue='lopri', countdown=10)

#with result backend configured 
res = add.delay(2, 2)
res.get(timeout=1)
res.id
#d6b3aea2-fb9b-4ebc-8da4-848818db9114

#raises exception 
res = add.delay(2)
res.get(timeout=1)
#or for the errors to propagate 
>>> res.get(propagate=False)
TypeError('add() takes exactly 2 arguments (1 given)',)
>>> res.failed()
True
>>> res.successful()
False
>>> res.state
'FAILURE'

#To pass the signature of a task invocation to another process 
#or as an argument to another function, use  signatures.
#A signature wraps the arguments and execution options of a single task invocation 

#eg  the arguments (2, 2), and a countdown of 10 seconds like this:
>>> add.signature((2, 2), countdown=10)
tasks.add(2, 2)
#or 
>>> add.s(2, 2)
tasks.add(2, 2)

#then call 
>>> s1 = add.s(2, 2)
>>> res = s1.delay()
>>> res.get()
4

#or partials:
# incomplete partial: add(?, 2)
>>> s2 = add.s(2)
# resolves the partial: add(8, 2)
>>> res = s2.delay(8)
>>> res.get()
10

#Keyword arguments can also be added later
>>> s3 = add.s(2, 2, debug=True)
>>> s3.delay(debug=False)   # debug is now False.

#signatures supports the calling API
sig.apply_async(args=(), kwargs={}, **options)


##The Primitives
#These primitives are signature objects themselves, 
#so they can be combined in any number of ways to compose complex work-flows.
group
chain
chord
map
starmap
chunks


##Groups
#A group calls a list of tasks in parallel, 
#and it returns a special result instance that lets you inspect the results 
#as a group, and retrieve the return values in order.

from celery import group
from proj.tasks import add

group(add.s(i, i) for i in xrange(10))().get()
#[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

#Partial group
g = group(add.s(i) for i in xrange(10))
g(10).get()
#[10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

##Chains
#Tasks can be linked together so that after one task returns the other is called:
from celery import chain
from proj.tasks import add, mul
# (4 + 4) * 8
>>> chain(add.s(4, 4) | mul.s(8))().get()
64

#or a partial chain:
# (? + 4) * 8
g = chain(add.s(4) | mul.s(8))
>>> g(4).get()
64

#Chains can also be written like this:
>>> (add.s(4, 4) | mul.s(8))().get()
64

##Chords
#A chord is a group with a callback:

from celery import chord
from proj.tasks import add, xsum
>>> chord((add.s(i, i) for i in xrange(10)), xsum.s())().get()
90

#A group chained to another task will be automatically converted to a chord:
>>> (group(add.s(i, i) for i in xrange(10)) | xsum.s())().get()
90

#Since these primitives are all of the signature type 
#they can be combined almost however you want
>>> upload_document.s(file) | group(apply_filter.s() for filter in filters)



##Routing
#Celery supports all of the routing facilities provided by RabbitMQ(AMQP), 
#but it also supports simple routing where messages are sent to named queues.

#The task_routes setting enables you to route tasks by name 
#and keep everything centralized in one location:
app.conf.update(
    task_routes = {
        'proj.tasks.add': {'queue': 'hipri'},
    },
)

#or 
from proj.tasks import add
add.apply_async((2, 2), queue='hipri')

#then make a worker consume from this queue 
#by specifying the celery worker -Q option:
$ celery -A proj worker -Q hipri

#specify multiple queues 
$ celery -A proj worker -Q hipri,celery


##Remote Control
#If you're using RabbitMQ (AMQP), Redis, or Qpid as the broker 
#then you can control and inspect the worker at runtime.
$ celery -A proj inspect active

#You can also specify one or more workers to act on the request 
#using the --destination option. 
#This is a comma separated list of worker host names:

$ celery -A proj inspect active --destination=celery@example.com

#If a destination isn't provided then every worker will act 
#and reply to the request.

#help 
$ celery -A proj inspect --help

#control: contains commands that actually changes things in the worker at runtime:
$ celery -A proj control --help

#For example you can force workers to enable event messages 
#(used for monitoring tasks and workers):
$ celery -A proj control enable_events

#When events are enabled you can then start the event dumper 
#to see what the workers are doing:
$ celery -A proj events --dump

#or you can start the curses interface:
$ celery -A proj events

#when you're finished monitoring you can disable events again:
$ celery -A proj control disable_events

#The celery status command also uses remote control commands 
#and shows a list of online workers in the cluster:
$ celery -A proj status



##Timezone
#All times and dates, internally and in messages uses the UTC timezone.
#or 
app.conf.timezone = 'Europe/London'



##Optimization
#The default configuration isn't optimized for throughput by default, 
#it tries to walk the middle way between many short tasks and fewer long tasks, 
#a compromise between throughput and fair scheduling.

#If you have strict fair scheduling requirements, 
#or want to optimize for throughput , read the Optimizing Guide.

#If you're using RabbitMQ then you can install the librabbitmq module: 
#this is an AMQP client implemented in C:
$ pip install librabbitmq





###Database migrations using Alembic

#Creating an Environment
$ cd yourproject
$ alembic init alembic

yourproject/
    alembic.ini   
    alembic/    #this directory lives within application's source tree and is the home of the migration environment
        env.py  #This is a Python script that is run whenever the alembic migration tool is invoked
                #contains instructions to configure and generate a SQLAlchemy engine, procure a connection from that engine along with a transaction, and then invoke the migration engine, using the connection as a source of database connectivity.
        README
        script.py.mako #This is a Mako template file which is used to generate new migration scripts. 
                        #Whatever is here is used to generate new files within versions/.
        versions/
            3512b954651e_add_account.py
            2b1ae634e5cd_add_order_id.py
            3adcc9a56557_rename_username_field.py

 
#Alembic also includes other environment templates. 
$ alembic list_templates
Available templates:
generic - Generic single-database configuration.
multidb - Rudimentary multi-database configuration.
pylons - Configuration that reads from a Pylons project environment.

#Templates are used via the 'init' command, e.g.:
$ alembic init --template pylons ./scripts


##Editing the .ini File
#The file generated with the 'generic' configuration looks like:


# A generic, single database configuration.

[alembic]
# path to migration scripts
script_location = alembic

# template used to generate migration files
# file_template = %%(rev)s_%%(slug)s

# timezone to use when rendering the date
# within the migration file as well as the filename.
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version location specification; this defaults
# to alembic/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path
# version_locations = %(here)s/bar %(here)s/bat alembic/versions

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = driver://user:pass@localhost/dbname

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S

#For starting up with just a single database and the generic configuration,
sqlalchemy.url = postgresql://scott:tiger@localhost/test



##Create a Migration Script

$ alembic revision -m "create account table"
Generating /path/to/yourproject/alembic/versions/1975ea83b712_create_accoun
t_table.py...done

#1975ea83b712_create_account_table.py 
"""create account table

Revision ID: 1975ea83b712
Revises:
Create Date: 2011-11-08 11:40:27.089406

"""

# revision identifiers, used by Alembic.
revision = '1975ea83b712' #identifiers for the current revision
down_revision = None      #This is how Alembic knows the correct order in which to apply migrations
branch_labels = None

from alembic import op
import sqlalchemy as sa

#Update this 
def upgrade():
    pass

def downgrade():
    pass

#When we create the next revision, 
#the new file's down_revision identifier would point to this one:
revision = 'ae1027a6acf'
down_revision = '1975ea83b712'

#Every time Alembic runs an operation against the versions/ directory, 
#it reads all the files in, and composes a list based on 
#how the down_revision identifiers link together, 
#with the down_revision of None representing the first file. 

#Then Update , sa means sqlalchemy, op means alembic
def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )

def downgrade():
    op.drop_table('account')

##Operations 
add_column(table_name, column, schema=None)
    Issue an 'add column' instruction using the current migration context.
    e.g.:
    from alembic import op
    from sqlalchemy import Column, String
    op.add_column('organization',
        Column('name', String())
    )
    The provided Column object can also specify a ForeignKey, referencing a remote table name. Alembic will automatically generate a stub 'referenced' table and emit a second ALTER statement in order to add the constraint separately:
    from alembic import op
    from sqlalchemy import Column, INTEGER, ForeignKey
    op.add_column('organization',
        Column('account_id', INTEGER, ForeignKey('accounts.id'))
    )
    Note that this statement uses the Column construct as is from the SQLAlchemy library. In particular, default values to be created on the database side are specified using the server_default parameter, and not default which only specifies Python-side defaults:
    from alembic import op
    from sqlalchemy import Column, TIMESTAMP, func
    # specify "DEFAULT NOW" along with the column add
    op.add_column('account',
        Column('timestamp', TIMESTAMP, server_default=func.now())
    )
alter_column(table_name, column_name, nullable=None, comment=False, 
        server_default=False, new_column_name=None, type_=None, 
        existing_type=None, existing_server_default=False, 
        existing_nullable=None, existing_comment=None, schema=None, **kw)
    Issue an 'alter column' instruction using the current migration context.
    Generally, only that aspect of the column which is being changed, i.e. name, type, nullability, default, needs to be specified. Multiple changes can also be specified at once and the backend should 'do the right thing', emitting each change either separately or together as the backend allows.
    MySQL has special requirements here, since MySQL cannot ALTER a column without a full specification. When producing MySQL-compatible migration files, it is recommended that the existing_type, existing_server_default, and existing_nullable parameters be present, if not being altered.
    Type changes which are against the SQLAlchemy 'schema' types Boolean and Enum may also add or drop constraints which accompany those types on backends that don’t support them natively. The existing_type argument is used in this case to identify and remove a previous constraint that was bound to the type object.
batch_alter_table(table_name, schema=None, recreate='auto', copy_from=None, table_args=(), table_kwargs={}, reflect_args=(), reflect_kwargs={}, naming_convention=None)
    Invoke a series of per-table migrations in batch.
bulk_insert(table, rows, multiinsert=True)
    Issue a 'bulk insert' operation using the current migration context.
    This provides a means of representing an INSERT of multiple rows which works equally well in the context of executing on a live connection as well as that of generating a SQL script. In the case of a SQL script, the values are rendered inline into the statement.
    e.g.:
    from alembic import op
    from datetime import date
    from sqlalchemy.sql import table, column
    from sqlalchemy import String, Integer, Date
    # Create an ad-hoc table to use for the insert statement.
    accounts_table = table('account',
        column('id', Integer),
        column('name', String),
        column('create_date', Date)
    )
    op.bulk_insert(accounts_table,
        [
            {'id':1, 'name':'John Smith',
                    'create_date':date(2010, 10, 5)},
            {'id':2, 'name':'Ed Williams',
                    'create_date':date(2007, 5, 27)},
            {'id':3, 'name':'Wendy Jones',
                    'create_date':date(2008, 8, 15)},
        ]
    )
    When using –sql mode, some datatypes may not render inline automatically, such as dates and other special types. When this issue is present, Operations.inline_literal() may be used:
    op.bulk_insert(accounts_table,
        [
            {'id':1, 'name':'John Smith',
                    'create_date':op.inline_literal("2010-10-05")},
            {'id':2, 'name':'Ed Williams',
                    'create_date':op.inline_literal("2007-05-27")},
            {'id':3, 'name':'Wendy Jones',
                    'create_date':op.inline_literal("2008-08-15")},
        ],
        multiinsert=False
    )
create_check_constraint(constraint_name, table_name, condition, schema=None, **kw)
    Issue a 'create check constraint' instruction using the current migration context.
    e.g.:
    from alembic import op
    from sqlalchemy.sql import column, func
    op.create_check_constraint(
        "ck_user_name_len",
        "user",
        func.len(column('name')) > 5
    )
create_exclude_constraint(constraint_name, table_name, *elements, **kw)
    Issue an alter to create an EXCLUDE constraint using the current migration context.
    Note
    This method is Postgresql specific, and additionally requires at least SQLAlchemy 1.0.
    e.g.:
    from alembic import op
    op.create_exclude_constraint(
        "user_excl",
        "user",
        ("period", '&&'),
        ("group", '='),
        where=("group != 'some group'")
    )
create_foreign_key(constraint_name, source_table, referent_table, local_cols, remote_cols, onupdate=None, ondelete=None, deferrable=None, initially=None, match=None, source_schema=None, referent_schema=None, **dialect_kw)
    Issue a 'create foreign key' instruction using the current migration context.
    e.g.:
    from alembic import op
    op.create_foreign_key(
                "fk_user_address", "address",
                "user", ["user_id"], ["id"])
create_index(index_name, table_name, columns, schema=None, unique=False, **kw)
    Issue a 'create index' instruction using the current migration context.
    e.g.:
    from alembic import op
    op.create_index('ik_test', 't1', ['foo', 'bar'])
    Functional indexes can be produced by using the sqlalchemy.sql.expression.text() construct:
    from alembic import op
    from sqlalchemy import text
    op.create_index('ik_test', 't1', [text('lower(foo)')])
create_primary_key(constraint_name, table_name, columns, schema=None)
    Issue a 'create primary key' instruction using the current migration context.
    e.g.:
    from alembic import op
    op.create_primary_key(
                "pk_my_table", "my_table",
                ["id", "version"]
            )
create_table(table_name, *columns, **kw)
    Issue a 'create table' instruction using the current migration context.
    This directive receives an argument list similar to that of the traditional sqlalchemy.schema.Table construct, but without the metadata:
    from sqlalchemy import INTEGER, VARCHAR, NVARCHAR, Column
    from alembic import op
    op.create_table(
        'account',
        Column('id', INTEGER, primary_key=True),
        Column('name', VARCHAR(50), nullable=False),
        Column('description', NVARCHAR(200)),
        Column('timestamp', TIMESTAMP, server_default=func.now())
    )
    Note that create_table() accepts Column constructs directly from the SQLAlchemy library. In particular, default values to be created on the database side are specified using the server_default parameter, and not default which only specifies Python-side defaults:
    from alembic import op
    from sqlalchemy import Column, TIMESTAMP, func
    # specify "DEFAULT NOW" along with the "timestamp" column
    op.create_table('account',
        Column('id', INTEGER, primary_key=True),
        Column('timestamp', TIMESTAMP, server_default=func.now())
    )
    The function also returns a newly created Table object, corresponding to the table specification given, which is suitable for immediate SQL operations, in particular Operations.bulk_insert():
    from sqlalchemy import INTEGER, VARCHAR, NVARCHAR, Column
    from alembic import op
    account_table = op.create_table(
        'account',
        Column('id', INTEGER, primary_key=True),
        Column('name', VARCHAR(50), nullable=False),
        Column('description', NVARCHAR(200)),
        Column('timestamp', TIMESTAMP, server_default=func.now())
    )
    op.bulk_insert(
        account_table,
        [
            {"name": "A1", "description": "account 1"},
            {"name": "A2", "description": "account 2"},
        ]
    )
create_table_comment(table_name, comment, existing_comment=None, schema=None)
    Emit a COMMENT ON operation to set the comment for a table.
create_unique_constraint(constraint_name, table_name, columns, schema=None, **kw)
    Issue a 'create unique constraint' instruction using the current migration context.
    e.g.:
    from alembic import op
    op.create_unique_constraint("uq_user_name", "user", ["name"])
drop_column(table_name, column_name, schema=None, **kw)
    Issue a 'drop column' instruction using the current migration context.
    e.g.:
    drop_column('organization', 'account_id')
drop_constraint(constraint_name, table_name, type_=None, schema=None)
    Drop a constraint of the given name, typically via DROP CONSTRAINT.
drop_index(index_name, table_name=None, schema=None, **kw)
    Issue a 'drop index' instruction using the current migration context.
    e.g.:
    drop_index("accounts")
drop_table(table_name, schema=None, **kw)
    Issue a 'drop table' instruction using the current migration context.
    e.g.:
    drop_table("accounts")
drop_table_comment(table_name, existing_comment=None, schema=None)
    Issue a 'drop table comment' operation to remove an existing comment set on a table.
execute(sqltext, execution_options=None)
    Execute the given SQL using the current migration context.
    The given SQL can be a plain string, e.g.:
    op.execute("INSERT INTO table (foo) VALUES ('some value')")
    Or it can be any kind of Core SQL Expression construct, such as below where we use an update construct:
    from sqlalchemy.sql import table, column
    from sqlalchemy import String
    from alembic import op
    account = table('account',
        column('name', String)
    )
    op.execute(
        account.update().\\
            where(account.c.name==op.inline_literal('account 1')).\\
            values({'name':op.inline_literal('account 2')})
            )
    OR use the 'bind' available from the context:
    from alembic import op
    connection = op.get_bind()
    connection.execute(
        account.update().where(account.c.name=='account 1').
        values({"name": "account 2"})
    )
    Additionally, when passing the statement as a plain string, it is first coerceed into a sqlalchemy.sql.expression.text() construct before being passed along. In the less likely case that the literal SQL string contains a colon, it must be escaped with a backslash, as:
    op.execute("INSERT INTO table (foo) VALUES ('\:colon_value')")
f(name)
    Indicate a string name that has already had a naming convention applied to it.
    op.add_column('t', 'x', Boolean(name=op.f('ck_bool_t_x')))
    Above, the CHECK constraint generated will have the name ck_bool_t_x regardless of whether or not a naming convention is in use.
    Alternatively, if a naming convention is in use, and ‘f’ is not used, names will be converted along conventions. If the target_metadata contains the naming convention {"ck": "ck_bool_%(table_name)s_%(constraint_name)s"}, then the output of the following:
        op.add_column(‘t’, ‘x’, Boolean(name=’x’))
    will be:
    CONSTRAINT ck_bool_t_x CHECK (x in (1, 0)))
rename_table(old_table_name, new_table_name, schema=None)
    Emit an ALTER TABLE to rename a table.

    
##Running our First Migration
#The alembic upgrade command will run upgrade operations, 
#proceeding from the current database revision, in this example None, to the given target revision. 

#We can specify 1975ea83b712 as the revision we'd like to upgrade to, 
#or the most recent  means head

$ alembic upgrade head
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
INFO  [alembic.context] Running upgrade None -> 1975ea83b712


##Running our Second Migration
$ alembic revision -m "Add a column"
Generating /path/to/yourapp/alembic/versions/ae1027a6acf_add_a_column.py...
done

#edit this file and add a new column to the account table:

"""Add a column

Revision ID: ae1027a6acf
Revises: 1975ea83b712
Create Date: 2011-11-08 12:37:36.714947

"""

# revision identifiers, used by Alembic.
revision = 'ae1027a6acf'
down_revision = '1975ea83b712'

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))

def downgrade():
    op.drop_column('account', 'last_transaction_date')


$ alembic upgrade head
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
INFO  [alembic.context] Running upgrade 1975ea83b712 -> ae1027a6acf

##Partial Revision Identifiers
#use ae1 to refer to revision ae1027a6acf. 
#Alembic will stop and let you know if more than one version starts with that prefix.
$ alembic upgrade ae1

##Relative Migration Identifiers
#To move two versions from the current, a decimal value '+N' can be supplied:
$ alembic upgrade +2

#Negative values are accepted for downgrades:
$ alembic downgrade -1

#Relative identifiers may also be in terms of a specific revision. 
#For example, to upgrade to revision ae1027a6acf plus two additional steps:
$ alembic upgrade ae10+2



##Getting Information
#view the current revision:
$ alembic current
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
Current revision for postgresql://scott:XXXXX@localhost/test: 1975ea83b712 -> ae1027a6acf (head), Add a column

#view history with alembic history; the --verbose option (accepted by several commands, including history, current, heads and branches) will show us full information about each revision:
$ alembic history --verbose

Rev: ae1027a6acf (head)
Parent: 1975ea83b712
Path: /path/to/yourproject/alembic/versions/ae1027a6acf_add_a_column.py

    add a column

    Revision ID: ae1027a6acf
    Revises: 1975ea83b712
    Create Date: 2014-11-20 13:02:54.849677

Rev: 1975ea83b712
Parent: <base>
Path: /path/to/yourproject/alembic/versions/1975ea83b712_add_account_table.py

    create account table

    Revision ID: 1975ea83b712
    Revises:
    Create Date: 2014-11-20 13:02:46.257104

    
    
##Viewing History Ranges
$ alembic history -r1975ea:ae1027
$ alembic history -r-3:current
$ alembic history -r1975ea:



##Downgrading
#downgrade back to the beginning, is called base:

$ alembic downgrade base
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
INFO  [alembic.context] Running downgrade ae1027a6acf -> 1975ea83b712
INFO  [alembic.context] Running downgrade 1975ea83b712 -> None

#Back to nothing - and up again:
$ alembic upgrade head
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
INFO  [alembic.context] Running upgrade None -> 1975ea83b712
INFO  [alembic.context] Running upgrade 1975ea83b712 -> ae1027a6acf



##Auto Generating Migrations
#Autogenerated scripts are rudimentary, check and update that 

#To use autogenerate, modify  env.py 

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

#we change to:
from myapp.mymodel import Base
target_metadata = Base.metadata

#which is used in below 
def run_migrations_online():
    engine = engine_from_config(
                config.get_section(config.config_ini_section), prefix='sqlalchemy.')

    with engine.connect() as connection:
        context.configure(
                    connection=connection,
                    target_metadata=target_metadata
                    )

        with context.begin_transaction():
            context.run_migrations()

#Now generate 
$ alembic revision --autogenerate -m "Added account table"
INFO [alembic.context] Detected added table 'account'
Generating /path/to/foo/alembic/versions/27c6a30d7c24.py...done

#27c6a30d7c24.py 
"""empty message

Revision ID: 27c6a30d7c24
Revises: None
Create Date: 2011-11-08 11:40:27.089406

"""

# revision identifiers, used by Alembic.
revision = '27c6a30d7c24'
down_revision = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    # commands auto generated by Alembic - please adjust! #
    op.create_table(
    'account',
    sa.Column('id', sa.Integer()),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.VARCHAR(200)),
    sa.Column('last_transaction_date', sa.DateTime()),
    sa.PrimaryKeyConstraint('id')
    )
    # end Alembic commands #

def downgrade():
    # commands auto generated by Alembic - please adjust! #
    op.drop_table("account")
    # end Alembic commands #

    
    
##Autogenerating Multiple MetaData collections
from myapp.mymodel1 import Model1Base
from myapp.mymodel2 import Model2Base
target_metadata = [Model1Base.metadata, Model2Base.metadata]

##Generating SQL Scripts (a.k.a. 'Offline Mode')
#A major capability of Alembic is to generate migrations as SQL scripts, 
#instead of running them against the database - 
#this is also referred to as offline mode. 

$ alembic upgrade ae1027a6acf --sql
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL
);

INFO  [alembic.context] Running upgrade None -> 1975ea83b712
CREATE TABLE account (
    id SERIAL NOT NULL,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    PRIMARY KEY (id)
);

INFO  [alembic.context] Running upgrade 1975ea83b712 -> ae1027a6acf
ALTER TABLE account ADD COLUMN last_transaction_date TIMESTAMP WITHOUT TIME ZONE;

INSERT INTO alembic_version (version_num) VALUES ('ae1027a6acf');

COMMIT;

#OR 
$ alembic upgrade ae1027a6acf --sql > migration.sql

#Getting the Start Version
$ alembic upgrade 1975ea83b712:ae1027a6acf --sql > migration.sql

#It's also possible to have the env.py script retrieve the 'last' version 
#from the local environment, such as from a local file. 

#A scheme like this would basically treat a local file in the same way 
#alembic_version works:

if context.is_offline_mode():
    version_file = os.path.join(os.path.dirname(config.config_file_name), "version.txt")
    if os.path.exists(version_file):
        current_version = open(version_file).read()
    else:
        current_version = None
    context.configure(dialect_name=engine.name, starting_rev=current_version)
    context.run_migrations()
    end_version = context.get_revision_argument()
    if end_version and end_version != current_version:
        open(version_file, 'w').write(end_version)


##The Importance of Naming Constraints
#The way constraints are referred to in migration scripts is by name, 
#however these names by default are in most cases generated by the relational database in use, 
#when the constraint is created. 

#For example, if you emitted two CREATE TABLE statements like this on Postgresql:
test=> CREATE TABLE user_account (id INTEGER PRIMARY KEY);
CREATE TABLE
test=> CREATE TABLE user_order (
test(>   id INTEGER PRIMARY KEY,
test(>   user_account_id INTEGER REFERENCES user_account(id));
CREATE TABLE

#Suppose we wanted to DROP the REFERENCES that 
#we just applied to the user_order.user_account_id column, 

#At the prompt, we'd use ALTER TABLE <tablename> DROP CONSTRAINT <constraint_name>, 
#or if using Alembic we'd be using Operations.drop_constraint(). 

#But both of those functions need a name - what's the name of this constraint?

test=> SELECT r.conname FROM
test->  pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
test->  JOIN pg_catalog.pg_constraint r  ON c.oid = r.conrelid
test->  WHERE c.relname='user_order' AND r.contype = 'f'
test-> ;
             conname
---------------------------------
 user_order_user_account_id_fkey
(1 row)

#The name above is different Oracle Database 10g Express Edition Release 10.2.0.1.0 - Production

SQL> CREATE TABLE user_account (id INTEGER PRIMARY KEY);

Table created.

SQL> CREATE TABLE user_order (
  2     id INTEGER PRIMARY KEY,
  3     user_account_id INTEGER REFERENCES user_account(id));

Table created.

SQL> SELECT constraint_name FROM all_constraints WHERE
  2     table_name='USER_ORDER' AND constraint_type in ('R');

CONSTRAINT_NAME
-----------------------------------------------------
SYS_C0029334

#The solution to having to look up names is to make your own names. 
from sqlalchemy import MetaData, Table, Column, Integer, ForeignKey

meta = MetaData()

user_account = Table('user_account', meta,
                  Column('id', Integer, primary_key=True)
              )

user_order = Table('user_order', meta,
                  Column('id', Integer, primary_key=True),
                  Column('user_order_id', Integer,
                    ForeignKey('user_account.id', name='fk_user_order_id'))
              )

#Simple enough, it's tedious
user_account = Table('user_account', meta,
                  Column('id', Integer, primary_key=True),
                  Column('name', String(50), unique=True)
              )

#Above, the unique=True flag creates a UniqueConstraint, 
#but again, it's not named. 
user_account = Table('user_account', meta,
                  Column('id', Integer, primary_key=True),
                  Column('name', String(50)),
                  UniqueConstraint('name', name='uq_user_account_name')
              )

#There's a solution to all this naming work, 
#which is to use an automated naming convention. 

#create a new MetaData object while passing a dictionary referring to a naming scheme:

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)


##Integration of Naming Conventions into Operations, Autogenerate
#The naming convention is passed to Operations 
#using the MigrationsContext.configure.target_metadata parameter in env.py, 
#which is normally configured when autogenerate is used:

# in application's model:

meta = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
      })
Base = declarative_base(metadata=meta)

#env.py:

# add your model's MetaData object here
# for 'autogenerate' support
from myapp import mymodel
target_metadata = mymodel.Base.metadata

# ...

def run_migrations_online():

    # ...

    context.configure(
                connection=connection,
                target_metadata=target_metadata
                )

#Then use transperantly 
op.add_column('sometable', Column('q', Boolean(name='q_bool')))
#creates  "ck_sometable_q_bool"

#OR use op directives with constraints 

def upgrade():
    op.create_unique_constraint(None, 'some_table', 'x')

#When autogenerate renders constraints in a migration script, 
#it renders them typically with their completed name. 
def upgrade():
    op.create_unique_constraint(op.f('uq_const_x'), 'some_table', 'x')



###Formatting code using Black
#To execute black, it requires Python 3.6 
$ black {source_file_or_directory}

#Black reformats entire files in place. It is not configurable. 
#It doesn't take previous formatting into account. 
#It doesn't reformat blocks that start with 

# fmt: off 

#and end with 

# fmt: on. 

## fmt: on/off have to be on the same level of indentation. 


