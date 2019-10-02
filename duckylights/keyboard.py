from . import hidapi
from contextlib import contextmanager


def device_path(vendor=0x04d9, product=0x0348, interface=1):
    return next(hidapi.enumerate(vendor_id=vendor, product_id=product, interface_number=interface)).path


@contextmanager
def keyboard(path=device_path()):
    device = DuckyKeyboard(hidapi.open_path(path))
    yield device
    device.close()


class DuckyKeyboard:
    PAYLOAD_LEN = 120

    def __init__(self, device):
        self._dev = device
    
    def close(self):
        hidapi.close(self._dev)

    def _write(self, msg):
        hidapi.write(self._dev, bytes.fromhex(msg))
        return hidapi.read(self._dev, 256).hex()

    @contextmanager
    def programming(self):
        self._write('4101')
        try:
            yield self
        finally:
            self._write('4100')

    def custom_mode(self, colors):
        """
        colors is a 6x22 matrix
        """
        PREFIX = '01000000800100c100000000ffffffff00000000'
        PACKET_COUNT = 8

        self._write('568100000100000008000000aaaaaaaa')
        #                             ^      ^ Some sort of mask to avoid coloring numlock indicators
        #                             ^ PACKET_COUNT
        data = PREFIX + ''.join(colors)
        for p in range(PACKET_COUNT):
            msg = '56830' + str(p) + '00' + data[p*self.PAYLOAD_LEN:(p+1)*self.PAYLOAD_LEN]
            self._write(msg)
        self._write('51280000ff')


ES_KEYBOARD = """
      0     1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19    20    21
  +-------------------------------------------------------------------------------------------------------------------------------------    
0 |  ESC          F1    F2    F3    F4          F5    F6    F7    F8    F9   F10   F11   F12  PRTSC SCRLK PAUSE  CALC  MUTE  VOL-  VOL+
1 |   º     1     2     3     4     5     6     7     8     9     0     '     ¡          BACK  INS   HOME PAGUP NUMLK  NUM/  NUM*  NUM-
2 |  TAB    Q     W     E     R     T     Y     U     I     O     P     `     +         ENTER  DEL   END  PAGDN  NUM7  NUM8  NUM9  NUM+
3 |  CAPS   A     S     D     F     G     H     J     K     L     Ñ     ´     ç                                  NUM4  NUM5  NUM6      
4 |  LSH    <     Z     X     C     V     B     N     M     ,     .     -          RTSH               UP         NUM1  NUM2  NUM3      
5 | LCTRL LMETA  LALT                   SPACE                   ALTGR       RMETA   FN  RCTRL  LEFT  DOWN RIGHT  NUM0        NUM. NENTR
"""


if __name__ == "__main__":
    with keyboard() as dev, dev.programming() as kb:
        import time
        for i in range(0,6*22+1):
            kb.custom_mode(['00fff0'] * (i))
            time.sleep(0.1)
        time.sleep(0.1)