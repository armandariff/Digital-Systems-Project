var rating = 0;
var results = null;
    
// Function to Give Rating
function rated(value, itemid){
    // var token = '{{csrf_token}}'
    console.log(token, "ratings")
    rating = value;
    for(var i = 1; i <= value; i++){
        document.getElementById(itemid+'star'+String(i)).className = 'fa fa-star checked';
    }
    for(var i = value+1; i <= 5; i++){
        document.getElementById(itemid+'star'+String(i)).className = 'fa fa-star unchecked';
    }
    fetch("/add-watch-list/", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': token,
        },
        body: JSON.stringify({'rating': rating, 'movies': itemid})
    }).then(repsonse => {
        repsonse.json()
    }).then(response => {
        console.log(response)
    }) 
};

// Function to clear all rating
function clearall(itemid){
    rating = 0;
    for(var i = 1; i <= 5; i++){
        // console.log(i, 'star'+String(i))
        document.getElementById(String(itemid)+'star'+String(i)).className = 'fa fa-star unchecked';
    }
    fetch("/add-watch-list/", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': token,
        },
        body: JSON.stringify({'rating': rating, 'movies': itemid})
    }).then(repsonse => {
        repsonse.json()
    }).then(response => {
        console.log(response)
    })
}

// function UpdateIndex(){
//     $.ajax({
//         type: 'POST',
//         url: '/search',
//         data: {'query':$('#search').val()},
//         success: function(data){
//             $('#main-div').html(data);
//         },
//         error: function(){
//             console.log('Error is ajax');
//         }
//     })
// }