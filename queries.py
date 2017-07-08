import web
import MySQLdb
import bcrypt


# Class for the Database
class Database:

   # Initialize class by connecting to database and creating cursor.
   def __init__(self):
      self.db = MySQLdb.connect(host = "localhost",
                              user = "root",
                              passwd = "knucklepickle",
                              db = "csdateme")
      self.cur = self.db.cursor()

   # Returns true for users that are in the database.
   def authCheck(self, username, password):
      self.cur.close()
      self.cur = self.db.cursor()
      saltQuery = "SELECT salt FROM Users WHERE username = %s;"
      self.cur.execute(saltQuery, (username))
      salt = self.cur.fetchall()
      if len(salt) == 0:
         return False
      passw = bcrypt.hashpw(password.encode('UTF_8'), salt[0][0].encode('UTF_8')).replace("'","")
      print "unhashed password: " + password
      print "hashed password: " + passw
      query = "SELECT id FROM Users WHERE username = %s AND password = %s;"
      self.cur.execute(query, (username, passw))
      res = self.cur.fetchall()
      if len(res) == 0:
         return False
      else:
         return True

   # Query for checking login credentials.
   def getUser(self, username, password):
      query = "SELECT * from Users WHERE username = %s AND password = %s;"
      self.cur.execute(query, (username, password))
      res = self.cur.fetchall()
      return res

   # Query to add a user to the database. Returns a list of users.
   def addUser(self, username, email, password, salt):
      self.cur.execute("START TRANSACTION;")
      cmd = "INSERT INTO Users VALUES (NULL, %s, %s, %s, NULL, NULL, %s);"
      self.cur.execute(cmd, (username, password, email, salt))
      cmd2 = "INSERT INTO Questions VALUES (NULL, FALSE, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'default.png', NULL, NULL);"
      self.cur.execute(cmd2)
      self.cur.execute("COMMIT;")
      self.cur.execute("SELECT * FROM Users;")
      res = self.cur.fetchall()
      return res

   # Returns true if username and email is unique
   def addUserCheck(self, username, email):
      query = "SELECT id FROM Users WHERE username = %s OR email = %s;"
      self.cur.execute(query, (username, email))
      res = self.cur.fetchall()
      if len(res) == 0:
         return True
      else:
         return False

   # Updates user profile's questions
   def setQuestions(self, userid, fName, mName, lName, gender, state, city, birthday, favoriteOS, phoneOS, relationship, gaming, favLang1, favLang2, favLang3, favHobby1, favHobby2, favHobby3, wpm, interest, bio):
      cmd = "UPDATE Questions SET completed = true, firstName = %s, middleName = %s, lastName = %s, gender = %s, state = %s, city = %s, birthday = %s, favoriteOS = %s, phoneOS = %s, relationship = %s, gaming = %s, favLang1 = %s, favLang2 = %s, favLang3 = %s,  favHobby1 = %s,  favHobby2 = %s, favHobby3 = %s, wpm = %s, interestedIn = %s, bio = %s WHERE id = " + str(userid) + ";"
      self.cur.execute("START TRANSACTION;")
      self.cur.execute(cmd, (fName, mName, lName, gender, state, city, birthday, favoriteOS, phoneOS, relationship, gaming, favLang1, favLang2, favLang3, favHobby1, favHobby2, favHobby3, wpm, interest, bio))
      self.cur.execute("COMMIT;")

   def updateQuestions(self, userId, fName, mName, lName, gender, interest, state, city, birthday, favoriteOS, phoneOS, relationship, gaming, favLang1, favLang2, favLang3, favHobby1, favHobby2, favHobby3, wpm, bio):
      # Valid means there is an update needed
      valid = False
      cmd = "UPDATE Questions SET"
      # Only update if variable is set
      if fName:
         valid = True
         cmd = cmd + " firstName = '" + MySQLdb.escape_string(fName) + "',"
      if mName:
         valid = True
         cmd = cmd + " middleName = '" + MySQLdb.escape_string(mName) + "',"
      if lName:
         valid = True
         cmd = cmd + " lastName = '" + MySQLdb.escape_string(lName) + "'," 
      if gender:
         valid = True
         cmd = cmd + " gender = '" + gender + "'," 
      if interest:
         valid = True
         cmd = cmd + " interestedIn = '" + interest + "',"
      if state:
         valid = True
         cmd = cmd + " state = '" + state + "'," 
      if city:
         valid = True
         cmd = cmd + " city = '" + MySQLdb.escape_string(city) + "'," 
      if birthday:
         valid = True
         cmd = cmd + " birthday = '" + birthday + "'," 
      if favoriteOS:
         valid = True
         cmd = cmd + " favoriteOS = '" + favoriteOS + "'," 
      if phoneOS:
         valid = True
         cmd = cmd + " phoneOS = '" + phoneOS + "',"
      if relationship:
         valid = True
         cmd = cmd + " relationship = '" + relationship + "',"
      if gaming:
         valid = True
         cmd = cmd + " gaming = '" + gaming + "',"
      if favLang1:
         valid = True
         cmd = cmd + " favLang1 = '" + MySQLdb.escape_string(favLang1) + "',"
      if favLang2:
         valid = True
         cmd = cmd + " favLang2 = '" + MySQLdb.escape_string(favLang2) + "',"
      if favLang3:
         valid = True
         cmd = cmd + " favLang3 = '" + MySQLdb.escape_string(favLang3) + "',"
      if favHobby1:
         valid = True
         cmd = cmd + " favHobby1 = '" + MySQLdb.escape_string(favHobby1) + "',"  
      if favHobby2:
         valid = True
         cmd = cmd + " favHobby2 = '" + MySQLdb.escape_string(favHobby2) + "'," 
      if favHobby3:
         valid = True
         cmd = cmd + " favHobby3 = '" + MySQLdb.escape_string(favHobby3) + "'," 
      if wpm:
         valid = True
         cmd = cmd + " wpm = " + wpm + "," 
      if bio:
         valid = True
         cmd = cmd + " bio = '" + MySQLdb.escape_string(bio) + "',"

      if valid:
         # Removing last comma and replacing with ';'
         cmd = cmd[0:len(cmd) - 1] + " WHERE id = " + str(userId) + ";"

         self.cur.execute("START TRANSACTION;")
         self.cur.execute(cmd)
         self.cur.execute("COMMIT;")

   # Returns a token. Checks if token on file has expired or is still valid. 
   def addToken(self, username, token):
      self.cur.close()
      self.cur = self.db.cursor()
      self.cur.execute("CALL addToken('" + MySQLdb.escape_string(username) + "', '" + MySQLdb.escape_string(token) + "');")
      res = self.cur.fetchall()
      self.cur.close()
      self.cur = self.db.cursor()
      return res[0][0]

   # Remove token on logout
   def removeToken(self, token):
      self.cur.execute("START TRANSACTION;")
      self.cur.execute("UPDATE Users SET tokenTime = NULL WHERE token = '" + token + "';")
      self.cur.execute("COMMIT;")

   # Returns true if user has finished questions
   def questionsDone(self, userId):
      query = ("SELECT completed FROM Questions WHERE id = " + str(userId) + " LIMIT 1;")
      self.cur.execute(query)
      result = self.cur.fetchall()
      return result[0][0]

   # Returns userId for given username
   def usernameToId(self, username):
      query = ("SELECT id FROM Users WHERE username = %s;")
      self.cur.execute(query, (username))
      userId = self.cur.fetchall()
      return userId[0][0]

   # Returns userId for given token and -1 if does not exist
   def tokenToId(self, token):
      query = ("SELECT id from Users WHERE token = '" + token + "';")
      self.cur.execute(query)
      userId = self.cur.fetchall()
      if len(userId):
        return userId[0][0]
      else:
        return -1

    #stores img source for each user into database
   def uploadImage(self, userid, imageName):
       query = ("UPDATE Questions SET pic = '" + imageName + "' WHERE id = " + str(userid) + ";")
       self.cur.execute("START TRANSACTION;")
       self.cur.execute(query)
       self.cur.execute("COMMIT;")

   def deleteImage(self, userid):
        query = ("UPDATE Questions SET pic = 'default.png' WHERE id = " + str(userid) + ";")
        self.cur.execute("START TRANSACTION;")
        self.cur.execute(query)
        self.cur.execute("COMMIT;")

    # searches database for single value matches, results in an array of id's ----- NO IDEA WHAT TO DO WITH THIS 
   def singleSearch(self, search, attribute, userid):
      if (attribute == "favLang" or attribute == "favHobby"):
         first = attribute + "1"
         second = attribute + "2"
         third = attribute + "3"
         cmd = "Select * from Questions WHERE (" + first + " = '" + MySQLdb.escape_string(search) + "' OR " + second + " = '" + MySQLdb.escape_string(search) + "' OR " + third + " = '" + MySQLdb.escape_string(search) + "') AND id != "+ str(userid) +  ";"
      elif (attribute == "wpm"):
         if('-' in search):
            nums = search.split('-')
            if(nums[0].isdigit() and nums[1].isdigit()):
                 num1 = int(nums[0])
                 num2 = int(nums[1])
            else:
                 num1 = -999
                 num2 = -999
            cmd = "Select * from Questions WHERE wpm >= " + str(num1) + " AND wpm <= " + str(num2) + " AND id != " + str(userid) + " ;"
      else:
         cmd = "Select * from Questions WHERE " + attribute + " = '" + MySQLdb.escape_string(search) + "' AND id != " + str(userid) + " ;"
      self.cur.execute(cmd)
      res = self.cur.fetchall()
      tuples = []
      for result in res:
         tuples.append(result)
      return tuples


   #extended search page -- query will only run (and return something?) if required - will ignore empty submits, lmk if u want it to do otherwise - sigal please do whatever you did with my single search
   def indepthSearch(self, require, fName, mName, lName, gender, state, city, favoriteOS, phoneOS, relationship, gaming, favLang1, favLang2, favLang3, wpm, userid, interest):
      # checks if the attribute has a value or not and writes a query based off of that 
      self.fName = ""
      self.mName = ""
      self.lName = ""
      self.gender = ""
      self.state = ""
      self.city = ""
      favOS = ""
      self.relationship = ""
      self.gaming = ""
      self.favLang1 = ""
      self.favLang2 = ""
      self.favLang3 = ""
      self.wpm = ""
      self.interest = ""
      #uses atLeastOne to make sure at least one query condition is required
      atLeastOne = 0
      if (len(fName) > 0):
         self.fName = require + " firstName = '" + MySQLdb.escape_string(fName) + "' " 
         atLeastOne = 1
      if (len(mName) > 0):
         self.mName = require + " middleName = '" + MySQLdb.escape_string(mName) + "' "
         atLeastOne = 1
      if (len(lName) > 0):
         self.lName = require + " lastName = '" + MySQLdb.escape_string(lName) + "' " 
         atLeastOne = 1
      if (len(gender) > 0 and gender != "none"):
         self.gender = require + " gender = '" + gender + "' " 
         atLeastOne = 1
      if (len(state) > 0 and state != "none"):
         self.state = require + " state = '" + state + "' "
         atLeastOne = 1
      if (len(city) > 0):
         self.city = require + " city = '" + MySQLdb.escape_string(city) + "' "
         atLeastOne = 1
      if (len(favoriteOS) > 0 and favoriteOS != "none"):
         favOS = require + " favoriteOS = '" + favoriteOS + "' "
         atLeastOne = 1
      if (len(relationship) > 0 and relationship != "none"):
         self.relationship  = require + " relationship = '" + relationship + "' " 
         atLeastOne = 1
      if (len(gaming) > 0 and gaming != "none"):
         self.gaming = require + " gaming = '" + gaming + "' " 
         atLeastOne = 1
      if (len(favLang1) > 0 ):
         self.favLang1 = require + " (favLang1 = '" + MySQLdb.escape_string(favLang1) + "' OR favLang2 = '" + MySQLdb.escape_string(favLang1) + "' OR favLang3 = '" + MySQLdb.escape_string(favLang1) + "') "
         atLeastOne = 1

      if (len(favLang2) > 0 ):
         self.favLang2 = require + " (favLang2 = '" + MySQLdb.escape_string(favLang2) +  "' OR favLang2 = '" + MySQLdb.escape_string(favLang2) + "' OR favLang3 = '" + MySQLdb.escape_string(favLang2) + "') "
         atLeastOne = 1

      if (len(favLang3) > 0 ):
         self.favLang3 = require + " (favLang2 = '" + MySQLdb.escape_string(favLang3) + "' OR favLang2 = '" + MySQLdb.escape_string(favLang3) + "' OR favLang3 = '" + MySQLdb.escape_string(favLang3) + "') "
         atLeastOne = 1

      if (len(interest) > 0):
         self.interest = require + " interestedIn = '" + interest + "' "
         atLeastOne = 1

      if ('-' in wpm and len(wpm) > 2):
         nums = wpm.split('-')
         if(nums[0].isdigit() and nums[1].isdigit()):
            num1 = int(nums[0])
            num2 = int(nums[1])
            atLeastOne = 1
         else:
            num1 = -999
            num2 = -999
         self.wpm = require + " (wpm >= " + str(num1) + " AND wpm <= " + str(num2) + ") "

      #two seperate queries depending if AND or OR is necessary 
      if(atLeastOne == 1 and require == "AND"):
         cmd = "SELECT * from Questions WHERE " + "1 = 1 "  + self.fName + self.mName + self.lName + self.gender + self.state + self.city + favOS + self.relationship + self.favLang1 + self.favLang2 + self.favLang3 + self.wpm + self.interest + " AND id != " + str(userid) + " ;"
         self.cur.execute(cmd)
         res = self.cur.fetchall()
         tuples = []
         for result in res:
            tuples.append(result)
         return tuples

      if(atLeastOne == 1 and require == "OR"):
         
         cmd = "SELECT * from Questions WHERE " + "1 = 0 "  + self.fName + self.mName + self.lName + self.gender + self.state + self.city + favOS + self.relationship + self.favLang1 + self.favLang2 + self.favLang3 + self.wpm + self.interest + " AND id != " + str(userid) + " ;"
         self.cur.execute(cmd)
         res = self.cur.fetchall()
         tuples = []
         for result in res:
            tuples.append(result)
         return tuples

   # Compare attribute of two users. Works for every attribute except
   # wpm and birthday.
   def compareTwoUsers(self, attribute, user1, user2):
      if ((attribute != "wpm") and (attribute != "birthday")):
         cmd = "SELECT Q1.%s FROM Questions Q1 JOIN Questions Q2 ON Q1.%s = Q2.%s WHERE Q1.id = %d AND Q2.id = %d" % (attribute, attribute, attribute, user1, user2)
      elif (attribute == "wpm"):
         cmd = "SELECT Q1.wpm FROM Questions Q1 JOIN Questions Q2 WHERE Q1.id = %d AND Q2.id = %d AND (Q1.wpm BETWEEN (Q2.wpm - 10) AND (Q2.wpm + 10))" % (user1, user2)
      elif (attribute == "city"):
         statecmd = "SELECT Q1.state FROM Questions Q1 JOIN Questions Q2 WHERE Q1.state = Q2.state AND Q1.id = %d AND Q2.id = %d" % (user1, user2)
         self.cur.execute(cmd)
         res = self.cur.fetchall()
         if (len(res) != 0):
            cmd = "SELECT Q1.city FROM Questions Q1 JOIN Questions Q2 WHERE Q1.city = Q2.city AND Q1.id = %d AND Q2.id" % (user1, user2)
         else:
            return False
      else:
         cmd = "SELECT birthday FROM Questions Q1 JOIN Questions Q2 WHERE Q1.id = user1 AND Q2.id = user2 AND (YEAR(Q1.birthday) BETWEEN (YEAR(Q2.birthday) - 5) AND (YEAR(Q2.birthday) + 5)"
      self.cur.execute(cmd)
      res = self.cur.fetchall()
      # If there is a result, the attribute matches.
      if (len(res) != 0):
         return True
      return False

   # Returns the total number of users currently in the database
   def numUsers(self):
      self.cur.execute("SELECT COUNT(*) FROM Users")
      res = self.cur.fetchall()
      return res[0][0]

   # Create list of tuples for scores.
   def createScores(self, userid):
      currUser = 1
      totalUsers = self.numUsers()
      scores = []
      while (currUser <= totalUsers):
         if (currUser != userid):
            scores.append((currUser, 0))
         currUser += 1
      return scores

   # Compare attribute of one user against all other users and add to 
   # total scores. Returns scores array of tuples (userId, score).
   def compareAttribute(self, attribute, weight, userid, scores):
      currUser = 1
      totalUsers = self.numUsers()
      while (currUser <= totalUsers):
         # Do not compare the user with itself.
         if (currUser != userid):
            # If the current user has the same value for this attribute, 
            # add the weight of the attribute to the score.
            if (self.compareTwoUsers(attribute, userid, currUser)):
               scores = [(uid, score) if (uid != currUser) else (uid, score + weight) for (uid, score) in scores]
         currUser += 1
      return scores

   # Calculates the score for the user against all other users.
   # Returns the scores in an array of tuples (userId, score).
   def calculateScores(self, userid):
      scores = self.createScores(userid)
      stateW = 8
      cityW = 3
      favoriteOSW = 4
      phoneOSW = 6
      gamingW = 5
      favLangW = 9
      scores = self.compareAttribute('favoriteOS', favoriteOSW, userid, scores)
      scores = self.compareAttribute('phoneOS', phoneOSW, userid, scores)
      scores = self.compareAttribute('state', stateW, userid, scores)
      scores = self.compareAttribute('city', cityW, userid, scores)
      scores = self.compareAttribute('gaming', gamingW, userid, scores)
      scores = self.compareAttribute('favLang1', favLangW, userid, scores)
      return scores

   # Sorts in order from highest score to lowest score for particular user.
   def sortProfiles(self, userid):
      scores = self.calculateScores(userid)
      scores.sort(key=lambda tup:tup[1], reverse = True)
      # Return an array of users with user data.
      tuples = []
      for (uid, score) in scores:
         self.cur.execute("SELECT * FROM Questions Q JOIN Users U ON Q.id = U.id WHERE Q.id = " + str(uid) + ";")
         res = self.cur.fetchall()
         tuples.append(res[0])
      return tuples

   def userProfile(self, userid):
      self.cur.execute("SELECT * FROM Questions Q JOIN Users U ON Q.id = U.id WHERE Q.id = " + str(userid) + ";")
      res = self.cur.fetchall()
      return res[0]
