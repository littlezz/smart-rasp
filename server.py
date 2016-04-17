from aiohttp import web
from manager import ws_manager as _ws_manager
from jinja2 import Environment, FileSystemLoader
from asyncio import coroutine

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
        print(msg)
        ws.send_str('Got' + msg.data)

    print('close ws')
    return ws



def init():
    app = web.Application()
    app.router.add_route('GET', '/', hi)
    app.router.add_route('GET', '/ws', websockets)
    app['ws_manager'] = _ws_manager

    return app

web.run_app(init())

