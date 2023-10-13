from screeninfo import get_monitors

class RelativeSize:
    def __init__(self, size):
        self.size = size

    def __repr__(self) -> str:
        return str(self.size)

    def __mul__(self, num) -> int:
        return round(self.size * num)
    
    def __rmul__(self, num) -> int:
        return round(self.size * num)

monitor = get_monitors()[0]
VW = RelativeSize(monitor.width / 100)
VH = RelativeSize(monitor.height / 100)