# chorelog

chorelog is a web based app that allows users to log their chores.

youtube video
https://youtu.be/mGzZMcnzZ9M 

chorelog was created as a final project for the wonderful cs50 introduction to computer science course. 

While I consider this app to be complete for the purposes of the cs50 final project, I intend to keep updating and refining the app!!!  If I don't submit it at some stage I will likely never submit it!!

This readme is a little longer than most. While it describes the functionality of this rather basic app, it also includes some broader thoughts about the philosophy of the app, as well as some extensive notes on implementing the hosting of this app. As such it is intended as a comprehensive document of my learning process, as well as a guide for myself (and possible others) on how to implement third party hosting of a web based app. 

The readme is set out in following section. If you are interested only in learning how to host an app, skip to section 3

- Section 1 - Functionality 
an explanation of the app's functionality

- Seciton 2 - Some considerations 
design thoughts and things I've learnt

- Section 3 - Implementation of app 
explanation of implementing the app as a flask app, hosted on render (free tier) and using a postgres database hosted on supabase (free tier)

## Section 1 - Functionality

#### houseprofile

Sign up to chorelog and set up a house profile.  You will receive a registration code via email which will allow you to then set up a user profile which will allow you to log your chores

Share the registration code with others who carry out chores at your house and they can set up a user profile so that their chores are logged as well.

#### index

The landing page will take you to the index of chores. Here, the most recent chore of each chore category is displayed, the user who completed that chore, the date that they completed that chore and the days since that chore was completed.

#### log chores

Log chores allows you to log a chore by selecting that chore from a down menu and the date that the chore was carried out.

#### history

You can view the entire history of chores completed by the following criteria a) by user, according to selected date range b) full history of chores, sorted by a range of conditions.

#### customise chore list

Each house account is created with a default list of standard chores that users can choose from when loggin their chores.

Users can customise the list of chores to select from by selecting or deselecting chores from a list of default chores. For example, if there are no pets in the house then all chores relating to pets can be omitted. However, if a pet is later added the chore can be reselected.

If a chore is deselected, and a chore has already been logged, it will remain displayed in the chore ledger. Deleting chores entirely may be included in a later update.

#### create custom chore

Users can also create a custom chore which will be added to their list of chores that they may log chores from.

Once a custom chore has been created it will remain permanently available for selection. If the custom chore is no longer wanted, it can be de-selected but it will always remain as an option.

Deleting a custom chore entirely may be included in a later update.

## Section 2 - Some considerations and things I've learnt

#### Gamification
I considered gamifying the logging of chores by including a points system for completing chores.  This would have opened up considerable potential for creating a gamification framework for completing chores, including monthly points totals, winners and losers, weighting chores differently according to perceive difficulty.  One of the implications for gamification is influencing, shaping or encouraging certain behaviours to be modified. For example, if you include a scoring points system with a leaderboard there is the potential for users to become competitive and carry out more chores than they would have otherwise in order to 'win' at chore log.

However, I decided to refrain from including a gamification system at this point.

The primary reason why is because I wanted chore log to be a straightforward tracking tool that keeps a record of existing behaviours.  The result of tracking any behaviour necessarily impacts on those behaviours. That is unavoidable. However, I wanted to maintain user autonomy over the chores they chose to do and the frequency with which they chose to do them.  I'm mindful of the impact on behaviour that suggestion algorithms have on user consumption of social media content and I wanted to place my app far away from this practice.

Chore log is intended to recognise the autonomy of it's users.  Chore log is intended to aid people in the management of their chores, and the relationships they have with people who they live with, but it isn't intended to modify or unduly influence the chore arrangements in a given house, which are worked out through a range of considerations that may not be readily addressable via an app.  For example, some chores are more favoured by some and avoided by others. Or some users will have more available time than others to do chores.  I believe that setting up rigid systems of accountability, according to predefined categories that aren't mutually negotiated, can be counter productive. Users may 'work' to a score. Or use a score to represent an objective distribution of labor, when the factors that contribute to the score don't in fact take into account all relevant considerations.  That's not to suggest that a scoring framework would not be possible to create, but I am of the view that it would need to be extensively tailored to each household, which is beyond the scope of this app. In my view, while an app like chore log can help with recording keeping and accountability, it is no replacement for regular communication and management of flexible and somewhat ad hoc house labour systems, which are potentially more resilient and effective in the long run.

Chore log will of course highlight chores that haven't been done for 'x' number of days. And this feature is intended to help householders negotiate the ongoing carrying out of chores.  But it is intended to put management of these affairs in the hands of the people living in a house, rather than to automate this process.


