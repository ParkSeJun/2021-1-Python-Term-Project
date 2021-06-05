import random
import tkinter as tk
root = tk.Tk()
root.title("Tkinter Bar and Pie Graph")

###############################################################################################
#바 차트

tk.Label(root, text='Bar Chart').pack()
data = [21, 20, 19, 16, 14, 13, 11, 9, 4, 3]
c_width = 400
c_height = 350
c = tk.Canvas(root, width=c_width, height=c_height, bg= 'white')
c.pack()

#experiment with the variables below size to fit your needs

y_stretch = 15
y_gap = 20
x_stretch = 10
x_width = 20
x_gap = 20
for x, y in enumerate(data):
    # calculate reactangle coordinates
    x0 = x * x_stretch + x * x_width + x_gap
    y0 = c_height - (y * y_stretch + y_gap)
    x1 = x * x_stretch + x * x_width + x_width + x_gap
    y1 = c_height - y_gap
    # Here we draw the bar
    c.create_rectangle(x0, y0, x1, y1, fill="red")
    c.create_text(x0+2, y0, anchor=tk.SW, text=str(y))

###############################################################################################
#파이차트

def random_color():
    color = '#'
    colors = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    for i in range(6):
        color += colors[random.randint(0,15)]
    return color

tk.Label(root, text='Pie Chart').pack()
c2 = tk.Canvas(width=c_width, height=c_height, bg='white')
c2.pack()
data2 = [100, 150, 200, 300, 50]
start = 0
s = sum(data2)

for i in range(5):
    extent = data2[i]/s * 360
    color = random_color()
    c2.create_arc((0,0,300,300),fill=color,outline='white',start=start,extent=extent)
    start = start+extent
    c2.create_rectangle(300,20+20*i,300+30,20+20*(i+1),fill=color)
    c2.create_text(300+50,10+20*(i+1),text=str(data2[i]))

root.mainloop()