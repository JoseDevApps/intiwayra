import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading  # Import threading to run long tasks in the background
from data_handler import process_inputs  # Import the real data handler function
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Geospatial Data App")
        self.root.geometry("800x500")
        self.root.minsize(700, 450)
        self.root.configure(bg="#2C3E50")  # Dark Blue-Gray Background

        # Styling
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#2C3E50")
        self.style.configure("TLabel", background="#2C3E50", foreground="#ECF0F1", font=("Arial", 12, "bold"))
        self.style.configure("TButton", font=("Arial", 12), padding=10, background="#1ABC9C", foreground="white", relief="flat")
        self.style.configure("TEntry", font=("Arial", 11), padding=6, fieldbackground="#34495E", foreground="white", relief="flat")
        self.style.configure("TCombobox", font=("Arial", 11), padding=6, background="#34495E", foreground="white", relief="flat")


        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Latitude and Longitude entry fields
        self.create_lat_lon_input()

        # Multiselector dropdown
        self.create_multiselector()

        # Action button
        self.create_action_button()

        # Progress bar (initially hidden)
        self.create_progress_bar()

        # Plot area
        self.create_plot_area()

        # Canvas for Matplotlib Figure
        self.figure_canvas = None  # Initialize as None

    def create_lat_lon_input(self):
        """Create Latitude & Longitude input fields"""
        input_frame = ttk.Frame(self.main_frame)
        input_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        ttk.Label(input_frame, text="📍 Latitude:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.lat_entry = ttk.Entry(input_frame)
        self.lat_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="📍 Longitude:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.lon_entry = ttk.Entry(input_frame)
        self.lon_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        input_frame.columnconfigure(1, weight=1)

    def create_multiselector(self):
        """Create a multiselect dropdown"""
        self.selector_label = ttk.Label(self.main_frame, text="📊 Select Data Type:")
        self.selector_label.grid(row=1, column=0, padx=5, pady=10, sticky="w")

        self.options = ["Irradiación Solar", "Option 2", "Option 3"]
        self.selector = ttk.Combobox(self.main_frame, values=self.options, state="readonly")
        self.selector.grid(row=1, column=1, padx=5, pady=10, sticky="ew")
        self.selector.set(self.options[0])

    def create_action_button(self):
        # """ Create a button to trigger an action """
        # self.action_button = tk.Button(self.root, text="Generate Action", command=self.on_button_click)
        # self.action_button.pack(pady=20)
        """Create a friendly action button"""
        self.action_button = tk.Button(
            self.main_frame, text="🚀 Generate Report",
            command=self.on_button_click, font=("Arial", 12, "bold"), bg="#FFA07A",
            fg="white", padx=10, pady=6, relief="flat", bd=3, activebackground="#FF7F50"
        )
        self.action_button.grid(row=2, column=0, columnspan=2, pady=20, sticky="ew")
    def create_progress_bar(self):
        """ Add a progress bar to indicate activity """
        self.progress_label = tk.Label(self.root, text="Processing...")
        self.progress = ttk.Progressbar(self.root, length=200, mode="indeterminate")
        
        # Initially, hide the progress bar and label
        self.progress_label.pack_forget()
        self.progress.pack_forget()

    def create_plot_area(self):
        """Create a canvas for displaying Matplotlib plots"""
        self.plot_frame = ttk.Frame(self.main_frame)
        self.plot_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")

        self.figure_canvas = None  # Placeholder for Matplotlib figure

        # Make the plot area expandable
        self.main_frame.rowconfigure(3, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

    def on_button_click(self):
        """ Handle the button click event """
        try:
            # Get the latitude and longitude values
            lat = float(self.lat_entry.get())
            lon = float(self.lon_entry.get())
            option = self.selector.get()

            # Show the progress bar when the button is clicked
            self.progress_label.pack(pady=5)
            self.progress.pack(pady=5)
            self.progress.start()  # Start the progress bar animation

            # Create a new thread to run the data processing function
            processing_thread = threading.Thread(target=self.process_data, args=(lat, lon, option))
            processing_thread.start()

        except ValueError:
            # Stop the progress bar and hide it if there's an error
            self.progress.stop()
            self.progress_label.pack_forget()
            self.progress.pack_forget()
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for latitude and longitude.")

    def process_data(self, lat, lon, option):
        """ Process the data in a background thread """
        try:
            # Call the real data handler function to process inputs
            result, df = process_inputs(lat, lon, option)
            GHI_values = df.iloc[0, :12].tolist()
            print(GHI_values)
            #######################
            # Graficos 
            #######################
            bins = GHI_values
            Meses = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 
                        'nov', 'dic']
            print(bins)
            fig, ax = plt.subplots(figsize=(4, 3))  # Create Matplotlib figure
            ax.bar(Meses, bins, color='#4F81BC', width=0.8, edgecolor='black', label='Frecuencia Observada')
            ax.set_title('Irradiacion GHI')
            ax.set_ylabel('[kWh/m2]')
            ax.grid(True)
            plt.tight_layout()
            plt.savefig('Irradiacion GHI.jpg')
            
            # Stop the progress bar and hide it after processing
            self.root.after(0, self.stop_progress)  # Update GUI from the main thread
            # Update the GUI with the plot
            self.root.after(0, self.display_plot, fig)
            # Show the result to the user
            self.root.after(0, self.show_result, result)  # Update GUI from the main thread
        except Exception as e:
            # Stop the progress bar and hide it if there's an error
            self.root.after(0, self.stop_progress)  # Update GUI from the main thread
            self.root.after(0, self.show_error, str(e))  # Update GUI from the main thread

    def stop_progress(self):
        """ Stop the progress bar and hide it """
        self.progress.stop()
        self.progress_label.pack_forget()
        self.progress.pack_forget()

    def display_plot(self, fig):
        """ Display the Matplotlib figure inside Tkinter """
        if self.figure_canvas:
            self.figure_canvas.get_tk_widget().destroy()  # Clear previous plot

        # Ensure the plot fits properly in the Tkinter window
        self.figure_canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)  # Make it expandable

        plt.tight_layout()  # Adjust the plot to avoid clipping of titles/labels
    
    def show_result(self, result):
        """ Show the result message in the GUI """
        messagebox.showinfo("Result", result)

    def show_error(self, error_message):
        """ Show error message in the GUI """
        messagebox.showerror("Error", f"An error occurred: {error_message}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
