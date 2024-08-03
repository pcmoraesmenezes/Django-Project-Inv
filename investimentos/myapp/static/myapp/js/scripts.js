document.addEventListener('DOMContentLoaded', function () {
    // Carregar dados ao iniciar
    fetchData('/get_sheet/');

    // Atualizar dados ao clicar no botão
    document.getElementById('update-button').addEventListener('click', function () {
        updateData('/data/');
    });
});

function fetchData(url) {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#investments-table tbody');
            tableBody.innerHTML = ''; // Limpar a tabela

            const investments = data.data_frame || data;

            const keys = Object.keys(investments);
            const rowsCount = investments[keys[0]].length;

            for (let i = 0; i < rowsCount; i++) {
                const row = document.createElement('tr');

                keys.forEach(key => {
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
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('Dados atualizados:', data);
            location.reload(); // Recarregar a página
        })
        .catch(error => console.error('Error updating data:', error));
}