#### The importance of UI/UX
For this project I have maintained a very minimal approach to user interaction as well as design.  My focus has been primarily on the interaction between the program logic and the SQL database which stores user information. I have also only used very light bootstrap frameworks, CSS and minimal design considerations, as well as minimised Javascript in the app. However, in the course of creating the app I came to appreciate how critical good User Interaction, User Experience and overall design are to ensure that the experience is as frictionless as possible for the user and how important that is increase the changes of users trying the app and sticking with it.

As a learning process, it is so easy to focus on solving back end problems without being able to properly prioritise how the solutions that are developed are experienced by the user.

At the moment, there is fairly standard sign up and registration process that would likely put off most casual users of the program. There is also no means to see what the program would operate like without registering first.  I can appreciate that in real word conditions, this would be enough to turn off many users from even trying the app. Something to consider in the future. But perhaps something that gets easier with more experience and once one moves beyond the feeling that they are inventing things for the first time.

While not investing too much in design for this particluar project, I appreciate it's importance and the contribution that team members with different specialisations would contribute to a project. To be grappling with the logic of an app as a noob programmer left little mental energy or time to consider the design considerations of an app, which as alluded to above, are often just as critical to the effectiveness of an app.  I can appreciate how using frameworks like bootstrap will make life a lot easier. I can appreciate how having a dedicated team member who is expert in bootstrap or other design elemetns would be a gamechanger. I also appreciate how having input from a design perspective would help build a better app as it can be too easy to get caught up in building the logic to make sure it actually works as you think it should, and then unfortunately leave the user interface as an afterthought if you run out of time. Which then can result in a significant barriers being in place in trying to get users to use your app.  The underlying mechanics of an app might be well thought out and top notch. But it wouldn't count for much if users find it difficult to engage with.


#### initial version - notes

The initial code for chorelog was created as part of cs50. I later took the cs50 Python course, and learnt a lot more about the functionality of python.  However, the code for chorelog was initially created without being aware of this functionality and so the code has some quite rudimentary structure. I also managed to incorporate the use of libraries (such as date) by googling, but without really understanding how they were used!

So the first 'final' version of the app may use python, but perhaps may not have particularly efficient use of the built in methods python has as its disposal or the many libraries that can be imported to solve problems.  I feel that my approach was akin to using the python language, but adopting an approach that is more reminiscent of the approached used when using C.  So potentially the worst of both worlds!  Using a more abstracted language without implementing the power of that abstraction (which makes the tradeoff for that abstraction worthwhile) but using more primitive basic methods akin to C (i.e. iterating over lists endlessly instead of using built in methods)

I may refactor and clean up the code at a later opportunity.

## Section 3 - Implementation of app

Many, many hours were spent trying to figure out how to host the app using a free hosting service and also tying that to a free database hosting service.  Previously one option for cs50 projects was to host them on the free tier provided by heroku and there is a tutorial for that. But following the withdrawal of that free tier in late 2022, this was no long possible.

So I spent quite a bit of time searching through tutorials to piece together a way of hosting this app. I actually found this one of the most challenging aspects of this project.  It was frankly BEWILDERING and took me days, which turned into weeks.  I found I could only do so much each day and had to take breaks, as relentless confusion is exhausting in it's own unique way. 

There are many tutorials available for every step you need to take. Unfortunately many of the tutorials assume a level of knowledge that beginners often don't have.  And while they often give a step by step account, they don't often explain the purpose behind certain steps so that if something is done slightly incorrectly it can be hard to rectify. There's also a bit of assumed knowledge that beginners don't have, and beginners (such as myself) often misread or don't quite understand the terminology used until the 3rd or 7th attempt at something!

This is what I've found and hopefully it works for others, as well as myself as no doubt I'll have to come back to check how I did it.

#### Initial setup - visual studio code and github

There are other ways to work with apps but I used vscode and github.

You will initially need to install vscode locally, and install github on vscode. You will then need to set up a repository on github, and then clone your repository to your local version of vscode. 
    
None of these tasks are straightforward for an absolute beginner, as I was.  I am going go through the steps I took but it's possible I may miss some details.  At least with the steps relating to vscode and github there are plenty of resources available so you shouldn't get too lost. Also,  how you go about it will also depend somewhat on the operating system you run. 


##### github

