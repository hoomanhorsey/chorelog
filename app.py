import os
import random
import cs50

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

#for calcuating date calculations
#import datetime
from datetime import timedelta, date, datetime 

from flask_mail import Mail, Message

# Configure application
app = Flask(__name__)

#Adding environmental variable

# Configure mail
# Requires that "Less secure app access" be on
# https://support.google.com/accounts/answer/6010255

# See bitwarden for .env file login details, including app password for gmail.

# Mail config. login details saved in .env file
app.config["MAIL_DEFAULT_SENDER"] = os.environ["MAIL_DEFAULT_SENDER"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config['MAIL_USE_SSL'] = False
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
mail = Mail(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter# TODO DON"T NEED
##app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
db = cs50.SQL("postgresql://postgres:"+POSTGRES_PASSWORD+"@db."+POSTGRES_HOST+".supabase.co:5432/postgres")  

# SHARED FUNCTIONS

def passwordcheck(newpassword): # checks password has special chars
    counter = 0
    passwordlength = len(newpassword)
    for c in newpassword:
        for d in c:
            if d.isdigit() == True:
                counter += 1
            if d.isalpha() == True:
                counter += 1
            if d.isspace() == True:
                return apology("Please provide a password without spaces", 400)
        if (counter == passwordlength):
            return apology("Please provide a password with at least one special character", 400)

def displaydate(index): # caculate display dates in day/month/year format
    for e in index:
        displaydate = datetime.strptime(e['date'], "%Y-%m-%d").date() #converting string date to date object.
        
        displaydate = displaydate.strftime("%d %B %Y") # converting date object to display format.
        e['displaydate'] = displaydate
    return index


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Please provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Please provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM t_user WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in, and their houseid
        session["user_id"] = rows[0]["id"]
        session["houseid"] = rows[0]["houseid"]
        session["username"] = rows[0]["username"]
            
        #Query database for chorelistid
        chorelistid = db.execute("SELECT chorelistid FROM t_reg WHERE id = ?", session["houseid"])
        session["chorelist"] = chorelistid[0]["chorelistid"]

        print('session chorelist')
        print(session['chorelist'])

        # Updating db to include login and previous login dates.
        dateprev = db.execute("SELECT datelogin FROM t_user WHERE id = ?", session["user_id"])
        today = str(date.today())
        db.execute("UPDATE t_user SET datelogin = ?, dateprev = ? WHERE id = ?", today, dateprev[0]['datelogin'], session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

@app.route("/regcode", methods=["GET", "POST"])
def regcode():
    """Register code"""

    # Forget any user_id    
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        regcode = request.form.get("regcode")

        # Ensure user has a valid registration code
        regcodes = db.execute("SELECT regcode FROM t_reg")
        for r in regcodes:
            if regcode == r['regcode']:
                break
        else:
            return apology("Sorry. Your registration code is invalid. Please email chorelog@gmail.com for an updated code to proceed.", 400)

        session["regcode"] = regcode

        return redirect("/register")

    else:
        return render_template("regcode.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Sign up"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if (not request.form.get("address") or not request.form.get("email")):
            return apology("Please provide an address and email", 403)

        if  (6 > len(request.form.get("address"))):
            return apology("If you are providing a house 'nick name' could you please ensure it is longer than six characters", 403)

        address = request.form.get("address")
        email = request.form.get("email")

        randomnum =  str(random.random())
        randomnum = randomnum[2] + randomnum[3] + randomnum[4] + randomnum[5] + randomnum[6] + randomnum[7]

        db.execute("INSERT into t_reg (regcode, address) VALUES (?, ?)", randomnum, address)

        # Send email msg
        msg = Message('Thank you for signing up to Chore Log!', recipients = [email])
        msg.body = "Thank you for signing up to Chore Log.\r\n\r\nYour registration code is '" + randomnum + "'. \r\n\r\nYour registration code will be used to create a house profile for '" +address+ "'.\r\n\r\nThis code is tied to '" +address+ "'. Share it with others who live (or spend a lot of time) at '" +address+ "' so they can also begin logging their chores.\r\n\r\nGo to " +'https://chorelog.onrender.com/regcode'+" to create your Chore Log profile.\r\n"
        mail.send(msg)

        # extracting chorelist number from t.reg for new houseprofile
        # creating a new table, named by reference to chorelistnumber, using 'u' prefix to distinguish from tables.
        # maybe copy an existing table that is already default?

        chorelistnumber = db.execute("SELECT chorelist FROM t_reg WHERE regcode = ?", randomnum)
               

        #db.execute("CREATE TABLE u_houselist_? (id INT, chorecategory VARCHAR(255), chore VARCHAR(255), choreid INT)", chorelistnumber[0]['chorelist'])                
        # Creating by copying, one command
        db.execute("CREATE TABLE u_chorelist_? AS SELECT * FROM t_choresdefault", chorelistnumber[0]['chorelist'])

        #create by copying, 2 commands
        #db.execute("CREATE TABLE u_chorelist_? LIKE t_choresdefault", chorelistnumber[0]['chorelist'])
        #db.execute("INSERT INTO u_chorelist_? SELECT * FROM t_choresdefault", chorelistnumber[0]['chorelist'])



        #created table but don't know where it exists!


        return redirect("/regcode")

    else:
        return render_template("signup.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        regcode = session['regcode']

        username = request.form.get("username")
        color = request.form.get("color")
        newpassword = request.form.get("password")
        passwordconfirm = request.form.get("confirmation")
        email = request.form.get("email")

        # Ensure username was submitted
        if not username:
            return apology("Please provide username", 400)

        # Ensure password was submitted
        elif not newpassword or not passwordconfirm:
            return apology("Please provide a password", 400)

        elif not email:
            return apology("Please provide your email address", 400)

        # Check password has special characters, using defined function. If password doesn't have special chars it fills the apology variable, if not the apology variable is empty and no apology is returned.
        nosymbols = passwordcheck(newpassword)
        if nosymbols != None:
            return apology("Please include a special character in y our password", 400)

        # Password confirmation must match password
        elif newpassword != passwordconfirm:
            return apology ("Passwords do not match. Please try again.", 400)

        # Check to see if username already exists
        existingusernames = db.execute("SELECT username FROM t_user")
        for x in existingusernames:
            if x["username"] == username:
                return apology("Username is already being used. Please choose another.", 400)

        today = date.today()

        #extract houseid and address
        houseprofile = db.execute("SELECT id, address FROM t_reg WHERE regcode = ?", regcode)

        # Insert user and password (hashed) into databse
        hash = generate_password_hash(newpassword, method='pbkdf2:sha256', salt_length=8)
        db.execute("INSERT INTO t_user (username, hash, email, datelogin, dateprev, color, houseid, address) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", username, hash, email, today, 0, color, houseprofile[0]['id'], houseprofile[0]['address'])

        #storing the houseid in a session
        print(houseprofile[0]['id'])
        session['houseid'] = houseprofile[0]['id']
        print('session', session['houseid'])

        # Send email msg
        msg = Message('You are registered with Chore Log!', recipients = [email])
        msg.body = "Hi " + username + ". Congratulations on registering with Chore Log. Chore log takes the chore out of logging chores."
        mail.send(msg)

        return render_template("login.html")

    else:

        # getting regcode to determine id, which then allows dropdown menu to determine which colors are available.
        regcode = session['regcode']
        household = db.execute("SELECT id, address FROM t_reg WHERE regcode = ?", regcode)
        house = household[0]['address']

        # Creates a hardcoded list of colours, but then extracts user colours from db.
        # Compares colours in db to hard coded colours and creates a revised list of colours that can be used for the colour selection drop down menu in registration
        colors = [{'color':'DODGERBLUE'}, {'color':'CYAN'}, {'color':'GREEN'}, {'color':'GOLD'}, {'color':'LIME'}, {'color':'MAGENTA'}, {'color':'MAROON'}, {'color':'PINK'}, {'color':'PURPLE'}, {'color':'VIOLET'}, {'color':'RED'}, {'color':'SALMON'}]
        dbcolor = db.execute("SELECT color FROM t_user JOIN t_reg ON t_user.houseid = t_reg.id WHERE regcode = ?", session['regcode'])
        revisedcolors = []
        for c in colors:
            temp = 0
            for d in dbcolor:
                if c['color'] == d['color']:
                    temp += 1
                    break
            if temp == 0:
                revisedcolors.append({'color':c['color']})

        return render_template("register.html", house=house, revisedcolors=revisedcolors)

@app.route("/account", methods=["GET", "POST"])
def account():
    """Change password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Redirect to retire page.  Placed in front of password change as it only takes one value and then redirects.
        # If put at the end it causes an error as it searches for more values, which aren't given.
        retire = request.form.get("retire")
        if retire == "retire":
            return redirect("/retire")

        #Password change
        oldpassword = request.form.get("oldpassword")
        newpassword = request.form.get("newpassword")
        confirmpassword = request.form.get("confirmpassword")

        # Ensure password was submitted
        if (not oldpassword) or (not newpassword) or (not confirmpassword):
            return apology("Please provide old password and/or new password", 400)

        # Check password has special characters, using defined function
        apology = passwordcheck(newpassword)
        if apology != None:
            return apology

       # Password confirmation must match password
        if newpassword != confirmpassword:
            return apology ("Passwords do not match. Please try again.", 400)

        # Insert user and password (hashed) into databse
        hash = generate_password_hash(newpassword, method='pbkdf2:sha256', salt_length=8)
        db.execute("UPDATE t_user SET hash = ? WHERE id = ?", hash, session["user_id"])

        return render_template("login.html")

    return render_template("account.html")

@app.route("/retire", methods=["GET", "POST"])
def retire():
    """Retire account"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Extract password values from form
        newpassword = request.form.get("newpassword")
        confirmpassword = request.form.get("confirmpassword")

        # Ensure password was submitted
        if (not newpassword) or (not confirmpassword):
            return apology("Please provide yourpassword", 400)

       # Password confirmation must match password
        if newpassword != confirmpassword:
            return apology ("Passwords do not match. Please try again.", 400)

        # extracts username from session id
        usernamedb = db.execute("SELECT username FROM t_user WHERE id = ?", session["user_id"])
        username = usernamedb[0]['username']

        # changes username to retired, and password to non-hashable password
        db.execute("UPDATE t_user SET username = ?, hash = '!DELETED!' WHERE id = ?", username + " (Retired)", session["user_id"])

        # Forget any user_id
        session.clear()
        return redirect("/")

    return render_template("retire.html")

@app.route("/")
@login_required
def index():
    """Show home of chores"""

    # extract chores, but maximum date, and grouped, so that is only one entry from each category, filtered by houseid.
    index = db.execute ("SELECT chorecategory, chore, username, MAX(date) AS date, color FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.id WHERE houseid = ? GROUP by chorecategory, chore, username, color ORDER BY chorecategory", session['houseid'])

    # Calculating date of previous log in.
    previouslog = db.execute ("SELECT dateprev FROM t_user WHERE id = ?", session["user_id"])
    if not previouslog:
        print('no users in db') #included as a safety for when the db is empty
    else:
        previouslog = previouslog[0]['dateprev']

    # Exctracts todays date + time. Note, now using function that calls the date only so you don't need to strip out the time....TODO
    todaydate = date.today()

    # Calculating 'days since' using today's date, then converting date from string to date object to calculate, then converting back to string to display
    # But also inserting '0 days' as a display  value if the date is less than 1 full day.
    for d in index:
        choredate = datetime.strptime(d['date'], "%Y-%m-%d").date()
        difference = (todaydate - choredate) # sum of calculation includes seconds....
        oneday = timedelta(days = 1)
        if difference < oneday:
            d['daysdifference'] = '0 days'
        else:
            difference = str(difference) # because 'difference' includes seconds, need to cast it as a string to extract seconds.
            difference = difference.split(",", 1)  # split string after comma into 2 lists, to retain only '# days'
            difference = difference[0] #extract first item of list, which is 'days'
            d['daysdifference'] = difference

    # Function to caculate display dates in day/month/year format
    index = displaydate(index)

    # Extracting username of current user for display
    currentuser = session['username']
    #renders index template
    return render_template("index.html", index=index, currentuser=currentuser, previouslog=previouslog)

@app.route("/historyfull", methods=["GET", "POST"])
@login_required
def historyfull():
    """Show full history of chores"""
    if request.method == "POST":

        # Uses values from form to sort SQL call. SQL variables are used for values, not column names - must reformat as string.
        sort = request.form.get("sort")
        # sorting tree imposes order on the remainder of the sort, after the initial primary value is chosen
        if sort == 'chorecategory':
            index = db.execute("SELECT * FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.id WHERE houseid = ? ORDER BY {}, chore ASC, date DESC".format(sort), session['houseid'])
        elif sort == 'chore':
            index = db.execute("SELECT * FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.id WHERE houseid = ? ORDER BY {}, chorecategory ASC, date DESC".format(sort), session['houseid'])
        elif sort == 'username':
            index = db.execute("SELECT * FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.id WHERE houseid = ? ORDER BY {}, chorecategory ASC, chore ASC, date DESC".format(sort), session['houseid'])
        elif sort == 'date DESC':
            index = db.execute("SELECT * FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.id WHERE houseid = ? ORDER BY {}, chorecategory ASC, chore ASC".format(sort), session['houseid'])
        elif sort == 'none':
            return apology ("You've not chosen anything. Please make a choice.", 400)

        # Function to caculate display dates in day/month/year format
        index = displaydate(index)

        currentuser = session['username']

        #renders historyfull template
        return render_template("historyfull.html", index=index, currentuser=currentuser)

    else:
        #users = db.execute("SELECT username FROM t_user")
        index = db.execute("SELECT * FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.id WHERE houseid = ? ORDER BY chorecategory ASC, chore ASC, date DESC", session['houseid'])

        # Function to caculate display dates in day/month/year format
        index = displaydate(index)

        currentuser = session['username']

        #renders historyfull template
        return render_template("historyfull.html", index=index, currentuser=currentuser)

@app.route("/chorebyuser", methods=["GET", "POST"])
@login_required
def chorebyuser():
    """Show history of chores"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Extract data from form
        user = request.form.get("user")
        fromdate = request.form.get("fromdate")
        todate = request.form.get("todate")

        #SQL QUERY TO LIMIT ITEMS BY DATE"
        index = db.execute("SELECT chorecategory, chore, username, date, color FROM (SELECT * FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.id WHERE date BETWEEN ? AND ? ORDER by date DESC) AS datesubquery WHERE username = ?", fromdate, todate, user)

        # Function to caculate display dates in day/month/year format
        index = displaydate(index)

        #calls function to add current user from session id
        currentuser = session['username']

        # calling users to populate drop down
        users = db.execute("SELECT username, color FROM t_user WHERE houseid = ?", session['houseid'])
        alert = "history" # An alert to let the template know whether or not to display the table.

        return render_template("chorebyuser.html", alert=alert, index=index, currentuser=currentuser, users=users)

    else:

        users = db.execute("SELECT username, color FROM t_user WHERE houseid = ?", session['houseid'])

        currentuser = session['username']

        return render_template("chorebyuser.html", currentuser=currentuser, users=users)

@app.route("/fame", methods=["GET"])
@login_required
def fame():
    """Show hall of fame"""

    ##Extract chores, but maximum date, and grouped so only one item from each category, to create a list of chores that have been completed
    choreindex = db.execute ("SELECT chore FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.id WHERE houseid = ? GROUP by chorecategory, chore ORDER BY chorecategory", session['houseid'])

    index = [] #declares list to be populated.

    # SQL select does the heavy lifting. Via each 'chore' it selects the top 3 chores, if there are 3
    for i in choreindex:
        sample = db.execute("SELECT chorecategory, chore, username, date, color FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.id WHERE chore = ? ORDER BY date DESC LIMIT 3", i['chore'])
        if (len(sample) == 3) and (sample[0]['username'] == sample[1]['username'] == sample[2]['username']): #checks if there are 3 entries, and if they all have the same name
            index = index + sample #if they past these tests, then they are 3 in a row and are added to the index for printing!

    # Function to caculate display dates in day/month/year format
    index = displaydate(index)

    currentuser = session['username']

    #renders chorebyuser template
    return render_template("fame.html", currentuser=currentuser, index=index)

@app.route("/logchore", methods=["GET", "POST"])
@login_required
def logchore():
    """Log completion of a chore"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # GET INFO FROM USER
        chorecategory = request.form.get("chorecategory")
        chore = request.form.get("chore")
        date = request.form.get("date")

        if chore == "":
            return apology("You haven't selected a chore to log", 400)

        # checks that a chore hasn't been entered twice for the same date.
        datecheck = db.execute("SELECT chorecategory, chore, date FROM t_ledger JOIN t_user ON t_user.id = t_ledger.userid WHERE houseid = ?", session['houseid'])
        for x in datecheck:
            if date == x['date'] and chorecategory == x['chorecategory'] and chore == x['chore']:
                return apology("It seems this chore has already been logged for this date. Nice try but TRY HARDER!", 400)

        # inserts chore into db
        db.execute("INSERT INTO t_ledger (userid, chorecategory, chore, date) VALUES(?, ?, ?, ?)", session["user_id"], chorecategory, chore, date)

        # preparing variable for display of confirmation
        confirm = [{'chorecategory': chorecategory, 'chore': chore, 'displaydate': date}]

        ##Extract chores, but maximum date, and grouped so only one item from each category,
        index = db.execute ("SELECT t_user.id, chorecategory, chore, username, MAX(date) AS date FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.id GROUP by chorecategory, chore, username, t_user.id ORDER BY chorecategory")

        currentuser = session['username']

        # creates alert variable to trigger summary alert for template
        alert = "logged"

        #renders index template
        return render_template("logchore.html", alert=alert, currentuser=currentuser, confirm=confirm)

    ## User reached route via GET (as by clicking a link or via redirect)
    else:

        currentuser = session['username']

        # extracts chores
        index = db.execute("SELECT t_user.id, chorecategory, chore, username, date FROM t_ledger INNER JOIN t_user ON t_user.id = t_ledger.userid ORDER BY chorecategory")
        print('****index*****')
        print(index)


        housecustom = db.execute("SELECT t_choresdefault.chorecategory, STRING_AGG(u_chorelist_20.choreid, ',') as choreid FROM u_chorelist_20 JOIN t_choresdefault ON u_chorelist_20.id = t_choresdefault.choreid GROUP BY t_choresdefault.chorecategory ORDER BY t_choresdefault.chorecategory ")
        
        print('housecustom')
        print(type(housecustom))
        print(type(housecustom[0]['choreid']))

        print(housecustom)

        for c in housecustom:
            c['choreid'] = c['choreid'].split(',')
            c['choreid'] = [int(i) for i in c['choreid']]
            print(type(c['choreid']))
            print(type(c['choreid'][0]))
            print(c)
        
        print('****housecustom*****')
        print(housecustom)
        #dbresult = db.execute("SELECT t_chores.id, t_chores.chorecategory, GROUP_CONCAT(t_chores.chore) as chore, GROUP_CONCAT(t_chores.id) FROM t_chores join t_houseselection on t_chores.id = t_houseselection.id WHERE t_houseselection.houseid = 1 GROUP BY chorecategory ORDER BY chorecategory, chore ASC")
       
        #for i in dbresult:
        #    i['chore'] = sorted(i['chore'].split(','))  # changes string into a list, split by ',', then sorts a-z
           
        choredefault = db.execute("SELECT t_choresdefault.id, t_choresdefault.chorecategory, t_choresdefault.chore FROM t_choresdefault ORDER BY chorecategory, chore ASC")
        print('*******choredefault********')
        print(choredefault)
        return render_template("logchore.html", housecustom = housecustom, choredefault = choredefault, index=index, currentuser=currentuser)

@app.route("/about", methods=["GET"])
def about():
    
    return render_template("about.html")



@app.route("/custom", methods=["GET", "POST"])
@login_required
def custom():

    if request.method == "POST":

        choredefault = db.execute("SELECT t_choresdefault.id, t_choresdefault.chorecategory, t_choresdefault.chore FROM t_choresdefault ORDER BY chorecategory, chore ASC")

        #print('housecustom')
        #print(housecustom)
        
        ## test housecustom variable. it works. 
        ##housecustom = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 9, 20, 21, 22]

        housecustom = request.form.keys()
        #print(key,val)
        housecustom = sorted(list(housecustom))
        housecustom = [int(i) for i in housecustom]
        print('housecustom', type(housecustom[0]))         
        print(housecustom)
        #housecustom = items
      
        return render_template("custom.html",choredefault=choredefault, housecustom=housecustom)	

    else:
      
        ## prob don't need dbresult = db.execute("SELECT t_chores.id, t_chores.chorecategory, GROUP_CONCAT(t_chores.chore) as chore, GROUP_CONCAT(t_chores.id) FROM t_chores join t_houseselection on t_chores.id = t_houseselection.id WHERE t_houseselection.houseid = 1 GROUP BY chorecategory ORDER BY chorecategory, chore ASC")
       
        #for i in dbresult:
        #    i['chore'] = sorted(i['chore'].split(','))  # changes string into a list, split by ',', then sorts a-z
        

        choredefault = db.execute("SELECT t_choresdefault.id, t_choresdefault.chorecategory, t_choresdefault.chore FROM t_choresdefault ORDER BY chorecategory, chore ASC")
        print('choredefault')
        print(choredefault)

        # extracting custom list of chores per house id            
        housecustom = db.execute("SELECT choreid FROM u_chorelist_?", session["chorelist"])

        temp = []
        for i in housecustom:
            temp.append(int(i['choreid']))
        
        housecustom = temp



        
        
        # housecustom = db.execute("SELECT GROUP_CONCAT(choreid) as choreid FROM u_chorelist_? WHERE , session["chorelist"])
        #housecustom = db.execute("SELECT GROUP_CONCAT(choreid) as choreid FROM t_houseselection as choreid WHERE houseid = ?", session['houseid'])

        #housecustom = db.execute("SELECT GROUP_CONCAT(choreid) as choreid FROM u_chorelist_?  WHERE houseid = ?", session['chorelist'], session['houseid'])
#        
        # using housecustom as a string of numbers, type string, stored in SQL..... but consider whether might be able to store it as a list of integers
        #housecustom = db.execute("SELECT housecustom FROM t_regcodes WHERE id = ?", session['houseid'])
        #housecustom = housecustom[0]['housecustom']
        
        print(type(housecustom))
        print(type(housecustom[0]))
        print(housecustom)

        #housecustom = sorted(housecustom[0]['choreid'].split(','))
        #housecustom = [int(i) for i in housecustom]
        print('get, housecustom')
        print(housecustom)

        ## prob don't needdbexpand = db.execute("SELECT t_chores.id, t_chores.chorecategory, t_chores.chore FROM t_chores join t_houseselection on t_chores.id = t_houseselection.id WHERE t_houseselection.houseid = 1 ORDER BY chorecategory, chore ASC")
   


    return render_template("custom.html",choredefault=choredefault, housecustom=housecustom)	
