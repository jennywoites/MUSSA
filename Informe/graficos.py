
# pip install matplotlib
# sudo apt install python3-tk
datos1 = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
datos2 = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]]
import matplotlib.pyplot as plt
plt.plot(*datos1)
plt.plot(*datos2)
plt.show()
