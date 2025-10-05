"""The `app` module launch the 'DoiToScopus' application through `AppMain` class
of `main_page` module of `dtsgui` package.
"""


# Local imports
from dtsgui.main_page import AppMain

def run_dts():
    """Main function used for starting the DoiToScopus application.
    """
    try:
        app = AppMain()
        app.mainloop()
    except Exception as err:
        print(err)

if __name__ == "__main__":
    run_dts()
