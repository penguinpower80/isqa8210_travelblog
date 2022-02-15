document.addEventListener('click', function (event) {
    if (event.target.matches('#search_reset')) {
        event.preventDefault()
        document.getElementById('searchinput').value = ''
        document.getElementById('searchform').submit()
    }
    if (event.target.matches('.favoritebutton')) {
        event.preventDefault();
        post = event.target.getAttribute("data-pk")
        if (event.target.classList.contains("fa-heart-o")) {
            fetch("/favorite/" + post).then(function (r) {
                if (r.ok) {
                    event.target.classList.toggle("fa-heart-o")
                    event.target.classList.toggle("fa-heart")
                }
            })
        } else {
            fetch("/favorite/" + post + "/delete").then(function (r) {
                if (r.ok) {
                    event.target.classList.toggle("fa-heart-o")
                    event.target.classList.toggle("fa-heart")
                }
            })
        }


    }
})

/* https://mymth.github.io/vanillajs-datepicker */
const elems = document.querySelectorAll('.dateinput');
const dateparser = {
    toValue(date, format, locale) {
        let dateparts = date.split('-')
        let dateObject;
        if (dateparts[0].length == 4) {
            dateObject = new Date(dateparts[0], dateparts[1] - 1, dateparts[2]);
        } else {
            dateObject = new Date(dateparts[2], dateparts[0] - 1, dateparts[1]);
        }
        return dateObject
    },
    toDisplay(date, format, locale) {
        return (date.getMonth() + 1) + '/' + date.getDate() + '/' + date.getFullYear()
    },
}
for (const elem of elems) {
    elem.type = 'text';
    const datepicker = new Datepicker(elem, {
        'autohide': true,
        'format': dateparser
    });
}

/* https://getbootstrap.com/docs/5.0/components/popovers/ */
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
})


