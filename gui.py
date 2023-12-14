from main import *
from curses import window
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Spinbox
from tkinter.filedialog import askopenfile, asksaveasfilename
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker


class GUI:
    def __init__(self, window):
        """
        Initializing the GUI Object Class.

            Params : 
                - window (object) : Tk() window object
            Returns : 
                - None
        """
        self.window = window
        self.file = None
        self.file_path = None

        self.prmpt = Label(
            self.window, width=30, text="Please Select Qualtrics Results:"
        )
        self.prmpt.grid(row=1, column=0, columnspan=2,
                        padx=8, pady=(16, 2), sticky="n")

        self.mod_label = Label(self.window, width=10, text="Module: ")
        self.mod_label.grid(row=2, column=0)

        self.module = StringVar()
        self.mod = Spinbox(
            self.window, width=4, from_=1, to=12, textvariable=self.module, wrap=True
        )
        self.mod.grid(row=2, column=1, pady=2, padx=(0, 4))

        self.btn_label = Label(self.window, width=10, text="Select File: ")
        self.btn_label.grid(row=3, column=0, padx=(6, 0))

        self.btn = Button(
            self.window, width=4, text="Open", command=self.open_dashboard
        )
        self.btn.grid(row=3, column=1, pady=2, padx=(0, 4))

    def get_module(self):
        """
        Gets the value from the Spinbox and sets self.module to that value.

            Params :
                - None
            Returns :
                - None
        """
        if self.mod.get():
            self.module = self.mod.get()
        else:
            self.module = None

    def open_dashboard(self):
        """
        Opens the new window for the analysis dashboard.

            Params : 
                - None
            Returns : 
                - None
        """
        self.get_module()

        self.file = askopenfile(
            mode="r", filetypes=[("Comma-Separated Values", "*.csv")]
        )

        if self.file is not None:
            content = self.file.read()
            self.file_path = self.file.name

            a_win = Toplevel(self.window)
            a_win.title("Analysis")

            # Set the new window position
            a_win.geometry(f"+{self.window.winfo_x()}+{self.window.winfo_y()}")
            a_win.geometry(f"+{a_win.winfo_screenwidth()//2}+0")
            a_win.resizable(False, False)

            self.label = Label(a_win, text=f"Selected File: {self.file_path}")
            self.label.pack()

            self.mod_label = Label(
                a_win,
                text=f"Analysis for Module {self.module}"
                if self.module
                else "Analysis for all Modules",
            )
            self.mod_label.pack()

            pre_fig, pre_key, sus_fig, sus_key, sus_chart, sus_report = self.analysis(
                self.file_path, self.module
            )

            self.pre_fig = FigureCanvasTkAgg(pre_fig, master=a_win)
            self.pre_fig.get_tk_widget().pack()

            self.pre_key = Label(a_win, text=pre_key, justify=LEFT, padx=3)
            self.pre_key.pack()

            self.sus_fig = FigureCanvasTkAgg(sus_fig, master=a_win)
            self.sus_fig.get_tk_widget().pack()

            self.sus_key = Label(a_win, text=sus_key, justify=LEFT, padx=3)
            self.sus_key.pack()

            self.sus_line_chart = FigureCanvasTkAgg(sus_chart, master=a_win)
            self.sus_line_chart.draw()
            self.sus_line_chart.get_tk_widget().pack()

            self.sus_lab = Label(a_win, text=sus_report)
            self.sus_lab.pack()

            self.save_button = Button(
                a_win,
                text="Save Charts",
                command=lambda: self.save_figures(
                    [pre_fig, sus_fig, sus_chart]),
            )
            self.save_button.pack()

            a_win.protocol("WM_DELETE_WINDOW", self.on_window_close)

    def on_window_close(self):
        """
        For closing down everything once the window is closed.

            Params : 
                - None
            Returns: 
                - None
        """
        plt.close("all")  # Close all Matplotlib figures
        self.window.quit()  # Quit the Tkinter main loop

    def analysis(self, file_path, module):
        """
        TODO: SPLIT THIS METHOD INTO SEVERAL METHODS INSTEAD OF SEVERAL DIFFERENT PARTS
        Performs the analysis of the file, makes the charts, and returns them.

            Params : 
                - file_path (str) : the path for the file
                - module (int) : integer value for the module number
            Returns : 
                - pre_fig (Figure) : box and whisker plot for the preliminary questions
                - pre_key (str) : key for the preliminary questions
                - sus_fig (Figure) : box and whisker plot for the system usability questions
                - sus_key (str) : key for the system usability questions
                - sus_chart (Figure) : line chart for the system usability score
                - sus_report (str) : report for the system usability score
        """
        df = pd.read_csv(file_path)
        df.drop(index=[1], inplace=True)
        df.drop(
            columns=[
                "StartDate",
                "EndDate",
                "Status",
                "IPAddress",
                "Progress",
                "Duration (in seconds)",
                "Finished",
                "RecordedDate",
                "ResponseId",
                "RecipientLastName",
                "RecipientFirstName",
                "RecipientEmail",
                "ExternalReference",
                "LocationLatitude",
                "LocationLongitude",
                "DistributionChannel",
            ],
            inplace=True,
        )
        if module:
            condition = (df["Module"] == module) | (df.index.isin([0]))
            df = df[condition]
        # df.dropna(inplace=True)

        # ============= Get Key ============= #
        questions = df.drop(
            columns=["UserLanguage", "Q_RecaptchaScore",
                     "Name", "Email", "Module"],
            inplace=True,
        )
        questions = df.iloc[0]

        x = {}
        q = {}

        for col_name, question in questions.items():
            preface, question = question.split(" - ")
            q[col_name[:2]] = preface
            x[col_name] = question

        keys = []
        for cat, pref in q.items():
            key = ""
            key += f"{pref}\n"
            for num, question in x.items():
                if num[:2] == cat:
                    key += f"  {num}\t: {question}\n"
            keys.append(key)

        # ============= Get Responses ============= #
        responses = df.drop(index=[0])
        responses = responses.astype(int)

        desc_stats = responses.agg(["mean"])

        labels, tables = [
            label.split("_")[0][:3] + label.split("_")[1]
            for label, table in desc_stats.items()
        ], [table for label, table in desc_stats.items()]

        labels = ['ease', 'time', 'support', 'useful', 'too complex', 'intuitive', 'support', 'integrated',
          'inconsistent', 'navigation', 'cumbersome', 'layout', 'prereqs']

        means = []
        for table in tables:
            for i, j in table.items():
                if i == "mean":
                    means.append(round(j, 2))

        # ============= Split Prelim and SUS ============= #
        pre_q = responses.iloc[:, :3]
        sus_q = responses.iloc[:, 3:]

        pre_lab = labels[:3]
        sus_lab = labels[3:]

        # ============= Make the Prelim Chart ============= #
        target_val = 4
        pre_fig = self.box_and_whisker(
            pre_q, pre_lab, target_val, module, "Preliminary Questions")

        # ============= Make the SUS Chart ============= #
        target_val = 3
        sus_fig = self.box_and_whisker(
            sus_q, sus_lab, target_val, module, "System Usability Breakdown")

        # ============= Make the SUS Line Chart ============= #
        sus = self.calc_sus(means[3:])
        sus_report, sus_chart = self.get_sus_report(sus)

        pre_key, sus_key = keys[0], keys[1]

        return pre_fig, pre_key, sus_fig, sus_key, sus_chart, sus_report

    def box_and_whisker(self, data, labels, target_val, module, type):
        """
        Makes the box and whisker chart with a target value line plotted on it.

        Params:
            - data (int[]) : a list of integer values used as data for the chart
            - labels (str[]) : a list of string values for labels on the x-axis
            - target_val (float) : a target value to be plotted as a horizonal line
            - module (int) : module number
            - type (str) : used for the title of the chart

        Returns: 
            - fig (Figure) : the box and whisker chart
        """
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_ylim(0, 6)
        plt.boxplot(data, labels=labels, widths=0.25)
        # Rotating X-axis labels
        ax.set_xticklabels(labels=labels, rotation = 30)
        fig.subplots_adjust(top=0.92, bottom=0.2)

        ax.hlines(
            target_val,
            xmin=0,
            xmax=len(labels) + 1,
            color="red",
            linestyle="dashed",
            linewidth=2,
            alpha=0.5,
            label=f"Target Value: {target_val}",
        )
        ax.legend()

        if module:
            ax.set_title(f"Module {module} {type}")
        else:
            ax.set_title(f"{type} for all Modules")
        return fig

    def get_sus_report(self, sus):
        """
        Generates the full report for the System Usability Score (SUS).

            Params : 
                - sus (float) : float value for the System Usability Score (SUS)
            Returns :
                - report (str) : string containing the SUS and Rating
                - chart (Figure) : line chart for the SUS
        """
        report = f"System Usability Score (SUS): {sus}\nSUS Rating - {self.check_sus_score_rating(sus)}"
        chart = self.get_sus_chart(sus)

        return report, chart

    def calc_sus(self, means):
        """
        Calculates the System Usability Score (SUS).

            Params :
                - means (float[]) : list of means for each of the system usability questions
            Returns :
                - sus (float) : float value for the System Usability Score (SUS)
        """
        o_sum, e_sum = 0, 0
        for i in range(len(means)):
            if i % 2 == 0:  # odd
                o_sum += means[i] - 1
            else:  # even
                e_sum += 5 - means[i]
        sus = round(((o_sum + e_sum) * 2.5), 2)

        return sus

    def check_sus_score_rating(self, sus):
        """
        Checks the rating of the System Usability Score (SUS).

            Params :
                - sus (float) : float value for the System Usability Score (SUS)
            Returns: 
                - str : string representing the level of acceptability for the SUS
        """
        if sus >= 80.3:
            return "ACCEPTABLE"

        if sus > 51 and sus < 80.3:
            return "MODERATE"

        if sus <= 51:
            return "UNACCEPTABLE"

    def get_sus_chart(self, sus):
        """
        Creates the line chart to display the System Usability Score (SUS).

            Params : 
                - sus (float) : calculated System Usability Score
            Returns :
                - fig (Figure) : line chart for the System Usability Score
        """
        fig, ax = plt.subplots(
            figsize=(6, 0.85)
        )  # Increase the height to make the line visible
        fig.subplots_adjust(top=0.35, bottom=0.27)

        ax.set_xlim(0, 100)
        # Set a small range for the y-axis (for visual purposes)
        ax.set_ylim(0, 3)
        ax.yaxis.set_major_locator(plt.NullLocator())  # Hide the y-axis

        # Calculate the y-coordinate for centering vertically
        y_center = 0.15  # Adjust this value as needed

        # Plot the points on the number line with square markers and labels
        ax.plot(sus, y_center, "s", markersize=8, color="red")  # Square marker
        ax.text(
            sus,
            y_center - 1.5,
            f" {sus}",
            verticalalignment="top",
            fontsize=10,
            color="red",
            ha="center",
        )

        # Customize tick locator
        ax.xaxis.set_major_locator(ticker.FixedLocator([0, 51, 80.3, 100]))
        ax.tick_params(
            axis="x",
            which="both",
            bottom=False,
            top=True,
            labelbottom=False,
            labeltop=True,
        )
        ax.axvspan(0, 51, facecolor='red', alpha=0.3)
        ax.axvspan(51, 80.3, facecolor='yellow', alpha=0.5)
        ax.axvspan(80.3, 100, facecolor='lightgreen', alpha=0.7)

        # Set labels and title
        if self.module:
            ax.set_title(f"Module {self.module} SUS Score", pad=10)
        else:
            ax.set_title(f"SUS Score for All Modules")
        return fig

    def save_figures(self, figs):
        """
        Opens the dialog window for saving the figures.

            Params : 
                - figs (Figure[]) : list of figures to be saved
            Returns :
                - None
        """
        # Create a new dialog window
        save_dialog = Toplevel(self.window)
        save_dialog.title("Save Charts")
        save_dialog.geometry(
            f"+{self.window.winfo_x()}+{self.window.winfo_y()}")
        save_dialog.resizable(False, False)
        save_dialog.geometry("300x120")

        # Create IntVar variables to track the state of checkboxes
        figure_states = [IntVar(value=1) for fig in figs]

        # Function to handle the save button click
        def save_button_click():
            """
            Helper function for the save_figures method.

            Params : 
                - None
            Returns : 
                - None
            """
            for i, fig_state in enumerate(figure_states):
                if fig_state.get() == 1:
                    # Save the figure only if the corresponding checkbox is selected
                    file_path = asksaveasfilename(
                        defaultextension=".tiff",
                        filetypes=[
                            ("TIFF files", "*.tiff"),
                            ("PNG files", "*.png"),
                            ("JPEG files", "*.jpg;*.jpeg"),
                            ("All files", "*.*"),
                        ],
                        initial_file=f"{figs[i].axes[0].get_title()}.png",
                    )
                    if file_path:
                        figs[i].savefig(file_path)
                        messagebox.showinfo(
                            "Saved", f"The figure has been saved to:\n{file_path}"
                        )

            # Close the dialog after saving
            save_dialog.destroy()

        # Create checkboxes for each figure
        for i, fig in enumerate(figs):
            self.check = Checkbutton(
                save_dialog,
                text=f"{fig.axes[0].get_title()}",
                variable=figure_states[i],
            )
            self.check.pack()

        # Create a Save button
        save_button = Button(save_dialog, text="Save",
                             command=save_button_click)
        save_button.pack()
