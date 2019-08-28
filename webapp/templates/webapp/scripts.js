
//this function runs everytime we want to update the JSON data div.
function updateQuoteDiv(){
	var quoteJSON = JSON.stringify({"name" : document.getElementById("quoteNameID").value,
	"price" : parseInt(document.getElementById("quotePriceID").value),
	"items" : quoteItems}, undefined, "\t");
	//var textedJson = JSON.stringify(quoteJSON, undefined, "\t");
	$('#JSONdiv').text(quoteJSON);
	
}

function onAddItemClicked(){
	addItem();
	updateQuoteDiv();
}

function addItem(){

let JSONcandidate = {"name" : document.getElementById("candidate").value, "id" : quoteItems.length};
quoteItems.push(JSONcandidate);
}

function onRemoveItemClicked(){
	findAndRemove(quoteItems,'name',document.getElementById("candidate").value);
	updateQuoteDiv();
}

function findAndRemove(array, property, value) {
  array.forEach(function(result, index) {
	if(result[property] === value) {
	  //Remove from array
	  array.splice(index, 1);
	}    
  });
  return array;
}

function getToken(usernameInputID,passwordInputID){
	//send a POST request to localhost/api-token-auth/ with username and password to get back a token
	JSONbody = {'username':document.getElementById(usernameInputID).value, 'password': document.getElementById(passwordInputID).value}
	
	$.ajax({
	url: 'http://localhost:8000/api-token-auth/',
	type: 'POST',
	dataType: 'json',
	/* data: JSON.stringify(body), /* wrong */
	data: JSONbody, /* right */
	headers:{
	"X-CSRFToken": "{{ csrf_token }}"},
	success: function(result) {
		//called when successful
		document.getElementById('tokenSpan').innerHTML = result['token'];
	},

	error: function(result) {
		//called when there is an error
		document.getElementById('tokenSpan').innerHTML = 'Error, wrong credentials';
	},
});
}