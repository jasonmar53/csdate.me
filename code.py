from queries import *
import random
import bcrypt
import shutil

# html templates
render = web.template.render('templates/')

# All urls
urls = (
    '/', 'index',
    '/login', 'login',
    '/questions', 'questions',
    '/main', 'main',
    '/search', 'search',
    '/test', 'test',
    '/logout', 'logout',
    '/deepSearch', 'deepSearch',
    '/profile(\d+)', 'profile',
    '/settings', 'settings',
    '/upload', 'upload'
)

# Initializing database connector
DB = Database()

class index:
    def GET(SELF):
        token = web.cookies().get("token")
        if token:
            return web.HTTPError('301', {'Location': 'http://www.csdate.me/main'})
        else:
            return render.index()
    def POST(self):
        i = web.input()
        check = DB.addUserCheck(i.username, i.email)
        # Username/Email not taken
        if check == True:
          salt = bcrypt.gensalt().replace("'","")
          hashpw = bcrypt.hashpw(i.password.encode('UTF_8'), salt.encode('UTF_8')).replace("'","") # had to encode before hashing
          DB.addUser(i.username, i.email, hashpw, salt)
          return render.userCreated();
        # Username/Email taken
        else:
          return render.signupTaken();

# Most pages will get redirected here if cookie is not set/cookie is expired
class login:
   def GET(self):
      token = web.cookies().get("token")
      if token:
        return web.HTTPError('301', {'Location': 'http://www.csdate.me/main'}) 
      else:
         # Direct to default login page
         return render.login()
   def POST(self):
      # Querying database
      i = web.input()
      auth = DB.authCheck(i.username, i.password)
      if auth == True:
         token = tokenSet(i.username)
         userId = DB.usernameToId(i.username)
         qCheck = DB.questionsDone(userId)
         if (qCheck == 1):
            return web.HTTPError('301', {'Location': 'http://www.csdate.me/main'}) 
         else:
            return web.HTTPError('301', {'Location': 'http://www.csdate.me/questions'})
      else:
         # Direct to failed login page
         return render.loginFailed()

# Main page accessed after login with results of our algorithm.
class main:
   def GET(self):
      token = web.cookies().get('token')
      i = web.input(search=None, attribute=None)
      #check to see if the cookie exists
      if token:
         userId = DB.tokenToId(token)
         params = web.input()
         page = params.page if hasattr(params, 'page') else 1
         if userId == -1:
            return web.HTTPError('301', {'Location': 'http://www.csdate.me/logout'})
         if (i.search==None):
            matches = DB.sortProfiles(userId)
            lower, upper = get_slices(page)
            return render.main(userId, matches[lower:upper], False)
         else:
            matches = DB.singleSearch(i.search, i.attribute, userId)
            lower, upper = get_slices(page)
            return render.main(userId, matches, True)
      else:
         return web.HTTPError('301', {'Location': 'http://www.csdate.me/login'})
   def POST(self):
      return web.HTTPError('301', {'Location': 'http://www.csdate.me/logout'})


#testing uploading here
class upload:
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render.upload()
    def POST(self):
        token = web.cookies().get('token')
        if token:
            userId = DB.tokenToId(token)
            if userId == -1: 
                return web.HTTPError('301', {'Location': 'http://www.csdate.me/logout'})
            else:
                x = web.input(myfile={}, verify=None)
                filedir = 'static/images' # change this to the directory you want to store the file in.

    #file has been checked on clientside
                if (x.verify == "good"):
                    if 'myfile' in x: # to check if the file-object is created
                        filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
                        filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
                        extension = filename.split('.')[-1] #recieves the extension
                        fout = open(filedir +'/'+ str(userId) + "." + extension,'wb') # creates the file where the uploaded file should be stored
                        fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
                        fout.close() # closes the file, upload complete.
                        DB.uploadImage(userId, str(userId) + "."  + extension)
                        return web.HTTPError('301', {'Location': 'http://www.csdate.me/main'})
                    else:
                        print "file submission has failed clientside check please redirect to error page?"
                if(i.verify == "bad"):
                    render.questionsIncorrect()

        else: 
            return web.HTTPError('301', {'Location': 'http://www.csdate.me/login'})

