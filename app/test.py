import unittest
#target = __import__("app/users_request.py")
#users_request = target.users_request
import users_request 
class TestUser(unittest.TestCase):
    
    
    def test_get_user(self):
        data =  {
            "johndoe": {
                "username": "johndoe",
                "full_name": "John Doe",
                "email": "johndoe@example.com",
                "hashed_password": "fakehashedsecret",
                "disabled": False,
            },
            "alice": {
                "username": "alice",
                "full_name": "Alice Wonderson",
                "email": "alice@example.com",
                "hashed_password": "fakehashedsecret2",
                "disabled": True,
                },
            } 
        result = users_request.get_user(data, "johndoe")
        result2 = users_request.get_user(data, "alice")
        self.assertEqual(result, data["johndoe"])
        self.assertEqual(result2, data["alice"])
    
    def test_get_current_user(self):
        user = users_request.fake_decode_token("johndoe")
        
        self.assertEqual(user.username, "johndoe" )
    def test_fake_hash_password(self):
        result = users_request.fake_hash_password("PASSWORD")
        self.assertEqual(result, "fakehashedPASSWORD")
        



if __name__ == '__main__':
    unittest.main()