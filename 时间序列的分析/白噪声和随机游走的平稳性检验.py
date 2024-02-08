import numpy as np
import matplotlib.pyplot as plt

# 样本数
n_sample = 1000
# 白噪声过程
w = np.random.normal(size=n_sample)
# 随机游走过程
x = np.zeros(n_sample)
for t in range(n_sample):
    x[t] = x[t - 1] + w[t]
# 可视化
fig = plt.figure()
ax_w = fig.add_subplot(211)
ax_x = fig.add_subplot(212)
ax_w.set_title("White Noise")
ax_x.set_title("Random Walk")
ax_w.plot(w)
ax_x.plot(x)
plt.show()
