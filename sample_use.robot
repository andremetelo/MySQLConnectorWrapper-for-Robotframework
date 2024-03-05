*** Settings ***
Library		../sharedlibs/mysqlwrapper.py

*** Variables ***
${DBhost} 	XXXXX.XXX.XXX
${user}	    user
${pwd}      password
${database} DBname
${sql}      INSERT INTO clients (name, email, cel) VALUES (%s, %s, %s);
${data}     ['name', 'email', 'cel']

*** Comment ***
	- Sample script using mysql wrapper in a RobotFramwork robot
  - I am using the save sql format that makes sure the DB escapes all strings
	

*** Test Cases ***
Simple Insert a record

    ${myconnection}=  Connect To DB ${DBhost} ${user} ${pwd}  ${database}
    ${insert}=  Execute Sql ${myconnection} ${sql}  ${data}
    close db  ${myconnection}
