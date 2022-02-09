
document.addEventListener('click', function(event){
    if ( event.target.matches('#search_reset') ) {
        event.preventDefault()
        document.getElementById('searchinput').value=''
        document.getElementById('searchform').submit()
    }
console.log(event.target);
    if ( event.target.matches('.favoritebutton') ) {
        event.preventDefault();
        post = event.target.getAttribute("data-pk")
        if ( event.target.classList.contains("fa-heart-o") ) {
            fetch("/favorite/"+ post).then(function(r){
                if ( r.ok ) {
                    event.target.classList.toggle("fa-heart-o")
                    event.target.classList.toggle("fa-heart")
                }
            })
        } else {
            fetch("/favorite/"+ post +"/delete").then(function(r){
                if ( r.ok ) {
                    event.target.classList.toggle("fa-heart-o")
                    event.target.classList.toggle("fa-heart")
                }
            })
        }


    }
})



/* https://getbootstrap.com/docs/5.0/components/popovers/ */
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    })


