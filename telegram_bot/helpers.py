import pytz
import datetime


def get_formated_date():

    # Defina o fuso horário do Brasil
    fuso_horario_brasil = pytz.timezone("America/Sao_Paulo")

    # Obtenha a data e hora atual no Brasil
    data_hora_brasil = datetime.datetime.now(fuso_horario_brasil)

    # Formate e imprima a data e hora
    formato = "%d-%m-%Y %H:%M:%S"  # Formato desejado, incluindo o fuso horário
    data_hora_formatada = data_hora_brasil.strftime(formato)

    return data_hora_formatada
