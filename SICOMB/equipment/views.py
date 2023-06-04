from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from . import models
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict


@login_required
def register_equipment(request):
    if request.method == "POST":
        models.Equipment(
            serial_number=request.POST.get("serial_number"),
            uid=request.POST.get("uid"),
            type=request.POST.get("type"),
            type_id=request.POST.get("type_id"),
        ).save()
        print("Chegou aqui")
        return render(
            request,
            "equipment/register-equipment.html",
            {"message": "Equipamento cadastrado com sucesso"},
        )
    else:
        return render(request, "equipment/register-equipment.html")


# Retorna o equipamento referente ao uid mais recente em formato JSON
def get_equipment(request):
    data = {"uid": ""}

    # models.Model_armament(
    #     model = "Pistola Glock",
    #     caliber = ".44",
    #     image_path = "img/pistola.png",
    #     description = "Descrição aqui"
    # ).save()
    # models.Equipment(
    #     serial_number="165161",
    #     uid="7c",
    #     type="armament",
    #     observation="Observação aqui",
    #     armament=models.Model_armament.objects.get(pk=1),
    # ).save()

    # Para caso o que o usuário esteja solicitando não seja algo que tenha uma tag
    if request.GET.get("type") != None:
        data["registred"] = request.POST.get("type")

        # Caso seja uma granada
        if request.POST.get("type") == "grenada":
            try:
                grenada = models.Grenada.objects.get(pk=request.GET.get("id"))
            except models.Equipment.DoesNotExist:
                return JsonResponse(
                    {"uid": "", "msm": "Equipamento não cadastrado"}
                )  # Caso o equipamento não esteja cadastrado ele simplismente ignora

            data["grenada"] = model_to_dict(grenada)

        # Caso seja uma munição
        if request.POST.get("type") == "bullet":
            try:
                bullet = models.Bullet.objects.get(pk=request.GET.get("pk"))
            except models.Equipment.DoesNotExist:
                return JsonResponse(
                    {"uid": "", "msm": "Equipamento não cadastrado"}
                )  # Caso o equipamento não esteja cadastrado ele simplismente ignora

            data["equipment"] = model_to_dict(bullet)

    # Para os equipamentos com a tag
    if settings.AUX["UID"] != "":
        data["uid"] = settings.AUX["UID"]

        try:
            equipment = models.Equipment.objects.get(
                uid=settings.AUX["UID"]
            )  # Recupera o objeto Equipamento
        except models.Equipment.DoesNotExist:
            return JsonResponse(
                {"uid": "", "msm": "Equipamento não cadastrado"}
            )  # Caso o equipamento não esteja cadastrado ele simplismente ignora

        data["registred"] = equipment.type
        data["equipment"] = model_to_dict(equipment)
        # soma o caminho estatico com o da imagem

        if (
            equipment.armament != None
        ):  # Recupera o objeto armamento, que complementa o equipamento
            equipment.armament.image_path = equipment.armament.image_path
            data["model"] = model_to_dict(equipment.armament)

        elif (
            equipment.wearable != None
        ):  # Recupera o objeto vestimento, que complementa o equipamento
            equipment.wearable.image_path = equipment.wearable.image_path
            data["model"] = model_to_dict(equipment.wearable)

        elif (
            equipment.accessory != None
        ):  # Recupera o objeto acessorio, que complementa o equipamento
            equipment.accessory.image_path = equipment.accessory.image_path
            data["model"] = model_to_dict(equipment.accessory)

        print(data)
        settings.AUX["UID"] = ""
    return JsonResponse(data)  # Retorna o dicionário em forma de api


# Recebe o UID do ESP
def set_uid(request):
    # Armazena o UID recebido numa variável global no arquivo settings
    if request.method == "POST":
        # TODO Mudar para método POST aqui e no esp
        settings.AUX["UID"] = request.POST.get("uid")
    elif request.method == "GET":
        # TODO Mudar para método POST aqui e no esp
        settings.AUX["UID"] = request.GET.get("uid")

    return HttpResponse(
        f"""<body>
  <div class="container">
    <p class="success-text">Sucesso, uid = {settings.AUX['UID']}</p>
    <a class="resend-link" href="set?uid={settings.AUX['UID']}">Reenviar</a>
  </div>
</body>
<style>
body {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      background-color: #f7f7f7;
      font-family: Arial, sans-serif;
    }}

    .container {{
      text-align: center;
      padding: 60px;
      background-color: #fff;
      border-radius: 12px;
      box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }}

    .success-text {{
      font-size: 36px;
      color: #333;
      margin-bottom: 60px;
    }}

    .resend-link {{
      display: inline-block;
      padding: 30px 60px;
      font-size: 28px;
      background-color: #4caf50;
      color: #fff;
      text-decoration: none;
      border-radius: 10px;
      transition: background-color 0.3s ease;
    }}

    .resend-link:hover {{
      background-color: #45a049;
    }}

</style>
"""
    )


# Retorna a lista de tipos, modelos e tipos de equipamentos em formato json para a página de registro
def get_models_equipment(request):
    armaments = models.Model_armament.objects.all()
    armament_models = []

    for i in armaments:
        armament_models.append(i.model)

    print(armament_models)

    wearbles = models.Model_wearable.objects.all()
    wearbles_models = []

    for i in wearbles:
        wearbles_models.append(i.model)

    accessory = models.Model_accessory.objects.all()
    accessory_models = []

    for i in accessory:
        accessory_models.append(i.model)

    grenada = models.Grenada.objects.all()
    grenada_models = []

    for i in grenada:
        grenada_models.append(i.model)

    bullet = models.Bullet.objects.all()
    bullet_models = []

    for i in bullet:
        bullet_models.append(i.model)

    types = {
        "Granada": {"name": "Granada", "eng_name": "Granade", "models": grenada_models},
        "Munição": {"name": "Munição", "eng_name": "Bullet", "models": bullet_models},
        "Acessório": {
            "name": "Acessorio",
            "eng_name": "Acessory",
            "models": accessory_models,
        },
        "Vestível": {
            "name": "Vestível",
            "eng_name": "Wearble",
            "models": wearbles_models,
        },
        "Armamento": {
            "name": "Armamento",
            "eng_name": "Armament",
            "models": armament_models,
        },
    }

    return JsonResponse(types)
