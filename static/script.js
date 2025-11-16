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

function initialize() {
    // for overlay of decline and accept
    const overlayleft = document.getElementById('overlay-left');
    const overlayright = document.getElementById('overlay-right');
    const declineButton = document.getElementById('declineButton');
    const acceptButton = document.getElementById('acceptButton');

    // attach event listeners
    overlayleft.addEventListener('mouseenter', handleHover);
    overlayleft.addEventListener('mouseleave', handleHover);
    overlayright.addEventListener('mouseenter', handleHover);
    overlayright.addEventListener('mouseleave', handleHover);

    // updating movie.html
    declineButton.addEventListener('click', () => updateMovie(false));
    acceptButton.addEventListener('click', () => updateMovie(true));
}


function updateMovie(likedMovie) {
    const card = document.getElementById('movie-card');
    // fade out
    card.classList.remove('opacity-100');
    card.classList.add('opacity-0');
    
    // make sure it's faded out before fetching
    card.addEventListener('transitionend', function handleFadeOut() {
        card.removeEventListener('transitionend', handleFadeOut);
        fetch('/update_movie', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ likedMovie })
        }).then(response => response.json())
        .then(data => {
            // change html
            card.innerHTML = data.movie_html;
            
            // make sure opacity=0 is applied
            void card.offsetWidth;

            // fade in before showing
            requestAnimationFrame(() => {
                card.classList.remove('opacity-0');
                card.classList.add('opacity-100');
            });

            // re-initialize elements
            initialize();
        })
        .catch(error => console.error("Error:", error));
    });
}
