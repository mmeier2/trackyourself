CREATE SCHEMA `SE_Database_Schema` ;

CREATE  TABLE `SE_Database_Schema`.`User` (
  
`userId` INT NOT NULL AUTO_INCREMENT ,
  
`firstName` VARCHAR(45) NOT NULL ,
  
`lastName` VARCHAR(45) NOT NULL ,
  
`emailId` VARCHAR(45) NOT NULL ,
  
`password` VARCHAR(100) NOT NULL ,
  
PRIMARY KEY (`userId`) );


CREATE  TABLE `SE_Database_Schema`.`Data` (
  
`dataId` INT NOT NULL AUTO_INCREMENT ,
  
`date` DATETIME NOT NULL ,
  
`userId` INT NOT NULL ,
  
`duration` INT NOT NULL ,
  
`descriptionType` INT NOT NULL ,
  
`dataType` INT NOT NULL ,
  
PRIMARY KEY (`dataId`) ,
  
CONSTRAINT `userId`
    FOREIGN KEY (`userId`)
    REFERENCES `SE_Database_Schema`.`user` (`userId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

INSERT INTO `SE_Database_Schema`.`User` (`firstName`, `lastName`, `emailId`, `password`) VALUES ('Samarth', 'Dave', 'dave_samarth2@yahoo.com', 'abc');
INSERT INTO `SE_Database_Schema`.`User` (`firstName`, `lastName`, `emailId`, `password`) VALUES ('Sam', 'Dav', 'samdave31@gmail.com', 'pqr');

INSERT INTO `SE_Database_Schema`.`Data` (`dataId`, `date`, `userId`, `duration`, `descriptionType`, `dataType`) VALUES ('1', '2013-08-05 18:19:03', '2', '2', '1', '1');
INSERT INTO `SE_Database_Schema`.`Data` (`dataId`, `date`, `userId`, `duration`, `descriptionType`, `dataType`) VALUES ('2', '2013-08-05 18:19:03', '1', '2', '2', '2');
