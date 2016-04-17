from aiohttp import web
from manager import ws_manager as _ws_manager
from jinja2 import Environment, FileSystemLoader
from asyncio import coroutine
import asyncio
from rasp import rcl

env = Environment(loader=FileSystemLoader('templates'))




@coroutine
def hi(request):
    html = env.get_template('base.html').render()
    return web.Response(body=bytes(html, encoding='utf8'))


@coroutine
def websockets(request):
    ws_manager = request.app['ws_manager']

    ws = web.WebSocketResponse()
    yield from ws.prepare(request)
    ws_manager.add(ws)
    ws_manager.broadcast('someone join, there is {} person'.format(len(ws_manager._list)))

    while True:
        try:
            msg = yield from ws.receive()
        except RuntimeError:
            print('ws shutdown')
            ws_manager.remove(ws)
        # print(msg)
        # ws.send_str('Got' + str(msg.data))

    ws_manager.remove(ws)
    print('close ws')
    return ws

@coroutine
def loop_sr_state():
    while True:
        intercept = yield from rcl.sr_once()
        if intercept < 0.5:
            _ws_manager.broadcast('Danger!')
            rcl.led_on()
            print('intercept', intercept)
        else:
            rcl.led_off()
        yield from asyncio.sleep(0.5)

@coroutine
def on_shutdown(app):
    rcl.cleanup()
    print('clean up')

def init():
    app = web.Application()
    app.router.add_route('GET', '/', hi)
    app.router.add_route('GET', '/ws', websockets)
    app['ws_manager'] = _ws_manager
    app.loop.create_task(loop_sr_state())
    app.on_shutdown.append(on_shutdown)

    return app

web.run_app(init())

