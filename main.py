from flask import *
import pyrebase
import speech_recognition as sr
import pyttsx3
import time 
from pydub import AudioSegment
from pydub.playback import play





config = {
'api stuff'
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
authen = firebase.auth()
db = firebase.database()

app = Flask(__name__)

app.secret_key = "hellosudeep"


def voice(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

    return text 

@app.route('/')
def home(): 
    return render_template('home.html')


@app.route('/result')
def result(): 
    final_res= []
    r = sr.Recognizer()

    suri = True
    
    
    try: 
        while suri:

            song = AudioSegment.from_wav("static/audio testing.wav")
            play(song)
            with sr.Microphone() as source: 
                r.adjust_for_ambient_noise(source, duration=0.2)
                main_l = r.listen(source)
                main_c = r.recognize_google(main_l)
                if main_c == "okay surendra" or main_c == "hello":
                    voice("heyy user what can i do for you")
                    song = AudioSegment.from_wav("static/audio testing.wav")
                    play(song)

                    sec_l = r.listen(source)
                    sec_c = r.recognize_google(sec_l)
                    if sec_c == "do something" or sec_c == "do anything":


                        voice("Do You want to create the user or update the user")
                    
                        listen_text = r.listen(source)
                        start = r.recognize_google(listen_text)
                        if start == "create" or start ==  "create user" or start ==  "create new user" or start ==  "create the user": 
                            song = AudioSegment.from_wav("static/audio testing.wav")
                            play(song)
                            voice("Please say the command to create the user")
                            time.sleep(2)
                            listen_text1 = r.listen(source)
                            output = f"{r.recognize_google(listen_text1)}"
                            for i in output.split(" "): 
                                final_res.append(i)
                            username = final_res[0]
                            if final_res[1] == "debit":
                                data = {
                                        'debited' : final_res[2],
                                        'credited' : 'null',
                                        'username' : username
                                    }

                                db.child(username).child('status').set(data)
                                msg = f"{username} is updated in {final_res[1]} with {final_res[2]}"
                                voice(msg)
                                song = AudioSegment.from_wav("static/audio testing.wav")
                                play(song)
                                details = db.child(username).child('status').get()
                                return render_template('home.html', details= details)
                            elif final_res[1] == "credit":


                                data = {
                                    'debited' : 'null',
                                    'credited' : final_res[2],
                                    'username' : username
                                }
                                db.child(username).child('status').set(data)
                                msg = f"{username} is updated in {final_res[1]} with {final_res[2]}"
                                voice(msg)
                                song = AudioSegment.from_wav("static/audio testing.wav")
                                play(song)
                                details = db.child(username).child('status').get()
                                return render_template('home.html', details = details)

                        elif start == "update" or start ==  "update user" or start ==  "update the user": 
                            song = AudioSegment.from_wav("static/audio testing.wav")
                            play(song)
                            voice("Please say the Update command to update the user")

                            time.sleep(2)
                            listen_text2 = r.listen(source)
                            output = f"{r.recognize_google(listen_text2)}"
                            for i in output.split(" "): 
                                final_res.append(i)
                            username = final_res[0]

                            user = db.child(username).get()

                            if user: 

                                if final_res[1] == "debit" or final_res[1] == "debited": 

                                    db.child(username).child('status').update({'debited' : final_res[2]})

                                    voice("Successfully updated")
                                    song = AudioSegment.from_wav("static/audio testing.wav")
                                    play(song)
                                    details = db.child(username).child('status').get()
                                    return render_template('home.html', details = details)

                                elif final_res[1] == "credit" or final_res[1] == "credited": 

                                    db.child(username).child('status').update({'credited' : final_res[2]})

                                    voice("Successfully updated")
                                    song = AudioSegment.from_wav("static/audio testing.wav")
                                    play(song)
                                    details = db.child(username).child('status').get()
                                    return render_template('home.html', details = details)

                            else: 
                                voice("No User Found")

                                return render_template('home.html', msg = "No User Found")

                    elif sec_c == "update name" or sec_c == "update username": #old_username to new_username
                        

                        voice("Please tell me the command to update the username")

                        song = AudioSegment.from_wav("static/audio testing.wav")
                        play(song)

                        update_n = r.listen(source)
                        output = f"{r.recognize_google(update_n)}"
                        for i in output.split(" "): 
                            final_res.append(i)

                        old_username = final_res[0]

                        new_username = final_res[2]

                        user = db.child(old_username).get()

                        if user: 

                            db.child(old_username).child('status').update({'username' : new_username})

                            voice("Updated the name successfully")

                            details = db.child(old_username).child('status').get()

                            return render_template('home.html', details = details)

                        else: 
                            voice("no user found")

                            return render_template('home.html', msg = "No User Found")

                    elif sec_c == "details": 
                        voice("Please tell the command") #details of username

                        song = AudioSegment.from_wav("static/audio testing.wav")
                        play(song)

                        details = r.listen(source)
                        output = f"{r.recognize_google(details)}"
                        for i in output.split(" "): 
                            final_res.append(i)

                        user_details = db.child(final_res[2]).child('status').get() 

                        if user_details:
                            voice("user exits")
                            for a,b in user_details.val().items(): 
                                if a != "username":
                                    voice(f"{a} amount is {b}")
                                else:
                                    voice(f"for the user {b}")
                            return render_template("home.html", details = user_details)

                        else: 
                            voice("user dont exist")
                            return render_template("home.html", msg = "user dont exist")


                else:

                    return render_template('home.html', msg = "unsuccessfull")
                








        

    except: 
        msg = "Voice Not Clear...Please speak again"
        return render_template('home.html', message = msg)



if __name__ == "__main__": 
    app.run(debug = True)
