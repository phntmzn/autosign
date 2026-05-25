import playwright
import requests
import subprocess
import faker

# launch playwright
subprocess.run['playwright launch']

# Create a new instance of the faker class
fake = faker.Faker()

# Genereate a list of random email addresses
email_addresses = []
for _ in range (10):
    email_addresses.append(fake.email())

# Generate a list of random passowrds
passwords = []
for _ in range(10):
    passwords.append(fake.password())

# Create a dictionary to store the email addresses and password
accounts = {}
for i, email in enumerate(email_addresses):
    accounts[i] = {
        'email': email,
        'password': passwords[i]
    }

print(accounts)

# Create a new instance of the playwright browser
browser = playwright.launch()

# Navigate to the soundcloud sign-up page
browser.page.navigate('https://soundcloud.com/signup')

# Fill in the form with your desired email adess nad passowrd
browser.page.fill('input[name="email"]', 'your_email@example.com')
browser.page.fill('input[name="password"]', 'your_password')

# submit the form to create a new souncloud account
browser.page.click('button[type="submit"]')




playwright.page.navigate('https://soundcloud.com.signup')

playwright.page.fill('input[name="email"]', 'your_email@example.com')
playwright.page.fill('input[name="password"]', 'your_password')

playwright.page.click('button[type="submit"]')

response = playwright.page.api('POST', 'https://soundcloud.com/api/v1/users', {
    "email": "your_email@example.com",
    "password": "your_password"
})
data = response.json()

# Print the data from the server response
print(data)

# Close the browser instance
browser.close()




# --- 30k comments ---

# setup the browser context
browser = playwright.chromium.launch()
context = browser.new_context()

# setup the page object
page = context.new_page()

# navigate to the soundcloud homepage
page.goto("https://soundcloud.com")

# Wait for the page to load
page.wait_for_load_state()

# Iterate over each song on the page and leave a comment
for song in page.querySelectorAll("div.song"):
    # Get the song URL from the element
    url = song.getAttribute("data-soundcloud-url")

    # Navigate to the song page
    page.goto(url)

    # wait for the page to load
    page.goto(url)

    # wait for the page to load
    page.wait_for_load_state()

    # Enter your comment and post it
    page.fill("#comment-text", "thumbs down emoji!")
    page.click("#post-button")

    # wait for the comment to be posted
    page.wait_for_selector(".comment")
