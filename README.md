# GF_Assignment_Project

------------------------------------- Step-by-step guide -------------------------------------

1. An appropriate IDE is required (VSCode as an example, found here: https://code.visualstudio.com/Download).

2. Download latest release off of the Github Repository, found here (Under releases): https://github.com/Minimonks/GF_Assignment_Project 

3. Extract contents of the downloaded ZIP file into your desired filepath.

4. Open folder with VSCode.

5. Go to the View > Command Pallete and select create virtual environment (.venv) and check box for requirements.txt to install app dependancies. This should install all you need, dependancies listed in requirements.txt if not. A guide can be seen here: https://code.visualstudio.com/docs/python/environments 

6. SSMS (Microsoft SQL Server Management Studio) is the required DB (Database) software for this application and can be downloaded here: https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver16 

7. Create both a Development DB and a Testing DB (if you wish for the unit tests to work) within SSMS.

8. Within config.py, adjust the connection strings to match the details of your databases (Development to your DevDB and Testing to your TestDB). (SQLALCHEMY_DATABASE_URI). Sample connection strings have been left populated... change "GeorgesLocalDB" to the name of your
DB, and "GFAssignmentDB" to the name of your table.

9. run the venv (virtual environment), and in terminal type in “flask shell“, followed by “db.create_all()”. This should create all the tables (specified within models.py) required for the project. (Backup SQL create commands have been added to the file).

10. Open a new query under your new database and insert data into the Roles table via SSMS: (This will have to be done on both Dev and Test)

INSERT INTO [dbo].[Role]
           ([RoleName])
     VALUES
           ('User')
GO

INSERT INTO [dbo].[Role]
           ([RoleName])
     VALUES
           ('Admin')
GO

11. The flask project should now be executable, in which you can start entering data via the UI.

12. Inserting data should be simple, however there are SQL INSERT scripts listed within the document as a fallback (Sample data).



------------------------------------- Application Architecture brief architecture explained -------------------------------------

References for this code project can be found within app/__init__.py.

As for the structure: This app follows a Flask Blueprint structure, allowing for better seperation of code.

app/__init.py__ specifies the app settings when initialised on run.py. This makes references to config.py, specifiying to load with the Development configuration.

config.py is where environment specific variables are specified, an example being alternating database connection strings.

requirements.txt is a file listing all dependancies used within this application and can be used on initialisation to pre-install all requirements.

app/main contains a series of files and folders:

forms.py - wtforms templates used to generate HTML forms on specified views

errors.py - a file dedicated to error handling and routes related to errors

routes.py - the main routing file in which URLs are resolved to views with gathered data

app/templates stores all the HTML views

tests folder contains the Unit Test logic.

vscode/launch.json specifies parameters required at launch of application.

app/models.py is my SQLAlchemy classes, representing tables used to generate, manipulate and display all related to the database.

------------------------------------- DEPENDANCIES -------------------------------------
As listed in requirements.txt, here are my dependancies: (I will explain the use of each here where appropriate)
alembic==1.9.4
click==8.1.3
colorama==0.4.6
dominate==2.7.0
Flask==2.2.2

Flask-Bootstrap==3.3.7.1 - Styling within the system, applied to the template to create a stylised UI such as the navigation menu.

Flask-Login==0.6.2 - Used for login management within the system

Flask-Migrate==4.0.4 - Used to track modifications made to the DB via SQLAlchemy objects, making updating the DB easier.

Flask-SQLAlchemy==3.0.3
Flask-WTF==1.1.1
greenlet==2.0.2
itsdangerous==2.1.2

Jinja2==3.1.2 - Engine allowing me to manipulate HTML templates within the program.

Mako==1.2.4
MarkupSafe==2.1.2
pyodbc==4.0.35
python-dotenv==1.0.0

SQLAlchemy==2.0.3 - Used to manipulate the database tables through classes in the code. Backbone for all CRUD operations.

typing_extensions==4.4.0
visitor==0.1.3

Werkzeug==2.2.2 - Security features used here for hashing passwords

WTForms==3.0.1 - Class based coding to generate HTML forms for pages such as login, software request, etc...


-------------------------------------DB SAMPLE DATA -------------------------------------
WARNING: It is suggested you enter your own sample data using the UI from scratch to further ensure initialisation success.

SSMS DB with Windows Authentication is required.

Scripts to insert test data:

dbo.Role

INSERT INTO [dbo].[Role]
           ([RoleName])
     VALUES
           ('User')
GO

INSERT INTO [dbo].[Role]
           ([RoleName])
     VALUES
           ('Admin')
GO


dbo.User

INSERT INTO [dbo].[User]
           ([Username]
           ,[Password]
           ,[Email]
           ,[RoleID])
     VALUES
           ('TestAdmin','sha256$KxXDzJDcPcn9ICwM$2b2298479793d2a5d5a158db362d5011cde2a41e452282b19eeb0d5ac54fd01e','Test@Test.com', 2)
GO



INSERT INTO [dbo].[User]
           ([Username]
           ,[Password]
           ,[Email]
           ,[RoleID])
     VALUES
           ('TestUser','sha256$XbaG6SR5Njnd254E$7f362bd565dc980bd4408c6fa8531c772584280724fa15a78ee1559d59331e12','Test2@Test.com', 1)
GO


dbo.SoftwareRequest

INSERT INTO [dbo].[SoftwareRequest]
           ([RequestTitle]
           ,[RequestDetails]
           ,[RequestImpact]
           ,[RequestDeadline]
           ,[RequestImportance]
           ,[RequestAccepted])
     VALUES
           ('TestRequest','Example details lalala, I want a user customisation screen.','This would enable me to update my details without seeking admin assistance', GETDATE(), 5, null)
GO


dbo.UserRequest - WARNING, User & Software ID values may need adjusting dependant on what IDs your database generates.

INSERT INTO [dbo].[UserRequest]
           ([UserID]
           ,[RequestId])
     VALUES
           (1, 1)
GO




-------------------------------------DB BACKUP CREATE SCRIPTS -------------------------------------
As mentioned prior, you shouldn't need this, only in the event you aren't able to generate tables uisng SQLAlchemy.

1. dbo.Role

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Role](
	[RoleID] [int] IDENTITY(1,1) NOT NULL,
	[RoleName] [varchar](64) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[RoleID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[RoleName] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


2. dbo.User

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[User](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Username] [varchar](125) NOT NULL,
	[Password] [varchar](125) NOT NULL,
	[Email] [varchar](255) NOT NULL,
	[RoleID] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[User]  WITH CHECK ADD FOREIGN KEY([RoleID])
REFERENCES [dbo].[Role] ([RoleID])
GO


3. dbo.SoftwareRequest


SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[SoftwareRequest](
	[RequestID] [int] IDENTITY(1,1) NOT NULL,
	[RequestTitle] [varchar](64) NOT NULL,
	[RequestDetails] [varchar](255) NOT NULL,
	[RequestImpact] [varchar](255) NULL,
	[RequestDeadline] [date] NULL,
	[RequestImportance] [int] NOT NULL,
	[RequestAccepted] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[RequestID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

4. dbo.UserRequest

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[UserRequest](
	[UserID] [int] NOT NULL,
	[RequestId] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[UserID] ASC,
	[RequestId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[UserRequest]  WITH CHECK ADD FOREIGN KEY([RequestId])
REFERENCES [dbo].[SoftwareRequest] ([RequestID])
GO

ALTER TABLE [dbo].[UserRequest]  WITH CHECK ADD FOREIGN KEY([UserID])
REFERENCES [dbo].[User] ([id])
GO