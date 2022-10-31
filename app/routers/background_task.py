from fastapi import APIRouter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import apscheduler

router = APIRouter()


@router.post('/background_task_change')
async def background_task_change(change_value: bool):
    return {}


@router.get('/task_status')
async def task_status():
    return {}
