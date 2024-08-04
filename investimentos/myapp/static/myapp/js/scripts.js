document.addEventListener('DOMContentLoaded', function () {
    fetchData('/get_sheet/');

    document.getElementById('update-button').addEventListener('click', function () {
        updateData('/data/');
    });
});

function fetchData(url) {
    fetch(url)
    .then(response => response.json())
    .then(data => {
        if (data.message !== "Dados obtidos com sucesso!") {
            console.error('Erro ao obter dados:', data.message);
            return;
        }

        const tableBody = document.querySelector('#investments-table tbody');
        tableBody.innerHTML = ''; // Limpar a tabela

        const investments = data.data;

        const rowsCount = Object.keys(investments['Tipo de investimento']).length;

        for (let i = 0; i < rowsCount; i++) {
            const row = document.createElement('tr');

            Object.keys(investments).forEach(key => {
                const cell = document.createElement('td');
                cell.textContent = investments[key][i];
                row.appendChild(cell);
            });

            tableBody.appendChild(row);
        }
    })
    .catch(error => console.error('Error fetching data:', error));
}

function updateData(url) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        location.reload(); 
    })
    .catch(error => console.error('Error updating data:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
