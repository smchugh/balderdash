from application.models.Player import Player
from application import login_manager

@login_manager.user_loader
def load_user(user_id):
    return Player.get(user_id)
