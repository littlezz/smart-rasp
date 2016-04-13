class WsManager:
    def __init__(self):
        self._list = list()

    def add(self, ws):
        self._list.append(ws)

    def remove(self, ws):
        self._list.remove(ws)

    def broadcast(self, msg):
        for ws in self._list:
            try:
                ws.send_str(msg)
            except RuntimeError:
                pass


ws_manager = WsManager()
