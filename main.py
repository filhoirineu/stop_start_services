import os
import traceback

from rich import print
from lib.functions import *
from lib.console import CONSOLE_ATUAL

from rich.align import Align

from time import sleep
from datetime import datetime

def main():

    clear_screen()
    pula_linha(CONSOLE_ATUAL,2)
    print(
        Align("[bold yellow]   ... AGUARDE, CARREGANDO AS CONFIGURACOES ... ", align="center"))

    services_info = get_info_from_config_ini_file()
    sleep(0.5)

    if len(services_info) > 0:
        while True:
            clear_screen()
            option = initial_screen(CONSOLE_ATUAL, services_info)

            clear_screen()
            if option in ("START","STOP","RESTART"):
                process_services(CONSOLE_ATUAL, services_info, option)
            elif option in ("SAIR", "EXIT"):
                finaliza_programa(CONSOLE_ATUAL)
                break
            elif option in ("ATUALIZAR", "REFRESH"):
                pass
            else:

                id_exists = False
                for s in services_info:
                    if s.id == option:
                        id_exists = True
                        service = ServiceManager(s.service_name,s.process_name)
                        if service.is_online:
                            newoption = "STOP"
                        else:
                            newoption = "START"

                        process_services(CONSOLE_ATUAL, [s] , newoption)
                        break


                if not id_exists:
                    error_message(CONSOLE_ATUAL,
                "OPCAO: " + option + ", INVALIDA!!!")

    else:

        error_message(CONSOLE_ATUAL,
            "PROBLEMAS COM O ARQUIVO DE CONFIGURACAO (CONFIGURATION.INI)")

if __name__ == "__main__":
    try:
        #configuracao_tela()
        #sleep(0.5)
        main()
    except:
        data_erro = datetime.now().strftime('%Y%m%d_%H%M%S')
        os.makedirs("@erros", exist_ok=True)
        arquivo_log = "@erros\\error_log_" + data_erro + ".log"
        f = open(arquivo_log, "w")
        f.write(traceback.format_exc())
        f.close()

        clear_screen()
        error_message(CONSOLE_ATUAL,"ERRORLOG: " + arquivo_log)
        sleep(5)
        finaliza_programa(CONSOLE_ATUAL)