Login to your github account and create a new repository for your project  (https://github.com/repositories)

When creating a repository you are presented with some options. Choose the following:
    - public - I'm not sure what the benefits are of making it public at this stage, but I know when I got github to host my website I had to make it 'public' for it to work. Apparently 'private' repositories for websites aren't allowed to be hosted for free. You can change it back again to private later if you wish.
    - add a readme file
    - add gitignore, 'python' template - this allows you to store sensitive info, like passwords, as 'environmental variables' in a document called '.env' but it also stops git hub from pushing that document to your public repostiory and allowing all the world to see those details.
    - Some kind of licence, I chose the MIT license  

##### installing vscode locally

Up to this point, if you're working on the cs50 course, you've been using the wonderful cloud based version of visual studio code which takes care of a lot of the behind the scenes things for you in it's specific 'codespace'. But there comes a time when one must break free and stand independently so I decided to set up vscode locally. Setting up locally also means you aren't timed out as you are in the cloud version if you are idle for a set period of time.  However, if you wish to work on different computers, setting up locally does mean having to install vscode on each machine and syncing up your code before you jumpt to another machine.

Installing vscode is pretty straightforward, like installing any other app:

https://visualstudio.microsoft.com/#vscode-section

One thing that tripped me up in transitioning from vs code via a codespace and running it locally is that VSCode looks to your last saved version of a file to run. Codespaces saves automatically so while there is sometimes a lag, by and large the code you see on your screen is the code that will run. However, when run locally you need to manually save before the changes take place. So if you have made changes, and it doesn't work, check to see if you've 'Ctrl S' saved the changes as that has been the source of frequent hiccups for me.



##### installing github on your local installation of vscode

Once you have installed vscode you then need to install 'git' for vscode, and install an extension for it to be able to interact with github. 

Note that git and github are distinct. Git is an open source version control system that lets you manage and keep track of your source code history. GitHub is a cloud-based hosting service owned by microsoft (as is vscode) that lets you manage Git repositories.  I understand that there ways of using Git without Github, although that's presently beyond me.

The following page is taken from github on how to implement git in vscode. It's quite comprehensive and there may be a bit of overlap with my explanations.

https://code.visualstudio.com/docs/sourcecontrol/github

I will note that macOS didn't allow me to install 'Git' in a straightforward manner (Macbook Air 2020, Ventura). At least when I tried to install Git it required me to install xcode on my mac, which required me to open a paid subscription developer account. The wiki page states that xcode is available for free: https://en.wikipedia.org/wiki/Xcode but I couldn't seem to install it without having to register as a developer first, which was not free.  It's likely that I am wrong about this.  But in the end, I managed to bypass this by installing xcode via 'homebrew'. (https://brew.sh)


##### cloning your repository to your local vscode installation

Open Visual Studio Code (locally installed), to clone the repository you have set up on github

Go to the 'Help'task bar menu and then 'Get Started' and choose 'Clone Git Repository' option.  The repositories on your github should appear. Choose the repository you just created and then open the repository in your workspace.

Save the repository locally in your 'Github' folder, which I have located at C:/Github


#### Create virtual environment

The next step after you've cloned your repository to your locally installed vscode, is to create a virtual environment (venv).  

The virtual environment allows you to install all the libraries and other things you need to support your app. 

The reason you do this is so that you have a consistent set of python libraries and dependencies installed for your app.  Over time, certain python libraries may become updated or deprecated and they are not guaranteed to interact with each other seamlessly. By creating a venv in which you install your python libraries, you effectively create a snapshot in time of a python installation that should happily work together. There may be other reasons, I'm still learning.

Instructions here: https://flask.palletsprojects.com/en/2.0.x/installation/

Type the following commands:

'$ py -3 -m venv venv'
'$ venv\Scripts\activate'

Note that if you wish to run your app locally, that is hosted on a flask server on your machine for testing, the virtual environment has to be activated each time you run Visual Studio Code with the command 'venv\Scripts\activate' for Windows. Instructions for mac are in the link above.

There may be a way of automating the activation. Or not. I'm not sure. For now I've accepted that it's a ritual like putting your seatbelt on before driving your car.


#### Installing libraries and dependencies

Next you will need to install a range of libraries. While the libraries you will require are dependent on your particular app, I'm installing the libraries required by cs50 for the last week's Finance project. 

You need these libraries to be able to run your app locally, that is when you run it as a flask app from your own machine.

Note, the cs50 codespace already includes some of these libraries as part of the codespace. While you need to specifically import them in your code, the libraries themselves are installed in that codespace environment.  However, because you are now setting up your own envrionment locally, you will need to install them into your virtual environment.  If you start a new project with a new venv, you will need to install them (or other libraries, depending on the project) into that environment. 

I hope this explanation makes sense. It didn't make sense to me for a long time. Now I understand, it seems pretty straightforward. I found this concept very confusing as I never came across any kind of explanation. I hope that the explanation above saves you some time.

Later, when you have your app hosted on a third party hosting service, you will need to specify the libraries you require in a 'requirements.txt' document, but the hosting service takes care of the libraries for you during the deployment of the app.

So just to be clear, you need to install these libraries to your venv so that you can run and text your app locally on your own machine.  However, when the app is hosted externally, the host sets up the environment for you.

##### Install Flask

Install flask, which is the web framework for the app, using the following command:

"https://flask.palletsprojects.com/en/2.2.x/installation/" 

Type the following command:
'$ pip install Flask'

Note: set up flask app

Flask documentation outlines a very simple flask app that is useful to create  so that you have a barebones app and can get that up and running to make it easier to diagnose problems unrelated to the app:
        - https://flask.palletsprojects.com/en/2.2.x/quickstart/#a-minimal-application
The CS50 finance project obviously represents a more complex app and you could use that. But you may find it's easier to start with something very simple to get a handle on all the dependencies.

Apparently one needs to enter debugging mode (using 'set FLASK_ENV=development' in CMD as per quickstart - https://flask.palletsprojects.com/en/2.0.x/quickstart/, but disable this for production. I'm not entirely sure I ever got this to work, but I got the app to work. And I'm not actually sure how to disable debugging mode either. I may return to this.


#### Install cs50

Install the cs50 library so that any elements the app uses that relies on the library are included.

https://cs50.readthedocs.io/libraries/cs50/python/

Type the following command:

'$ pip install cs50'

To make the creation of my app a little easier, I initially based it on the app structure of the last week 'finance' app, which included the cs50 library.

While the cs50 library contains a lot of features. the key inclusion of the cs50 library in respect of this app is it's implementation of SQL searches.  There seem to be a range of different databases and different ways to communicate with SQL databases, with different ways of actually issuing instructions to the database  To keep things simple at this stage, I decided to stick with the CS50 libraries so that I don't have to rewrite the commands I send to the database. And also because I have become so confused about how to implement other ways to communicate with databases.

Remember to include 'import cs50' in the code for the app.    


#### Install python-dotenv

Install dotenv to allow you to save a set of environmental variables. 

Type the following command:

'$ pip install python-dotenv'

Environmental vairables allow you to save information locally on your machine, which your app will call. This includes information such as the passwords for your email functions as well as access to your database. You don't want to include such information in your main code as to do so will reveal confidential information to the world when you upload your code to github.

Note, as described above, when you create your repository you also create 'gitignore' file which specifically excludes certain files from being uploaded to your github repository.  Your .env file will be included in this list. 

Another thing to consider is that you can also store confidential information as a file on your hosting service (i.e render). If you store such info on the hosting website why do you also need a local file?  Well, when you are running your app locally for testing, then your app will look for locally stored environmental variables so it is still necesssary to include this file and the library that allows you to access it.


### Install 'flask session'

Install flask-session to add support in flask for a 'server side' session for your app. 

I've taken this description from the link below, and I'm not entirely sure what these words actually mean, but in practice, I beleive it allows you to store information when you run your app that is specific to a particular seession when the app runs.  For example, I use it to store information relating to the user when the user logs into the app - information such as the user's houseid, name etc, which is information that isn't local to a particular function and can be accessed by different functions in the app...almost like a global variable, but that only persists for as long as the session is active/ when the user is logged in.

https://flask-session.readthedocs.io/en/latest/

Type the following command:

'$ pip install Flask-Session'

### Install 'requests'

Install 'requests' to handle 'post' data to online forms, which is used in the cs50 finance project. 

I don't fully understand the operation of this library. In other problem sets in cs50 python, the library is used to pull information from APIs. In relation to this app it seems to allow for the processing of 'post' data when users input information to your app via forms.

https://requests.readthedocs.io/en/latest/

Type the following command:

'$ pip install requests'

### Install flask_mail

Install 'flask_mail' to handle sending emails from your app.

I've included more information below on how to configure your app to send emails.

https://pythonhosted.org/Flask-Mail/

Type the following command:

'$ pip install flask_mail'

### Install psycopg2

Install psycopg2 to interpret python comamands for post-greSQL databases. 

Basically allows your queries to your SQL database included in your app to communicate with a separate post-greSQL database hosted on a third party hosting service. It sounds like the name of a sequel to a move about a Psychological Police Unit! PSYCH!COP!2!

https://pypi.org/project/psycopg2/ 

Type the following command:

'$ pip install psycopg2'

- NOTE - may need to include an import psycopg2 command in app to get it to run




## Hosting a web app and a SQL database for free.

Following are the extensive steps I took to host my app for free on Render, and my SQL database on Supabase.

This part of the project took several weeks to do.  Many of the tutorials I encounterd were written in a way that made absolute sense if you already knew how to do what the tutorial purported to explain. Alas, this is one of the features of some technical writing. It's quite challenging to pitch to a noob audience. But even then, some noobs are less noobier than others. And all it takes if for a few key items of knowledge to be presumed, for some users to feel completely lost.  So I'm including all of my findings here for posterity.


### Initial summary

So far we have:
- created repository locally using visual studio code
- pushed to github
- created a flask app with code, requiring a 'venv' virtual environment to run it

Next we need to:
- create sql database (hosted on supabase) which you can then access via visual code studio? (Previously, under cs50, the sql database was running via the cloudbased codespace)
- provision gunicorn to serve the app.  Render already kind of sets it up in it's default settings for Flask apps. Flask instructions are here: https://flask.palletsprojects.com/en/2.2.x/deploying/gunicorn/




#### Create database at Supabase
There aren't too many free SQL database hosters out there. I chose supabase because it has a free tier without a cut off date, it came recommended in various forum/reddit posts I read, and it also has a built in browser database manager, which is handy so you can see how your database looks without having to issue commands and reading it in the command line.
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

#### Exporting database from CS50 to Supabase
    - Jumping ahead a little, but you may wish to export a database from your CS50 project to Supabase.
    - Note exporting a database from CS50 to Supabase was one of the few things I found to be relatively straighforward. Although who knows at this stage whether I've made an error that will come back to bite me.
        - Open your database via phpLiteAdmin. 
        - Choose a table within your database, and select 'Export'. Select 'csv', give it a name your happy with, and then save the file somewhere locally.
        - Then login to your Supabase account and choose 'New Project'. Name the project, give it a password (I recommend bitwarden as a tool for remembering all these passwords)
        - Once the project is created, go to 'Table Editor' and then choose 'Create New Table'. It will give you the option to 'Import data via spreadhseet' and once you click that it will give you a 'csv' option. Choose that option and then click on the csv file you've previously saved and it should appear as a new table in your Supabase project.  I did have some teething problems with some tables due to some conflicts (i.e. non-null entries that were actually null, seemed to put it off.) So if you have issues, then cleaning up the original table may be what's needed.

#### Mail - Set up a gmail account
    - In order for gmail to be accessible from your app, you need to create an app password that allows a third party app to access your gmail account
    - Go to Security and turn on 2 Factor Authentication
    - Once 2 Factor has been turned on, you'll see a new option called 'App Passwords'
    - Click on this option to create a new 'app password'. Give it a name that relates to your app. This password will be used in your flask app, stored in your .env file, to allow your app to access gmail. Typically I save passwords but google tells me not to save this one. So long as you save it straight into your app you probably won't need to use it again.  However, if you somehow lose it on the way to copying it over to your app it's pretty easy to delete the old one and generate a new one.

#### Environmental variables
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

    - Note:  Use environmental variables provided by Render.  Saving a 'secret' file called .env doesn't seem to work


- You should be able to run your flask app locally and hopefully it will all work!

#### Requirements.txt
    - Create a file called 'requirements.txt' and include it in your root directory.
    - In the file include (new line for each item, do not include the dashes)
        - cs50
        - Flask
        - flask-mail
        - Gunicorn
        - psycopg2
        - python dot-env

        Note, dot-env is the library you need to install locally, but when having your app hosted, it seems that 'python dot-env' is the way to go.

        As mentioned above, this requirements document tells the hosting services what libraries it needs to install into the environment it creates for your app to work.
    
#### Host with Render
    - Sign up with Render
    - Select 'New+' and choose 'Web Service'
    - Choose the repository for the app you are working on at 'Choose Repository'. 
    - You will now be at the settings/deployment page.
        - Give the service a name
        - Choose the region closest to you
        - Environment - Choose Python3
        - Start Command - change from 'gunicorn your_application.wsgi' to 'gunicorn app:app'
        - Choose the Free Tier. Hopefully that will be enough for now.
        - Go to 'Advanced' and add the credentials of your .env file to so that they are on the hosting service as per: https://render.com/docs/configure-environment-variables 

        Note, I tried just including a standalone .env file but it never worked. Inserting the credentials into render via the above link did work for me.

#### Deployment

After all this you should be able to go to render and click on the name of your webservice and get your app to deploy.

If it doesn't work the log should tell you if anything is missing, although it sends a lot of information and can be quite cryptic.

It took me about 12 attempts over 2 days or so to get it deploy. Hence the extensive details set out above.



