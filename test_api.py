import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(endpoint, a, b, expected):
    url = f"{BASE_URL}{endpoint}"
    payload = {"a": a, "b": b}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()["result"]
            if result == expected:
                print(f"PASS: {endpoint}({a}, {b}) = {result}")
                return True
            else:
                print(f"FAIL: {endpoint}({a}, {b}) expected {expected}, got {result}")
                return False
        else:
            print(f"FAIL: {endpoint}({a}, {b}) returned status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"ERROR: {endpoint}({a}, {b}) raised exception: {e}")
        return False

def test_divide_by_zero():
    url = f"{BASE_URL}/divide"
    payload = {"a": 10, "b": 0}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 400:
            print("PASS: /divide(10, 0) returned 400 as expected")
            return True
        else:
            print(f"FAIL: /divide(10, 0) expected 400, got {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: /divide(10, 0) raised exception: {e}")
        return False

if __name__ == "__main__":
    tests = [
        ("/add", 10, 5, 15.0),
        ("/subtract", 10, 5, 5.0),
        ("/multiply", 10, 5, 50.0),
        ("/divide", 10, 5, 2.0),
    ]
    
    success = True
    for endpoint, a, b, expected in tests:
        if not test_endpoint(endpoint, a, b, expected):
            success = False
            
    if not test_divide_by_zero():
        success = False
        
    if not success:
        sys.exit(1)
    print("All tests passed!")
    sys.exit(0)
