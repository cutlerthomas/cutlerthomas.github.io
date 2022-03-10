1. Resource
    - Char (Character)
        - name
        - age
        - height
        - weight
        - affiliation
        - df (Devil Fruit)

2. Schema
    - CREATE TABLE opChars (id INTEGER PRIMARY KEY, 
    name TEXT, 
    age INT, 
    height TEXT, 
    weight TEXT, 
    affiliation TEXT, 
    df TEXT);

3. REST Endpoints
    - Retrive char collection GET /chars
    - Retrieve single char GET /chars/<id>
    - Create new char POST /chars
    - Update char PUT /chars/<id>
    - Delete char DELETE /chars/<id>>