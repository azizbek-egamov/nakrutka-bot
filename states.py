from aiogram.fsm.state import State, StatesGroup

class phone_add(StatesGroup):
    phone = State()
    
class Step(StatesGroup):
    text = State()

class AddQuote(StatesGroup):
    text = State()
    sorovlar = State()
    
class AllUsersMessage(StatesGroup):
    txt = State()
    
class UserMess(StatesGroup):
    user = State()
    txt = State()
    
class AddChann(StatesGroup):
    channel = State()
    
    
class AddApiKey(StatesGroup):
    url = State()
    key = State()
    
class AddZakaz(StatesGroup):
    soni = State()
    url = State()
    
class AddZakazPoll(StatesGroup):
    soni = State()
    raqam = State()
    url = State()
    
    
    
class Support(StatesGroup):
    text = State()
    
class UserSendSupport(StatesGroup):
    text = State()
    
class AddPayCards(StatesGroup):
    name = State()
    card = State()
    info = State()
    
class Payments(StatesGroup):
    count = State()
    rasm = State()
    
class usercontrol(StatesGroup):
    id = State()
    
class userPlus(StatesGroup):
    count = State()
    
class userMinus(StatesGroup):
    count = State()
    
