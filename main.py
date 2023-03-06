import sqlite3
from flask import Flask, request, g, render_template, send_file

DATABASE = '/tmp/db.example'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

def commit():
    get_db().commit()

@app.route("/")
def hello():
    execute_query("DROP TABLE IF EXISTS userstable")
    execute_query("CREATE TABLE userstable (firstname text, lastname text, email text)")
    return render_template('index.html')

@app.route('/startenquiry', methods=['POST', 'GET'])
def startinquiry():
    message = ''

    if request.method == 'POST' and request.form.get('ufname') and request.form.get('ulname') and request.form.get('mail'):
        firstname = request.form['ufname']
        lastname = request.form['ulname']
        email = request.form['mail']
        execute_query("INSERT INTO userstable (firstname, lastname, email) VALUES (?, ?, ?)", (firstname, lastname, email))
        commit()

    elif request.method == 'POST':
        message = 'Please make sure you fill all feilds in the page.'

    return render_template('Chat.html', message=message)

ChatWindowHTMLFirst = """

<!DOCTYPE html>
<html>
    <title>College Inquiry Chabot</title>
    <head>
        <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700" rel="stylesheet">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.1/css/all.css" integrity="sha384-5sAR7xN1Nv6T6+dT2mhtzEpVJvfS3NScPQTrOxhwjIuvcA67KV2R5Jz6kr4abQsz" crossorigin="anonymous">
        <style>
            html, body {{
                display: flex;
                justify-content: center;
                font-family: Roboto, Arial, sans-serif;
                font-size: 15px;
            }}
            form {{
                border: 5px solid #f1f1f1;
            }}
            input[type=text], input[type=password] {{
                width: 100%;
                padding: 16px 8px;
                margin: 8px 0;
                display: inline-block;
                border: 1px solid #ccc;
                box-sizing: border-box;
            }}
            .icon {{
                font-size: 110px;
                display: flex;
                justify-content: center;
                color: #FF0000;
            }}
            .send-button {{
                background-color: #FF0000;
                color: white;
                padding: 12px 0;
                margin: 10px 0;
                border: none;
                cursor: grab;
                width: 12%;
            }}
            .end-button {{
                background-color: #000000;
                color: white;
                padding: 4px 0;
                margin: 2px 0;
                border: none;
                cursor: grab;
                width: 24%;
            }}
            h1 {{
                text-align:center;
                font-size: 28px;
                color: #FF0000;
            }}
            button:hover {{
                opacity: 0.8;
            }}
            .formcontainer {{
                text-align: center;
                margin: 24px 50px 12px;
            }}
            .text-box {{
                font-size: 16px;
                display: flex;
                width: 100%;
            }}
            .container {{
                padding: 16px 0;
                text-align:left;
            }}
            span.psw {{
                float: right;
                padding-top: 0;
                padding-right: 15px;
            }}
            /* Change styles for span on extra small screens */
            @media screen and (max-width: 300px) {{
                span.psw {{
                    display: block;
                    float: none;
                }}
            }}
            label {{
                color: #000000;
            }}
            strong {{
                color: #FF0000;
            }}
        </style>
    </head>
    <body>
        <form {{url_for('chatbotsystem')}} method="POST">
            <h1>College Inquiry Chabot</h1>
            <div class="formcontainer">
          <div class="container">
           <label for="ufname"><strong>Hi!! Welcome to college inquiry portal</strong></label></br></br>
    	  <label for="ufname"><strong>Choose your questions from below list</strong></label></br>
    	  <label for="ufname"><strong>1.Does the college have a football team?</strong></label></br>
    	  <label for="ufname"><strong>2.Does it have Computer Science Major?</strong></label></br>
    	  <label for="ufname"><strong>3.What is the in-state tuition?</strong></label></br>
    	  <label for="ufname"><strong>4.Does its have on campus housing?</strong></label></br>
    """
ChatWindowHTMLLast = """
    </div>
    	<div class="text-box">
            <input type="text" name="question" id="message" autocomplete="off" placeholder="Type your Question Number here">
    	  <input class="send-button" type="submit" value=">">
          </div>
           <a href='/endchat' align='center'">End Chat</a>
    	</div>
        </form>
      </body>
    </html>
    """


