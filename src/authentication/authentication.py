class Authentication:
    def create_user(self, username: str, password: str) -> None:
        """Creates a user with the supplied username and password,
           assuming no user with that username already exists."""

    def login_user(self, username: str, password: str) -> str:
        """Logs in a user with the supplied username and password,
           assuming the user exists and is verified.

           Returns a token for authenticated requests."""

    def authenticate_user(self, token: str):  # -> User
        """Authenticates the supplied token and returns
           the user associated with it."""
