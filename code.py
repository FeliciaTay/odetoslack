import json, os

from flask import Flask, jsonify, request, Response, render_template
from flask.helpers import make_response
import pymysql
import os, json
from slack_sdk import WebClient
from datetime import datetime

app = Flask(__name__)
client = WebClient(token=os.environ.get('TOKEN'))

conn = pymysql.connect(
        host= '', 
        port = 3306,
        user = os.environ.get('USER'), 
        password = os.environ.get('PASSWORD'),
        db = '',
        autocommit=True
        )
cur=conn.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        return "The database has been updated!"
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def runtest():
    # to find the number of sets in database
    all_sets_no_qur = "SELECT COUNT(*) FROM QUESTION_SET"
    cur.execute(all_sets_no_qur)
    total_sets = cur.fetchall()
    set_count = total_sets[0][0]

    all_sets_qur = "SELECT * FROM QUESTION_SET"
    cur.execute(all_sets_qur)
    all_sets = cur.fetchall()

    with open("startmodal.txt", "r") as file:
        json_object=json.load(file)
        count = 1
        list = []
        for row in all_sets:
            set_id = row[0]
            set_text = row[1]
            if count == 1: # for the first set
                list.append(json.loads('{"text":{"type":"plain_text","text":"%s"},"value":"%s"}' % (set_text, set_id)))
                count = count + 1
            else: #subsequent sets
                list.append(json.loads('{"text":{"type":"plain_text","text":"%s"},"value":"%s"}' % (set_text, set_id)))
                count = count + 1
        json_object["blocks"][0]["element"]["options"] = list
        client.views_open(trigger_id=request.form["trigger_id"], view=json_object)
    return Response()

def check_row_number(list, target_question_id):
    no = 0
    for row in list:
        if row[0] == target_question_id:
            break
        else:
            no = no + 1
    return no

def run_quiz(set_id):
    with open("quizmodal.txt", "r") as modalfile:
        json_object=json.load(modalfile)
        question_query = "SELECT * FROM QUESTIONS WHERE set_id = %s" % (set_id) # get the respective set
        cur.execute(question_query)
        question_records = cur.fetchall()
        question = question_records[0][3]
        json_object["blocks"][0]["text"]["text"] = "1. %s" % (question) # get the first question
        question_id = question_records[0][0]
        option_query = "SELECT * FROM OPTIONS WHERE question_id = %s" % (question_id)
        cur.execute(option_query)
        option_rows = cur.fetchall()
        option1 = option_rows[0][0]
        option2 = option_rows[1][0]
        option3 = option_rows[2][0]
        option4 = option_rows[3][0]
        option1_txt = option_rows[0][2]
        option2_txt = option_rows[1][2]
        option3_txt = option_rows[2][2]
        option4_txt = option_rows[3][2]
        json_object["blocks"][0]["accessory"]["options"][0]["text"]["text"] = "%s" % (option1_txt)
        json_object["blocks"][0]["accessory"]["options"][0]["value"] = "%s" % (option1)
        json_object["blocks"][0]["accessory"]["options"][1]["text"]["text"] = "%s" % (option2_txt)
        json_object["blocks"][0]["accessory"]["options"][1]["value"] = "%s" % (option2)
        json_object["blocks"][0]["accessory"]["options"][2]["text"]["text"] = "%s" % (option3_txt)
        json_object["blocks"][0]["accessory"]["options"][2]["value"] = "%s" % (option3)
        json_object["blocks"][0]["accessory"]["options"][3]["text"]["text"] = "%s" % (option4_txt)
        json_object["blocks"][0]["accessory"]["options"][3]["value"] = "%s" % (option4)
    return json_object

@app.route('/createset', methods=['GET', 'POST'])
def createSet():
    with open("admin.txt", "r") as modalfile:
        json_object=json.load(modalfile)
        json_object["title"]["text"] = "Create set"
        json_object["blocks"][0]["element"]["action_id"] = "ask_password_set"
        client.views_open(trigger_id=request.form["trigger_id"], view=json_object)
    return Response()
    
