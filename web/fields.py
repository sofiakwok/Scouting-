
import flask_wtf
from widgets import * #http://wtforms.readthedocs.org/en/latest/fields.html

class Form(flask_wtf.Form):
    match_id = IntegerField('Match #', buttons=False)
    team_id = IntegerField('Team #', buttons=False)
    #Auton Section
    auton_balls = IntegerField('Auton balls possessed', default=0)
    auton_high = RadioField("Auton High Goal", choices=[('0','N/A'),('1','Missed'),('2','Scored')],default=0)
    auton_low = RadioField("Auton Low Goal", choices=[('0','N/A'),('1','Missed'),('2','Scored')],default=0)
    #Teleop Section
    high = IntegerField('Teleop High Goals:',default=0)
    high_miss = IntegerField('High Goals Missed:',default=0)
    low = IntegerField('Teleop Low Goals:',default=0)

    low_speed = RadioField('Teleop Low Goal Speed:', choices=[('-1', 'N/A'),('0','Slow'),('1','Medium'),('2','Fast')],default=-1)
    pass_truss = RadioField('Pass Consistency Over Truss', choices=[('-1','N/A'),('0','Inconsistent'),('1','Consistent')],default=-1)
    pass_ranged = RadioField('Pass Consistency Ranged', choices=[('-1','N/A'),('0','Inconsistent'),('1','Consistent')],default=-1)

    fouls = IntegerField('Fouls:',default=0)
    tfouls = IntegerField('Technical Fouls:',default=0)
    defense = RadioField('Defense:',choices=[('-1','N/A'),('0','Bad'),('1','Mediocre'),('2','Good')],default=-1)

    catch_truss = CheckboxButtonField('Truss', col_md=12)
    catch_ranged = CheckboxButtonField('Ranged', col_md=12)
    catch_human = CheckboxButtonField('From Human', col_md=12)
    result = RadioField("Match Result:", choices=[('2','Win'),('0', 'Loss'),('1', 'Tie')])
    comments = TextAreaField('', col_md=12)