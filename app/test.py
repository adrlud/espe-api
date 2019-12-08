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
        self.assertNotEqual(result2, data["alice"])



if __name__ == '__main__':
    unittest.main()