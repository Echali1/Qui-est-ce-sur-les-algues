from shiny import App, ui
from pathlib import Path
from modules.about import about_ui
from modules.catalogue import catalogue_ui, catalogue_server
from modules.who import who_ui, who_server

app_ui = ui.page_navbar(

    ui.head_content(ui.include_css("www/styles.css")),

    ui.nav_panel("Accueil", ui.h3("Bienvenue")),
    ui.nav_panel("A propos", about_ui()),
    ui.nav_panel("Catalogue", catalogue_ui()),
    ui.nav_panel("Jeu", who_ui()),

    title="Qui est ce ?",

    footer=ui.div(
        ui.input_dark_mode(),
        style="position:absolute; right:20px; top:10px;"
    )
)

def server(input, output, session):
    catalogue_server(input, output, session)
    who_server(input, output, session)

app_dir = Path(__file__).parent

app = App(app_ui, server, static_assets=app_dir / "www")













