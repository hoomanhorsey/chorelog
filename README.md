# chorelog

chorelog is a web based app that allows users to log their chores.

youtube video
https://youtu.be/mGzZMcnzZ9M 

While I consider this app to be complete for the purposes of the cs50 final project, I intend to keep updating and refining the app!!!  If I don't submit it at some stage I will likely never submit it!!

## functionality

Houseprofile

Sign up to chorelog and set up a house profile.  You will receive a registration code via email which will allow you to then set up a user profile.  Share the registration code with others who carry out chores at your house and they can set up a user profile so that their chores are logged as well.


#### Index

The landing page will take you to the index of chores. Here, the most recent chore of each chore category is displayed, the user who completed that chore, the date that they completed that chore and the days since that chore was completed.


#### Log chores


#### History

chore log allows you to view all chores a) by user, according to selected date range b) full history of chores, sorted by a range of conditions.

Customise chore list

Users can customise the list of chores to select from by selecting or deselecting chores from a list of default chores.

If a chore is deselected, it will currently remain displayed in the chore ledger. Deleting chores entirely may be included in a later update.

#### Create chore

Users can also create a custom chore which will be added to their list of chores.

Once a custom chore has been created it will remain permanently available for selection. If the custom chore is no longer wanted, it can be de-selected but it will always remain as an option.
Deleting a custom chore entirely may be included in a later update.


## Considerations

### Gamification
I considered gamifying the logging of chores by including a points system for completing chores.  This would have opened up considerable potential for creating a gamification framework for completing chores, including monthly points totals, winners and losers, weighting chores differently according to perceive difficulty.  One of the implications for gamification is influencing, shaping or encouraging certain behaviours to be modified. For example, if you include a scoring points system with a leaderboard there is the potential for users to become competitive and carry out more chores than they would have otherwise in order to 'win' at chore log.

However, I decided to refrain from including a gamification system at this point.

The primary reason why is because I wanted chore log to be a straightforward tracking tool that keeps a record of existing behaviours.  The result of tracking any behaviour necessarily impacts on those behaviours, that is unavoidable. However, I wanted to maintain user autonomy over the chores they chose to do and the frequency with which they chose to do them.  I'm mindful of the impact on behaviour that suggestion algorithms have on user consumption of social media content and I wanted to place my app far away from this practice.

Chore log is intended to recognise the autonomy of it's users.  Chore log is intended to aid people in the management of their chores, and the relationships they have with people who they live with, but it isn't intended to modify or unduly influence the chore arrangements in a given house, which are worked out through a range of considerations that may not be readily addressable via an app.  For example, some chores are more favoured by some and avoided by others, some users will have more available time than others.  I believe that setting up rigid systems of accountability is unproductive. But having ad hoc, flexible systems that require regular oversight, management, communication and tweaking are more resilient and effective in the long run.

Chore log will of course highlight chores that haven't been done for 'x' number of days. And this feature is intended to help householders negotiating the ongoing carrying out of chores.  But it is intended to put management of these affairs in the hands of the people living in a house, rather than to automate this process.


### The importance of UI
For this project I have maintained a very minimal approach to user interaction as well as design.  My focus has been primarily on the interaction between the program logic and the SQL database which stores user information. I have also only used very light bootstrap frameworks, CSS and minimal design considerations, as well as minimised Javascript in the app. However, in the course of creating the app I came to appreciate how critical good UI and overall design are to ensure that the experience is frictionless for the user and how important that is increase the changes of users trying the app and sticking with it.

At the moment, there is fairly standard sign up and registration process that would likely put off most casual users of the program. There is also no means to see what the program would operate like without registering first.  I can appreciate that in real word conditions, this would be enough to turn off many users from even trying the app. Something to consider in the future.

