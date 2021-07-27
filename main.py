from flask import *
import speech_recognition as sr

app = Flask(__name__)

@app.route('/')
def home(): 
    return render_template('home.html')


@app.route('/result')
def result(): 
    final_res= []
    r = sr.Recognizer()
    with sr.Microphone() as source: 

        
        listen_text = r.listen(source)
        try: 
            output = f"{r.recognize_google(listen_text)}"
            for i in output.split(" "): 
                final_res.append(i)

            if final_res[0] == "save" or final_res[0] == "delete": 
                msg = output
                return render_template('home.html', msg = msg)
            else: 
                msg = "Command invalid" 
                return render_template('home.html', message = msg)

            

        except: 
            msg = "Voice Not Clear...Please speak again"
            return render_template('home.html', message = msg)



if __name__ == "__main__": 
    app.run(debug = True)