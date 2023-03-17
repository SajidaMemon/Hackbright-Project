const headers = {
    'Content-Type': 'application/json'
}


function addedtocart (item_id){
    console.log(item_id)
    fetch(`/add_to_cart/${item_id}`,{
        
            method: "GET",
            headers: headers
        })
        .then(response => response.text())
        .then(data => alert(data))
    

    

}