While not investing too much in design for this particluar project, I appreciate it's importance and the contribution that team members with different specialisations would contribute to a project. To be grappling with the logic of an app as a noob programmer left little mental energy or time to consider the design considerations of an app, which as alluded to above, are often just as critical to the effectiveness of an app.  I can appreciate how using frameworks like bootstrap will make life a lot easier. I can appreciate how having a dedicated team member who is expert in bootstrap or other design elemetns would be a gamechanger. I also appreciate how having input from a design perspective would help build a better app as it can be too easy to get caught up in building the logic to make sure it actually works as you think it should, and then unfortunately leave the user interface as an afterthought if you run out of time. Which then can result in a significant barriers being in place in trying to get users to use your app.  The underlying mechanics of an app might be well thought out and top notch. But it wouldn't count for much if users find it difficult to engage with.




### After I've cloned the repository

### Create virtual environment
https://flask.palletsprojects.com/en/2.2.x/installation/ 
$ py -3 -m venv venv
$ venv\Scripts\activate

### Install Flask
https://flask.palletsprojects.com/en/2.2.x/installation/ 

$ pip install Flask

### Upgrade pip...
$ python.exe -m pip install --upgrade pip

### Install cs50
$ pip install cs50
include 'import cs50' in code

### Install python-dotenv
$ pip install python-dotenv

### Install 'flask session'
$ pip install Flask-Session

### Install 'requests'
$ pip install requests

### Install flask_mail
$ pip install flask_mail

### Install psycopg2
@ pip install psycopg2

- Use environmental variables provided by Render.  Saving a 'secret' file called .env doesn't seem to work

# Hosting a web app and a SQL database for free.

Following are the extensive steps I took to host my app for free on Render, and my SQL database on Supabase.

This part of the project took several weeks to do.  Many of the tutorials I encounterd were written in a way that made absolute sense if you already knew how to do what the tutorial purported to explain. Alas, this is one of the features of some technical writing. It's quite challenging to pitch to a noob audience. But even then, some noobs are less noobier than others. And all it takes if for a few key items of knowledge to be presumed, for some users to feel completely lost.  So I'm including all of my findings here for posterity.


- Initial summary
<li>create repository locally using visual studio code</li>
<li>push to github</li>
<li>create flask app within code, requiring a 'venv' virtual environment to run it</li>
<li>create sql database (hosted on supabase) which you can then access via visual code studio? (Previously, under cs50, the sql database was running via the cloudbased codespace)</li>
<li>apparently I need to install pyscopg2 in order for the app to speak to the postgres sql database hosted by supabase. full instructions are here: https://pypi.org/project/psycopg2/#description</li>
<li>provision gunicorn to serve the app.  Render already kind of sets it up in it's default settings for Flask apps. Flask instructions are here: https://flask.palletsprojects.com/en/2.2.x/deploying/gunicorn/</li>



I am going to try to :
- create a web app using flask, 
- hosted on render, 
- that takes user input via a form, 
- then inserts that data into a SQL database, 
- and then sends the user an email, 
- with credentials saved in an .env file.


- Always save....
- One thing that tripped me up in transitioning from vs code via a codespace and running it locally is that VSCode looks to your last saved version of a file to run. Cloudspace saves automatically so while there is sometimes a lag, by and large the code you see on your screen is the code that will run. However, when run locally you need to manually save before the changes take place. So if you have made changes, and it doesn't work, check to see if you've 'Ctrl S' saved the changes as that has been the source of frequent hiccups for me.

Step-by-step instructions

