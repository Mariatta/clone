"""Automatically close a PR as it opens."""

import gidgethub.routing
from . import tasks
router = gidgethub.routing.Router()


@router.register("pull_request", action="opened")
@router.register("pull_request", action="reopened")
async def close_pr(event, gh, *args, **kwargs):
    tasks.close_pr.delay(event, gh)