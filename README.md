# Flask-Login-With-JWT


![Capture](https://user-images.githubusercontent.com/107461719/224911529-ad298671-2d6d-458c-95b7-1186344c60ba.PNG)

# Flask-Login System  Using JWT
- setup all step .

## add some configrations 
    app.secret_key = 'jaypateltopsecret789654123'
    app.config["JWT_SECRET_KEY"] =    "jaypateltopsecret789654123" 
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=60) 
    jwt = JWTManager(app)


## Login Page :
 - import flask_jwt_extended
 - add token :
    ```
    access_token = create_access_token(identity='Sallubhai')
    res = redirect(url_for('HomePage'))
    set_access_cookies(res, access_token) 
    session['login_user'] = userdata['name']
    return res
- genrate token uisng identity and encrpt them using jwt
- add redirect function as a veriable 
- create session for chekup 
- return redircet veriable  
## Home Page
- when use authentication token then use 
 ``` 
 @jwt_required() 
```
- check session if session is present then name display on home page  other vise name no dispaplay 

## Test Page :
- add @jwt_required()  and access token using 
```
        data = get_jwt_identity()
        name = data['name']
        ```

## logout
 - delete session id and create blank 
 - in home page if session is not define then redirect Login  page 
 - when login then session create and then we use test other vise not use Test page 


