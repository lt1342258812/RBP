from os.path import join, abspath, dirname, pardir

# Directories
BASE_DIR = abspath(join(dirname(__file__), pardir))  # abspath为返回路径的绝对路径，dirname(__file__)返回当前文件的执行路径
RESULTS_DIR = join(BASE_DIR, "results")  # 链接两个路径，表明results的路径

# Files
CONFIG_FILE = join(BASE_DIR, 'config.ini')

# Logging format
LOG_FORMAT = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
# Characters
CSV_SEP = ';'
TRACE_SEP = '\t'
NL = '\n'  # new line

# MPU
TOR_CELL_SIZE = 512
# 设置tor网络中单元大小为512
MTU = 1443.0
# Directions，确定流量方向与数字对应，-1为进，1为出
IN  = -1
OUT =  1
DIR_NAMES = {IN: "in", OUT: "out"}
DIRECTIONS = [OUT, IN]

# Mappings
EP2DIRS = {'client': OUT, 'server': IN}
# MODE2STATE = {'gap': GAP, 'burst': BURST}

# Histograms。float("inf")表示为正无穷
INF = float("inf")