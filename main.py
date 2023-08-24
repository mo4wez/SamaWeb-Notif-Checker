from sanaweb_notif_checker import SamaWebNotifChecker

if __name__ == "__main__":
    # user_ids = ["652429947", "176198851"]# Replace with the user ID you want to send the notification to
    notifier = SamaWebNotifChecker(user_id="176198851")
    notifier.run()


# moawezz - 8/17/2023 - 4:36 PM