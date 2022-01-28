document.addEventListener('click', function(event){
    if ( event.target.matches('#search_reset') ) {
        event.preventDefault()
        document.getElementById('searchinput').value=''
        document.getElementById('searchform').submit()
    }
})


