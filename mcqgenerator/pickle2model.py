import pandas as pd
import re
from mcqgenerator.models import Question, Answer
from mcqdjango import settings
import os


# RUN IN PYTHON MANAGE.PY SHELL:
#   >>> from mcqgenerator.pickle2model import uploadqandas
#   >>> uploadqandas()

def uploadqandas(filename = 'usmle_sample_questions.pkl'):
    file_path = os.path.join(settings.BASE_DIR, 'algorithms/pickles', filename)
    with open(file_path, 'rb') as pickle:  # + ('.pkl' if re.search('.pkl', filename) else None)) as pickle:
        df = pd.read_pickle(pickle)
        print(df)

    for row in df.iloc():
        q_text = row['question_text']
        if q_text =='nan':
            continue

        q = Question()
        q.question = q_text
        q.correct_answer = row['correct_answer']
        
        a = Answer()
        a.question = q
        a_text = row['A_choice']
        if a_text =='nan':
            continue
        a.text = a_text
        a.letter_key = 'A'
        
        b = Answer()
        b.question = q
        b_text = row['B_choice']
        if b_text =='nan':
            continue
        b.text = b_text
        b.letter_key = 'B'

        c = Answer()
        c.question = q
        c_text = row['C_choice']
        if a_text =='nan':
            continue
        c.text = c_text
        c.letter_key = 'C'

        d = Answer()
        d.question = q
        d_text = row['D_choice']
        if a_text =='nan':
            continue
        d.text = d_text
        d.letter_key = 'D'

        e = Answer()
        e.question = q
        e_text = row['E_choice']
        if a_text =='nan':
            continue
        e.text = e_text
        e.letter_key = 'E'

        f = Answer()
        f.question = q
        f_text = row['F_choice']
        if a_text =='nan':
            continue
        f.text = f_text
        f.letter_key = 'F'

        g = Answer()
        g.question = q
        g_text = row['G_choice']
        if a_text =='nan':
            continue
        g.text = g_text
        g.letter_key = 'G'

        q.save()
        answers = [a,b,c,d,e,f,g]
        for ans in answers:
            if q.correct_answer == ans.letter_key:
                ans.is_correct = True
            ans.save()