class questions:
   def GET(self):
      token = web.cookies().get('token')
      if token:
           return render.questions()
      else:
         userId = DB.tokenToId(token)
         if userId == -1: 
            return web.HTTPError('301', {'Location': 'http://www.csdate.me/logout'})

   def POST(self):
           token = web.cookies().get('token')
           userId = DB.tokenToId(token)
           i = web.input(myfile={}, verify=None)
           filedir = 'static/images' # change this to the directory you want to store the file in.

    #file has been checked on clientside
           if (i.verify == "good"):
              if 'myfile' in i: # to check if the file-object is created
                 filepath=i.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
                 filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
                 extension = filename.split('.')[-1] #recieves the extension
                 fout = open(filedir +'/'+ str(userId) + "." + extension,'wb') # creates the file where the uploaded file should be stored
                 fout.write(i.myfile.file.read()) # writes the uploaded file to the newly created file.
                 fout.close() # closes the file, upload complete.
                 DB.uploadImage(userId, str(userId) + "."  + extension)
              else:
                 render.questionsIncorrect()
                 print "file submission has failed clientside check please redirect to error page?"
           if(i.verify == "bad"):
                render.questionsIncorrect()
           DB.setQuestions(userId, i.firstName, i.middleName, i.lastName, 
                                        i.gender, i.state, i.city, i.birthday, 
                                        i.favoriteOS, i.phoneOS, i.relationship, i.gaming, 
                                        i.favLang1, i.favLang2, i.favLang3, i.favHobby1,
                                        i.favHobby2, i.favHobby3, i.wpm, i.interest, i.bio)
           return web.HTTPError('301', {'Location': 'http://www.csdate.me/main'}) 


# Searching other users page. -- pending deletion
class search:
  def GET(self):
    i = web.input(search=None)
    if(i.search == None):            
        return render.search()
    else:
        DB.singleSearch(i.search, i.attribute)
        return render.search()        

# Testing Hashing here
class test:
    def GET(self):
        return render.test()

class logout:
   def GET(self):
      cookie = web.cookies().get('token')
      if cookie:
         DB.removeToken(cookie)
         web.setcookie('token', '', expires="-1", domain="csdate.me")
         return render.logout()
      else:
         web.HTTPError('301', {'Location': 'http://www.csdate.me/login'})

class deepSearch:
    def GET(self):
        token = web.cookies().get("token")
        if token:
            i = web.input(submit=None)
            userId = DB.tokenToId(token)
            if(i.submit == None):
                return render.deepSearch()
            else:
                matches = DB.indepthSearch(i.required, i.firstName, i.middleName, i.lastName, i.gender, i.state, i.city, i.favoriteOS, i.phoneOS, i.relationship, i.gaming, i.favLang1, i.favLang2, i.favLang3, i.wpm, userId, i.interest)
            return render.main(userId, matches, True)
        else:
            return web.HTTPError('301', {'Location': 'http://www.csdate.me/main'})

class profile:
   def GET(self, profileId):
      token = web.cookies().get("token")
      if token:
         userId = DB.tokenToId(token)
         if userId == -1:
            return web.HTTPError('301', {'Location': 'http://www.csdate.me/logout'})
         tuple = DB.userProfile(profileId)
         return render.profile(tuple)
      else:
         return web.HTTPError('301', {'Location': 'http://www.csdate.me/login'})

class settings:
   def GET(self):
      token = web.cookies().get('token')
      if token:
           return render.settings()
      else:
         userId = DB.tokenToId(token)
         if userId == -1: 
            return web.HTTPError('301', {'Location': 'http://www.csdate.me/logout'})

   def POST(self):
           token = web.cookies().get('token')
           userId = DB.tokenToId(token)
           i = web.input(myfile={}, verify=None)
           filedir = 'static/images' # change this to the directory you want to store the file in.
           
           if (i.reset == "pressed"):
              DB.deleteImage(userId)
    #file has been checked on clientside
           if (i.verify == "good"):
              if 'myfile' in i: # to check if the file-object is created
                 filepath=i.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
                 filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
                 extension = filename.split('.')[-1] #recieves the extension
                 fout = open(filedir +'/'+ str(userId) + "." + extension,'wb') # creates the file where the uploaded file should be stored
                 fout.write(i.myfile.file.read()) # writes the uploaded file to the newly created file.
                 fout.close() # closes the file, upload complete.
                 DB.uploadImage(userId, str(userId) + "."  + extension)
              else:
                 render.questionsIncorrect()
                 print "file submission has failed clientside check please redirect to error page?"
           if(i.verify == "bad"):
                render.questionsIncorrect()
           DB.updateQuestions(userId, i.firstName, i.middleName, i.lastName, 
                                        i.gender, i.interest, i.state, i.city, i.birthday, 
                                        i.favoriteOS, i.phoneOS, i.relationship, i.gaming, 
                                        i.favLang1, i.favLang2, i.favLang3, i.favHobby1,
                                        i.favHobby2, i.favHobby3, i.wpm, i.bio)
           return web.HTTPError('301', {'Location': 'http://www.csdate.me/main'}) 

def tokenSet(username):
    r = random.randint(0, 2147483647)
    rString = str(r)
    token = bcrypt.hashpw(rString, bcrypt.gensalt())
    token = token.replace("'","")
    validToken = DB.addToken(username, token)
    web.setcookie('token', validToken, expires='7200', domain="csdate.me", secure=False)

def get_slices(page, page_size=10):
  return (page_size * (page - 1), (page_size * page + 1))

def internalerror():
    return web.internalerror("Bad, bad server. No donut for you. Please contact the server admins of the error.")

if __name__ == "__main__":
    web.config.debug = False
    app = web.application(urls, globals())
    app.run()
