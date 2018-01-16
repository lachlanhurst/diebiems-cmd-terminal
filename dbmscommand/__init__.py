from pyvesc.messages.base import VESCMessage

# remove whatever commands were setup for the VESC, as these are outdated
# and may not apply to the DieBieMS anyway
VESCMessage._msg_registry.clear()
