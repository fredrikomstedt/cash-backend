from src.database.categories.category import Category
from src.database.users.user import User

User.update_forward_refs(Category=Category)
Category.update_forward_refs(User=User)
