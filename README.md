1. Resources
    1. Char (Character)
        - name
        - age
        - height
        - weight
        - affiliation
        - df (Devil Fruit)
    2. Users
        - firstname
        - lastname
        - email
        - encrypted_password

2. Schemas
    1. Chars
        - CREATE TABLE opChars (id INTEGER PRIMARY KEY, 
        - name TEXT, 
        - age INT, 
        - height TEXT, 
        - weight TEXT, 
        - affiliation TEXT, 
        - df TEXT);
    2. Users
        - CREATE TABLE opUsers (id INTEGER PRIMARY KEY,
        - firstname TEXT,
        - lastname TEXT,
        - email TEXT,
        - encrypted_password TEXT);

3. REST Endpoints
    - Retrive char collection GET /chars
    - Retrieve single char GET /chars/id
    - Create new char POST /chars
    - Update char PUT /chars/id
    - Delete char DELETE /chars/id
    - Create new user POST /users
    - login user/ create session POST /sessions

4. Passwords
    - Password hashing done with bcrypt()