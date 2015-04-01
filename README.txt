CREATE THE TOURNAMENT DATABASE.

The file tournament.sql contains sql statements to create, or recreate, the tournament database. 
It is expected to be interpreted by psql with the command 

     $ psql < tournament.sql 
	 
The result output should show the database tables (relations):  

         List of relations
 Schema |  Name   | Type  |  Owner
--------+---------+-------+---------
 public | matches | table | vagrant
 public | players | table | vagrant
(2 rows)  
	 

RUN THE TEST.

The test program is tournament_test.py. It can be executed by the command

     $ python tournament_test.py

