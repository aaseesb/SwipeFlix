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

initialize();


function updateMovie(likedMovie) {
    const movieCard = document.getElementById('card-to-animate');
    const cardContainer = document.getElementById('movie-card');

    if (!movieCard) return;

    // start throw animation
    movieCard.classList.remove('throw-right', 'throw-left', 'fade-in', 'opacity-0');
    
    // force reflow so animation won't replay
    void movieCard.offsetWidth;
    
    if(likedMovie) {
        movieCard.classList.add('throw-right'); // right
    } else {
        movieCard.classList.add('throw-left'); // left
    }

    movieCard.addEventListener('animationend', function handleEnd() {
        movieCard.removeEventListener('animationend', handleEnd);

        // fetch new movie
        fetch('/update_movie', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ likedMovie })
        })
        .then(response => response.json())
        .then(data => {
            // replace container content
            cardContainer.innerHTML = data.movie_html;

            // select new card
            const newCard = document.getElementById('card-to-animate');
            if (!newCard) return;

            // start invisible
            newCard.classList.add('opacity-0');

            // force reflow
            void newCard.offsetWidth;

            // smooth fade-in
            newCard.classList.add('fade-in');

            // remove throw class
            newCard.classList.remove('throw-right','throw-left');

            // reattach hover & buttons
            initialize();
        })
        .catch(error => console.error("Error:", error));
    });
}

// fade in animation
// function updateMovie(likedMovie) {
//     const movieCard = document.getElementById('movie-card');

//     // fade out
//     movieCard.classList.remove('opacity-100');
//     movieCard.classList.add('opacity-0');
    
//     // make sure it's faded out before fetching
//     movieCard.addEventListener('transitionend', function handleFadeOut() {
//         movieCard.removeEventListener('transitionend', handleFadeOut);
//         fetch('/update_movie', {
//             method: 'POST',
//             headers: {'Content-Type': 'application/json'},
//             body: JSON.stringify({ likedMovie })
//         }).then(response => response.json())
//         .then(data => {
//             // change html
//             movieCard.innerHTML = data.movie_html;
            
//             // make sure opacity=0 is applied
//             void movieCard.offsetWidth;

//             // fade in before showing
//             requestAnimationFrame(() => {
//                 movieCard.classList.remove('opacity-0');
//                 movieCard.classList.add('opacity-100');
//             });

//             // re-initialize elements
//             initialize();
//         })
//         .catch(error => console.error("Error:", error));
//     });
// }
