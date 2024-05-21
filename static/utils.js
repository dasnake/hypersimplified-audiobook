    function arrayBufferToMd5(arrayBuffer) {
	// Convert ArrayBuffer to WordArray first
	var wordArray = CryptoJS.lib.WordArray.create(arrayBuffer);
    
	// Compute MD5 hash
	var hash = CryptoJS.MD5(wordArray);
    
	// Convert the hash to a hexadecimal string
	return hash.toString(CryptoJS.enc.Hex);
    }
    
    function getClientId() {
        let clientId = localStorage.getItem("clientId");
        if (!clientId) {
            clientId = Math.floor(Math.random() * 10000).toString();
            localStorage.setItem("clientId", clientId);
        }
        return clientId;
    }

    // Function to fetch the file size from the FastAPI endpoint
    function fetchFileSize() {
	return fetch(`https://${location.host}/size`)
	    .then(response => {
		if (!response.ok) {
		    throw new Error('Network response was not ok');
		}
		return response.json();
	    })
	    .then(data => {
		if (data.error) {
		    console.error('Error fetching file size:', data.error);
		} else {
		    console.log("File size", data.file_size);
		    //totalSize = data.file_size;
		}
		return data.file_size;
	    })
	    .then(size => { return size; })
	    .catch(error => {
		console.error('There was a problem with your fetch operation:', error);
	    });
    }    

// Function to calculate the percentage
    function calculatePercentage(totalSize) {
	const position = getCookie('last_position');
	if (position) {
	    console.log("Current position", position);
	    console.log("Max position", totalSize);
	    const percentage = (position / totalSize) * 100;
	    console.log(`Percentage: ${percentage.toFixed(2)}%`);
	    return percentage.toFixed(2);
	} else {
	    console.log("Cookie 'position' not found.");
	    return 0;
	}
    }
    
    function getCookie(name) {
	let cookieArray = document.cookie.split(';'); // Split document.cookie at each semicolon (which separates cookies)
	for (let cookie of cookieArray) {
            let [cookieName, cookieValue] = cookie.trim().split('='); // Split each individual cookie into name and value at the equal sign
            if (cookieName === name) {
		return cookieValue; // Return the value if the names match
            }
	}
	return null; // Return null if the cookie was not found
    }

    function updateCookie(name, value) {
	const daysToExpire = 7; // Number of days until the cookie should expire
	let expires = new Date(Date.now() + daysToExpire * 86400000).toUTCString(); // Calculate expiration date
	document.cookie = `${name}=${value}; expires=${expires}; path=/`; // Set the cookie with expiration and path
    }
