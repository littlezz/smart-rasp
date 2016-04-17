from asyncio import coroutine

class WsManager:
    def __init__(self):
        self._list = list()

    def add(self, ws):
        self._list.append(ws)

    def remove(self, ws):
        try:
            self._list.remove(ws)
        except ValueError:
            pass

    def broadcast(self, msg):
        for ws in self._list:
            try:
                ws.send_str(msg)
            except RuntimeError:
                self.remove(ws)

    def close_all(self):
        for ws in self._list:
            try:
                yield from ws.close()
            except RuntimeError:
                pass


ws_manager = WsManager()
