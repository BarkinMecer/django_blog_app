// CREATE OPERATION

let comment_form = document.getElementById('create-comment');
let form_input = document.getElementById('form-input');

comment_form.addEventListener('submit', function(e){

    let endpoint = "/create-comment/";
    let slug = this.dataset.slug + "/";
    let content = form_input.value;
    let url = endpoint + slug + content;

    fetch(url)
    .then(response => response.json())
    .then(data => {
        location.reload();
        })
    .catch(err => console.log(err))

    e.preventDefault();
})


// DELETE OPERATION

let deleteComments = document.getElementsByClassName('delete-comment');
let deleteAccepts = document.getElementsByClassName('delete-accept');
let deleteCancels = document.getElementsByClassName('delete-cancel');

for(let i=0; i<deleteComments.length; i++){
    deleteComments[i].addEventListener('click', function(e){
        deleteComments[i].setAttribute("hidden", true);
        deleteAccepts[i].removeAttribute("hidden");
        deleteCancels[i].removeAttribute("hidden");
        e.preventDefault();
    }) 

    deleteCancels[i].addEventListener('click', function(e){
        deleteComments[i].removeAttribute("hidden");
        deleteAccepts[i].setAttribute("hidden", true);
        deleteCancels[i].setAttribute("hidden", true);
        e.preventDefault();
    })     

    deleteAccepts[i].addEventListener('click', function(e){
        deleteComments[i].removeAttribute("hidden");
        deleteAccepts[i].setAttribute("hidden", true);
        deleteCancels[i].setAttribute("hidden", true);


        let endpoint = "/delete-comment/";
        let commentId = this.dataset.id;
        let url = endpoint + commentId
    
        console.log(url)
        
        fetch(url)
        .then(response => response.json())
        .then(data => {
            location.reload();
        })
        .catch(err => console.log(err))


        e.preventDefault();
    }) 

};