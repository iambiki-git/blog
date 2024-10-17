const csrftoken = '{{ csrf_token }}';

const menu_icon = document.querySelector("#menu-icon");
const menus = document.querySelector("#mobile-menus");

menu_icon.addEventListener("click", ()=>{
    if(menus.style.display == 'flex'){
        menus.style.display = "none";
    }else {
        menus.style.display = "flex";
    }
})


//search functionality
// function searchPosts() {
//     let query = document.getElementById('searchInput').value;

//     if (query.length === 0) {
//         document.getElementById('searchResults').innerHTML = '';
//         return;  // Don't send an empty query to the server
//     }

//     fetch(`/search/?q=${query}`, {
//         method: 'GET',
//         headers: {
//             'X-CSRFToken': csrftoken,  // CSRF token to secure the request
//             'Content-Type': 'application/json',
//         },
//     })
//     .then(response => response.json())
//     .then(data => {
//         let resultDiv = document.getElementById('searchResults');
//         resultDiv.innerHTML = '';  // Clear previous results

//         if (data.results.length > 0) {
//             data.results.forEach(post => {
//                 let postElement = document.createElement('div');
//                 postElement.innerHTML = `<p>${post.title}</p>`;
//                 resultDiv.appendChild(postElement);
//             });
//         } else {
//             resultDiv.innerHTML = '<p>No such result</p>';
//         }
//     })
//     .catch(error => {
//         console.error('Error fetching search results:', error);
//     });
// }

function searchPosts() {
    let query = document.getElementById('searchInput').value;

    if (query.length === 0) {
        document.getElementById('searchResults').innerHTML = '';
        document.getElementById('searchResults').classList.add('hidden');  // Hide results if query is empty
        return;
    }

    fetch(`/search/?q=${query}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken,  // CSRF token to secure the request
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        let resultDiv = document.getElementById('searchResults');
        resultDiv.innerHTML = '';  // Clear previous results

        if (data.results.length > 0) {
            data.results.forEach(post => {
                let postElement = document.createElement('div');
                postElement.className = 'p-2 border-b border-gray-200';  // Tailwind styling for each result
                postElement.innerHTML = `<p class="text-gray-700">${post.title}</p>`;
                resultDiv.appendChild(postElement);
            });
            resultDiv.classList.remove('hidden');  // Show results
        } else {
            resultDiv.innerHTML = '<p class="p-2 text-gray-500">No such result</p>';
            resultDiv.classList.remove('hidden');  // Show "No result" message
        }
    })
    .catch(error => {
        console.error('Error fetching search results:', error);
    });
}
