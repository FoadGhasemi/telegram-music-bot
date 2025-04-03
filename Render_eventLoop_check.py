import asyncio

try:
    loop = asyncio.get_running_loop()
    print("🔴 A running event loop was detected!")
except RuntimeError:
    print("🟢 No running event loop. Safe to use asyncio.run()")
