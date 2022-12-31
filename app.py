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
from datetime import timedelta, date, datetime 

# for mail
from flask_mail import Mail, Message

# Configure application
app = Flask(__name__)

# Adding environmental variables, saved as .env file, which isn't committed to github

# Mail config. login details saved in .env file
app.config["MAIL_DEFAULT_SENDER"] = os.environ["MAIL_DEFAULT_SENDER"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config['MAIL_USE_SSL'] = False
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
mail = Mail(app)

# supabase postgres login details
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
db = cs50.SQL("postgresql://postgres:"+POSTGRES_PASSWORD+"@db."+POSTGRES_HOST+".supabase.co:5432/postgres")  

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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
        displaydate = e['date'].strftime("%e %B %Y") # converting date object to string display format. Note %e eliminates leading '0' from day.
        e['displaydate'] = displaydate
    return index

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show home of chores"""

    # extract chores, but maximum date, and grouped, so that is only one entry from each category, filtered by houseid.
    index = db.execute ("SELECT t_choresdefault.chorecategory, t_choresdefault.chore, username, MAX(date) AS date, color FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.userid JOIN t_choresdefault on t_choresdefault.choreid = t_ledger.choreid WHERE houseid = ? GROUP by t_choresdefault.chorecategory, t_choresdefault.chore, username, color ORDER BY t_choresdefault.chorecategory", session['houseid'])

    # Calculating date of previous log in.
    previouslog = db.execute ("SELECT dateprev FROM t_user WHERE userid = ?", session["user_id"])
    if not previouslog:
        print('no users in db') #included as a safety for when the db is empty
    else:
        previouslog = previouslog[0]['dateprev'].strftime('%e %B %Y')
   
    # Calculating 'days since' using today's date as date object. inserting 'daysdifference' dict into 'index'
    todaydate = date.today() # Extracts todays date
    for d in index:
        choredate = d['date']
        difference = (todaydate - choredate) # sum of calculation includes seconds....
        oneday = timedelta(days = 1)
        if difference < oneday:
            d['daysdifference'] = '0 days' # inserting '0 days' as a display  value if the date is less than 1 full day.
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

@app.route("/about", methods=["GET"])
def about():
    
    return render_template("about.html")

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
        index = db.execute("SELECT t_choresdefault.chorecategory, t_choresdefault.chore, username, date, color FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.userid JOIN t_choresdefault ON t_ledger.choreid = t_choresdefault.choreid  WHERE date BETWEEN ? AND ? AND username = ? ORDER by date DESC ", fromdate, todate, user)

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
        
@app.route("/create", methods=["GET", "POST"])
@login_required
def create():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
      
        chorecategory = request.form.get("chorecategory")        
        chore = request.form.get("chore").capitalize() #changes to sentence case
       
        if chorecategory == "" or chore == "" or not chore:
            return apology("You haven't selected a chore cateogry, or a chore to log", 400)

        # db query to provide chorecategories for selelction       
        category = db.execute("Select chorecategory FROM t_choresdefault GROUP BY chorecategory ORDER BY chorecategory")

        # create choreid number for custom chore
        counter = db.execute("SELECT customnumber from t_customcounter")
        counter = counter[0]['customnumber']
        customchoreid = counter + 1

        # insert custom chore into t_choresdefault
        db.execute("INSERT INTO t_choresdefault (choreid, chorecategory, chore) VALUES (?, ?, ?)", customchoreid, chorecategory, chore)
        # inserts custom chore into chorelist_users
        db.execute("INSERT INTO u_chorelist_? (choreid) VALUES (?)", session['houseid'], customchoreid)    

        # updating customnumber in customcounter
        db.execute("UPDATE t_customcounter SET customnumber = ?", customchoreid)
        
        # info for alert on creation of chore
        currentuser = session['username']
        alert = "created"

        return render_template("create.html", alert=alert, category=category, chore=chore, chorecategory=chorecategory, currentuser=currentuser)

    else:       
        category = db.execute("Select chorecategory FROM t_choresdefault GROUP BY chorecategory ORDER BY chorecategory")
        
        return render_template("create.html", category=category)


@app.route("/custom", methods=["GET", "POST"])
@login_required
def custom():

    if request.method == "POST":

        # Query db to create list of default chores, by chorecategory, chore and choreid, for printing options in template
        choredefault = db.execute("SELECT t_choresdefault.choreid, t_choresdefault.chorecategory, t_choresdefault.chore FROM t_choresdefault ORDER BY chorecategory, chore ASC")

        # Query db to create list of choreids of default chores, for comparing against custom list of chores. Selected with choreid values aggregated as a string.
        currentchorelist = db.execute("SELECT STRING_AGG(CAST(u_chorelist_?.choreid AS TEXT), ',') as choreid FROM u_chorelist_?", session["houseid"], session["houseid"])      

        # for loop extracts values from string of choreids expressed as a value of a dict, and creates a list of integers
        for c in currentchorelist:
            c['choreid'] = c['choreid'].split(',')
            c['choreid'] = [int(i) for i in c['choreid']]
        
        currentchorelist = sorted(currentchorelist[0]['choreid'])    # sorts by alpha to aid reading   
        housecustom = request.form.keys()                            # form values extracted, as keys
        housecustom = sorted(list(housecustom))                      # changed to a list of char values
        housecustom = sorted([int(i) for i in housecustom])          # transforms values from char to int, and then sorts by alpha
     
        # Comparison of the two lists
        diffdefault = set(currentchorelist) - set(housecustom)
        diffcustom = set(housecustom) -  set(currentchorelist)

        # test for difference from default list.

        if not not diffdefault:
            for i in diffdefault:
                n = str(i)         
                db.execute("DELETE FROM u_chorelist_? WHERE choreid = ?", session["houseid"], n)    
              
        if not not diffcustom:
            for j in diffcustom:
                p = str(j)
                db.execute("INSERT INTO u_chorelist_? (choreid) VALUES (?)", session['houseid'], p)    
              
        return render_template("custom.html",choredefault=choredefault, housecustom=housecustom)	

    else:

        choredefault = db.execute("SELECT t_choresdefault.choreid, t_choresdefault.chorecategory, t_choresdefault.chore FROM t_choresdefault ORDER BY chorecategory, chore ASC")

        # extracting custom list of chores per house id            
        housecustom = db.execute("SELECT choreid FROM u_chorelist_?", session["houseid"])

        temp = []
        for i in housecustom:
            temp.append(int(i['choreid']))       
        housecustom = temp
 
    return render_template("custom.html",choredefault=choredefault, housecustom=housecustom)	


@app.route("/fame", methods=["GET"])
@login_required
def fame():
    """Show hall of fame"""

    ##Extract chores, but maximum date, and grouped so only one item from each category, to create a list of chores that have been completed
    choreindex = db.execute ("SELECT t_choresdefault.chore FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.userid JOIN t_choresdefault ON t_ledger.choreid = t_choresdefault.choreid WHERE houseid = ? GROUP by t_choresdefault.chorecategory, t_choresdefault.chore ORDER BY t_choresdefault.chorecategory", session['houseid'])

    index = [] #declares list to be populated.

    # SQL select does the heavy lifting. Via each 'chore' it selects the top 3 chores, if there are 3
    for i in choreindex:
        sample = db.execute("SELECT t_choresdefault.chorecategory, t_choresdefault.chore, username, date, color FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.userid JOIN t_choresdefault ON t_ledger.choreid = t_choresdefault.choreid WHERE t_choresdefault.chore = ? ORDER BY date DESC LIMIT 3", i['chore'])
        if (len(sample) == 3) and (sample[0]['username'] == sample[1]['username'] == sample[2]['username']): #checks if there are 3 entries, and if they all have the same name
            index = index + sample #if they past these tests, then they are 3 in a row and are added to the index for printing!

    # Function to caculate display dates in day/month/year format
    index = displaydate(index)

    currentuser = session['username']

    #renders chorebyuser template
    return render_template("fame.html", currentuser=currentuser, index=index)

@app.route("/historyfull", methods=["GET", "POST"])
@login_required
def historyfull():
    """Show full history of chores"""
    if request.method == "POST":

        # Uses values from form to sort SQL call. SQL variables are used for values, not column names - must reformat as string.
        sort = request.form.get("sort")
        # sorting tree imposes order on the remainder of the sort, after the initial primary value is chosen
        if sort == 'chorecategory':
            index = db.execute("SELECT * FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.userid JOIN t_choresdefault ON t_ledger.choreid = t_choresdefault.choreid WHERE houseid = ? ORDER BY t_choresdefault.{}, t_choresdefault.chore ASC, date DESC".format(sort), session['houseid'])
        elif sort == 'chore':
            index = db.execute("SELECT * FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.userid JOIN t_choresdefault ON t_ledger.choreid = t_choresdefault.choreid WHERE houseid = ? ORDER BY t_choresdefault.{}, t_choresdefault.chorecategory ASC, date DESC".format(sort), session['houseid'])
        elif sort == 'username':
            index = db.execute("SELECT * FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.userid JOIN t_choresdefault ON t_ledger.choreid = t_choresdefault.choreid WHERE houseid = ? ORDER BY {}, t_choresdefault.chorecategory ASC, t_choresdefault.chore ASC, date DESC".format(sort), session['houseid'])
        elif sort == 'date DESC':
            index = db.execute("SELECT * FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.userid JOIN t_choresdefault ON t_ledger.choreid = t_choresdefault.choreid WHERE houseid = ? ORDER BY {}, t_choresdefault.chorecategory ASC, t_choresdefault.chore ASC".format(sort), session['houseid'])
        elif sort == 'none':
            return apology ("You've not chosen anything. Please make a choice.", 400)

        # Function to caculate display dates in day/month/year format
        index = displaydate(index)

        currentuser = session['username']

        #renders historyfull template
        return render_template("historyfull.html", index=index, currentuser=currentuser)

    else:
        #users = db.execute("SELECT username FROM t_user")
        index = db.execute("SELECT * FROM t_ledger JOIN t_user ON t_ledger.userid = t_user.userid JOIN t_choresdefault ON t_ledger.choreid = t_choresdefault.choreid WHERE houseid = ? ORDER BY t_choresdefault.chorecategory ASC, t_choresdefault.chore ASC, date DESC", session['houseid'])

        # Function to caculate display dates in day/month/year format
        index = displaydate(index)

        currentuser = session['username']

        #renders historyfull template
        return render_template("historyfull.html", index=index, currentuser=currentuser)

@app.route("/logchore", methods=["GET", "POST"])
@login_required
def logchore():
    """Log completion of a chore"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # GET INFO FROM USER
        chore = request.form.get("chore")
        date = request.form.get("date")
        choreid = request.form.get("choreid")
 
        if chore == "":
            return apology("You haven't selected a chore to log", 400)

        # checks that a chore hasn't been entered twice for the same date.
        datecheck = db.execute("SELECT t_ledger.choreid, t_ledger.date FROM t_ledger JOIN t_user ON t_user.userid = t_ledger.userid WHERE houseid = ?", session['houseid'])
        # note, dates stored in db as datetime object, choreid as an int. Both items are cast to meet test of equality '=='
        for x in datecheck:
            if date == x['date'].strftime('%Y-%m-%e') and int(choreid) == x['choreid']:
                return apology("It seems this chore has already been logged for this date. Nice try but TRY HARDER!", 400)

        # inserts chore into db by reference to userid and choreid only......app can later  extract chore details by joining choreid query with t_choresdefault
        db.execute("INSERT INTO t_ledger (userid, choreid, date) VALUES(?, ?, ?)", session["user_id"], choreid, date)

        # preparing variable for display of confirmation
        confirm = db.execute("SELECT chorecategory, chore FROM t_choresdefault WHERE choreid = ?", choreid)
      

        # inserts the display date key value pair, but converts the string date entered, into display format.
        confirm[0].update({"displaydate" : datetime.strptime(date, '%Y-%m-%d').strftime('%e %B %Y')})

        currentuser = session['username']

        # creates alert variable to trigger summary alert for template
        alert = "logged"

        housecustom = db.execute("SELECT t_choresdefault.chorecategory, STRING_AGG(CAST(u_chorelist_?.choreid AS TEXT), ',') as choreid FROM u_chorelist_? JOIN t_choresdefault ON u_chorelist_?.choreid = t_choresdefault.choreid GROUP BY t_choresdefault.chorecategory ORDER BY t_choresdefault.chorecategory", session["houseid"], session["houseid"], session["houseid"])
#  
        for c in housecustom:
            c['choreid'] = c['choreid'].split(',')
            c['choreid'] = [int(i) for i in c['choreid']]      
        
        choredefault = db.execute("SELECT t_choresdefault.choreid, t_choresdefault.chorecategory, t_choresdefault.chore FROM t_choresdefault ORDER BY chorecategory, chore ASC")

        #renders index template
        return render_template("logchore.html", alert=alert, currentuser=currentuser, confirm=confirm, housecustom = housecustom, choredefault = choredefault)

    ## User reached route via GET (as by clicking a link or via redirect)
    else:

        currentuser = session['username'] # for alert printing in template.
        
        housecustom = db.execute("SELECT t_choresdefault.chorecategory, STRING_AGG(CAST(u_chorelist_?.choreid AS TEXT), ',') as choreid FROM u_chorelist_? JOIN t_choresdefault ON u_chorelist_?.choreid = t_choresdefault.choreid GROUP BY t_choresdefault.chorecategory ORDER BY t_choresdefault.chorecategory", session["houseid"], session["houseid"], session["houseid"])
        
        # This loop converts the aggregated choreid numbers from a list of strings, into a list of integers, which is required for comparison.
        for c in housecustom:
            c['choreid'] = c['choreid'].split(',')
            c['choreid'] = [int(i) for i in c['choreid']]      
        
        choredefault = db.execute("SELECT t_choresdefault.choreid, t_choresdefault.chorecategory, t_choresdefault.chore FROM t_choresdefault ORDER BY chorecategory, chore ASC")

        return render_template("logchore.html", housecustom = housecustom, choredefault = choredefault, currentuser=currentuser)

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
        session["user_id"] = rows[0]["userid"]
        session["houseid"] = rows[0]["houseid"]
        session["username"] = rows[0]["username"] 
       
        # Updating db to include login and previous login dates.
        dateprev = db.execute("SELECT datelogin FROM t_user WHERE userid = ?", session["user_id"])
        today = str(date.today())
        db.execute("UPDATE t_user SET datelogin = ?, dateprev = ? WHERE houseid = ?", today, dateprev[0]['datelogin'], session["user_id"])

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

        # Ensure user has a valid registration code by checking with existing regcodes
        regcodes = db.execute("SELECT regcode FROM t_reg")
        for r in regcodes:
            if regcode == r['regcode']:
                break
        else:
            return apology("Sorry. Your registration code is invalid. Please email chorelog@gmail.com for an updated code to proceed.", 400)

        session["regcode"] = regcode # TODO Does this need to be here?

        # New house profile chore list is created when first user uses regcode, but no longer created when other users create user profile.
        regstatus = db.execute("SELECT houseid, regcodestatus FROM t_reg WHERE regcode = ?", regcode)
        if regstatus[0]['regcodestatus'] == 'unused':
                db.execute("CREATE TABLE u_chorelist_? (choreid int NOT NULL, PRIMARY KEY(choreid))", regstatus[0]['houseid'])
                db.execute("UPDATE t_reg SET regcodestatus = 'used' WHERE regcode = ?", regcode)  

        return redirect("/register")

    else:
        
        return render_template("regcode.html")
        
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
        houseprofile = db.execute("SELECT houseid, address FROM t_reg WHERE regcode = ?", regcode)

        # Insert user and password (hashed) into databse
        hash = generate_password_hash(newpassword, method='pbkdf2:sha256', salt_length=8)
        db.execute("INSERT INTO t_user (username, hash, email, datelogin, dateprev, color, houseid, address) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", username, hash, email, today, today, color, houseprofile[0]['houseid'], houseprofile[0]['address'])

        #storing the houseid in a session
        session['houseid'] = houseprofile[0]['houseid']

        # Send email msg
        msg = Message('You are registered with Chore Log!', recipients = [email])
        msg.body = "Hi " + username + ". Congratulations on registering with Chore Log. Chore log takes the chore out of logging chores."
        mail.send(msg)

        # Populates u_chorelist_#, but only if it's the first time the registration code has been entered.
        regstatus = db.execute("SELECT houseid, choreliststatus FROM t_reg WHERE regcode = ?", regcode)
        if regstatus[0]['choreliststatus'] == 'uncreated':
            db.execute("INSERT INTO u_chorelist_? SELECT choreid FROM t_choresdefault", session['houseid'])
            db.execute("UPDATE t_reg SET choreliststatus = 'created' WHERE regcode = ?", regcode)  

        return render_template("login.html")

    else:

        # getting regcode to determine id, which then allows dropdown menu to determine which colors are available.
        regcode = session['regcode']
        household = db.execute("SELECT houseid, address FROM t_reg WHERE regcode = ?", regcode)
        house = household[0]['address']

        # Creates a hardcoded list of colours, but then extracts user colours from db.
        # Compares colours in db to hard coded colours and creates a revised list of colours that can be used for the colour selection drop down menu in registration
        colors = [{'color':'DODGERBLUE'}, {'color':'CYAN'}, {'color':'GREEN'}, {'color':'GOLD'}, {'color':'LIME'}, {'color':'MAGENTA'}, {'color':'MAROON'}, {'color':'PINK'}, {'color':'PURPLE'}, {'color':'VIOLET'}, {'color':'RED'}, {'color':'SALMON'}]
        dbcolor = db.execute("SELECT color FROM t_user JOIN t_reg ON t_user.houseid = t_reg.houseid WHERE regcode = ?", session['regcode'])
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

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Sign up"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if (not request.form.get("address") or not request.form.get("email")):
            return apology("Please provide an address and email", 403)     

        address = request.form.get("address")
        email = request.form.get("email")

        # generate random number for regcode
        randomnum =  str(random.random())
        randomnum = randomnum[2] + randomnum[3] + randomnum[4] + randomnum[5] + randomnum[6] + randomnum[7] + randomnum[8] + randomnum[9]

        # insert regcode and address into database
        db.execute("INSERT INTO t_reg (regcode, address) VALUES (?, ?)", randomnum, address)

        # Send email msg
        msg = Message('Thank you for signing up to Chore Log!', recipients = [email])
        msg.body = "Thank you for signing up to Chore Log.\r\n\r\nYour registration code is '" + randomnum + "'. \r\n\r\nYour registration code will be used to create a house profile for '" +address+ "'.\r\n\r\nThis code is tied to '" +address+ "'. Share it with others who live (or spend a lot of time) at '" +address+ "' so they can also begin logging their chores.\r\n\r\nGo to " +'https://chorelog.onrender.com/regcode'+" to create your Chore Log profile.\r\n"
        mail.send(msg)

        return redirect("/regcode")

    else:
        return render_template("signup.html")


