import asyncio

try:
    loop = asyncio.get_running_loop()
    print("🔴 A running event loop was detected!")
except RuntimeError:
    print("🟢 No running event loop. Safe to use asyncio.run()")

# Keep the bot running
while True:
    asyncio.sleep(10) # ensures the script actually runs inside Render.
                      # prints whether an event loop is already active.
                      # does not exit immediately, so logs should show output.