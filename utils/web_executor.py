from selenium import webdriver

def execute_web_actions(data):
    url = data['url']
    commands = data['tests'][0]['commands']

    # Initialize the web driver
    driver = webdriver.Chrome()

    # Execute the commands
    for command in commands:
        action = command['command']
        target = command['target']
        value = command.get('value', '')

        if action == 'open':
            driver.get(url + target)
        elif action == 'click':
            element = driver.find_element_by_css_selector(target)
            element.click()
        elif action == 'type':
            element = driver.find_element_by_css_selector(target)
            element.send_keys(value)
        # ... Add more actions as needed

    driver.quit()

    return {"status": "success"}
