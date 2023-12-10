function register_bullet() {
    $.ajax({
        url: 'http://localhost:8000/equipamento/bullets/get/',
        type: 'POST',
        dataType: 'json',
        data: {
            user: user,
            pass: pass
        },
        success: function (bullets) {
            var bullet_options = '';
            if (bullets) {
                $.each(bullets, function (i, bullet) {
                    bullet_options += '\n<option value="' + bullet['id'] + '">' + bullet['description'] + '</option>';
                });
            }

            var csrf = $('input[type="hidden"][name="csrfmiddlewaretoken"]');
            var bullet_html =
                `
                <form method="post" action="." class="form-element" style="min-height:220px;min-whidth:300px;">
                    <div style="background-color: rgb(91,73,57, 0.9); whidth: 100%; border-radius: 20px; text-align:center; color: #fff; padding:5px;">
                        </div>
                            <h3 class="input-title">
                                CADASTRAR MUNIÇÃO
                            </h3>
                            <div class="input-div">
                            ` + csrf[0].outerHTML + `
                            <div class="input-box">
                                <h4 class="input-title">MUNIÇÕES</h4>
                                <div class="select">
                                    <select name="bullet" class="select-field" id="dropdown_bullets" required>
                ` +
                    bullet_options
                + `
                                    </select>
                                </div>
                            </div>
                            <div class="input-box">
                            <h4 class="input-title">QUANTIDADE</h4>
                                <input name="amount" class="input-data" type="number" id="input_amount" required>
                            </div>
                        <div class="finalize-registration" style="padding-bottom: 0px;">
                        <label><input type="submit" id="submit-btn" class="box-shadow-registration" value="Adicionar"></label>
                    </div>
                </form>
                `;

            popUp("", { closeBtn: true, adicional: bullet_html });
        },
        error: function (error) {
            console.error('Erro ao buscar dados da munição:', error);
        }
    });
}

$(document).ready(function () {
    var choicesTypes = $("#type-choices");
    choicesTypes.val(""); 

    // Requisita e valida o UID para cadastrar
    function fetchUid() {
        $.ajax({
            url: 'http://localhost:8000/equipamento/valid_uid',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                var input_uid = $("#input-uid");
                var text_uid = $("#text-uid");

                if (data.msm != null) {
                    popUp(data.msm);
                }
                if (data.uid !== '') {
                    input_uid.val(data.uid);
                    text_uid.text("UID : " + data.uid);

                    clearInterval(interval);
                } else if (input_uid.val() !== '') {
                    text_uid.text("UID : " + input_uid.val());
                    clearInterval(interval);
                }
            },
            error: function (error) {
                console.error('Erro ao buscar dados do equipamento:', error);
            }
        });
    }

    var interval = setInterval(fetchUid, 1000);

    // Limpa o UID setado
    $("#clear-btn").on('click', function () {
        var input_uid = $("#input-uid");
        var text_uid = $("#text-uid");

        setInterval(fetchUid, 1000);

        input_uid.val('');
        text_uid.text("Passe a tag no sensor");
    });

    // Checa tudo antes de dar o submit
    $("#submit-btn").on('click', function () {
        var choices = $(".type-choices-type");
        var selectedIndex = 0;

        choices.each(function () {
            if ($(this).val() !== '') {
                selectedIndex++;
            }
        });

        var serial_num = $("#serial-number-input").val();

        if (serial_num === '') {
            popUp("Por favor insira o número de série.");
            return;
        }

        $.ajax({
            url: 'http://localhost:8000/equipamento/valid_serial_number/' + serial_num + '/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                if (data.exists) {
                    popUp("Numero de série já cadastrado!");
                    return;
                }
            },
            error: function (error) {
                console.error('Erro ao buscar dados do equipamento:', error);
            }
        });

        if ($("#input-uid").val() === '') {
            popUp("Por favor passe uma tag no sensor.");
            return;
        }
        if (selectedIndex === 0) {
            popUp("Por favor selecione uma opção de modelo.");
            return;
        }
        if (selectedIndex === 1) {
            $("#form-equipment").submit();
        }
    });

    // Função para registrar munição
    
    $("#register-bullet-btn").on('click', function () {
        register_bullet();
    });

    // Libera o campo certo com base no tipo selecionado
    function change_field() {
        var selectedValue = choicesTypes.val();
        var choiceModels = $("#type-choices-" + selectedValue);
        var choices = $(".type-choices-type");
        var labelClass = $("#lable-type-input");

        if (labelClass) labelClass.remove();

        choices.prop('disabled', true).hide().val('');

        if (selectedValue !== '') {
            choiceModels.show().prop('disabled', false);
        }
    }

    // Executa a função uma vez inicialmente
    change_field();

    choicesTypes.on('change', change_field);
});

