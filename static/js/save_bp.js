let saveButtons = document.getElementsByClassName('save-button');

for (let i=0; i<saveButtons.length; i++){
    
  saveButtons[i].addEventListener('click', function(e){
    let endpoint = "/save-blogpost/";
    let slug = this.dataset.slug;
    let url = endpoint + slug

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