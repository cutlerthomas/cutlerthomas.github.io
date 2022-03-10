console.log("One Piece database");
var n = 1;
var url = "http://localhost:8080/chars";
var listDiv = document.getElementById("favList");
var ul = document.createElement("ul");
var add = document.querySelector("#my-button");
var clear = document.querySelector("#clear-button");
var favList = [];
console.log("add query:", add);
add.onclick = function() {
    postData();
}


clear.onclick = function() {
    var empty = "";
    document.getElementById("op-name").value =  empty;
        document.getElementById("op-age").value = empty;
        document.getElementById("op-height").value = empty;
        document.getElementById("op-weight").value = empty;
        document.getElementById("op-affiliation").value = empty;
        document.getElementById("op-df").value = empty;
}


function loadCharList() {
    fetch(url).then(function (response) {
        response.json().then(function (data) {
            console.log("from the server:", data);
            favList = data;
            reBuildList();
        });
    });
}

function postData() {
    var nameValue = document.getElementById("op-name").value;
    var ageValue = document.getElementById("op-age").value; 
    var heightValue = document.getElementById("op-height").value;
    var weightValue = document.getElementById("op-weight").value;
    var affiliationValue = document.getElementById("op-affiliation").value;
    var dfValue = document.getElementById("op-df").value;
    var data = "name=" + encodeURIComponent(nameValue);
    data += "&age=" + encodeURIComponent(ageValue);
    data += "&height=" + encodeURIComponent(heightValue);
    data += "&weight=" + encodeURIComponent(weightValue);
    data += "&affiliation=" + encodeURIComponent(affiliationValue);
    data += "&df=" + encodeURIComponent(dfValue);
    fetch(url, {
        method: "POST",
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: data,
    }).then(function (response) {
        loadCharList();
    });
}

function reBuildList() {
    listDiv.innerHTML = "";
    favList.forEach(function (char) {
        var li = document.createElement("li");
        var nameDiv = document.createElement("div");
        nameDiv.innerHTML = "Name: " + char.name;
        nameDiv.classList.add("char-name");
        li.appendChild(nameDiv)
        var ageDiv = document.createElement("div");
        ageDiv.innerHTML = "Age: " + char.age;
        li.appendChild(ageDiv);
        var heightDiv = document.createElement("div");
        heightDiv.innerHTML = "Height: " + char.height;
        li.appendChild(heightDiv);
        var weightDiv = document.createElement("div");
        weightDiv.innerHTML = "Weight: " + char.weight;
        li.appendChild(weightDiv);
        var affiliationDiv = document.createElement("div");
        affiliationDiv.innerHTML = "Affiliation: " + char.affiliation;
        li.appendChild(affiliationDiv);
        var dfDiv = document.createElement("div");
        dfDiv.innerHTML = "Devil Fruit: " + char.df;
        li.appendChild(dfDiv);
        var delBut = document.createElement("button");
        delBut.innerHTML = "Delete";
        delBut.classList.add("button");
        delBut.onclick = function() {
            console.log("delete button clicked");
            if (confirm("Are you sure?")) {
                deleteChar(char.id);
            }
        };
        var editBut = document.createElement("button");
        editBut.innerHTML = "Edit";
        editBut.classList.add("button");
        editBut.onclick = function() {
            console.log("edit button clicked");
            editChar(char.id, char.name, char.age, char.height, char.weight, char.affiliation, char.df);
        };
        li.appendChild(delBut);
        li.appendChild(editBut);
        listDiv.appendChild(li);
    })
}

function deleteChar(char_id) {
    fetch(url + "/" + char_id, {
        method: "DELETE"
    }).then(function(response) {
        if (response.status == 200) {
            console.log("character succesfully deleted");
            loadCharList();
        }
    });
}

function editChar(char_id) {
    favList.forEach(function(char) {
        if (char.id == char_id) {
            var nameValue = char.name;
            var ageValue = char.age; 
            var heightValue = char.height;
            var weightValue = char.weight;
            var affiliationValue = char.affiliation;
            var dfValue = char.df;
            document.getElementById("op-name").value = nameValue;
            document.getElementById("op-age").value = ageValue;
            document.getElementById("op-height").value = heightValue;
            document.getElementById("op-weight").value = weightValue;
            document.getElementById("op-affiliation").value = affiliationValue;
            document.getElementById("op-df").value = dfValue;
        }
    })
    var conBut = document.getElementById("confirm-button")
    conBut.onclick = function() {
        var nameValue = document.getElementById("op-name").value;
        var ageValue = document.getElementById("op-age").value;
        var heightValue = document.getElementById("op-height").value;
        var weightValue = document.getElementById("op-weight").value;
        var affiliationValue = document.getElementById("op-affiliation").value;
        var dfValue = document.getElementById("op-df").value;
        var data = "name=" + encodeURIComponent(nameValue);
        data += "&age=" + encodeURIComponent(ageValue);
        data += "&height=" + encodeURIComponent(heightValue);
        data += "&weight=" + encodeURIComponent(weightValue);
        data += "&affiliation=" + encodeURIComponent(affiliationValue);
        data += "&df=" + encodeURIComponent(dfValue);
        fetch(url + "/" + char_id, {
            method: "PUT",
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: data,
        }).then(function (response) {
            if (response.status == 200) {
                console.log("character succesfully changed");
                loadCharList();
            }
        });
    }
}

loadCharList();