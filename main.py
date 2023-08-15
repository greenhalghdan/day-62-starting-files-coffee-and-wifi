from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    cafelocation = StringField('Cafe Location', validators=[DataRequired(), URL(message='Not a valid URL')])
    cafeopen = StringField('Opening Time', validators=[DataRequired()])
    cafeClose = StringField('Closing Time', validators=[DataRequired()])
    cafeCoffeeRating = SelectField('Coffee Rating', validators=[DataRequired()], choices=["☕","☕☕","☕☕☕","☕☕☕☕","☕☕☕☕☕"])
    cafeWifiStrength = SelectField('Wifi Strength', validators=[DataRequired()], choices=["❌","🌐","🌐🌐","🌐🌐🌐","🌐🌐🌐🌐","🌐🌐🌐🌐🌐"])
    cafePowerSocket = SelectField('Power Socket Availability', validators=[DataRequired()], choices=["❌","🔌","🔌🔌","🔌🔌🔌","🔌🔌🔌🔌","🔌🔌🔌🔌🔌"])
    submit = SubmitField('Submit')



# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        data = {
                "Cafe Name": form.cafe.data,
                "Location": form.cafelocation.data,
                "Open": form.cafeopen.data,
                "Close": form.cafeClose.data,
                "Coffee": form.cafeCoffeeRating.data,
                "Wifi": form.cafeWifiStrength.data,
                "Power": form.cafePowerSocket.data,

        }
        with open('cafe-data.csv', 'a', encoding='UTF8', newline="\n") as f:
            # Create a dictionary writer with the dict keys as column fieldnames
            writer = csv.DictWriter(f, fieldnames=data.keys())
            # Append single row to CSV
            writer.writerow(data)
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafe=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