- Got to github, create a new repository on github (https://github.com/repositories)
- Choose the following options
    - public - I'm not sure what the benefits are of making it public at this stage, but I know when I got github to host my website I had to make it 'public' for it to work. Apparently 'private' repositories for websites aren't allowed to be hosted for free.
    - add a readme file
    - add gitignore, 'python' template - this allows you to store sensitive info, like passwords, as 'environmental variables' in a document called '.env' but it also stops git hub from pushing that document to your public repostiory and allowing all the world to see.
    - Some kind of licence, I chose the MIT license  

- Open Visual Studio Code (locally installed), to clone the repository.
    - Go to 'Help' and then 'Get Started' choose 'Clone Git Repository' option and then open repository in y our workspace.
    - Save the repository locally in your 'Github' folder, which I have located at C:/Github

- Create virtual environment
    - The virtual environment allows you to install all the libraries and other things you need to support your app. 
    - Presumably libraries get updated, or deprecated, and having a unique virtual environment with libraries tailored to your app make it easier to manage your app as time passes. There may be other reasons, I'm still learning.
    - Follow instructions here: https://flask.palletsprojects.com/en/2.0.x/installation/)
    - Note that the virtual environment has to be activated each time y ou run Visual Studio Code with the command 'venv\Scripts\activate'
    - There may be a way of automating the activation. Or not. I'm not sure. For now I've accepted that it's a ritual like putting your seatbelt on before driving your car.


- Install Flask
    - Install Flask via pip. Full instructions here: https://flask.palletsprojects.com/en/2.2.x/installation/
    - 'pip Flask install' is the command.  


- Set up flask app
    - Flask documentation outlines a very simple flask app that is useful to create  so that you have a barebones app and can get that up and running to make it easier to diagnose problems unrelated to the app:
        - https://flask.palletsprojects.com/en/2.2.x/quickstart/#a-minimal-application
    - The CS50 finance project obviously represents a more complex app and you could use that. But I find it's easier to start with something very simple to get a handle on all the dependencies.

- Run Flask
    - enter debugging mode (using 'set FLASK_ENV=development' in CMD as per quickstart - https://flask.palletsprojects.com/en/2.0.x/quickstart/, but disable for production. Not actually sure how to disable.)

- Install CS50 library to access the CS50 SQL commands:
    - There seem to be a range of different databases and different ways to communicate with SQL databases, with different ways of actually issuing instructions to the database  To keep things simple at this stage, I've decided to stick with the CS50 libraries so that I don't have to rewrite the commands I send to the database. And also because I have become so confused about how to implement other ways to communicate with databases.
    - Type 'pip3 install cs50' in CMD as per: https://cs50.readthedocs.io/libraries/cs50/python/
    
- postgres python adapter
    - It seems that python requires another piece of software to communicate with postgres databses, psycopg2.  I'm not quite sure what it does but it sounds like the name of a Psychological Police Unit! PSYCH!COP!
    - Install psycopg2, as per: https://pypi.org/project/psycopg2/ 
    - type 'pip install psycopg2' in CMD

- Create database at Supabase
    - There aren't too many free SQL database hosters out there. I chose supabase because it has a free tier without a cut off date, it came recommended in various forum/reddit posts I read, and it also has a built in browser database manager, which is handy so you can see how your database looks without having to issue commands and reading it in the command line.
    - link github account
    - access connection details at 'Settings -> Database'
    - Click on 'Connection String -> URI' which will give you the following string.  Note that it is very similar to the sample usage given in the CS50 Library documentation, but with one very important difference:
        - CS50 library documentation sample usage: 
            - db = cs50.SQL("postgres://username:password@host:port/database")  # For PostgreSQL 
        - Supabase connection string format:
            - postgresql://postgres:[YOUR-PASSWORD]@db.[HOST]:[PORT]/[USER]
        - Supabase connection string with details filled in, but placeholder password and host name.
            - postgresql://postgres:abcdefghijk@db.abcdefghijk.supabase.co:5432/postgres
    - Note, that the supabase connection string requires 'postgresql' before the :// whereas the cs50.SQL command simply uses 'postgres'.  Some explanation is here, although I don't really understand it....yet:  https://stackoverflow.com/questions/62688256/sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy-dialectspostgre

- Exporting database from CS50 to Supabase
    - Jumping ahead a little, but you may wish to export a database from your CS50 project to Supabase.
    - Note exporting a database from CS50 to Supabase was one of the few things I found to be relatively straighforward. Although who knows at this stage whether I've made an error that will come back to bite me.
        - Open your database via phpLiteAdmin. 
        - Choose a table within your database, and select 'Export'. Select 'csv', give it a name your happy with, and then save the file somewhere locally.
        - Then login to your Supabase account and choose 'New Project'. Name the project, give it a password (I recommend bitwarden as a tool for remembering all these passwords)
        - Once the project is created, go to 'Table Editor' and then choose 'Create New Table'. It will give you the option to 'Import data via spreadhseet' and once you click that it will give you a 'csv' option. Choose that option and then click on the csv file you've previously saved and it should appear as a new table in your Supabase project.  I did have some teething problems with some tables due to some conflicts (i.e. non-null entries that were actually null, seemed to put it off.) So if you have issues, then cleaning up the original table may be what's needed.

- Mail - Set up a gmail account
    - In order for gmail to be accessible from your app, you need to create an app password that allows a third party app to access your gmail account
    - Go to Security and turn on 2 Factor Authentication
    - Once 2 Factor has been turned on, you'll see a new option called 'App Passwords'
    - Click on this option to create a new 'app password'. Give it a name that relates to your app. This password will be used in your flask app, stored in your .env file, to allow your app to access gmail. Typically I save passwords but google tells me not to save this one. So long as you save it straight into your app you probably won't need to use it again.  However, if you somehow lose it on the way to copying it over to your app it's pretty easy to delete the old one and generate a new one.

- Set up Flask Mail
    - enter command 'pip install Flask-Mail'
    https://flask-mail.readthedocs.io/en/latest/

- Environmental variables
    - set up an .env file to store key and password data.
    - enter command 'pip install python-dotenv'
    - https://pypi.org/project/python-dotenv/
      
    - Store your gmail credentials in this .env file as well as your postgres credentials. I have saved them in this format:
        MAIL_DEFAULT_SENDER="1234567"
        MAIL_PASSWORD="1234567"
        MAIL_USERNAME="1234567"

        POSTGRES_PASSWORD="1234567"
        POSTGRES_HOST="1234567"
    - In the app itself, I have included this code to access the credentials: 

        # Mail config. login details saved in .env file
        app.config["MAIL_DEFAULT_SENDER"] = os.environ["MAIL_DEFAULT_SENDER"]
        app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_SERVER"] = "smtp.gmail.com"
        app.config["MAIL_USE_TLS"] = True
        app.config['MAIL_USE_SSL'] = False
        app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
        mail = Mail(app)

        # Postgres password saved in .env file.
        POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
        POSTGRES_HOST = os.environ["POSTGRES_HOST"]

        # Access database
        db = cs50.SQL("postgresql://postgres:(?)@db.(?).supabase.co:5432/postgres", POSTGRES_PASSWORD, POSTGRES_HOST)  
    - I also include an '.envsample' file which includes the format of the credentials, but without the sensitive information so that if you wish to share the code with soemone else they can see how they need to format their own .env file.

- Set up your app to be hosted by Render

- You should be able to run your flask app locally and hopefully it will all work!

- Now that you have your credential safely stowed away in an .env file, and you have a 'gitignore' file that excludes .env files (and many others) from being uploaded to GIT, it should be save to upload your code onto GIT which will be required to allow Render to hose your app.

- Requirements.txt
    - Create a file called 'requirements.txt' and include it in your root directory.
    - In the file include (new line for each item, do not include the dashes)
        - cs50
        - Flask
        - flask-mail
        - Gunicorn
        - psycopg2
        - python dot-env

        [note, dot-env is the library you need to install locally, but when having your app hosted, it seems that 'python dot-env' is the way to go.]

    
- Host with Render
    - Sign up with Render
    - Select 'New+' and choose 'Web Service'
    - Choose the repository for the app you are working on at 'Choose Repository'. 
    - You will now be at the settings/deployment page.
        - Give the service a name
        - Choose the region closest to you
        - Environment - Choose Python3
        - Start Command - change from 'gunicorn your_application.wsgi' to 'gunicorn app:app'
        - Choose the Free Tier. Hopefully that will be enough for now.
        - Ignore 'Advanced' for now, although interestingly these options include provision for including environmental variables which is an alternative to your .env file.

    - Add .env to render environmental variables
        - Simply copy and paste the contents of your .env file to a file hosted on render, as per: https://render.com/docs/configure-environment-variables 

    [NOTE - figure out whether the standalone .env file works???]

- NOTE - may need to include an import psycopg2 command in app to get it to run
    NOTE- Is a requirements.file the hosted equivalent of installing libraries in your VScode venv?



