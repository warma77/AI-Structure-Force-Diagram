import numpy as np
import matplotlib.pyplot as plt

def calculate_shear_moment(loads, beam_length, step=0.001):
    """计算剪力和弯矩分布"""
    x = np.arange(0, beam_length + step, step)
    V = np.zeros_like(x)  # 剪力 (N)
    M = np.zeros_like(x)  # 弯矩 (N·m)

    for load in loads:
        if load['type'] == 'force':
            pos = load['position']
            val = load['value']
            # 剪力突变
            V += val * (x >= pos)
            # 弯矩线性变化
            M += val * np.maximum(x - pos, 0)
        
        elif load['type'] == 'distributed':
            s = load['start']
            e = load['end']
            val = load['value']
            # 剪力在线性变化段
            V += val * np.clip(x - s, 0, e - s)
            # 弯矩在分布载荷段为二次曲线
            mask = (x >= s) & (x <= e)
            M[mask] += val * 0.5 * (x[mask] - s)**2
            # 分布载荷结束后，弯矩恢复线性
            M[x > e] += val * 0.5 * (e - s)**2 + val * (e - s) * (x[x > e] - e)
        
        elif load['type'] == 'moment':
            pos = load['position']
            val = load['value']
            # 弯矩突变
            M += val * (x >= pos)

    return x, V, M

def plot_diagrams(x, V, M, beam_length):
    """绘制剪力图和弯矩图 (单位：kN, kN·m)"""
    # 设置中文字体（根据系统可能需要调整，SimHei是常用黑体）
    plt.rcParams['font.sans-serif'] = ['SimHei'] 
    plt.rcParams['axes.unicode_minus'] = False 

    plt.figure(figsize=(10, 8))
    
    # 剪力图
    plt.subplot(2, 1, 1)
    plt.plot(x, V / 1000, 'r-', linewidth=2)
    plt.fill_between(x, V / 1000, 0, color='r', alpha=0.3)
    plt.title('剪力图 (Shear Force Diagram)')
    plt.xlabel('位置 (m)')
    plt.ylabel('剪力 (kN)')
    plt.grid(True, linestyle='--')
    plt.xlim(0, beam_length)
    plt.axhline(0, color='black', lw=1)
    
    # 弯矩图
    plt.subplot(2, 1, 2)
    plt.plot(x, M / 1000, 'b-', linewidth=2)
    plt.fill_between(x, M / 1000, 0, color='b', alpha=0.3)
    plt.title('弯矩图 (Bending Moment Diagram)')
    plt.xlabel('位置 (m)')
    plt.ylabel('弯矩 (kN·m)')
    plt.grid(True, linestyle='--')
    plt.xlim(0, beam_length)
    plt.axhline(0, color='black', lw=1)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # --- 参数设置 ---
    beam_length = 3.2  # 总长3.2m
    CA_length = 0.8
    AB_length = 1.6
    
    # 支反力 (kN)
    Ra = 7.0    
    Rb = 29.0   

    # --- 载荷配置 ---
    loads = [
        # 1. CA段分布载荷 (0 to 0.8m), 20kN/m 向下
        {
            'type': 'distributed',
            'start': 0,
            'end': CA_length,
            'value': -20000  
        },
        # 2. A点支反力 (0.8m), 7kN 向上
        {
            'type': 'force',
            'position': CA_length,
            'value': Ra * 1000
        },
        # 3. AB段中点力偶矩 (1.6m), 8kN·m 逆时针
        {
            'type': 'moment',
            'position': CA_length + AB_length / 2,
            'value': -8000
        },
        # 4. B点支反力 (2.4m), 29kN 向上
        {
            'type': 'force',
            'position': CA_length + AB_length,
            'value': Rb * 1000
        },
        # 5. D点集中力 (3.2m), 20kN 向下
        {
            'type': 'force',
            'position': beam_length,
            'value': -20000
        }
    ]

    # 执行计算与绘图
    x_vals, v_vals, m_vals = calculate_shear_moment(loads, beam_length)
    plot_diagrams(x_vals, v_vals, m_vals, beam_length)
