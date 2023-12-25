function search() {
    var matriculaInput = document.querySelector('#matricula-input');
    var matricula = matriculaInput.value;
    if (matricula != '') {
        window.location.href = '/police/search/' + matricula + '/';
    } else {
        var messageText = "Insira uma matrícula";
        // Crie um elemento de alerta para cada mensagem
        popUp(messageText, {timer: 2000, overlay: false});
    }
}

$(document).ready(function() {
    $("#delete-digital").on("click", function () {
        popUp("Tem certeza que deseja deletar a digital de " + $("input[name='police_name']").val() + "?", {
            yn: true,
            yesFunction: function () {
                $.ajax({
                    url: "/police/fingerprint/delete/" + $("input[name='police_id']").val(),
                    type: "POST",
                    dataType: "json",
                    data: {
                        user: user,
                        pass: pass,
                    },
                    success: function (data) {
                        if(data.status) {
                            popUp("Deletado com sucesso!", {closeBtn: false});
                            setTimeout(function () {
                                window.location="/police/filter/";
                            }, 1000);
                        } else {
                            popUp(data.message, {timer: 2000, overlay: false});
                        }
                    },
                    error: function (error) {
                        console.log("Erro de requisição: " + error);
                        popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
                    }
                });
            }
        });
    });

    $(document).ready(function () {
        $("#register-fingerprint").on("click", function (e) {
            $.ajax({
                url: "/police/register/fingerprint/" + $("input[name='police_id']").val() + "/",
                type: "POST",
                dataType: "json",
                data: {
                    user: user,
                    pass: pass,
                },
                success: function (data) {
                    popUp(data['message']);
                },
                error: function (error) {
                    console.log("Erro de requisição: " + error);
                    popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
                }
            });
        });
    });
});

