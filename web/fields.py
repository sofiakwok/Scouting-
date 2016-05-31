
import flask_wtf
from widgets import * #http://wtforms.readthedocs.org/en/latest/fields.html

class Form(flask_wtf.Form):
    name = TextAreaField('Your name', col_md = 12)
    person = TextAreaField('Their name', col_md = 12)

    #Rating people
    preferences = RadioField("How much do you like this person?", choices=[('0','Love them'),('1','Meh'),('2','Could be a lot better'),('3','Actually Satan')],default='3')
    rating = IntegerField('Rate them from 1 to 10!',default=1)

    time = IntegerField("How long have you known them?", default=1)
   
    #robotics stuff
    subteam = RadioField('What subteam are they in?', choices=[('-1', 'CAD'),('0','Programming'),('1','Mechanical'),('2','Electrical'),('3','Marketing')],default='-1')
    proficiency = RadioField('How good are they at working in their subteam?', choices=[('-1','Horrible'),('0','Inconsistent'),('1','Good')],default='-1')
    communication = RadioField('Can they talk with other people?', choices=[('-1','Not really'),('0','They can hiss'),('1','Threatened to disembowel someone')],default='-1')
    years = IntegerField('Years on the team:',default = 0)
    safety = BooleanField('Are they safe?', false_values = None)

    defense = RadioField('Defense:',choices=[('-1','N/A'),('0','Bad'),('1','Mediocre'),('2','Good')],default='-1')

    catch_truss = CheckboxButtonField('Truss', col_md=12)
    catch_ranged = CheckboxButtonField('Ranged', col_md=12)
    catch_human = CheckboxButtonField('From Human', col_md=12)
    result = RadioField("Match Result:", choices=[('2','Win'),('0', 'Loss'),('1', 'Tie')], default = '2')
    comments = TextAreaField('', col_md=12)