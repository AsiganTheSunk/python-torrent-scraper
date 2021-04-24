# -*- coding: utf-8 -*-

# Import System Libraries
import re
from filters.constants.l_han import LHan


def chinese_filter():
    L = []
    for i in LHan:
        if isinstance(i, list):
            f, t = i
            try:
                f = chr(f)
                t = chr(t)
                L.append('%s-%s' % (f, t))
            except:
                pass # A narrow python build, so can't use chars > 65535 without surrogate pairs!

        else:
            try:
                L.append(chr(i))
            except:
                pass

    RE = '[%s]' % ''.join(L)
    #print('RE:', str(RE.encode('utf-8')))
    return re.compile(RE, re.UNICODE)