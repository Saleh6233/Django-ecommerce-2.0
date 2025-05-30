// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get search input elements
    const mainSearchInput = document.getElementById('mainSearchInput');
    const mobileSearchInput = document.getElementById('mobileSearchInput');
    const searchResults = document.getElementById('searchResults');
    const mobileSearchResults = document.getElementById('mobileSearchResults');

    // Function to perform search
    function performSearch(input, resultsContainer) {
        const query = input.value.trim();

        // Clear previous results and hide the container if query is empty
        if (query === '') {
            resultsContainer.innerHTML = '';
            resultsContainer.classList.add('d-none');
            return;
        }

        // Make AJAX request
        fetch(`/ajax-search/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                // Clear previous results
                resultsContainer.innerHTML = '';

                if (data.results.length > 0) {
                    // Create results HTML
                    data.results.forEach(product => {
                        const resultItem = document.createElement('div');
                        resultItem.className = 'p-2 border-bottom search-result-item';
                        resultItem.innerHTML = `
                            <a href="${product.url}" class="d-flex align-items-center text-decoration-none text-dark">
                                ${product.image ? `<img src="${product.image}" class="me-2" width="40" height="40" style="object-fit: cover;">` : ''}
                                <div>
                                    <div>${product.title}</div>
                                    <div class="small text-muted">$${product.price}</div>
                                </div>
                            </a>
                        `;

                        resultsContainer.appendChild(resultItem);
                    });

                    // Add "View all results" link
                    const viewAllLink = document.createElement('div');
                    viewAllLink.className = 'p-2 text-center';
                    viewAllLink.innerHTML = `
                        <a href="/search/?q=${encodeURIComponent(query)}" class="btn btn-sm btn-outline-dark w-100">
                            View all results for "${query}"
                        </a>
                    `;
                    resultsContainer.appendChild(viewAllLink);

                    // Show results container
                    resultsContainer.classList.remove('d-none');
                } else {
                    // No results found
                    const noResults = document.createElement('div');
                    noResults.className = 'p-3 text-center text-muted';
                    noResults.textContent = `No products found for "${query}"`;
                    resultsContainer.appendChild(noResults);
                    resultsContainer.classList.remove('d-none');
                }
            })
            .catch(error => {
                console.error('Error fetching search results:', error);
            });
    }

    // Set up event listeners for main search input
    if (mainSearchInput) {
        // Debounce function to limit API calls
        let mainDebounceTimer;
        mainSearchInput.addEventListener('input', function() {
            clearTimeout(mainDebounceTimer);
            mainDebounceTimer = setTimeout(() => {
                performSearch(mainSearchInput, searchResults);
            }, 300);
        });

        // Hide search results when clicking outside
        document.addEventListener('click', function(event) {
            if (!mainSearchInput.contains(event.target) && !searchResults.contains(event.target)) {
                searchResults.classList.add('d-none');
            }
        });
    }

    // Set up event listeners for mobile search input
    if (mobileSearchInput) {
        let mobileDebounceTimer;
        mobileSearchInput.addEventListener('input', function() {
            clearTimeout(mobileDebounceTimer);
            mobileDebounceTimer = setTimeout(() => {
                performSearch(mobileSearchInput, mobileSearchResults);
            }, 300);
        });

        // Hide mobile search results when clicking outside
        document.addEventListener('click', function(event) {
            if (!mobileSearchInput.contains(event.target) && !mobileSearchResults.contains(event.target)) {
                mobileSearchResults.classList.add('d-none');
            }
        });
    }

    // Add CSS for search results
    const style = document.createElement('style');
    style.textContent = `
        .search-result-item:hover {
            background-color: #f8f9fa;
        }
        
        .search-result-item a {
            display: block;
        }
    `;
    document.head.appendChild(style);

    // Message timer for alerts
    const messageTimer = document.getElementById('message-timer');
    if (messageTimer) {
        setTimeout(function() {
            messageTimer.style.display = 'none';
        }, 5000); // Hide after 5 seconds
    }
});








var message_timeout = document.getElementById("message-timer");

setTimeout(function () {
  message_timeout.style.display = "none";
}, 2500);
