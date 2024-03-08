from flask import Flask,render_template,request,redirect,url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_wtf import FlaskForm
from wtforms import StringField,SelectField
from wtforms.validators import DataRequired


class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    link = StringField('Google Maps Link', validators=[DataRequired()])
    wifi_speed = SelectField('Wifi Speed', choices=[('💪', '💪'), ('💪💪', '💪💪'), ('💪💪💪', '💪💪💪'), ('💪💪💪💪', '💪💪💪💪'), ('💪💪💪💪💪', '💪💪💪💪💪')], validators=[DataRequired()])
    cakes = SelectField('Cakes quality', choices=[('🍰', '🍰'), ('🍰🍰', '🍰🍰'), ('🍰🍰🍰', '🍰🍰🍰'), ('🍰🍰🍰🍰', '🍰🍰🍰🍰'), ('🍰🍰🍰🍰🍰', '🍰🍰🍰🍰🍰')], validators=[DataRequired()])
    coffee_quality = SelectField(u'Coffee quality', choices=[('☕', '☕'), ('☕☕', '☕☕'), ('☕☕☕', '☕☕☕'), ('☕☕☕☕', '☕☕☕☕'), ('☕☕☕☕☕', '☕☕☕☕☕')], validators=[DataRequired()])


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///coffee.db"

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)
Bootstrap5(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100), nullable=False)
    wifi_speed = db.Column(db.String(100), nullable=False)
    cakes = db.Column(db.String(100), nullable=False)
    coffee_quality = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/cafes')
def cafes():
    cafes = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars()
    return render_template("cafes.html",cafes=cafes)


@app.route('/addcafe', methods=['GET', 'POST'])
def add_new_cafe():
    form=MyForm(request.form)
    
    if request.method == 'POST':
        name = request.form['name']
        link = request.form['link']
        wifi_speed = request.form['wifi_speed']
        cakes= request.form['cakes']
        coffee_quality = request.form['coffee_quality']
        new_cafe = Cafe(name=name,link=link,wifi_speed=wifi_speed,cakes=cakes,coffee_quality=coffee_quality)
        db.session.add(new_cafe)
        db.session.commit()

   
        return redirect(url_for('cafes'))
    return render_template("add.html",form=form,option="add")

@app.route('/edit/<int:cafeid>', methods=['GET', 'POST'])
def edit(cafeid):
    cafe = db.get_or_404(Cafe, cafeid)
    form=MyForm(request.form)
    form.name.data = cafe.name
    form.link.data = cafe.link
    form.wifi_speed.data = cafe.wifi_speed
    form.cakes.data = cafe.cakes
    form.coffee_quality.data = cafe.coffee_quality
  
    if request.method == 'POST':
        cafe.name = request.form['name']
        cafe.link = request.form['link']
        cafe.wifi_speed = request.form['wifi_speed']
        cafe.cakes= request.form['cakes']
        cafe.coffee_quality = request.form['coffee_quality'] 
        db.session.commit()
               
        return redirect(url_for('cafes'))
    
    return render_template("add.html",form=form,option="edit")

@app.route('/delete/<int:cafeid>')
def delete(cafeid):
    cafe = db.get_or_404(Cafe, cafeid)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('cafes'))

if __name__ == "__main__":
    app.run(debug=True)