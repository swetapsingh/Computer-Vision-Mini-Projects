"""
Image to Pencil Sketch Converter - Tkinter GUI Application

A simple GUI application that converts images to pencil sketches using OpenCV.
Features side-by-side image display, background processing, and keyboard shortcuts.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
from typing import Optional
import os

from utils import convert_to_sketch_cv2, cv2_to_pil_gray


class ImageSketchApp:
    """Main application class for the Image to Pencil Sketch converter."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Image → Pencil Sketch (Demo)")
        self.root.geometry("900x520")
        self.root.resizable(False, False)
        
        # Image data
        self.original_image: Optional[Image.Image] = None
        self.sketch_array: Optional[Image.Image] = None
        self.current_image_path: Optional[str] = None
        
        # Setup GUI
        self._setup_gui()
        self._setup_keyboard_shortcuts()
        self._update_status("Ready")
    
    def _setup_gui(self) -> None:
        """Setup the main GUI layout."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Control panel
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.LEFT)
        
        ttk.Button(button_frame, text="Open Image", command=self._open_image).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Create Sketch", command=self._create_sketch).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Save Sketch", command=self._save_sketch).pack(side=tk.LEFT, padx=(0, 5))
        
        # Parameters frame
        params_frame = ttk.Frame(control_frame)
        params_frame.pack(side=tk.RIGHT)
        
        ttk.Label(params_frame, text="Blur:").pack(side=tk.LEFT, padx=(0, 2))
        self.blur_var = tk.StringVar(value="21")
        blur_entry = ttk.Entry(params_frame, textvariable=self.blur_var, width=8)
        blur_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(params_frame, text="Scale:").pack(side=tk.LEFT, padx=(0, 2))
        self.scale_var = tk.StringVar(value="256")
        scale_entry = ttk.Entry(params_frame, textvariable=self.scale_var, width=8)
        scale_entry.pack(side=tk.LEFT)
        
        # Image display frame
        display_frame = ttk.Frame(main_frame)
        display_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Original image panel
        original_frame = ttk.LabelFrame(display_frame, text="Original Image", padding="5")
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.original_label = ttk.Label(original_frame, text="No image loaded", anchor=tk.CENTER)
        self.original_label.pack(fill=tk.BOTH, expand=True)
        
        # Sketch image panel
        sketch_frame = ttk.LabelFrame(display_frame, text="Pencil Sketch", padding="5")
        sketch_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.sketch_label = ttk.Label(sketch_frame, text="No sketch created", anchor=tk.CENTER)
        self.sketch_label.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(5, 0))
    
    def _setup_keyboard_shortcuts(self) -> None:
        """Setup keyboard shortcuts."""
        self.root.bind('<Control-o>', lambda e: self._open_image())
        self.root.bind('<Control-s>', lambda e: self._save_sketch())
        self.root.bind('<Return>', lambda e: self._create_sketch())
    
    def _update_status(self, message: str) -> None:
        """Update status bar message."""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def _open_image(self) -> None:
        """Open and display an image file."""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        try:
            # Load and display original image
            self.original_image = Image.open(file_path)
            self.current_image_path = file_path
            self._display_image(self.original_image, self.original_label)
            
            # Clear sketch display
            self.sketch_array = None
            self.sketch_label.configure(image='', text="No sketch created")
            
            self._update_status(f"Loaded: {os.path.basename(file_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image:\n{str(e)}")
            self._update_status("Error loading image")
    
    def _create_sketch(self) -> None:
        """Create pencil sketch in background thread."""
        if not self.current_image_path:
            messagebox.showwarning("Warning", "Please open an image first.")
            return
        
        # Validate parameters
        try:
            blur_ksize = int(self.blur_var.get())
            scale = int(self.scale_var.get())
        except ValueError:
            messagebox.showerror("Error", "Blur and Scale must be valid integers.")
            return
        
        # Start background processing
        self._update_status("Processing...")
        thread = threading.Thread(target=self._process_sketch, args=(blur_ksize, scale))
        thread.daemon = True
        thread.start()
    
    def _process_sketch(self, blur_ksize: int, scale: int) -> None:
        """Process sketch in background thread."""
        try:
            # Create sketch using utils function
            sketch_array = convert_to_sketch_cv2(self.current_image_path, blur_ksize, scale)
            
            # Convert to PIL image
            sketch_pil = cv2_to_pil_gray(sketch_array)
            
            # Update GUI in main thread
            self.root.after(0, self._on_sketch_complete, sketch_pil)
            
        except Exception as e:
            self.root.after(0, self._on_sketch_error, str(e))
    
    def _on_sketch_complete(self, sketch_image: Image.Image) -> None:
        """Handle successful sketch completion."""
        self.sketch_array = sketch_image
        self._display_image(sketch_image, self.sketch_label)
        self._update_status("Sketch created successfully")
    
    def _on_sketch_error(self, error_message: str) -> None:
        """Handle sketch processing error."""
        messagebox.showerror("Error", f"Failed to create sketch:\n{error_message}")
        self._update_status("Error creating sketch")
    
    def _display_image(self, image: Image.Image, label: ttk.Label) -> None:
        """Display image in label with auto-resize to fit."""
        # Calculate display size (max 400x350 to fit in panels)
        max_width, max_height = 400, 350
        img_width, img_height = image.size
        
        # Calculate scale factor
        scale_factor = min(max_width / img_width, max_height / img_height, 1.0)
        
        # Resize image if needed
        if scale_factor < 1.0:
            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage and display
        photo = ImageTk.PhotoImage(image)
        label.configure(image=photo, text="")
        label.image = photo  # Keep reference to prevent garbage collection
    
    def _save_sketch(self) -> None:
        """Save the current sketch to file."""
        if self.sketch_array is None:
            messagebox.showwarning("Warning", "No sketch to save. Create a sketch first.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Sketch",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        try:
            self.sketch_array.save(file_path)
            self._update_status(f"Sketch saved: {os.path.basename(file_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save sketch:\n{str(e)}")
            self._update_status("Error saving sketch")


def main():
    """Main application entry point."""
    root = tk.Tk()
    app = ImageSketchApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
