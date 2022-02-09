
document.addEventListener('click', function(event){
    if ( event.target.matches('#search_reset') ) {
        event.preventDefault()
        document.getElementById('searchinput').value=''
        document.getElementById('searchform').submit()
    }
})



/* https://getbootstrap.com/docs/5.0/components/popovers/ */
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    })
