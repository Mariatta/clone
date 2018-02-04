import os
from aiohttp import web

import tasks

async def handle(request):
    """Respond to incoming requests."""

    tasks.regen_task.delay()

    return web.Response(status=200)





app = web.Application()
app.router.add_get('/', handle)

port = os.environ.get("PORT")
if port is not None:
    port = int(port)
web.run_app(app, port=port)