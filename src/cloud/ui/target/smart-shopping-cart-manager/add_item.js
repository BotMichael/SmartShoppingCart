function add_item() {
    let item = document.getElementById("item").value.toString();
    let region = document.getElementById("region").value.toString();
    let price = document.getElementById("price").value.toString();
    add_new_item(item, region, price);
}


function add_new_item(item, region, price){
    $.ajax("api/addaction", {
        method: "POST",
        data: {"action": "add_item", "item": item, "region": region, "price": price},
        success: resultData => add_item_alert(resultData)
    });
}


function add_item_alert(resultData){
    console.log(resultData);
    let resultDataJson = JSON.parse(resultData);
    if(resultDataJson["status"] == "success"){
        alert("Add item " + resultDataJson["item"] + "in region " + resultDataJson["region"] + " with price " + resultDataJson["price"] + " successfully.");
    }
    else{
        alert("Fail to add the item.");
    }
}