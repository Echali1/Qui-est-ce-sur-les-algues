from shiny import ui, render
import os
import pandas as pd
from pathlib import Path

# UI
def catalogue_ui():
    return ui.output_ui("catalogue_content")

# SERVER
def catalogue_server(input, output, session):
    @output
    @render.ui
    def catalogue_content():
        image_folder = "www"
        df = pd.read_csv("data/data.csv", encoding="latin-1")
        images_files = sorted(
           f for f in os.listdir(image_folder) 
           if f.endswith((".jpg", ".png", ".jpeg"))
        )
        df = df.iloc[:len(images_files)]

        elements = []

        # Header
        elements.append(
           ui.div(
              {"class":"catalogue-header"},
              ui.h1("CATALOGUE"),
              ui.p("Explore the collection below")
           )
        )

        # STATS
        elements.append(
           ui.div(
              {"class": "stats-container"},
              ui.div(
                 {"class": "stat-card"},
                 ui.h2(str(len(images_files))),
                 ui.p("Images")
              ),
              ui.div(
                {"class": "stat-card"},  
                ui.h2(str(len(df))),
                ui.p("Entries")
              )
           )
        )

         # GRID

        grid_items = []

        for i in range(len(images_files)):
         
         image_path = images_files[i]
         row = df.iloc[i]

         grid_items.append(
            ui.div(
                {"class": "catalogue-card"},
               ui.img(src=image_path),
               ui.div(
                  {"class": "code-badge"},
                  f"Code {row['Code_prelevement']}"
               )
            )

         )

        elements.append(
           ui.div(
              {"class": "catalogue-grid"},
              grid_items
           )
        )

        return elements
