import numpy as np
import matplotlib.pyplot as plt

def calculate_shear_moment(loads, beam_length, step=0.01):
    """计算剪力和弯矩分布"""
    x = np.arange(0, beam_length + step, step)
    V = np.zeros_like(x)  # 剪力
    M = np.zeros_like(x)  # 弯矩

    for load in loads:
        if load['type'] == 'force':
            pos = load['position']
            val = load['value']
            V += val * (x >= pos)
            M += val * np.maximum(x - pos, 0)
        
        elif load['type'] == 'moment':
            pos = load['position']
            val = load['value']
            M += val * (x >= pos)

    return x, V, M

def plot_diagrams(x, V, M, beam_length):
    """绘制剪力图和弯矩图"""
    plt.figure(figsize=(12, 8))
    
    # 剪力图
    plt.subplot(2, 1, 1)
    plt.plot(x, V/1000, 'r-', linewidth=2)
    plt.fill_between(x, V/1000, 0, color='r', alpha=0.3)
    plt.title('剪力图 (单位：kN)', fontproperties='SimHei')
    plt.xlabel('位置 (m)')
    plt.ylabel('剪力')
    plt.grid(True)
    plt.xlim(0, beam_length)
    
    # 弯矩图
    plt.subplot(2, 1, 2)
    plt.plot(x, M/1000, 'b-', linewidth=2)
    plt.fill_between(x, M/1000, 0, color='b', alpha=0.3)
    plt.title('弯矩图 (单位：kN·m)', fontproperties='SimHei')
    plt.xlabel('位置 (m)')
    plt.ylabel('弯矩')
    plt.grid(True)
    plt.xlim(0, beam_length)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 输入参数
    l = 4.0          # 梁长（米）
    M = 8000         # 力偶矩（N·m），顺时针方向
    
    # 计算支反力（理论推导）
    R_A = M / l     # A点支反力（向上）
    R_B = -M / l    # B点支反力（向下）

    # 载荷配置（单位：N和N·m）
    loads = [
        # 三角支座反力
        {'type': 'force', 'position': 0, 'value': R_A},
        {'type': 'force', 'position': l, 'value': R_B},
        
        # AB中点力偶
        {'type': 'moment', 'position': l/2, 'value': M}
    ]

    # 计算并绘图
    x, V, M = calculate_shear_moment(loads, l)
    plot_diagrams(x, V, M, l)
