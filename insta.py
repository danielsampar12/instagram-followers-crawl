import os
import sys
import json
import helper
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys


INSTAGRAM_USERNAME = "andersonjoaquim89"
INSTAGRAM_PASSWORD = "Teste123-"
url_user_detail = 'https://www.instagram.com/%s/?__a=1'
# url_followers = 'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"%s","include_reel":true,"fetch_mutual":false,"first":50,"after":"%s"}'
url_followers = 'https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5&variables={"id":"%s","include_reel":true,"fetch_mutual":false,"first":100,"after":"%s"}'



def login(driver):
    driver.get("https://www.instagram.com/")
    try:
        accept = helper.waitForXpath(driver, '//button[contains(text(), "Accept")]', 4)
        helper.javaClick(driver, accept)
    except:
        pass

    try:
        username = helper.waitForXpath(driver, '//input[@name="username"]')
        username.send_keys(INSTAGRAM_USERNAME)
        password = helper.waitForXpath(driver, '//input[@name="password"]')
        password.send_keys(INSTAGRAM_PASSWORD, Keys.ENTER)
        helper.randomSleep(2,3)
        print("Successfully Logged in...")

        return True
    except:
        return False


def exitPopup(driver):
    try:
        accept_btn = helper.waitForClass(driver, "bIiDR")
        helper.javaClick(driver, accept_btn)
    except:
        pass


def loopOverURL(driver, url):
    for i in range(5):
        try:
            driver.get(url)
            all_data = json.loads(driver.find_element_by_tag_name('body').text)
            return all_data
        except:
            helper.randomSleep(1,2)

    return {}


def get_userinfo_by_username(driver, username):
    """ Get user info by username """
    user_info = None
    url_info = url_user_detail % (username)
    all_data = loopOverURL(driver, url_info)
    if len(all_data) > 0:
        user_info = all_data['graphql']['user']

    return user_info


def get_all_followers_by_user_id(driver, user_id, filename, target_username):
    """Get All followers by User Id"""
    after = ""
    has_next = True
    while has_next:
        url_follower = url_followers % (user_id, after)
        all_data = loopOverURL(driver, url_follower)
        if len(all_data) > 0:
            has_next_page = all_data['data']['user']['edge_followed_by']['page_info']['has_next_page']
            if has_next_page:
                after = all_data['data']['user']['edge_followed_by']['page_info']['end_cursor']
            else:
                has_next = False

            for username_id in all_data['data']['user']['edge_followed_by']['edges']:
                username = username_id['node']['username']
                helper.writeCSV(filename, [username, target_username])
                # user_id = username_id['node']['id']

        helper.randomSleep(20,20)



def main():
    try:
        target_username = sys.argv[1]
        if INSTAGRAM_PASSWORD == "" or INSTAGRAM_USERNAME == "":
            print("Please provide instagram credentials.")
            exit(1)
    except Exception:
        print("Please pass username in parameter")
        exit(1)

    # target_username = input("Enter the target username: ")
    path = helper.createDirectory("data" + os.sep + target_username)

    url = "https://www.instagram.com/"
    executable_path = os.getcwd() + "/chromedriver"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    driver = helper.startChrome(user_agent, executable_path)
    driver.get(url)
    exitPopup(driver)
    helper.randomSleep(3,4)
    if not login(driver):
        print("Please! Try Again...")
        driver.quit()
        exit()
    userInfo = get_userinfo_by_username(driver, target_username)
    if userInfo != None:
        filename = path + os.sep + "followers"
        get_all_followers_by_user_id(driver, userInfo['id'], filename, target_username)

    driver.quit()


if __name__ == '__main__':
    main()

