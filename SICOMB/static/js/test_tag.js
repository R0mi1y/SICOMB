let tags = [];

let interval = setInterval(fetchTagData, 2000);

function clearData() {
    tags = [];
    refreshTable();
}

function fetchTagData() {
    let url = '/equipamento/tag/api/test/';

    fetch(url, {
            method: 'POST', // Método HTTP POST para enviar dados
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                'user': user,
                'pass': pass,
            })
        })
        .then(response => response.json())
        .then(data => {
            let uid = data.uid;
            if (typeof uid === 'string' && uid.trim() !== '') {
                let is_in = false;
                console.log(uid);
                data['read'] = data['read'] ?? 1;

                tags.forEach((tag) => {
                    if (uid == tag.uid) {
                        tag.read += 1;
                        refreshTable();
                        is_in = true;
                    }
                    return;
                });
                if (!is_in) {
                    tags.push(data);
                    refreshTable();
                }
            }
        })
        .catch(error => {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {
                timer: 2000,
                overlay: false
            });
        });
}

function refreshTable() {
    let body_table = '';

    if(tags.length > 0) {
        tags.forEach((tag) => {
            console.log(tag);
            body_table += `<tr><td>${tag.equipment?.serial_number ?? '-'}</td>
            <td>${tag.equipment?.status ?? '-'}</td>
            <td>${tag.type ?? '-'}</td>
            <td>${tag.model?.model ?? '-'}</td>
            <td>${tag.equipment?.activated ?? '-'}</td>
            <td>${tag.uid ?? '-'}</td>
            <td>${tag.equipment?.activator ?? '-'}</td>
            <td>${tag.read ?? '-'}</td></tr>`;
        });
    } else {
        body_table = `<tr><td colspan="100%">Nenhuma tag passada</td></tr>`;
    }

    $('#body_table').html(body_table);
}