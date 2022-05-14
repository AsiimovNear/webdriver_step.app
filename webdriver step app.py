from selenium import webdriver
import imaplib
import time

link = f"https://app.step.app?r={input('Enter ref code: ')}"


def get_mails():
    mails = {}

    with open("mails.txt", "r") as file:
        for i in file.readlines():
            e, p = i.split(":")[0], i.split(":")[1]
            mails[e] = p

    return mails


def get_wallets():
    with open("wallets.txt", "r") as file:
        wallets = file.readlines()

    return wallets


def get_code_from_rambler(login, password):
    mail = imaplib.IMAP4_SSL('imap.rambler.ru')
    mail.login(login, password)
    mail.list()
    mail.select("inbox")
    result, data = mail.search (None, "ALL")
    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[-1]
    result, data = mail.fetch(latest_email_id,'(RFC822)')
    result, data = mail.uid('search', None, "ALL")
    latest_email_uid = data[0].split()[-1]
    result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = data[0][1]
    mail = raw_email.decode('UTF-8')
    el = mail.find("Your verification code")
    els = []
    for k in range (24,30):
        t = el+k
        els.append (mail[t])
    code = ""
    return code.join(els)


def main():
    mails = get_mails()
    wallets = get_wallets()
    i = 0

    for mail, password in mails.items():
        wallet = wallets[i]
        i += 1
        driver = webdriver.Chrome()
        driver.get(link)
        time.sleep(5)
        option1 = driver.find_element_by_css_selector("[class='email__input']")
        option1.send_keys(mail)
        time.sleep(2)
        option2 = driver.find_element_by_css_selector("[class='welcome-button']")
        option2.click()
        time.sleep(5)
        option3 = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div[1]/input")
        time.sleep(120)
        try:
            option3.send_keys(get_code_from_rambler(mail, password))
            time.sleep(5)
            option4 = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[4]/div/div[2]")
            option4.click()
            time.sleep(5)
            option5 = driver.find_element_by_css_selector("[class='modal-wallet__input']")
            option5.send_keys(wallet)
            time.sleep(5)
            option6 = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[3]/div")
            option6.click()
            driver.close()
        except:
            with open("не пришёл код.txt", "a") as file:
                file.write(f"{mail}:{password}:{wallet}\n")
            continue


if __name__ == "__main__":
    main()
