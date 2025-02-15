import tkinter as tk
from tkinter import ttk

class ChatbotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot UI")
        self.root.geometry("900x550")
        self.root.minsize(600, 500)  # Set minimum width and height

        # Set the theme to the system's theme
        style = ttk.Style()
        style.theme_use()  # Use the system's theme

        # Main container frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame for left panel
        self.left_panel = ttk.Frame(self.main_frame, width=150)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)

        # Scrollable list in left panel
        self.listbox_frame = ttk.Frame(self.left_panel)
        self.listbox_frame.pack(fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(self.listbox_frame, bg="lightgray", selectbackground="lightblue")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.listbox_frame, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Chat display container
        self.chat_display = ttk.Frame(self.main_frame)
        self.chat_display.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Scrollable chat area
        self.chat_canvas = tk.Canvas(self.chat_display)
        self.chat_scrollbar = ttk.Scrollbar(self.chat_display, orient="vertical", command=self.chat_canvas.yview)
        self.chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)

        # Frame inside canvas for messages
        self.chat_frame = ttk.Frame(self.chat_canvas, padding=(5, 2))
        self.chat_window = self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor="n", width=900)

        # Auto-scroll behavior
        self.chat_frame.bind("<Configure>", lambda e: self.update_scroll_region())

        # Input frame inside chat display
        self.input_frame = ttk.Frame(self.chat_display)
        self.input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=50, pady=5)

        # Text input box
        self.input_box = ttk.Entry(self.input_frame)
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.input_box.bind("<Return>", self.send_message)

        # Send button
        self.send_btn = ttk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.RIGHT)

        # Toggle button
        self.toggle_btn = ttk.Button(root, text="☰",width=5, command=self.toggle_panel)
        self.toggle_btn.place(x=4, y=4)

        # Track panel state
        self.panel_visible = True

        # Update width dynamically
        self.root.bind("<Configure>", self.update_chat_width)

    def toggle_panel(self):
        if self.panel_visible:
            self.left_panel.pack_forget()
        else:
            self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.panel_visible = not self.panel_visible

    def send_message(self, event=None):
        user_text = self.input_box.get()
        if user_text.strip():
            self.add_message(user_text, align="right", bg="lightblue")  # User messages on the right
            response = self.bot_response()
            self.add_message(response, align="left", bg="lightgray")  # Bot messages on the left
            self.input_box.delete(0, tk.END)
            self.scroll_to_bottom()

    def add_message(self, text, align, bg):
        msg_frame = ttk.Frame(self.chat_frame, padding=(5, 2))

        msg_label = tk.Label(msg_frame, text=text, bg=bg, wraplength=900, padx=10, pady=5, justify=tk.LEFT)
        msg_label.pack(side=align, padx=7, pady=5, fill=tk.X)

        msg_frame.pack(fill="x", anchor="w" if align == "left" else "e")

        self.chat_canvas.update_idletasks()
        self.update_scroll_region()

    def scroll_to_bottom(self):
        self.root.after(100, lambda: self.chat_canvas.yview_moveto(1.0))

    def bot_response(self):
        return "Hi"

    def update_scroll_region(self):
        """ Updates the scrolling region of the chat canvas. """
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))

    def update_chat_width(self, event=None):
        """ Adjusts the chat width dynamically to match the window width. """
        new_width = self.chat_display.winfo_width()
        self.chat_canvas.itemconfig(self.chat_window, width=new_width - tk.Canvas.winfo_reqwidth(self.chat_scrollbar))
        
        # Update wraplength for all message labels
        for msg_frame in self.chat_frame.winfo_children():
            for widget in msg_frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(wraplength=new_width - 40)  # Adjust wraplength based on new width
        

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotUI(root)
    root.mainloop()