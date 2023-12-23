import mesa
from main.agents import Person
from main.model import BankReserves

#set colors#

RICH_COLOR = "#2ca02c"

POOR_COLOR = "#d62728"

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
