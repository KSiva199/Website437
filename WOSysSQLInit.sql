-- --------------------------------------------------------

--
-- Table structure for all Tables in Work Order System Database (No FKs)
CREATE TABLE Assets
(
  AssetID INT NOT NULL,  
  ParentAsset VARCHAR(10) NOT NULL,
  AssetTag VARCHAR(10) NOT NULL,
  AssetType VARCHAR(15) NOT NULL,
  PRIMARY KEY (AssetID)
);

CREATE TABLE Problems
(
  ProblemID INT NOT NULL,
  ProblemDesc VARCHAR(100) NOT NULL,
  Shop VARCHAR(10) NOT NULL,
  ProblemCode VARCHAR(10) NOT NULL,
  PRIMARY KEY (ProblemID)
);

CREATE TABLE Users
(
  UserID INT NOT NULL,
  UserFirstName VARCHAR(25) NOT NULL,
  UserLastName VARCHAR(25) NOT NULL,
  Username VARCHAR(50) NOT NULL,
  Password VARCHAR(50) NOT NULL,
  PhoneNumber VARCHAR(11) NOT NULL,
  Role VARCHAR(15) NOT NULL,
  Shop VARCHAR(25),
  LocationID INT,
  PRIMARY KEY (UserID),
);

CREATE TABLE WorkOrders
(
  RequestDate DATE NOT NULL,
  WorkOrderID INT NOT NULL,
  Issue VARCHAR(100) NOT NULL,
  Shop VARCHAR(25) NOT NULL,
  Status VARCHAR(10) NOT NULL,
  LaborHours INT,
  Solution VARCHAR(200),
  RequesterID INT NOT NULL,
  TechnicianID INT,
  ProblemID INT,
  AssetID INT NOT NULL,
  PRIMARY KEY (WorkOrderID),
);

CREATE TABLE WorkOrderComms
(
  WOCommID INT NOT NULL,
  CommDate DATE NOT NULL,
  Message VARCHAR(250) NOT NULL,
  MsgUserID INT NOT NULL,
  WkOrdID INT NOT NULL,
  PRIMARY KEY (WOCommID),
);
--
-- Creation of base users to initialize the database

INSERT INTO `Users` (`UserID`, `UserFirstName`, `UserLastName`, `Username`, `Password`, `PhoneNumber`, `Role`, `Shop`, `LocationID`) VALUES
(1, 'Justin', 'M', 'justinm@gmail.com', '7bdebb5272eaed652341385389006168', '2147483647', 'Manager', 'Management', 0),
(2, 'justin', 't', 'justint@gmail.com', '7bdebb5272eaed652341385389006168', '999999999', 'Technician', 'Locksmith', 0),
(3, 'Pashi', 'bro', 'pashi@gmail.com', '89286134b43535ab80149c87c2a9b754', '1234567891', 'Requester', 'None', 0),
