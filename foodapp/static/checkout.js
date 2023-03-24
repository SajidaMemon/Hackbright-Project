const validateCard = () => {
    let cardNumber = document.getElementById("card-number").value;
    if (cardNumber == "") {
        alert("Please enter card number")
        return false;
    }
}