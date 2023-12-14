var fetching = false;

function fetchList() {
    if (fetching) {
        // Ainda estamos buscando os dados, então saia desta chamada
        return;
    }

    fetching = true; // Definir o indicador de que estamos buscando os dados

    $.ajax({
        url: 'http://localhost:8000/police/get_fingerprint/',
        type: 'POST',
        dataType: 'json',
        data: {
            user: user,
            pass: pass
        },
        complete: function() {
            fetching = false; // Resetar o indicador após a conclusão da solicitação
        },
        success: function(data) {
            if (data.status) {
                $('input[name="type_login"]').val("fingerprint");
                $('input[name="matricula"]').val(data.matricula);
                $('input[name="token"]').val(data.token);

                $('#form_login').submit();
            } else if (data.message) {
                console.log(data.message);
                popUp(data.message, { timer: 2000, overlay: false });
            }
        }
    });
}

setInterval(fetchList, 3000);
