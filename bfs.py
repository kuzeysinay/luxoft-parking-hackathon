import random
import numpy as np
from collections import deque

# Park yeri oluşturma fonksiyonu
def create_parking_lot(x, y, occupancy_percentage):
    total_cells = x * y  # Toplam hücre sayısı
    num_occupied = total_cells * occupancy_percentage // 100  # Dolu hücre sayısı
    num_empty = total_cells - num_occupied  # Boş hücre sayısı
    cells = [1] * num_occupied + [0] * num_empty  # Dolu (1) ve boş (0) hücreler
    random.shuffle(cells)  # Hücreleri rastgele sırala
    parking_lot = np.array([cells[i * x:(i + 1) * x] for i in range(y)])  # 2D array olarak park yeri oluştur
    return parking_lot

# BFS algoritması
def bfs_find_nearest(parking_lot, start):
    directions = [(-1, 0, "Sol"), (1, 0, "Sağ"), (0, -1, "Yukarı"), (0, 1, "Aşağı")]  # 4 yön
    queue = deque([(start[0], start[1], [])])  # BFS kuyruğu, başlangıç koordinatı ve yolu tutar
    visited = set()  # Ziyaret edilen hücreler
    visited.add((start[0], start[1]))  # Başlangıç hücresini ziyaret edildi olarak işaretle

    while queue:  # Kuyrukta eleman olduğu sürece devam et
        x, y, path = queue.popleft()  # Kuyruktan eleman al
        for dx, dy, direction in directions:  # 4 yönü dolaş
            nx, ny = x + dx, y + dy  # Yeni koordinatlar
            if 0 <= nx < len(parking_lot[0]) and 0 <= ny < len(parking_lot) and (nx, ny) not in visited:
                if parking_lot[ny][nx] == 0:  # Boş yer bulduğunda
                    return len(path) + 1, path + [direction]  # Mesafe ve yolu döndür
                visited.add((nx, ny))  # Yeni hücreyi ziyaret edildi olarak işaretle
                queue.append((nx, ny, path + [direction]))  # Kuyruğa yeni eleman ekle

    return "Boş yer yok", []  # Eğer boş yer bulunamazsa
