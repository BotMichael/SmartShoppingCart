function add_user() {
    let phone = document.getElementById("phone").value.toString();
    let password = document.getElementById("password").value.toString();
    add_new_user(phone, password);
}


function add_new_user(phone, password){
    $.ajax("api/addaction", {
        method: "POST",
        data: {"action": "add_user", "phone": phone, "password": password},
        success: resultData => add_user_alert(resultData)
    });
}


function add_user_alert(resultData){
    let resultDataJson = JSON.parse(resultData);
    if(resultDataJson["status"] == "success"){
        alert("Add user with phone " + resultDataJson["phone"] + " successfully.");
    }
    else{
        alert("Fail to add the user.");
    }
}