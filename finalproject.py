import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Drawing App")
        
        self.color = 'black'
        self.drawing_tool = 'line'
        self.brush_size = 2
        self.fill_color = None
        
        # Frame for tools
        self.tool_frame = ttk.Frame(self.root)
        self.tool_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Canvas for drawing
        self.canvas = tk.Canvas(self.root, bg='white', width=800, height=600)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        
        # Drawing tools
        ttk.Label(self.tool_frame, text="Drawing Tools").pack(pady=10)
        
        ttk.Button(self.tool_frame, text="Line", command=lambda: self.set_drawing_tool('line')).pack(fill=tk.X)
        ttk.Button(self.tool_frame, text="Rectangle", command=lambda: self.set_drawing_tool('rectangle')).pack(fill=tk.X)
        ttk.Button(self.tool_frame, text="Circle", command=lambda: self.set_drawing_tool('circle')).pack(fill=tk.X)
        
        # Brush size
        ttk.Label(self.tool_frame, text="Brush Size").pack(pady=10)
        self.size_slider = ttk.Scale(self.tool_frame, from_=1, to=10, orient=tk.HORIZONTAL, command=self.change_brush_size)
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(fill=tk.X)
        
        # Color selection
        ttk.Label(self.tool_frame, text="Color").pack(pady=10)
        ttk.Button(self.tool_frame, text="Choose Color", command=self.choose_color).pack(fill=tk.X)
        
        # Fill color (for shapes)
        ttk.Label(self.tool_frame, text="Fill Color").pack(pady=10)
        ttk.Button(self.tool_frame, text="Choose Fill Color", command=self.choose_fill_color).pack(fill=tk.X)
        
        # Save/load buttons
        ttk.Button(self.tool_frame, text="Save", command=self.save_image).pack(fill=tk.X)
        ttk.Button(self.tool_frame, text="Load", command=self.load_image).pack(fill=tk.X)
        
        # Mouse events
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        
        # Image for drawing
        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)
    
    def set_drawing_tool(self, tool):
        self.drawing_tool = tool
    
    def change_brush_size(self, event):
        self.brush_size = int(self.size_slider.get())
    
    def choose_color(self):
        color = colorchooser.askcolor()
        if color:
            self.color = color[1]
    
    def choose_fill_color(self):
        fill_color = colorchooser.askcolor()
        if fill_color:
            self.fill_color = fill_color[1]
    
    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y
    
    def draw(self, event):
        if self.drawing_tool == 'line':
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.color, width=self.brush_size)
            self.draw.line([self.start_x, self.start_y, event.x, event.y], fill=self.color, width=self.brush_size)
        elif self.drawing_tool == 'rectangle':
            x0, y0 = self.start_x, self.start_y
            x1, y1 = event.x, event.y
            if self.fill_color:
                self.canvas.create_rectangle(x0, y0, x1, y1, outline=self.color, fill=self.fill_color)
                self.draw.rectangle([x0, y0, x1, y1], outline=self.color, fill=self.fill_color)
            else:
                self.canvas.create_rectangle(x0, y0, x1, y1, outline=self.color)
                self.draw.rectangle([x0, y0, x1, y1], outline=self.color)
        elif self.drawing_tool == 'circle':
            x0, y0 = self.start_x, self.start_y
            x1, y1 = event.x, event.y
            if self.fill_color:
                self.canvas.create_oval(x0, y0, x1, y1, outline=self.color, fill=self.fill_color)
                self.draw.ellipse([x0, y0, x1, y1], outline=self.color, fill=self.fill_color)
            else:
                self.canvas.create_oval(x0, y0, x1, y1, outline=self.color)
                self.draw.ellipse([x0, y0, x1, y1], outline=self.color)
        self.start_x = event.x
        self.start_y = event.y
    
    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            try:
                self.image.save(file_path)
                messagebox.showinfo("Save", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")
    
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*"), ("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            try:
                image = Image.open(file_path)
                self.image = image.copy()
                self.draw = ImageDraw.Draw(self.image)
                self.canvas.delete("all")
                self.canvas.image = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas.image)
                messagebox.showinfo("Load", "Image loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")

# Main function
def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()




   

