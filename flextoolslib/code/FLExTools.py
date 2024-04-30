#
#   Project: FlexTools
#   Module:  FLExTools
#   Platform: .NET v2 Windows.Forms (Python.NET 2.7)
#
#   The main entry point for the FlexTools application is here as main().
#   It is called from the launcher application in 
#   FlexTools\scripts\RunFlexTools.py.
#
#   First, set up the following:
#        - logging
#        - configuration parameters and paths (flextools.ini)
#        - load flexlibs and handle any errors
#   Then, in main()
#        - initialise the Flex interface (flexlibs)
#        - launch the FlexTools UI
#
#   Copyright Craig Farrow, 2010 - 2022
#

import sys
import os
import platform
import traceback


# -----------------------------------------------------------
# Imports
# -----------------------------------------------------------

# This call is required to initialise the threading mode for COM calls
# (e.g. using the clipboard) It must be made before clr is imported.
# Note: ctypes doesn't have windll on Linux
if platform.system() == "Windows":
    import ctypes
    ctypes.windll.ole32.CoInitialize(None)
else:
    # import clr_loader
    import pythonnet
    mono_base = '/opt/mono5-sil'
    # mono_base = '/usr'
    # mono_base = '/var/lib/flatpak/app/org.sil.FieldWorks/current/active/files'
    # mono_base = '/app/lib'
    mono_path = [
        f"{mono_base}/lib/mono/gac",
        f"{mono_base}/lib/mono/4.5",
        f"{mono_base}/lib",
    ]
    # os.environ['LD_RUN_PATH'] = os.getenv('LD_LIBRARY_PATH', '')
    # os.environ['MONO_ENV_OPTIONS'] = "--optimize=-gshared"
    # os.environ['MONO_ENV_OPTIONS'] = "--interp"
    # os.environ['MONO_GAC_PREFIX'] = "/usr/lib"
    # os.environ['MONO_PATH'] = ':'.join(mono_path)
    # https://www.mono-project.com/docs/advanced/runtime/logging-runtime-events
    os.environ['MONO_LOG_LEVEL'] = 'debug'
    # os.environ['MONO_LOG_MASK'] = 'asm,cfg,dll,io-layer,type'

    pythonnet.load(
        'mono',
        assembly_dir=mono_base,
        # debug=True,
        # libmono="/usr/lib/libmono-2.0.so.1",
        # set_signal_chaining=True,
    )
    # Alternative runtime loading.
    # rt = clr_loader.get_mono(assembly_dir=mono_sil)
    # pythonnet.set_runtime(rt)

import clr
import System

clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import (
        Application,
        MessageBox, 
        MessageBoxButtons, 
        MessageBoxIcon)

# -----------------------------------------------------------
# Logging
# -----------------------------------------------------------

import logging

if "DEBUG" in sys.argv[1:]:
    loggingLevel = logging.DEBUG
else:
    loggingLevel = logging.INFO

logging.basicConfig(filename='flextools.log', 
                    filemode='w', 
                    level=loggingLevel)

logger = logging.getLogger(__name__)


# -----------------------------------------------------------
# Paths and configuration
# -----------------------------------------------------------

from .. import version
logger.info(f"FLExTools library version: {version}")

from .FTConfig import FTConfig

#----------------------------------------------------------- 
# flexlibs
#----------------------------------------------------------- 

from .. import MinFWVersion, MaxFWVersion

try:
    from flexlibs import FLExInitialize, FLExCleanup

except Exception as e:
    msg = f"There was a fatal error during initialisation, which might be because of a newer version of FieldWorks.\n" \
          f"(This version of FLExTools has been tested with FieldWorks versions {MinFWVersion} - {MaxFWVersion}.)\n"\
          f"Details: {e}\n"\
          f"See flextools.log for more information."
    logger.error(msg)
    MessageBox.Show(msg,
                    "FLExTools: Fatal Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Exclamation)
    logger.error("Fatal exception importing flexlibs:\n%s" % traceback.format_exc())
    sys.exit(1)

logger.info(f"flexlibs imported successfully")


#----------------------------------------------------------- 
# UI
#----------------------------------------------------------- 

from .UIMain import FTMainForm

mainForm = None
# ------------------------------------------------------------------
def main(appTitle=None, customMenu=None, statusbarCallback=None):
    """
    Parameters:
        appTitle - a string with the name and version to display in 
            the main title bar. This allows systems built on FlexTools 
            to supply a custom title.
        customMenu - a tuple defining a custom menu that is inserted
            before the Help menu:
                (Menu Title, Menu Items)
                    Menu Title is a string
                    Menu Items is a list of tuples:
                        (Handler, Menu Text, Shortcut, Tooltip)
                    Handlers are functions that take two parameters, 
                    sender and event. 
                    If the Handler is None, then the menu is disabled.
                    Menu Text and Tooltip are strings.
                    Shortcut is a System.Windows.Forms.Shortcut sub-value,
                    or None.
                    If the tuple is None, then a separator is inserted.
        statusbarCallback - a function that returns a string to be
            included in the status bar.
        
    """
    global FTConfig
    global mainForm

    FLExInitialize()

    logger.debug("Creating MainForm")
    mainForm = FTMainForm(appTitle, customMenu, statusbarCallback)
    logger.debug("Launching WinForms Application")
    Application.Run(mainForm)

    # Save the configuration
    FTConfig.save()
    
    FLExCleanup()
    

def refreshStatusbar():
    global mainForm
    mainForm.UpdateStatusBar()
