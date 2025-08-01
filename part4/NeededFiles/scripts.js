document.addEventListener('DOMContentLoaded', () => {
    const loginButton = document.querySelector('.login-button');
    const logoutButton = document.getElementById('logout-button');
    const token = localStorage.getItem('access_token');

    if (loginButton) {
        loginButton.style.display = token ? 'none' : 'inline-block';
    }

    if (logoutButton) {
        logoutButton.style.display = token ? 'inline-block' : 'none';

        logoutButton.addEventListener('click', async () => {
            const token = localStorage.getItem('access_token');

            if (token) {
                try {
                    await fetch('http://localhost:5000/api/v1/auth/logout', {
                        method: 'DELETE',
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });
                } catch (error) {
                    console.error('Logout failed:', error);
                }
                localStorage.removeItem('access_token');
            }
            window.location.href = 'index.html';
        });
    }

    // Login page logic
    if (window.location.pathname.includes('login.html')) {
        const loginForm = document.getElementById('login-form');
        let statusMessage = document.getElementById('status-message');

        if (!statusMessage) {
            statusMessage = document.createElement('div');
            statusMessage.id = 'status-message';
            statusMessage.className = 'status-message';
            loginForm.parentNode.insertBefore(statusMessage, loginForm.nextSibling);
        }

        const urlParams = new URLSearchParams(window.location.search);
        const successMessage = urlParams.get('success');

        if (successMessage) {
            statusMessage.textContent = 'Account created successfully. Please log in.';
            statusMessage.className = 'status-message status-success';
            statusMessage.style.display = 'block';
        }

        if (loginForm) {
            loginForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                statusMessage.style.display = 'none';

                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;

                try {
                    const response = await fetch('http://localhost:5000/api/v1/auth/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email, password })
                    });

                    const data = await response.json();

                    if (response.ok) {
                        localStorage.setItem('access_token', data.access_token);
                        window.location.href = 'index.html';
                    } else {
                        statusMessage.textContent = data.message || 'Login failed. Please check your credentials.';
                        statusMessage.className = 'status-message status-error';
                        statusMessage.style.display = 'block';
                    }
                } catch (error) {
                    statusMessage.textContent = 'Network error. Please try again later.';
                    statusMessage.className = 'status-message status-error';
                    statusMessage.style.display = 'block';
                }
            });
        }
    }

    // Load and display places on index.html
    if (window.location.pathname.endsWith('index.html') || window.location.pathname === '/' ) {
        const placesContainer = document.getElementById('places');

        fetch('http://127.0.0.1:5000/api/v1/places')
            .then(response => response.json())
            .then(places => {
                places.forEach(place => {
                    const placeDiv = document.createElement('div');
                    placeDiv.className = 'place-card';

                    placeDiv.innerHTML = `
                        <h3>${place.name}</h3>
                        <div class="place-images">
                            <img src="static/images/place1.jpg" alt="Image 1" class="place-image">
                            <img src="static/images/place2.jpg" alt="Image 2" class="place-image">
                        </div>
                        <p>${place.description || ''}</p>
                        <ul>
                            <li>
                                <img src="static/images/icon_bed.png" alt="Bedrooms" class="amenity-icon" />
                                Bedrooms: ${place.number_rooms}
                            </li>
                            <li>
                                <img src="static/images/icon_bath.png" alt="Bathrooms" class="amenity-icon" />
                                Bathrooms: ${place.number_bathrooms}
                            </li>
                            <li>
                                <img src="static/images/icon_wifi.png" alt="WiFi" class="amenity-icon" />
                                WiFi Available
                            </li>
                            <li>Max Guests: ${place.max_guests}</li>
                            <li>Price per Night: $${place.price_per_night}</li>
                        </ul>
                    `;
                    placesContainer.appendChild(placeDiv);
                });
            })
            .catch(error => {
                console.error('Error fetching places:', error);
                if (placesContainer) {
                    placesContainer.innerHTML = '<p>Failed to load places.</p>';
                }
            });
    }
});
document.addEventListener("DOMContentLoaded", function () {
  const params = new URLSearchParams(window.location.search);
  const placeId = params.get("place_id");

  // Fetch and display place name if the span exists
  if (placeId) {
    fetch(`/api/v1/places/${placeId}`)
      .then(res => res.json())
      .then(place => {
        const nameSpan = document.getElementById("place-name-review");
        if (nameSpan) nameSpan.textContent = place.name;

        const detailsSection = document.getElementById("place-details");
        if (detailsSection) {
          detailsSection.innerHTML = `
            <h1>${place.name}</h1>
            <p>${place.description || "No description available."}</p>
            <p><strong>Price:</strong> $${place.price_by_night}</p>
            <p><strong>Guests:</strong> ${place.max_guest} | <strong>Bedrooms:</strong> ${place.number_rooms} | <strong>Bathrooms:</strong> ${place.number_bathrooms}</p>
          `;
        }
      });
  }

  // Handle review form submission
  const reviewForm = document.getElementById("review-form");
  if (reviewForm) {
    reviewForm.addEventListener("submit", function (e) {
      e.preventDefault();

      const ratingEl = document.getElementById("rating");
      const rating = ratingEl ? parseInt(ratingEl.value) : 5;

      const comment =
        document.getElementById("review-comment")?.value ||
        document.getElementById("review-text")?.value;

      fetch(`/api/v1/places/${placeId}/reviews`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rating, text: comment })
      })
        .then(res => res.json())
        .then(() => {
          const msg = document.getElementById("status-message");
          if (msg) {
            msg.textContent = `Review posted!`;
            msg.style.color = "green";
          }
          reviewForm.reset();
        })
        .catch(() => {
          const msg = document.getElementById("status-message");
          if (msg) {
            msg.textContent = "Failed to post review.";
            msg.style.color = "red";
          }
        });
    });
  }
});

