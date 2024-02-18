from time import sleep

from ciou.progress import MessageStatus, OutputConfig, Progress, Update

LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

p = Progress(OutputConfig())
p.start()

p.push(Update(key="first", message="Progress is a library for communicating CLI app progress to the user", status=MessageStatus.STARTED))

sleep(1.5)

p.push(Update(key="parallel", message="There can be multiple active progress messages at once", status=MessageStatus.STARTED))
p.push(Update(key="progress", message="Progress message can include part that is only outputted to TTY terminals", status=MessageStatus.STARTED))

sleep(0.3)
for i in range(10):
    p.push(Update(key="progress", progress_message=f"({(i+1)*10} %)"))
    sleep(0.3)

p.push(Update(key="progress", status=MessageStatus.SUCCESS))
p.push(Update(key="first", message="Progress messages can be updated while they are in pending or started state"))
sleep(1.5)

p.push(Update(key="parallel", status=MessageStatus.ERROR, details="Error: Message details can be used, for example, to communicate error messages to the user."))
sleep(1.5)

p.push(Update(key="unknown", status=MessageStatus.STARTED, message="If message has started status when log is closed, its status is set to unknown"))
p.push(Update(key="pending", message="Pending tasks are not written to output. If message has pending status when log is closed, its status is set to skipped", status=MessageStatus.PENDING))
sleep(1.5)

p.push(Update(key="first", message="Progress messages are, by default, written to stderr", status=MessageStatus.SUCCESS))
sleep(1.5)

p.push(Update(key="long", message=f"Long messages are truncated - {LOREM_IPSUM}", details=LOREM_IPSUM, status=MessageStatus.STARTED))
sleep(3)

p.push(Update(key="long", status=MessageStatus.WARNING))
sleep(3)


p.stop()