@app.route('/chatbotsystem', methods =['GET', 'POST'])
def chatbotsystem():
    global ChatWindowHTMLFirst
    ChatWindowHTMLMiddle = ''
    if request.method == 'POST' and str(request.form['question']) !="":
        questionasked = str(request.form['question'])
        if(questionasked == "Does the college have a football team" or questionasked == "1"):
            ChatWindowHTMLMiddle="""
            </br><label for="ufname" style="color:blue;"><strong>"""+questionasked+"""</strong></label></br>
            <label for ="ufname"><strong style="color:black;"> Yes, it has a football team and is one of the most popular university teams across the country. Go BearCats! </strong></label></br>            """
        elif(questionasked == "Does it have Computer Science Major?" or questionasked == "2"):
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong style="color:black;">Yes, it has a Computer Science major. You can find the details <a href="https://ceas.uc.edu/academics/departments/computer-science.html">here</a>.</strong></label></br>            """
        elif (questionasked == "What is the in-state tuition?" or questionasked == "3"):
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong style="color:black;">The in-state tuition differs from course to course. For more details, visit <a href="https://www.uc.edu/about/financial-aid/starting/costs/costs-2023.html">UC Costs 2022-2023</a>.</strong></label></br>
            """
        elif (questionasked == "Does its have on campus housing?" or questionasked == "4"):
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong style="color:black;">Yes, you can contact UC Residential and Development to book a room according to your choice three months in advance.</strong></label></br>
            """
        else:
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong style="color:black;">We cannot answer your question at the moment. For more details, visit <a href="https://www.uc.edu/">UC.edu</a>.</strong></label></br>
            """
    ChatWindowHTMLFirst=ChatWindowHTMLFirst + ChatWindowHTMLMiddle
    return ChatWindowHTMLFirst+ChatWindowHTMLLast

EndChatHTMLFirst="""
<!DOCTYPE html>
<html>
  <title>Session Closed</title>
  <head>
    <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700" rel="stylesheet">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.1/css/all.css" integrity="sha384-5sAR7xN1Nv6T6+dT2mhtzEpVJvfS3NScPQTrOxhwjIuvcA67KV2R5Jz6kr4abQsz" crossorigin="anonymous">
    <style>
      html, body {
        display: flex;
        justify-content: center;
        font-family: Roboto, Arial, sans-serif;
        font-size: 15px;
      }
      form {
        border: 5px solid #f1f1f1;
      }
      input[type=text], input[type=password] {
        width: 100%;
        padding: 16px 8px;
        margin: 8px 0;
        display: inline-block;
        border: 1px solid #ccc;
        box-sizing: border-box;
      }
      .icon {
        font-size: 110px;
        display: flex;
        justify-content: center;
        color: #FF0000;
      }
      .send-button {
        background-color: #FF0000;
        color: white;
        padding: 12px 0;
        margin: 10px 0;
        border: none;
        cursor: grab;
        width: 12%;
      }
      .end-button {
        background-color: #FF0000;
        color: white;
        padding: 12px 0;
        margin: 10px 0;
        border: none;
        cursor: grab;
        width: 12%;
      }
      h1 {
        text-align:center;
        fone-size:18;
        color: #FF0000;
      }
      button:hover {
        opacity: 0.8;
      }
      .formcontainer {
        text-align: center;
        margin: 24px 50px 12px;
      }
      .text-box {
        font-size: 16px;
        display: flex;
        width: 100%;
      }
      .container {
        padding: 16px 0;
        text-align:left;
      }
      span.psw {
        float: right;
        padding-top: 0;
        padding-right: 15px;
      }
      /* Change styles for span on extra small screens */
      @media screen and (max-width: 300px) {
        span.psw {
          display: block;
          float: none;
        }
      }
      label {
        color: #000000;
      }
    </style>
  </head>
  <body>
    <form>
      <h1>Chat Session Closed</h1>
      <div class="icon">
        <img src="ChatClosed.jpg"></img>
      </div>
      <div class="formcontainer">
        <div class="container">
          <label for="ufname"><strong style="color:#FF0000;">Hope your Questions are answered!!</strong></label></br></br>
"""
EndChatHTMLLast="""
 </div>
	</div>
    </form>
  </body>
</html>
"""

