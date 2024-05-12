import asyncio
import time
from uuid import UUID
from app import crud
from app.core.celery import celery
from app.db.session import SessionLocal
import logging
from celery import Task
from app.deps.account_deps import get_account_by_id
from app import crud
from proxy_checker_httpx import ProxyChecker
from app.tinder_utils.session import Session


@celery.task(name="tasks.increment")
def increment(value: int) -> int:
    time.sleep(5)
    new_value = value + 1
    return new_value


# async def get_hero(hero_id: UUID) -> Hero:
#     async with SessionLocal() as session:
#         await asyncio.sleep(5)  # Add a delay of 5 seconds
#         hero = await crud.hero.get(id=hero_id, db_session=session)
#         return hero
    

async def get_account(account_id: UUID):
    async with SessionLocal() as session:
        await asyncio.sleep(5)  # Add a delay of 5 seconds
        account = await crud.account.get(id=account_id, db_session=session)
        return account
    

async def update_account(account, new_account_data):
    async with SessionLocal() as session:
        await asyncio.sleep(5)  # Add a delay of 5 seconds
        account = await crud.account.update(obj_current=account, obj_new=new_account_data, db_session=session)
        return account


# @celery.task(name="tasks.print_hero")
# def print_hero(hero_id: UUID) -> None:    
#     hero = asyncio.get_event_loop().run_until_complete(get_hero(hero_id=hero_id))
#     return hero.id


@celery.task(name="tasks.validate_account_proxy")
def validate_account_proxy(account_id: UUID):
    # async with SessionLocal() as session:
    #     checker = ProxyChecker()
    #     account = await crud.account.get(id=account_id, db_session=session)
    #     await checker.initialize()
    #     await asyncio.sleep(5)  # Add a delay of 5 seconds
    #     proxy_data = await checker.check_proxy(account.proxy)
    #     updated_data = {"valid_proxy": True if proxy_data else False}
    #     await asyncio.sleep(5) 
    #     account = await crud.account.update(
    #         obj_current=account, obj_new=updated_data, db_session=session)
    #     return account
    time.sleep(5)
    checker = ProxyChecker()
    account = asyncio.get_event_loop().run_until_complete(get_account(account_id))
    proxy_parts = account.proxy.split(':') if account.proxy else []
    asyncio.get_event_loop().run_until_complete(checker.initialize())
    if len(proxy_parts) == 2:
        proxy_data = asyncio.get_event_loop().run_until_complete(
            checker.check_proxy(f'{proxy_parts[0]}:{proxy_parts[1]}'))
    elif len(proxy_parts) == 4:
        proxy_data = asyncio.get_event_loop().run_until_complete(
            checker.check_proxy(f'{proxy_parts[0]}:{proxy_parts[1]}', 
            user=proxy_parts[2], password=proxy_parts[3]))
    else:
        return
    updated_data = {"valid_proxy": True if proxy_data else False}
    updated_account = asyncio.get_event_loop().run_until_complete(update_account(account, updated_data))


@celery.task(name="tasks.validate_account_credentials")
def validate_account_credentials(account_id: UUID):
    time.sleep(5)

    # Validate Proxy
    checker = ProxyChecker()
    account = asyncio.get_event_loop().run_until_complete(get_account(account_id))
    proxy_parts = account.proxy.split(':') if account.proxy else []
    asyncio.get_event_loop().run_until_complete(checker.initialize())
    proxy_data = None
    is_verified = False
    proxy_formatted = None
    if len(proxy_parts) == 2:
        proxy_data = asyncio.get_event_loop().run_until_complete(
            checker.check_proxy(f'{proxy_parts[0]}:{proxy_parts[1]}'))
        if proxy_data:
            proxy_formatted = f"{proxy_parts[0]}:{proxy_parts[1]}"
    elif len(proxy_parts) == 4:
        proxy_data = asyncio.get_event_loop().run_until_complete(
            checker.check_proxy(f'{proxy_parts[0]}:{proxy_parts[1]}', 
            user=proxy_parts[2], password=proxy_parts[3]))
        if proxy_data:
            proxy_formatted = f"{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}"

    # Validate Account
    if account.credentials:
        session = Session(
            proxy=proxy_formatted, 
            headless=False, store_session=False)
        email = account.credentials.get("email")
        password = account.credentials.get("password")
        if account.platform == "facebook":
            session.login_using_facebook(email, password)
        elif account.platform == "google":
            session.login_using_google(email, password)
        # elif account.platform == "sim":
        #     session.login_using_sms()
        is_verified = session._is_logged_in()
        session.browser.quit()
    updated_data = {
        "valid_proxy": True if proxy_data else False,
        "is_verified": is_verified
        }
    
    updated_account = asyncio.get_event_loop().run_until_complete(update_account(account, updated_data))