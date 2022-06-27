from flask import Blueprint, render_template,request
import pandas as pd
import pickle
# import pdb

# with open('model.pkl', 'rb') as pickle_file:
#         model = pickle.load(pickle_file)

# print(model)
# breakpoint()

submit_bp = Blueprint('calculate', __name__, url_prefix = '/main')

@submit_bp.route('/calculate', methods = ['POST', 'GET'])
def calculate():
    DATE = request.args.get('date')
    WATER = request.args.get('water')
    MEAN = request.args.get('mean')
    MIN = request.args.get('min')
    MAX = request.args.get('max')

    with open('model.pkl', 'rb') as pickle_file:
        model = pickle.load(pickle_file)

    row = [str(DATE), float(WATER), float(MEAN), float(MIN), float(MAX)]
    df_row = pd.DataFrame(row).T
    df_row.columns = ['날짜', '강수량(mm)', '평균기온(C)', '최저기온(C)','최대기온(C)'] 
    pred = model.predict(df_row)
    if pred < 50:
        submit = render_template('level_one.html', pred=pred)
    elif pred < 200:
        submit = render_template('level_two.html', pred=pred)
    elif pred < 500:
        submit = render_template('level_three.html', pred=pred)
    else:
        submit = render_template('level_four.html', pred=pred)

    return submit, 200

