from shiny import ui
from shiny import reactive, render
import random
from pathlib import Path
import os

def who_ui():
    return ui.page_fluid(

        ui.div({"class": "game-title"}, "Qui est-ce ?"),

        ui.layout_columns(
            ui.div(
                {"class": "grid-container"},
                ui.output_ui("grid_perso")
            ),

            ui.div(
                {"class": "control-panel"},
                ui.h4("Pose une question"),
                ui.input_selectize(
                    "questions",
                    None,
                    [
                        "Est-ce que c'est un homme ?",
                        "Est-ce qu'il porte des lunettes ?",
                        "Est-ce qu'il a un teint clair ?",
                        "Est-ce qu'il est roux ?",
                        "Est-ce qu'il a des cheveux chatin ?"
                    ]
                ),
                ui.div({"class": "answer-box"}, ui.output_text("value")),
                ui.input_action_button("verification_button", "Vérification"),
                ui.div({"class": "verification-box"}, ui.output_text("verification")),
                ui.input_action_button("rejouer_button", "Nouvelle partie"),
                ui.div(ui.output_text("rejouer"))
            ),

            col_widths=(8, 4)
        )
    )

def who_server(input, output, session):

    BASE_DIR = Path(__file__).resolve().parent.parent
    image_folder = BASE_DIR / "www"

    images = sorted(
    f for f in os.listdir(image_folder)
    if f.endswith((".jpg", ".png", ".jpeg"))
    )

    perso = [
    {
        "image": img,
        "elimine": reactive.Value(False)
    }
    for img in images
    ]

    NB_PERSO = len(perso)

    id_mystere = reactive.Value(random.randint(0, NB_PERSO - 1))

    @output
    @render.ui
    def grid_perso():
       

       cards = []

       for i in range(NB_PERSO):

        eliminated = perso[i]["elimine"].get()

        image_style = "width:100%; border-radius:12px;"

        overlay = None

        if eliminated:
            image_style += "filter: grayscale(100%) blur(3px); opacity:0.4;"
            overlay = ui.div({"class": "eliminated-overlay"}, "✖")

        cards.append(
            ui.div(
                {"class": "character-card"},
                ui.input_action_button(
                    f"click_perso{i}",
                    ui.div(
                        ui.img(src=perso[i]["image"], style=image_style),
                        overlay
                    ),
                    style="background:none; border:none; padding:0;"
                )
            )
        )

       return ui.div({"class": "grid"}, cards)
    
    for i in range(NB_PERSO):
       

       @reactive.effect
       @reactive.event(input[f"click_perso{i}"])
       def _(i=i):
        perso[i]["elimine"].set(
            not perso[i]["elimine"].get()
        )


    questions = [
        "Est-ce que c'est un homme ?",
        "Est-ce qu'il porte des lunettes ?",
        "Est-ce qu'il a un teint clair ?",
        "Est-ce qu'il est roux ?",
        "Est-ce qu'il a des cheveux chatin ?"
    ]

    reponses = [
        ["oui", "oui", "oui", "non", "non"],
        ["non", "oui", "oui", "non", "oui"],
        ["oui", "non", "oui", "non", "oui"],
        ["oui", "non", "non", "non", "non"],
        ["non", "non", "oui", "non", "non"],
        ["oui", "oui", "oui", "oui", "non"],
        ["oui", "oui", "non", "non", "non"],
        ["non", "oui", "non", "non", "non"],
        ["non", "non", "oui", "non", "oui"]
    ]

    @output
    @render.text
    def value():
        q = input.questions()
        if q is None:
            return ""
        i = questions.index(q)
        id = id_mystere.get()
        rep = reponses[id][i]
        return f"Réponse : {rep}"

    @output
    @render.text
    @reactive.event(input.verification_button)
    def verification():

        visibles = [i for i in range(NB_PERSO) if not perso[i]["elimine"].get()]

        if len(visibles) > 1:
            return "Il doit vous rester un seul personnage visible."
        if len(visibles) == 0:
            return "Il faut garder un personnage visible."
        if visibles[0] == id_mystere.get():
            return "Vous avez deviné la bonne personne"
        
        return "Ce n'est pas la bonne personne"
    
    

    @output
    @render.text
    @reactive.event(input.rejouer_button)
    def rejouer():
        id_mystere.set(random.randint(0, NB_PERSO - 1))
        for i in range(NB_PERSO):
            perso[i]["elimine"].set(False)
        return "Nouvelle partie commencée"