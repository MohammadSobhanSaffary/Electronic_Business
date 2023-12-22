import mesa
import numpy as np
from main.agents import Bank, Person



# Start of datacollector functions


def get_num_rich_agents(model):
    """return number of rich agents"""

    rich_agents = [a for a in model.schedule.agents if a.savings > model.rich_threshold]
    return len(rich_agents)


def get_num_poor_agents(model):
    """return number of poor agents"""

    poor_agents = [a for a in model.schedule.agents if a.loans > 10]
    return len(poor_agents)


def get_num_mid_agents(model):
    """return number of middle class agents"""

    mid_agents = [
        a
        for a in model.schedule.agents
        if a.loans < 10 and a.savings < model.rich_threshold
    ]
    return len(mid_agents)


def get_total_savings(model):
    """sum of all agents' savings"""

    agent_savings = [a.savings for a in model.schedule.agents]
    # return the sum of agents' savings
    return np.sum(agent_savings)


def get_total_wallets(model):
    """sum of amounts of all agents' wallets"""

    agent_wallets = [a.wallet for a in model.schedule.agents]
    # return the sum of all agents' wallets
    return np.sum(agent_wallets)


def get_total_money(model):
    # sum of all agents' wallets
    wallet_money = get_total_wallets(model)
    # sum of all agents' savings
    savings_money = get_total_savings(model)
    # return sum of agents' wallets and savings for total money
    return wallet_money + savings_money


def get_total_loans(model):
    # list of amounts of all agents' loans
    agent_loans = [a.loans for a in model.schedule.agents]
    # return sum of all agents' loans
    return np.sum(agent_loans)


class BankReserves(mesa.Model):
    """
این پروژه یک مدل اقتصادی ساده سازی شده است که از عواملی به نام افراد و یک بانک استفاده می‌کند. هدف این مدل شبیه‌سازی فرآیندهای اقتصادی است که افراد با یکدیگر تعامل داشته و از خدمات بانکی بهره می‌برند. دسته بندی افراد شامل قشر متوسط ، ثروتمند و فقیر میباشد که در ابتدا همه ی افراد جزو دسته قشر متوسط هستند، همچنین برای در نظر گرفتن اینکه آیا فرد جزو دسته ثروتمندان است یا خیر یک آستانه به عنوان ورودی از کاربر گرفته میشود.تعامل افراد باهم میتواند سبب معامله شودهمچنین تعامل هر فرد با بانک شامل سرمایه گذاری یا دریافت وام است که هرکدام دارای شرایط خاصی هستند.

عملکرد اصلی مدل به شرح زیر است:

• افراد (نماینده‌شان با دایره‌های رنگی) به صورت تصادفی در شبکه حرکت می‌کنند. • اگر دو یا چند نفر در یک مکان قرار گیرند، احتمال معامله با یکدیگر 50 درصد است. • اگر معامله صورت گیرد، احتمال برابری وجود دارد که یکی از آن‌ها به مبلغ 5 دلار یا 2 دلار از دیگری خرید کند. • معاملات مثبت به عنوان پس‌انداز در بانک واریز می‌شود و در صورت معامله منفی، فرد سعی می‌کند از پس‌انداز خود برای پرداخت مبلغ منفی استفاده کند. در صورت عدم توانایی در پرداخت مبلغ منفی، اقدام به گرفتن وام از بانک می‌کند. • بانک نیز موظف به نگه‌داشتن درصد مشخصی از سپرده‌ها به عنوان احتیاط است و توانایی وام‌دهی آن به میزان سپرده‌ها، احتیاطات و میزان وام‌های در جریان است.
    
    """

    # grid height
    grid_h = 20
    # grid width
    grid_w = 20

    """init parameters "init_people", "rich_threshold", and "reserve_percent"
       are all set via Slider"""

    def __init__(
        self,
        height=grid_h,
        width=grid_w,
        init_people=2,
        rich_threshold=10,
        reserve_percent=50,
    ):
        self.height = height
        self.width = width
        self.init_people = init_people
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        # rich_threshold is the amount of savings a person needs to be considered "rich"
        self.rich_threshold = rich_threshold
        self.reserve_percent = reserve_percent
        # see datacollector functions above
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "ثروتمند": get_num_rich_agents,
                "فقیر": get_num_poor_agents,
                "سطح متوسط جامعه": get_num_mid_agents,
                "Savings": get_total_savings,
                "Wallets": get_total_wallets,
                "Money": get_total_money,
                "Loans": get_total_loans,
            },
            agent_reporters={"Wealth": lambda x: x.wealth},
        )

        # create a single bank for the model
        self.bank = Bank(1, self, self.reserve_percent)

        # create people for the model according to number of people set by user
        for i in range(self.init_people):
            # set x, y coords randomly within the grid
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            p = Person(i, (x, y), self, True, self.bank, self.rich_threshold)
            # place the Person object on the grid at coordinates (x, y)
            self.grid.place_agent(p, (x, y))
            # add the Person object to the model schedule
            self.schedule.add(p)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        # tell all the agents in the model to run their step function
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    def run_model(self):
        for i in range(self.run_time):
            self.step()
