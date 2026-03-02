import numpy as np
import matplotlib.pyplot as plt

def calculate_shear_moment(loads, beam_length, step=0.01):
    x = np.arange(0, beam_length + step, step)
    V = np.zeros_like(x)  # 剪力
    M = np.zeros_like(x)  # 弯矩

    for load in loads:
        if load['type'] == 'force':
            pos = load['position']
            val = load['value']
            V += val * (x >= pos)
            M += val * np.maximum(x - pos, 0)
        
        elif load['type'] == 'distributed':
            s = load['start']
            e = load['end']
            val = load['value']
            V += val * np.clip(x - s, 0, e - s)
            mask = (x >= s) & (x <= e)
            M[mask] += val * 0.5 * (x[mask] - s)**2
            M[x > e] += val * 0.5*(e-s)**2 + val*(e-s)*(x[x>e]-e)
        
        elif load['type'] == 'moment':
            pos = load['position']
            val = load['value']
            M += val * (x >= pos)

    return x, V, M

def plot_diagrams(x, V, M, beam_length):
    plt.figure(figsize=(10, 8))
    
    plt.subplot(2, 1, 1)
    plt.plot(x, V/1000, 'r-', linewidth=2)  # 转换为kN
    plt.fill_between(x, V/1000, 0, color='r', alpha=0.3)
    plt.title('剪力图', fontproperties='SimHei')
    plt.xlabel('位置 (m)')
    plt.ylabel('剪力 (kN)')
    plt.grid(True)
    plt.xlim(0, beam_length)
    
    plt.subplot(2, 1, 2)
    plt.plot(x, M/1000, 'b-', linewidth=2)  # 转换为kN·m
    plt.fill_between(x, M/1000, 0, color='b', alpha=0.3)
    plt.title('弯矩图', fontproperties='SimHei')
    plt.xlabel('位置 (m)')
    plt.ylabel('弯矩 (kN·m)')
    plt.grid(True)
    plt.xlim(0, beam_length)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 参数配置
    beam_length = 3.2  # 总长3.2m
    CA_length = 0.8    # C到A段长度
    AB_length = 1.6    # A到B段长度
    
    # 支反力 (已计算结果)
    Ra = 7.0    # 单位：kN
    Rb = 29.0   # 单位：kN

    # 载荷配置（单位已转换为N和N·m）
    loads = [
        # CA段分布载荷 (0-0.8m)
        {
            'type': 'distributed',
            'start': 0,
            'end': CA_length,
            'value': -20_000  # 20kN/m向下
        },
        # AB段中点力偶矩 (1.6m处)
        {
            'type': 'moment',
            'position': CA_length + AB_length/2,
            'value': -8_000  # 逆时针8kN·m
        },
        # D点集中力 (3.2m处)
        {
            'type': 'force',
            'position': beam_length,
            'value': -20_000  # 20kN向下
        },
        # A点支反力 (0.8m处)
        {
            'type': 'force',
            'position': CA_length,
            'value': Ra * 1_000  # 7kN向上
        },
        # B点支反力 (2.4m处)
        {
            'type': 'force',
            'position': CA_length + AB_length,
            'value': Rb * 1_000  # 29kN向上
        }
    ]

    # 计算并绘图
    x, V, M = calculate_shear_moment(loads, beam_length)
    plot_diagrams(x, V, M, beam_length)
