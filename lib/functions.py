import keyboard
import configparser
import os
from time import sleep

from rich import print
from rich.align import Align
from rich.table import Table
from rich.prompt import Prompt
from rich.console import Console
from rich.live import Live

from lib.service_info import ServiceInfo
from lib.service_manager import ServiceManager

MARGEM = " " * 20

CAPTION = "." * 8

def clear_screen():
    os.system("cls")

def configuracao_tela():
    keyboard.press('left windows')
    keyboard.press('up')
    keyboard.release('up')
    keyboard.release('left windows')

def pula_linha(CONSOLE_ATUAL: Console = Console(), vezes: int = 1):
    for i in range(vezes):
        CONSOLE_ATUAL.print("")

def cabecalho_programa(CONSOLE_ATUAL):
    pula_linha(CONSOLE_ATUAL, 2)
    CONSOLE_ATUAL.print(
        Align("[bold white on red]   STOP/START TOTVS/PROTHEUS SERVICES   ", align="center"))
    CONSOLE_ATUAL.print(
        Align("           [green on white]   by: @filhoirineu   ", align="center"))
    pula_linha(CONSOLE_ATUAL, 1)

def config_ini_file():
    return "@configuration.ini"

def get_info_from_key(config, section, key):
    info_return = ""

    if config.has_section(section):
        if config.has_option(section, key):
            info_return = config[section][key]

    return info_return

def get_info_from_config_ini_file():
    services = []
    config_file = config_ini_file()
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        sections = config.sections()

        for index, s in enumerate(sections):
            services.append(
                ServiceInfo(id=str(index).zfill(len(str(len(sections)))+1), section=s, display_name=get_info_from_key(config, s, "display_name"), service_name=get_info_from_key(
                    config, s, "service_name"), process_name=get_info_from_key(config, s, "process_name"))
            )

    return services

def services_info_table(services_info_table):
    table = Table(
        show_lines=True,
    )

    table.add_column(Align("[bold white on blue]ID", align="center"), justify="center")
    table.add_column(Align("[bold white on blue]SESSAO", align="center"), justify="left")
    table.add_column(Align("[bold white on blue]NOME DE EXIBICAO", align="center"), justify="left")
    table.add_column(Align("[bold white on blue]NOME DO SERVICO", align="center"), justify="left")
    table.add_column(Align("[bold white on blue]NOME DO PROCESSO", align="center"), justify="left")
    table.add_column(Align("[bold white on blue]HABILITADO", align="center"), justify="center")
    table.add_column(Align("[bold white on blue]STATUS", align="center"), justify="center")

    for service in services_info_table:
        id = service.id
        section = service.section
        display_name = service.display_name
        service_name = service.service_name
        process_name = service.process_name

        service_status = ServiceManager(
            service_name=service.service_name, process_name=process_name
        )

        if service_status.is_disabled:
            enable = "[bold white on red]DESABILITADO"
        else:
            enable = "[bold white on green]HABILITADO"

        if service_status.is_online:
            status = "[bold white on green]"
            status += service_status.service_status_description
        else:
            status = "[bold white on red]"
            status += service_status.service_status_description

        table.add_row(id, section, display_name, service_name,
                      process_name, enable, status)

    return table

def initial_screen(CONSOLE_ATUAL: Console = Console(), services_info: list = []):

    clear_screen()
    pula_linha(CONSOLE_ATUAL, 2)

    CONSOLE_ATUAL.print(Align(
        services_info_table(services_info), align="center")
    )

    cabecalho_programa(CONSOLE_ATUAL)

    return Prompt.ask(MARGEM + "[bold yellow]ID/START/STOP/RESTART/REFRESH/EXIT").upper()

def finaliza_programa(CONSOLE_ATUAL: Console = Console()):

    clear_screen()

    pula_linha(CONSOLE_ATUAL, 5)
    CONSOLE_ATUAL.print(
        Align("[bold green]   PROGRAMA FINALIZADO   ", align="center"))
    sleep(1.5)
    CONSOLE_ATUAL.print(
        Align("[bold green]   by: Irineu Filho (@filhoirineu)   ", align="center"))
    sleep(5)

def error_message(CONSOLE_ATUAL: Console = Console(), message: str = ""):

    clear_screen()
    pula_linha(CONSOLE_ATUAL, 5)
    for x in range(3):
        print(
            Align("[bold red]" + message, align="center"))

    sleep(5)

def process_services(CONSOLE_ATUAL: Console = Console(), servicos: list = [], opcao: str = ""):

    clear_screen()
    pula_linha(CONSOLE_ATUAL, 2)

    table = Table(
        show_lines=True
    )

    table.add_column("[bold white on blue]ID")
    table.add_column("[bold white on blue]NOME DE EXIBICAO")
    table.add_column("[bold white on blue]NOME DO SERVICO")
    table.add_column("[bold white on blue]NOME DO PROCESSO")
    table.add_column("[bold white on blue]STATUS", justify="center")

    # update 4 times a second to feel fluid
    with Live(Align(table, align="center"), refresh_per_second=4):

        for servico in servicos:
            sleep(0.4)
            id = servico.id
            display_name = servico.display_name
            service_name = servico.service_name
            process_name = servico.process_name

            table.add_row(id, display_name, service_name,
                          process_name, "[bold yellow]EXECUTANDO")
            service = ServiceManager(service_name, process_name)

            if not service.is_disabled:
                if opcao in ("START"):
                    service.start_service()
                    status = "[bold white on green]" + \
                        service.service_status_description
                elif opcao in ("STOP"):
                    service.stop_service()
                    status = "[bold white on red]" + \
                        service.service_status_description
                elif opcao in ("RESTART"):
                    service.restart_service()
                    status = "[bold white on green]" + \
                        service.service_status_description
            else:
                status = "[bold white on red]DESABILITADO"

            table.add_row("", "", "", "", status)

    print(
        Align("[bold green]   ... FINALIZADO ... ", align="center"))
    sleep(5)
    clear_screen()
