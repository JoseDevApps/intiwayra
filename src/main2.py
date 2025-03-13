import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from data_handler import process_inputs  

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Geospatial Data Analysis")
        self.root.geometry("800x550")
        self.root.configure(bg="#2C3E50")  

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#2C3E50")
        self.style.configure("TLabel", background="#ECF0F1", font=("Arial", 12, "bold"))
        self.style.configure("TButton", font=("Arial", 12), padding=10, background="#1ABC9C", foreground="white", relief="flat")
        self.style.configure("TEntry", font=("Arial", 11), padding=6, fieldbackground="#34495E", foreground="white", relief="flat")

        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_input_options()
        self.create_multiselector()
        self.create_action_button()
        self.create_progress_bar()
        self.create_plot_area()

    def create_input_options(self):
        """Option to manually enter Latitude/Longitude or upload an Excel file"""
        self.input_mode = tk.StringVar(value="manual")  

        input_frame = ttk.Frame(self.main_frame)
        input_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        # Radio buttons to choose input method
        self.radio_manual = ttk.Radiobutton(input_frame, text="Manual Entry", variable=self.input_mode, value="manual", command=self.toggle_input_mode)
        self.radio_manual.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.radio_excel = ttk.Radiobutton(input_frame, text="Upload Excel", variable=self.input_mode, value="excel", command=self.toggle_input_mode)
        self.radio_excel.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Latitude & Longitude Entry Fields
        self.lat_label = ttk.Label(input_frame, text="Latitude:")
        self.lat_entry = ttk.Entry(input_frame)

        self.lon_label = ttk.Label(input_frame, text="Longitude:")
        self.lon_entry = ttk.Entry(input_frame)

        self.lat_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.lat_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.lon_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.lon_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # File selection button (initially hidden)
        self.upload_button = ttk.Button(input_frame, text="Select Excel File", command=self.load_excel)
        self.upload_button.grid(row=3, column=0, columnspan=2, pady=5)
        self.upload_button.grid_remove()  

        input_frame.columnconfigure(1, weight=1)

    def toggle_input_mode(self):
        """Switch between manual entry and file upload"""
        if self.input_mode.get() == "manual":
            self.lat_label.grid()
            self.lat_entry.grid()
            self.lon_label.grid()
            self.lon_entry.grid()
            self.upload_button.grid_remove()
        else:
            self.lat_label.grid_remove()
            self.lat_entry.grid_remove()
            self.lon_label.grid_remove()
            self.lon_entry.grid_remove()
            self.upload_button.grid()

    def load_excel(self):
        """Load Latitude and Longitude from an Excel file"""
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        self.filedir = file_path
        if not file_path:
            return  

        try:
            df = pd.read_excel(file_path, skiprows=1)
            
            if "Latitude" in df.columns and "Longitude" in df.columns:
                self.lat_entry.delete(0, tk.END)
                self.lon_entry.delete(0, tk.END)
                self.lat_entry.insert(0, str(df["Latitude"].iloc[0]))
                self.lon_entry.insert(0, str(df["Longitude"].iloc[0]))
                messagebox.showinfo("Success", "Coordinates loaded successfully.")
            else:
                messagebox.showerror("Error", "Excel must contain 'Latitude' and 'Longitude' columns.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {e}")

    def create_multiselector(self):
        """Dropdown for selecting data type"""
        self.selector_label = ttk.Label(self.main_frame, text="Select Data Type:")
        self.selector_label.grid(row=1, column=0, padx=5, pady=10, sticky="w")

        self.options = ["Irradiación Solar", "Eolico"]
        self.selector = ttk.Combobox(self.main_frame, values=self.options, state="readonly")
        self.selector.grid(row=1, column=1, padx=5, pady=10, sticky="ew")
        self.selector.set(self.options[0])

    def create_action_button(self):
        """Action Button with hover effect"""
        self.action_button = tk.Button(self.main_frame, text="Generate Report",
                                       command=self.on_button_click, font=("Arial", 12, "bold"),
                                       bg="#1ABC9C", fg="white", padx=10, pady=6, relief="flat", bd=3,
                                       activebackground="#16A085")
        self.action_button.grid(row=2, column=0, columnspan=2, pady=20, sticky="ew")
        self.action_button.bind("<Enter>", lambda e: self.action_button.config(bg="#16A085"))
        self.action_button.bind("<Leave>", lambda e: self.action_button.config(bg="#1ABC9C"))

    def create_progress_bar(self):
        """Animated Progress Bar"""
        self.progress_label = ttk.Label(self.main_frame, text="Processing...")
        self.progress = ttk.Progressbar(self.main_frame, length=200, mode="indeterminate")

    def create_plot_area(self):
        """Canvas for Matplotlib"""
        self.plot_frame = ttk.Frame(self.main_frame)
        self.plot_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")
        self.figure_canvas = None  

    def on_button_click(self):
        """Handle button click"""
        try:
            lat = float(self.lat_entry.get())
            lon = float(self.lon_entry.get())
            option = self.selector.get()
            input_mode = self.input_mode.get()  # Get the selected input mode

            self.progress_label.grid(row=4, column=0, columnspan=2, pady=5)
            self.progress.grid(row=5, column=0, columnspan=2, pady=5)
            self.progress.start()

            processing_thread = threading.Thread(target=self.process_data, args=(lat, lon, option, input_mode), daemon=True)
            processing_thread.start()

        except ValueError:
            self.stop_progress()
            messagebox.showerror("Invalid Input", "Please enter valid numeric values.")

    def process_data(self, lat, lon, option, mode):
        """ Process the data in a background thread """
        try:
            fig = None
            # Call the real data handler function to process inputs
            if self.input_mode.get()=="excel":
                print(self.filedir)
                result, df = process_inputs(lat, lon, option, mode, file=self.filedir)
            else:
                result, df = process_inputs(lat, lon, option, mode, file="")

            if option=="Irradiación Solar":
                for i in range(0,df.shape[0]):
                    #######################
                    # Graficos GHI
                    ####################### 
                    GHI_values = df.iloc[i, :12].tolist()
                    bins = GHI_values
                    Meses = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 
                                'nov', 'dic']
                    fig, ax = plt.subplots(figsize=(4, 3))  # Create Matplotlib figure
                    ax.bar(Meses, bins, color='#4F81BC', width=0.8, edgecolor='black', label='Frecuencia Observada')
                    ax.set_title('Irradiacion GHI')
                    ax.set_ylabel('[kWh/m2]')
                    ax.grid(True)
                    plt.tight_layout()
                    plt.savefig(str(i+1)+'-Irradiacion GHI.jpg')
                    #######################
                    # Graficos DNI
                    #######################
                    DNI_values = df.iloc[i, 12:24].tolist()
                    bins = DNI_values
                    Meses = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 
                                'nov', 'dic']
                    fig, ax = plt.subplots(figsize=(4, 3))  # Create Matplotlib figure
                    ax.bar(Meses, bins, color='#4F81BC', width=0.8, edgecolor='black', label='Frecuencia Observada')
                    ax.set_title('Irradiacion DNI')
                    ax.set_ylabel('[kWh/m2]')
                    ax.grid(True)
                    plt.tight_layout()
                    plt.savefig(str(i+1)+'-Irradiacion DNI.jpg')      
                    #######################
                    # Graficos DIF
                    #######################
                    DIF_values = df.iloc[i, 24:36].tolist()
                    bins = DIF_values
                    Meses = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 
                                'nov', 'dic']
                    fig, ax = plt.subplots(figsize=(4, 3))  # Create Matplotlib figure
                    ax.bar(Meses, bins, color='#4F81BC', width=0.8, edgecolor='black', label='Frecuencia Observada')
                    ax.set_title('Irradiacion DIF')
                    ax.set_ylabel('[kWh/m2]')
                    ax.grid(True)
                    plt.tight_layout()
                    plt.savefig(str(i+1)+'-Irradiacion DIF.jpg')  
                    #######################
                    # Graficos TEMP
                    #######################
                    TEMP_values = df.iloc[i, 36:48].tolist()
                    bins = TEMP_values
                    Meses = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 
                                'nov', 'dic']
                    fig, ax = plt.subplots(figsize=(4, 3))  # Create Matplotlib figure
                    ax.bar(Meses, bins, color='#4F81BC', width=0.8, edgecolor='black', label='Frecuencia Observada')
                    ax.set_title('Temperatura en grados celcius')
                    ax.set_ylabel('Grados celcius')
                    ax.grid(True)
                    plt.tight_layout()
                    plt.savefig(str(i+1)+'-Temperatura.jpg')  

            # Stop the progress bar and hide it after processing
            self.root.after(0, self.stop_progress)  # Update GUI from the main thread
            # Update the GUI with the plot
            if self.input_mode.get()!="excel":
                self.root.after(0, self.display_plot, fig)
            # Show the result to the user
            self.root.after(0, self.show_result, result)  # Update GUI from the main thread
        except Exception as e:
            # Stop the progress bar and hide it if there's an error
            self.root.after(0, self.stop_progress)  # Update GUI from the main thread
            self.root.after(0, self.show_error, str(e))  # Update GUI from the main thread


    def display_plot(self, fig):
        """ Display the Matplotlib figure inside Tkinter """
        if self.figure_canvas:
            self.figure_canvas.get_tk_widget().destroy()  # Clear previous plot

        # Ensure the plot fits properly in the Tkinter window
        self.figure_canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)  # Make it expandable

        plt.tight_layout()  # Adjust the plot to avoid clipping of titles/labels
    

    def stop_progress(self):
        """Stop progress bar animation"""
        self.progress.stop()
        self.progress_label.grid_remove()
        self.progress.grid_remove()

    def show_result(self, result):
        """Show result"""
        messagebox.showinfo("Success", result)

    def show_error(self, error_message):
        """Show error"""
        messagebox.showerror("Error", f"An error occurred: {error_message}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