@app.route("/endchat")
def endchat():
    global ChatWindowHTMLFirst
    ChatWindowHTMLFirst = """
        <!DOCTYPE html>
        <html>
          <title>College Inquiry Chatbot</title>
          <head>
            <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700" rel="stylesheet">
            <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.1/css/all.css" integrity="sha384-5sAR7xN1Nv6T6+dT2mhtzEpVJvfS3NScPQTrOxhwjIuvcA67KV2R5Jz6kr4abQsz" crossorigin="anonymous">
            <style>
              html, body {
                display: flex;
                justify-content: center;
                font-family: Roboto, Arial, sans-serif;
                font-size: 15px;
              }
              form {
                border: 5px solid #F44336;
              }
              input[type=text], input[type=password] {
                width: 100%;
                padding: 16px 8px;
                margin: 8px 0;
                display: inline-block;
                border: 1px solid #ccc;
                box-sizing: border-box;
              }
              .icon {
                font-size: 110px;
                display: flex;
                justify-content: center;
                color: #F44336;
              }
              .send-button {
                background-color: #F44336;
                color: white;
                padding: 12px 0;
                margin: 10px 0;
                border: none;
                cursor: pointer;
                width: 12%;
              }
        	  .end-button {
                background-color: #000000;
                color: white;
                padding: 4px 0;
                margin: 2px 0;
                border: none;
                cursor: pointer;
                width: 24%;
              }
              h1 {
                text-align:center;
                font-size: 28px;
                color: #F44336;
              }
              button:hover {
                opacity: 0.8;
              }
              .formcontainer {
                text-align: center;
                margin: 24px 50px 12px;
              }
        	  .text-box {
                font-size: 16px;
                display: flex;
                width: 100%;
              }
              .container {
                padding: 16px 0;
                text-align:left;
                color: #000000;
              }
              span.psw {
                float: right;
                padding-top: 0;
                padding-right: 15px;
              }
              /* Change styles for span on extra small screens */
              @media screen and (max-width: 300px) {
                span.psw {
                  display: block;
                  float: none;
                }
              }
            </style>
          </head>
          <body>
            <form {{url_for('chatbotsystem')}} method="POST">
              <h1>College Inquiry Chatbot</h1>
              <div class="icon">
        	 <i class="fas fa-user-circle"></i>
              </div>
              <div class="formcontainer">
              <div class="container">
             <label for="ufname"><strong style="color: #F44336;">Hi!! Welcome to the College Inquiry Portal</strong></
        	  <label for="ufname"><strong>Choose your questions from below list</strong></label></br>
        	  <label for="ufname"><strong>1.Does the college have a football team?</strong></label></br>
        	  <label for="ufname"><strong>2.Does it have Computer Science Major?</strong></label></br>
        	  <label for="ufname"><strong>3.What is the in-state tuition?</strong></label></br>
        	  <label for="ufname"><strong>4.Does its have on campus housing?</strong></label></br>
        """
    result = execute_query("""SELECT firstname,lastname,email  FROM userstable""")
    if result:
        for row in result:
            Userdetails=row[0]+","+row[1]+","+row[2]
    EndChatHTMLMiddle="""
    User Details - <br>
    <label for="ufname"><strong>"""+Userdetails+"""</strong></label></br></br>
    Chatbox Creator - <br>
    <label for="ufname"><strong>This chatbot is created by Bhavana Garapati [garapabv@mail.uc.edu] from University of Cincinnati</strong></label></br></br>
    <br>
    <br>
    <label for="ufname"><strong style="color:#FF0000;">Thank you for talking with us, for more details visit <a href="https://www.uc.edu/" style="color:#000000;">UC.edu.</a></strong></label><br><br"""
    return EndChatHTMLFirst+EndChatHTMLMiddle+EndChatHTMLLast

if __name__ == '__main__':
  app.run()
