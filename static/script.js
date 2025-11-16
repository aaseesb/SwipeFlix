// for overlay of decline and accept
const overlayleft = document.getElementById('overlay-left');
const overlayright = document.getElementById('overlay-right');
const hiddenClass = 'hidden';


function handleHover(event) {
    const trigger = event.currentTarget;
    const targetElement = trigger.querySelector('.button-option');

    if (event.type == "mouseenter") {
        targetElement.classList.remove(hiddenClass);
    }
    if (event.type == "mouseleave") {
        targetElement.classList.add(hiddenClass);
    }
}

overlayleft.addEventListener('mouseenter', handleHover);
overlayleft.addEventListener('mouseleave', handleHover);
overlayright.addEventListener('mouseenter', handleHover);
overlayright.addEventListener('mouseleave', handleHover);


// updating movie.html
function updateMovie(likedStatus) {
    fetch('/update_movie', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ likedStatus })
    }).then(response => response.json())
    .then(data => {
        document.getElementById('movie-card').innerHTML = data.movie_html;
    })
    .catch(error => console.error("Error:", error));
}