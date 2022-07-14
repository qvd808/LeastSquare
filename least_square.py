import tkinter as tk
import numpy as np
from tkinter import messagebox

class Application(tk.Frame):

    width = 600
    height = 600

    s = []
    point = []

    xmax = 10
    xmin = -10

    ymax = 10
    ymin = -10

    xscl = width/(xmax - xmin)
    yscl = height/(ymax - ymin)

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.main_grid(root)
        self.data(root)

    def main_grid(self, root):
        # This is where we put the grid on the window
        main_grid = tk.LabelFrame(root, padx=0, pady=0)
        main_grid.grid(row=0, column=0)
        self.draw_grid(main_grid)

    def data(self, root):
        data = tk.LabelFrame(root, width=190, height=600)
        data.grid(row=0, column=1)
        data.grid_propagate(0)
        self.draw_data(data)

    def draw_grid(self, main_grid):
        # This function setting up the grid to draw
        myCanvas = tk.Canvas(main_grid, bg="white",
                             width=self.width, height=self.height)
        for x in range(self.xmin, self.xmax+1):
            myCanvas.create_line((x*self.xscl+self.width/2), (self.ymin*self.yscl+self.height/2),
                                 (x*self.xscl+self.width/2), (self.ymax*self.yscl+self.height/2), width=2, fill="green")

        for y in range(self.ymin, self.ymax+1):
            myCanvas.create_line((self.xmin*self.xscl+self.width/2), (y*self.yscl+self.height/2),
                                 (self.xmax*self.xscl+self.width/2), (y*self.yscl+self.height/2), width=2, fill="green")
        horizontal = myCanvas.create_line(
            0, self.height/2, self.width, self.height/2, width=3)
        vertical = myCanvas.create_line(
            self.width/2, 0, self.width/2, self.height, width=3)
        self.graph(myCanvas)
        self.draw_graph(myCanvas)
        self.draw_point(myCanvas)
        myCanvas.pack(fill=tk.BOTH, expand=1)

    def draw_data(self, data):
        #draw the API to get input from user
        # Frame 1
        f1 = tk.LabelFrame(data, padx=0, pady=0, borderwidth=0)
        f1.grid(row=0, column=0)
        text = tk.StringVar()
        text.set("X coordinate = ")
        lb1 = tk.Label(f1, text="X-Coordinate").grid(row=0, column=0)
        e1 = tk.Entry(f1, width=16)
        e1.grid(row=0, column=1)
        lb2 = tk.Label(f1, text="Y-Coordinate").grid(row=1, column=0)
        e2 = tk.Entry(f1, width=16)
        e2.grid(row=1, column=1)
        # Frame 2
        f2 = tk.LabelFrame(data, padx=0, pady=0, borderwidth=0)
        f2.grid(row=1, column=0)
        b2 = tk.Button(f2, text="Submit",
                       command=lambda: self.draw_line(e1, e2)).pack()

    def input(self, e1, e2):
        # get in put from the two entry, assuming they input integer data
        try:
            v1 = e1.get()
            v2 = e2.get()
            v1 = float(v1)
            v2 = float(v2)
            self.point.append((v1, v2))
            e1.delete(0, tk.END)
            e2.delete(0, tk.END)
        except ValueError:
            reponse = messagebox.showerror("Value Error!!!", "Value enter must be a number!!")
            e1.delete(0, tk.END)
            e2.delete(0, tk.END)

    def draw_line(self, e1, e2):
        #activate when push the submit button draw a new main grid
        self.input(e1, e2)
        if len(self.point) < 2:
            print("Does not have enough data to calculate")
        else:
            print("Starting calculate")
            self.main_grid(root)

    def least_square(self, point):
        #generating the list square point form self.point
        listx = [(1, x[0]) for x in point]
        listy = [(y[1]) for y in point]
        mx = np.matrix(listx)
        my = np.matrix(listy)
        my = mx.T.dot(my.T)
        mx = mx.T.dot(mx)
        result = mx.I.dot(my)
        return result.T.A

    def f(self, x, point):
        #generating function from the least square point
        return sum(point[0][i]*x**i for i in range(len(point[0])))

    def graph(self, myCanvas):
        #Generating a list of point in self.s to draw a graph
        self.reset_graph()
        if len(self.point) >= 2:
            try:
                x = self.xmin
                while x < self.xmax:
                    try:
                        self.s.append([x*self.xscl+self.width/2, self.height /
                                      2-self.f(x, self.least_square(self.point))*self.yscl])
                    except ValueError:
                        pass
                    x += 0.002
                return self.s
            except ZeroDivisionError:
                pass
        else:
            pass

    def draw_graph(self, myCanvas):
        # draw a graph on the canvas
        for i in range(len(self.s)-1):
            try:
                myCanvas.create_line((int(self.s[i][0]), int(self.s[i][1])), (int(
                    self.s[i+1][0]), int(self.s[i+1][1])), width=2, fill="red")
            except ZeroDivisionError:
                pass

    def reset_graph(self):
        # reset the list of point for new function
        self.s = []

    def draw_circle(self, myCanvas, x, y, r):
        return myCanvas.create_oval(x-r, y-r, x+r, y+r, fill="blue")

    def draw_point(self, myCanvas):
        # draw point on the canvas
        for p in self.point:
            self.draw_circle(myCanvas, self.width/2 +
                             p[0]*self.xscl, self.height/2 - p[1]*self.yscl, 5)


root = tk.Tk()
app = Application(root)
root.geometry("800x600")
root.title("Least square Approximations")

if __name__ == "__main__":
    root.mainloop()
