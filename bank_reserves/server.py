import mesa
from bank_reserves.agents import Person
from bank_reserves.model import BankReserves

"""
Citation:
The following code was adapted from server.py at
https://github.com/projectmesa/mesa/blob/main/examples/wolf_sheep/wolf_sheep/server.py
Accessed on: November 2, 2017
Author of original code: Taylor Mutch
"""

# The colors here are taken from Matplotlib's tab10 palette
# Green
RICH_COLOR = "#2ca02c"
# Red
POOR_COLOR = "#d62728"
# Blue
MID_COLOR = "#1f77b4"


def person_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    # update portrayal characteristics for each Person object
    if isinstance(agent, Person):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 0
        portrayal["Filled"] = "true"

        color = MID_COLOR

        # set agent color based on savings and loans
        if agent.savings > agent.model.rich_threshold:
            color = RICH_COLOR
        if agent.savings < 10 and agent.loans < 10:
            color = MID_COLOR
        if agent.loans > 10:
            color = POOR_COLOR

        portrayal["Color"] = color

    return portrayal


# dictionary of user settable parameters - these map to the model __init__ parameters
model_params = {
    "init_people": mesa.visualization.Slider(
        "تعداد مردم", 25, 1, 200, description="تعداد اولیه مردم"
    ),
    "rich_threshold": mesa.visualization.Slider(
        "آستانه ثروتمند بودن",
        10,
        1,
        20,
        description="آستانه مقدار مجاز کیف پول اولیه برای  قرار گرفتن در سطح متوسط جامعه",
    ),
    "reserve_percent": mesa.visualization.Slider(
      "دارایی و ذخایر بانک",
        50,
        1,
        100,
        description="درصدی از هرسپرده که بانک ذخیره می کند و اجازه برداشت از آن را ندارید.",
    ),
}

# set the portrayal function and size of the canvas for visualization
canvas_element = mesa.visualization.CanvasGrid(person_portrayal, 20, 20, 500, 500)

# map data to chart in the ChartModule
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "ثروتمند", "Color": RICH_COLOR},
        {"Label": "فقیر", "Color": POOR_COLOR},
        {"Label": "سطح متوسط جامعه", "Color": MID_COLOR},
    ]
)

# create instance of Mesa ModularServer
server = mesa.visualization.ModularServer(
    BankReserves,
    [canvas_element, chart_element],
    "مدل انتزاعی اقتصاد برای تعامل یک بانک و جامعه",
    model_params=model_params,
)
