document.addEventListener('DOMContentLoaded', () => {

    // Helper function to get a cookie value by name
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    // Function to handle the logout process
    function logoutUser() {
        document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        window.location.href = 'index.html';
    }

    // Attach logout function to the logout button if it exists
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', logoutUser);
    }

    // Function to check login state and update UI (header, buttons)
    function checkLoginState() {
        const token = getCookie('token');
        const loginLink = document.getElementById('login-link');
        const logoutButton = document.getElementById('logout-button');
        const addReviewButton = document.getElementById('add-review-button');

        if (token) {
            if (loginLink) loginLink.style.display = 'none';
            if (logoutButton) logoutButton.style.display = 'block';
            if (addReviewButton) addReviewButton.style.display = 'inline-block';
        } else {
            if (loginLink) loginLink.style.display = 'block';
            if (logoutButton) logoutButton.style.display = 'none';
            if (addReviewButton) addReviewButton.style.display = 'none';
        }
    }

    // Check login state on every page load
    checkLoginState();

    // --- Page-specific logic starts here ---

    // Logic for Login Page
    if (window.location.pathname.includes('login.html')) {
        const loginForm = document.getElementById('login-form');
        const errorMessageDiv = document.getElementById('error-message');
        if (loginForm) {
            loginForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                try {
                    const response = await fetch('https://your-api-url/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email, password })
                    });
                    if (response.ok) {
                        const data = await response.json();
                        document.cookie = `token=${data.access_token}; path=/; secure; samesite=Lax`;
                        window.location.href = 'index.html';
                    } else {
                        const errorData = await response.json();
                        const message = errorData.message || 'An error occurred during login.';
                        errorMessageDiv.textContent = 'Login failed: ' + message;
                        errorMessageDiv.style.display = 'block';
                    }
                } catch (error) {
                    errorMessageDiv.textContent = 'Network error. Please try again.';
                    errorMessageDiv.style.display = 'block';
                    console.error('Network error:', error);
                }
            });
        }
    }

    // Logic for Index Page
    if (window.location.pathname.includes('index.html')) {
        let allPlaces = [];
        const placesListContainer = document.getElementById('places-list');
        const loadingMessage = document.getElementById('loading-message');
        
        async function fetchPlaces() {
            const token = getCookie('token');
            const headers = { 'Content-Type': 'application/json' };
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
            try {
                const response = await fetch('https://your-api-url/places', { headers });
                if (response.ok) {
                    allPlaces = await response.json();
                    displayPlaces(allPlaces);
                } else {
                    placesListContainer.innerHTML = '<p>Failed to load places. Please try again later.</p>';
                }
            } catch (error) {
                placesListContainer.innerHTML = '<p>Network error. Could not connect to the API.</p>';
                console.error('Fetch places error:', error);
            } finally {
                if (loadingMessage) loadingMessage.style.display = 'none';
            }
        }

        function displayPlaces(places) {
            placesListContainer.innerHTML = '';
            if (places.length === 0) {
                placesListContainer.innerHTML = '<p>No places found matching the filter.</p>';
                return;
            }
            places.forEach(place => {
                const placeCard = document.createElement('div');
                placeCard.classList.add('place-card');
                placeCard.innerHTML = `
                    <img src="${place.image_url || 'images/default-place.jpg'}" alt="${place.name}">
                    <div class="place-info">
                        <h3>${place.name}</h3>
                        <p>Price per night: $${place.price_per_night}</p>
                        <a href="place.html?id=${place.id}" class="details-button">View Details</a>
                    </div>
                `;
                placesListContainer.appendChild(placeCard);
            });
        }

        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('change', (event) => {
                const maxPrice = event.target.value;
                let filteredPlaces = [];
                if (maxPrice === 'all') {
                    filteredPlaces = allPlaces;
                } else {
                    const priceValue = parseInt(maxPrice);
                    filteredPlaces = allPlaces.filter(place => place.price_per_night <= priceValue);
                }
                displayPlaces(filteredPlaces);
            });
        }
        
        fetchPlaces(); // Initial call to fetch places
    }

    // Logic for Place Details and Add Review Pages
    if (window.location.pathname.includes('place.html') || window.location.pathname.includes('add_review.html')) {
        const placeId = new URLSearchParams(window.location.search).get('id');
        const token = getCookie('token');

        // Logic for Place Details Page
        if (window.location.pathname.includes('place.html') && placeId) {
            async function fetchAndDisplayPlaceDetails() {
                const headers = { 'Content-Type': 'application/json' };
                if (token) {
                    headers['Authorization'] = `Bearer ${token}`;
                }
                try {
                    const placeResponse = await fetch(`https://your-api-url/places/${placeId}`, { headers });
                    const placeData = await placeResponse.json();
                    const reviewsResponse = await fetch(`https://your-api-url/places/${placeId}/reviews`, { headers });
                    const reviewsData = await reviewsResponse.json();
                    
                    document.getElementById('place-main-image').src = placeData.image_url || 'images/default-place.jpg';
                    document.getElementById('place-main-image').alt = placeData.name;
                    document.getElementById('place-name').textContent = placeData.name;
                    document.getElementById('place-host').textContent = placeData.host_id;
                    document.getElementById('place-price').textContent = placeData.price_per_night;
                    document.getElementById('place-description').textContent = placeData.description;

                    const amenitiesList = document.getElementById('amenities-list');
                    amenitiesList.innerHTML = '';
                    if (placeData.amenities && placeData.amenities.length > 0) {
                        placeData.amenities.forEach(amenity => {
                            const li = document.createElement('li');
                            li.textContent = amenity.name;
                            amenitiesList.appendChild(li);
                        });
                    } else {
                        amenitiesList.innerHTML = '<li>No amenities listed.</li>';
                    }
                    displayReviews(reviewsData);
                } catch (error) {
                    console.error('Error fetching place details:', error);
                    document.querySelector('.place-details-container').innerHTML = '<h2>Failed to load place details.</h2>';
                }
            }

            function displayReviews(reviews) {
                const reviewsList = document.getElementById('reviews-list');
                reviewsList.innerHTML = '';
                if (reviews.length === 0) {
                    reviewsList.innerHTML = '<p>No reviews yet. Be the first to add one!</p>';
                    return;
                }
                reviews.forEach(review => {
                    const reviewCard = document.createElement('div');
                    reviewCard.classList.add('review-card');
                    reviewCard.innerHTML = `
                        <p class="review-comment">"${review.text}"</p>
                        <p class="review-meta"><strong>User:</strong> ${review.user_id} | <strong>Rating:</strong> ${review.rating}/5</p>
                    `;
                    reviewsList.appendChild(reviewCard);
                });
            }
            fetchAndDisplayPlaceDetails();
        }

        // Logic for Add Review Page
        if (window.location.pathname.includes('add_review.html')) {
            if (!token) {
                alert('You must be logged in to add a review.');
                window.location.href = 'index.html';
                return;
            }
            const placeNameSpan = document.getElementById('place-name-review');
            const reviewForm = document.getElementById('review-form');
            const statusMessage = document.getElementById('status-message');
            
            async function getPlaceName() {
                try {
                    const response = await fetch(`https://your-api-url/places/${placeId}`);
                    const placeData = await response.json();
                    placeNameSpan.textContent = placeData.name;
                } catch (error) {
                    placeNameSpan.textContent = '...';
                }
            }

            if (placeId) {
                getPlaceName();
            } else {
                reviewForm.innerHTML = '<h2>Error: No place specified.</h2>';
            }

            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const rating = document.getElementById('rating').value;
                const reviewComment = document.getElementById('review-comment').value;

                try {
                    const response = await fetch(`https://your-api-url/places/${placeId}/reviews`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify({ rating, text: reviewComment })
                    });
                    if (response.ok) {
                        statusMessage.textContent = 'Review submitted successfully!';
                        statusMessage.className = 'status-success';
                        statusMessage.style.display = 'block';
                        reviewForm.reset();
                    } else {
                        const errorData = await response.json();
                        statusMessage.textContent = '
