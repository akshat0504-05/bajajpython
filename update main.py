
import requests

# Generate webhook using user data
user_info = {
    "name": "Akshat Sharma",
    "regNo": "0827AL221015",
    "email": "akshatsharma220226@acropolis.in"
}

try:
    response = requests.post(
        "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON",
        json=user_info
    )
    response.raise_for_status()
    data = response.json()
    webhook_url = data.get("webhook")
    access_token = data.get("accessToken")

    print("Webhook URL:", webhook_url)
    print("Access Token:", access_token)

    # SQL query to retrieve highest salary employee info
    query_payload = {
        "finalQuery": """
        SELECT 
            p.AMOUNT AS SALARY,
            CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
            FLOOR(DATEDIFF(CURDATE(), e.DOB)/365) AS AGE,
            d.DEPARTMENT_NAME
        FROM PAYMENTS p
        JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
        JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
        WHERE DAY(p.PAYMENT_TIME) != 1
        ORDER BY p.AMOUNT DESC
        LIMIT 1;
        """
    }

    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }

    result = requests.post(webhook_url, headers=headers, json=query_payload)

    print("Submission Status:", result.status_code)
    print("Server Response:", result.text)

except requests.RequestException as e:
    print("An error occurred:", e)
