# GF_Assignment_Project

------------------------------------- Step-by-step guide -------------------------------------

1. An appropriate IDE is required (VSCode as an example).

2. Download latest release off of the Github Repository

3. Extract contents into desired filepath.

4. Open folder with VSCode.

5. Go to the create pallete and select create virtual environment (.venv) and check box for requirements.txt to install app dependancies. This should install all you need, dependancies listed in requirements.txt if not.

6. Create both a Development DB and a Testing DB (if you wish for the unit tests to work) within SSMS.

7. Within config.py, adjust the connection strings to match the details of your databases (Development to your DevDB and Testing to your TestDB). (SQLALCHEMY_DATABASE_URI)

8. run the venv, and in terminal type in “flask shell“, followed by “db.create_all()”. This should create all the tables (specified within models.py) required for the project. (Backup SQL create commands have been added to the file).

9. Insert data into the Roles table via SSMS:

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

10. The flask project should now be executable, in which you can start entering data via the UI.

11. Inserting data should be simple, however there are SQL INSERT scripts listed within the document as a fallback (Sample data).



------------------------------------- Application Architecture & Common Code Explained -------------------------------------

TODO

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