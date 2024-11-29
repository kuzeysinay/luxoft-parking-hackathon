import streamlit as st
import matplotlib.pyplot as plt
from bfs import create_parking_lot, bfs_find_nearest
import numpy as np

def main():
    st.set_page_config(page_title="Luxoft Parking") # Sekme başlığı

    # İki sütun oluştur: sol ve sağ
    col1, col2 = st.columns([1, 2])

    # Sol sütunda kullanıcıdan parametreleri al
    with col1:
        # Kullanıcıdan giriş verilerini al
        x = st.number_input("Park yeri genişliğini (x) girin:", min_value=1, max_value=20, value=10)
        y = st.number_input("Park yeri yüksekliğini (y) girin:", min_value=1, max_value=20, value=10)
        occupancy_percentage = st.slider("Park yeri doluluk yüzdesini girin (1-100):", 1, 100, 50)

        # Başlangıç koordinatları
        start_x = st.number_input(f"Başlangıç koordinatı x (1 ile {x} arasında):", min_value=1, max_value=x, value=1) - 1
        start_y = st.number_input(f"Başlangıç koordinatı y (1 ile {y} arasında):", min_value=1, max_value=y, value=1) - 1

    # Sağ sütunda park yeri gridini ve BFS sonucu göster
    with col2:
        # Park yeri oluştur
        parking_lot = create_parking_lot(x, y, occupancy_percentage)
        
        # BFS algoritması ile en yakın boş park yerini bul
        distance, path = bfs_find_nearest(parking_lot, (start_x, start_y))

        # Park alanını görselleştir
        fig, ax = plt.subplots()

        # Dolu yerleri kırmızı, boş yerleri yeşil olarak göster
        ax.imshow(1 - parking_lot, cmap="RdYlGn", interpolation="nearest")

        # Başlangıç noktasını tamamen mavi kare olarak işaretle
        ax.add_patch(plt.Rectangle((start_x - 0.5, start_y - 0.5), 1, 1, color="blue", alpha=0.5))

        # Kullanılacak yolu oklarla gösterme
        directions_map = {"Sol": (-1, 0), "Sağ": (1, 0), "Yukarı": (0, -1), "Aşağı": (0, 1)}
        for i in range(len(path) - 1):
            direction = path[i]
            x1, y1 = start_x + directions_map[direction][0], start_y + directions_map[direction][1]
            # Karelerin merkezine ok çizmek için
            ax.annotate('', xy=(x1 + 0.5, y1 + 0.5), xytext=(start_x + 0.5, start_y + 0.5),
                        arrowprops=dict(facecolor='yellow', edgecolor='yellow', arrowstyle='->', lw=2))
            start_x, start_y = x1, y1

        # Her bir karenin sınırlarını göstermek için grid çiz
        ax.set_xticks(np.arange(-0.5, x, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, y, 1), minor=True)
        ax.grid(which="minor", color="black", linestyle='-', linewidth=0.5)

        # Eksenleri karelerin koordinatlarını gösterecek şekilde ayarla (1'den başlayarak)
        ax.set_xticks(np.arange(0, x, 1))
        ax.set_yticks(np.arange(0, y, 1))
        ax.set_xticklabels(np.arange(1, x + 1, 1))  # 1'den başlayacak şekilde ayarla
        ax.set_yticklabels(np.arange(1, y + 1, 1))  # 1'den başlayacak şekilde ayarla

        # Lejand ekleme
        red_patch = plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='red', markersize=10, label="Dolu")
        green_patch = plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='green', markersize=10, label="Boş")
        blue_patch = plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='blue', markersize=10, label="Başlangıç Noktası")
        
        ax.legend(handles=[red_patch, green_patch, blue_patch], loc='upper left', bbox_to_anchor=(1, 1))

        # Başlangıç noktası ve BFS sonucu
        st.write(f"### **En yakın boş park yeri mesafesi: {distance}**")
        st.write(f"### **Kullanılacak yol: {' -> '.join(path)}**")

        # Görselleştirme
        st.pyplot(fig)

if __name__ == "__main__":
    main()