@app.route('/setquestions', methods=['GET', 'POST'])
def setQuestions():
    with open("admin.txt", "r") as modalfile:
        json_object=json.load(modalfile)
        json_object["title"]["text"] = "Set questions"
        json_object["blocks"][0]["element"]["action_id"] = "ask_password_questions"
        client.views_open(trigger_id=request.form["trigger_id"], view=json_object)
    return Response()

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    with open("admin.txt", "r") as modalfile:
        json_object=json.load(modalfile)
        json_object["title"]["text"] = "See statistics"
        json_object["blocks"][0]["element"]["action_id"] = "ask_password_stats"
        client.views_open(trigger_id=request.form["trigger_id"], view=json_object)
    return Response()

@app.route('/interactive',  methods=['POST'])
def testInput():
    payload = json.loads(request.form["payload"])
    #slack_client.chat_postMessage(channel="C01UFUCHLSC", text = payload)

    if payload["type"] == "view_submission": 
        # for the screen allowing user to choose set
        if payload["view"]["blocks"][0]["type"] == "input" and payload["view"]["blocks"][0]["label"]["text"] == "Please select the set of questions to try!": 
            block_id = payload["view"]["blocks"][0]["block_id"]
            set_id = payload["view"]["state"]["values"][block_id]["static_select-action"]["selected_option"]["value"]
            with open("httprequest.txt", "r") as file:
                json_object = json.load(file)
                json_object["view"]["blocks"] = run_quiz(set_id)["blocks"]
                return make_response(jsonify(json_object),200)
        # for the screen allowing user to choose question to show statistics
        elif payload["view"]["blocks"][0]["type"] == "input" and payload["view"]["blocks"][0]["label"]["text"] == "Please select which question to see statistics for!": 
            block_id = payload["view"]["blocks"][0]["block_id"]
            question_id = payload["view"]["state"]["values"][block_id]["static_select-action"]["selected_option"]["value"]
            attempts_qur = "SELECT COUNT(*) FROM SUBMISSION_LOG WHERE question_id = '%s'" % (question_id)
            cur.execute(attempts_qur)
            no_of_attempts = cur.fetchall()[0][0]
            correct_ans_qur = "SELECT * FROM ANSWERS WHERE question_id = '%s'" % (question_id)
            cur.execute(correct_ans_qur)
            correct_ans = cur.fetchall()[0][1]
            correct_attempts_qur = "SELECT COUNT(*) FROM SELECTION_LOG WHERE opt_id = '%s'" % (correct_ans)
            cur.execute(correct_attempts_qur)
            correct_ans = cur.fetchall()[0][0]
            with open("httprequest.txt", "r") as file:
                json_object = json.load(file)
                with open("statistics.txt", "r") as modalfile:
                    reaction_object = json.load(modalfile)
                    reaction_object["blocks"][0]["text"]["text"] = "Number of attempts: %s" % (no_of_attempts)
                    reaction_object["blocks"][1]["text"]["text"] = "Number of correct attempts: %s" % (correct_ans)
                    reaction_object["blocks"][2]["text"]["text"] = "Percentage of correct attempts: %0.2f%%" % (correct_ans/no_of_attempts * 100)
                    json_object["view"] = reaction_object
                    return make_response(jsonify(json_object),200)
        # for the screen to authorise admin password
        elif payload["view"]["blocks"][0]["type"] == "input" and payload["view"]["blocks"][0]["label"]["text"] == "Please provide the admin password.": 
            block_id = payload["view"]["blocks"][0]["block_id"]
            try: # for creating sets
                inputted = payload["view"]["state"]["values"][block_id]["ask_password_set"]["value"]
            except Exception as e: # this is for enabling the setting questions modal   
                try: # for creating questions
                    inputted = payload["view"]["state"]["values"][block_id]["ask_password_questions"]["value"]
                    with open("httprequest.txt", "r") as file:
                        json_object = json.load(file)
                        if inputted == os.environ.get('SET_PASSWORD'):
                            all_sets_qur = "SELECT * FROM QUESTION_SET"
                            cur.execute(all_sets_qur)
                            all_sets = cur.fetchall()

                            with open("createquestion.txt", "r") as reaction_file:
                                reaction_object = json.load(reaction_file)
                                count = 1
                                list = []
                                for row in all_sets:
                                    set_id = row[0]
                                    set_text = row[1]
                                    if count == 1: # for the first set
                                        list.append(json.loads('{"text":{"type":"plain_text","text":"%s"},"value":"%s"}' % (set_id + " - " + set_text, set_id)))
                                        count = count + 1
                                    else: #subsequent sets
                                        list.append(json.loads('{"text":{"type":"plain_text","text":"%s"},"value":"%s"}' % (set_id + " - " + set_text, set_id)))
                                        count = count + 1
                                reaction_object["blocks"][0]["element"]["options"] = list
                                json_object["view"] = reaction_object
                                return make_response(jsonify(json_object),200)  
                        else:
                            with open("donotproceed.txt", "r") as reaction_file:
                                reaction_object = json.load(reaction_file)
                                json_object["view"] = reaction_object
                                return make_response(jsonify(json_object),200)
                except Exception as err: # for seeing statistics
                    inputted = payload["view"]["state"]["values"][block_id]["ask_password_stats"]["value"]
                    with open("httprequest.txt", "r") as file:
                        json_object = json.load(file)
                        if inputted == os.environ.get('SET_PASSWORD'):
                            with open("start-stats.txt", "r") as reaction_file:
                                reaction_object = json.load(reaction_file)
                                all_question_id_qur = "SELECT DISTINCT question_id FROM SUBMISSION_LOG"
                                cur.execute(all_question_id_qur)
                                all_question_id = cur.fetchall()
                                count = 1
                                list = []
                                for ques_id in all_question_id:
                                    id = ques_id[0]
                                    set_id_qur = "SELECT * FROM QUESTIONS WHERE question_id = %s" % (id)
                                    cur.execute(set_id_qur)
                                    set_id = cur.fetchall()[0][1]
                                    if count == 1: # for the first set
                                        list.append(json.loads('{"text":{"type":"plain_text","text":"Set %s: %s"},"value":"%s"}' % (set_id, id, id)))
                                        count = count + 1
                                    else: #subsequent sets
                                        list.append(json.loads('{"text":{"type":"plain_text","text":"Set %s: %s"},"value":"%s"}' % (set_id, id, id)))
                                        count = count + 1
                                reaction_object["blocks"][0]["element"]["options"] = list
                                json_object["view"] = reaction_object
                                return make_response(jsonify(json_object),200)  
                        else:
                            with open("donotproceed.txt", "r") as reaction_file:
                                reaction_object = json.load(reaction_file)
                                json_object["view"] = reaction_object
                                return make_response(jsonify(json_object),200)
            else:
                with open("httprequest.txt", "r") as file:
                    json_object = json.load(file)
                    if inputted == "admin1234":
                        with open("createset.txt", "r") as reaction_file:
                            reaction_object = json.load(reaction_file)
                            json_object["view"] = reaction_object
                            return make_response(jsonify(json_object),200)  
                    else:
                        with open("donotproceed.txt", "r") as reaction_file:
                            reaction_object = json.load(reaction_file)
                            json_object["view"] = reaction_object
                            return make_response(jsonify(json_object),200)
        # for the submission of create set details
        elif payload["view"]["blocks"][0]["type"] == "input" and payload["view"]["blocks"][0]["label"]["text"] == "Please input the set id.":
            try:
                set_id_block_id = payload["view"]["blocks"][0]["block_id"]
                set_title_block_id = payload["view"]["blocks"][1]["block_id"]
                set_id = payload["view"]["state"]["values"][set_id_block_id]["set_id"]["value"] 
                set_title = payload["view"]["state"]["values"][set_title_block_id]["set_title"]["value"]
                create_set_qur = "INSERT INTO QUESTION_SET (set_id, set_title, created_date) VALUE ('%s', '%s', NOW());" % (set_id, set_title)
                cur.execute(create_set_qur)
                conn.commit()
            except Exception as e:
                exception = e.args[0]
                if exception == 1062: # duplicate key error
                    with open("httprequest.txt", "r") as file:
                        json_object = json.load(file)
                        with open("duplicateset.txt", "r") as reaction_file:
                            reaction_object = json.load(reaction_file)
                            json_object["view"] = reaction_object
                            return make_response(jsonify(json_object),200)
            return Response()
        # for the submission of set question details
        elif payload["view"]["blocks"][0]["type"] == "input" and payload["view"]["blocks"][0]["label"]["text"] == "Please select the set.":
            try:
                question_id_block_id = payload["view"]["blocks"][1]["block_id"]
                question_id = payload["view"]["state"]["values"][question_id_block_id]["question_id"]["value"]
                set_id_block_id = payload["view"]["blocks"][0]["block_id"]
                set_id = payload["view"]["state"]["values"][set_id_block_id]["static_select-action"]["selected_option"]["value"]
                question_text_block_id = payload["view"]["blocks"][2]["block_id"]
                question_text = payload["view"]["state"]["values"][question_text_block_id]["question_text"]["value"]
                explanation_text_block_id = payload["view"]["blocks"][3]["block_id"]
                explanation_text = payload["view"]["state"]["values"][explanation_text_block_id]["explanation_text"]["value"]
                option1_block_id = payload["view"]["blocks"][4]["block_id"]
                option_1 = payload["view"]["state"]["values"][option1_block_id]["option1"]["value"]
                option2_block_id = payload["view"]["blocks"][5]["block_id"]
                option_2 = payload["view"]["state"]["values"][option2_block_id]["option2"]["value"]
                option3_block_id = payload["view"]["blocks"][6]["block_id"]
                option_3 = payload["view"]["state"]["values"][option3_block_id]["option3"]["value"]          
                option4_block_id = payload["view"]["blocks"][7]["block_id"]
                option_4 = payload["view"]["state"]["values"][option4_block_id]["option4"]["value"]       
                correct_ans_block_id = payload["view"]["blocks"][8]["block_id"]
                correct_ans_but =  payload["view"]["state"]["values"][correct_ans_block_id]["radio_buttons-action"]["selected_option"]["value"]
                insert_ques_qur = "INSERT INTO QUESTIONS (question_id, set_id, ask_rationale, question_text, explanation_text) VALUE ('%s', '%s', '0', '%s', '%s')" % (question_id, set_id, question_text, explanation_text)
                cur.execute(insert_ques_qur)
                conn.commit()
                options_qur = "INSERT INTO OPTIONS (opt_id, question_id, opt_text) VALUES ('%s', '%s', '%s'), ('%s', '%s', '%s'), ('%s', '%s', '%s'), ('%s', '%s', '%s')" % (question_id+".1", question_id, option_1, question_id+".2", question_id, option_2, question_id+".3", question_id, option_3, question_id+".4", question_id, option_4)
                cur.execute(options_qur)
                conn.commit()
                if correct_ans_but == "option1-but":
                    correct_ans = question_id + ".1"
                elif correct_ans_but == "option2-but":
                    correct_ans = question_id + ".2"
                elif correct_ans_but == "option3-but":
                    correct_ans = question_id + ".3"
                elif correct_ans_but == "option4-but":
                    correct_ans = question_id + ".4"
                ans_qur = "INSERT INTO ANSWERS (question_id, answer) VALUES ('%s', '%s')" % (question_id, correct_ans)
                cur.execute(ans_qur)
                conn.commit()
            except Exception as e:
                exception = e.args[0]
                if exception == 1062: # duplicate key error
                    with open("httprequest.txt", "r") as file:
                        json_object = json.load(file)
                        with open("duplicatequestionid.txt", "r") as reaction_file:
                            reaction_object = json.load(reaction_file)
                            json_object["view"] = reaction_object
                            return make_response(jsonify(json_object),200)
            return Response()
        else: 
            return Response()
    else:
        # from any of the options, get the q_id first then the set_id
        any_option_id = payload["view"]["blocks"][0]["accessory"]["options"][0]["value"]
        question_id_qur = "SELECT * FROM OPTIONS WHERE opt_id = %s" % (any_option_id)
        cur.execute(question_id_qur)
        question_id_row = cur.fetchall()
        question_id = question_id_row[0][1]
        set_id_qur = "SELECT * FROM QUESTIONS WHERE question_id = %s" % (question_id)
        cur.execute(set_id_qur)
        set_id_row = cur.fetchall()
        set_id = set_id_row[0][1]

        # get all questions in the set
        all_sets_qur = "SELECT * FROM QUESTIONS WHERE set_id = %s" % (set_id)
        cur.execute(all_sets_qur)
        all_sets_row = cur.fetchall()

        # get the row number of the question shown currently, and the next row(question) to show
        current_row = check_row_number(all_sets_row, question_id)

        if payload["actions"][0]["action_id"] == "next-but":
            get_count_qur = "SELECT COUNT(*) FROM QUESTIONS WHERE set_id = %s" % (set_id)
            cur.execute(get_count_qur)
            get_count_row = cur.fetchall()
            get_count = get_count_row[0][0]
            last_row_no = int(get_count) - 1
            last_row = all_sets_row[last_row_no]
            last_question_id = last_row[0]
            if question_id == last_question_id: # it is the last question
                with open("last.txt", "r") as file:
                    json_object=json.load(file)
                    client.views_push(trigger_id=payload["trigger_id"], view=json_object)
            else:
                next_row_no = int(current_row) + 1
                next_question_id = all_sets_row[next_row_no][0] 
        
                with open("quizmodal.txt", "r") as modalfile:
                    json_object=json.load(modalfile)
                    question_row_qur = "SELECT * FROM QUESTIONS WHERE question_id = %s" % (next_question_id)
                    cur.execute(question_row_qur)
                    question_row = cur.fetchall()
                    question = question_row[0][3]
                    json_object["blocks"][0]["text"]["text"] = "%s. %s" % (str(next_row_no+1),question)
                    option_query = "SELECT * FROM OPTIONS WHERE question_id = %s" % (next_question_id)
                    cur.execute(option_query)
                    option_rows = cur.fetchall()
                    option1 = option_rows[0][0]
                    option2 = option_rows[1][0]
                    option3 = option_rows[2][0]
                    option4 = option_rows[3][0]
                    option1_txt = option_rows[0][2]
                    option2_txt = option_rows[1][2]
                    option3_txt = option_rows[2][2]
                    option4_txt = option_rows[3][2]
                    json_object["blocks"][0]["accessory"]["options"][0]["text"]["text"] = "%s" % (option1_txt)
                    json_object["blocks"][0]["accessory"]["options"][0]["value"] = "%s" % (option1)
                    json_object["blocks"][0]["accessory"]["options"][1]["text"]["text"] = "%s" % (option2_txt)
                    json_object["blocks"][0]["accessory"]["options"][1]["value"] = "%s" % (option2)
                    json_object["blocks"][0]["accessory"]["options"][2]["text"]["text"] = "%s" % (option3_txt)
                    json_object["blocks"][0]["accessory"]["options"][2]["value"] = "%s" % (option3)
                    json_object["blocks"][0]["accessory"]["options"][3]["text"]["text"] = "%s" % (option4_txt)
                    json_object["blocks"][0]["accessory"]["options"][3]["value"] = "%s" % (option4)
                    client.views_update(view_id = payload["view"]["id"], hash = payload["view"]["hash"], view=json_object)

            return Response()
        elif payload["actions"][0]["action_id"] == "previous-but":      
            if current_row == 0: # it is the first question
                with open("first.txt", "r") as file:
                    json_object=json.load(file)
                    client.views_push(trigger_id=payload["trigger_id"], view=json_object)
            else:
                previous_row_no = int(current_row) - 1
                previous_question_id = all_sets_row[previous_row_no][0] 
        
                with open("quizmodal.txt", "r") as modalfile:
                    json_object=json.load(modalfile)
                    question_row_qur = "SELECT * FROM QUESTIONS WHERE question_id = %s" % (previous_question_id)
                    cur.execute(question_row_qur)
                    question_row = cur.fetchall()
                    question = question_row[0][3]
                    json_object["blocks"][0]["text"]["text"] = "%s. %s" % (str(previous_row_no+1),question)
                    option_query = "SELECT * FROM OPTIONS WHERE question_id = %s" % (previous_question_id)
                    cur.execute(option_query)
                    option_rows = cur.fetchall()
                    option1 = option_rows[0][0]
                    option2 = option_rows[1][0]
                    option3 = option_rows[2][0]
                    option4 = option_rows[3][0]
                    option1_txt = option_rows[0][2]
                    option2_txt = option_rows[1][2]
                    option3_txt = option_rows[2][2]
                    option4_txt = option_rows[3][2]
                    json_object["blocks"][0]["accessory"]["options"][0]["text"]["text"] = "%s" % (option1_txt)
                    json_object["blocks"][0]["accessory"]["options"][0]["value"] = "%s" % (option1)
                    json_object["blocks"][0]["accessory"]["options"][1]["text"]["text"] = "%s" % (option2_txt)
                    json_object["blocks"][0]["accessory"]["options"][1]["value"] = "%s" % (option2)
                    json_object["blocks"][0]["accessory"]["options"][2]["text"]["text"] = "%s" % (option3_txt)
                    json_object["blocks"][0]["accessory"]["options"][2]["value"] = "%s" % (option3)
                    json_object["blocks"][0]["accessory"]["options"][3]["text"]["text"] = "%s" % (option4_txt)
                    json_object["blocks"][0]["accessory"]["options"][3]["value"] = "%s" % (option4)
                    client.views_update(view_id = payload["view"]["id"], hash = payload["view"]["hash"], view=json_object)

            return Response()
        else: 
            # verifiying user's response (need to get the option id that the user has pressed + question id of the current question)
            user_response_id = payload["actions"][0]["selected_option"]["value"]
            option_id = payload["view"]["blocks"][0]["accessory"]["options"][0]["value"]
            options_qur = "SELECT * FROM OPTIONS WHERE opt_id = '%s'" % (option_id)
            cur.execute(options_qur)
            option_row = cur.fetchall()
            question_id = option_row[0][1]
            question_qur = "SELECT * FROM QUESTIONS WHERE question_id = '%s'" % (question_id)
            cur.execute(question_qur)
            question_row = cur.fetchall()

            # store students' input
            # 1. retrieve the number of submissions in the system
            cur.execute("SELECT * FROM SUBMISSION_LOG LIMIT 0, 1")
            first_row = cur.fetchall()
            counter = first_row[0][1]
            # 2. adding in this current submission
            slack_id = payload["user"]["id"]
            count = int(counter) + 1
            cur.execute("INSERT INTO SUBMISSION_LOG (submission_id, slack_id, question_id, timestp, rationale) VALUE ('%s', '%s', '%s', NOW(), 'nil')" %(str(count), slack_id, question_id))
            conn.commit()
            cur.execute("INSERT INTO SELECTION_LOG (submission_id, opt_id) VALUE ('%s', '%s')" % (count, user_response_id))
            conn.commit()
            # 3. updating 'count'
            cur.execute("UPDATE SUBMISSION_LOG SET slack_id = '%s' WHERE submission_id = '0'" %(str(count)))
            conn.commit()
            
            answer_query = "SELECT * FROM ANSWERS WHERE question_id = %s" %(question_id)
            cur.execute(answer_query)
            answer_records = cur.fetchall()
            real_answer_id = answer_records[0][1]
            if real_answer_id == user_response_id:
                with open("correct.txt", "r") as file:
                    json_object=json.load(file)
                    client.views_push(trigger_id=payload["trigger_id"], view=json_object)
            else:
                with open("incorrect.txt", "r") as file:
                    json_object=json.load(file)
                    exp = "Explanation: " + question_row[0][4]
                    json_object["blocks"][1]["text"]["text"] = exp
                    client.views_push(trigger_id=payload["trigger_id"], view=json_object)

# only for local development.
if __name__ == '__main__':
 app.run()
