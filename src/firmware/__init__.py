# Firmware
#
# Defines the platform and device definitions for all platforms where SenseOS can be used
# This includes the attached devices and their respective pins, OTA updates and another
# low-level operations for preparing the SenseOS environment
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>

# ---------------------------------------------------------------------
#                      Libraries and References
# ---------------------------------------------------------------------

# SenseOS Libraries
from senseos import SenseOS

# ---------------------------------------------------------------------
#                             SenseOS
# ---------------------------------------------------------------------

# Initialize Operating System
os = SenseOS()
os.initialize()

# ---------------------------------------------------------------------
#                             Exports
# ---------------------------------------------------------------------

__all__ = [
  "os"
]

