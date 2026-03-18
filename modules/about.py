from shiny import ui

def about_ui():
    return ui.page_fluid(
        ui.h2("À propos du projet"),
        
        ui.p("Cette application est un jeu interactif inspiré du célèbre 'Qui est-ce ?'."),
        
        ui.h3("Fonctionnement"),
        ui.p("L'utilisateur explore le catalogue de personnages et tente de deviner l'identité secrète."),
        
        ui.h3("Technologies utilisées"),
        ui.tags.ul(
            ui.tags.li("Python"),
            ui.tags.li("Shiny for Python"),
            ui.tags.li("Bootstrap"),
            ui.tags.li("CSS personnalisé")
        ),
        
        ui.hr(),
        ui.p("Projet réalisé par  – 2026")
    )