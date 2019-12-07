from main import oauth2_scheme



def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )



async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user