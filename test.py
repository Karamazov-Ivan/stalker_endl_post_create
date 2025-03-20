from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator


def print_1():
    print(11111111111111111111)

def main():
    action = inquirer.rawlist(
        message="Меню:",
        choices=[
            "Upload",
            "Download",
            Choice(value='some_value', name="Вход"),
            Choice(value=None, name="Exit"),
        ],
        default=None,
    ).execute()

    if action == 'some_value':
        print_1()
        region = inquirer.select(
            message="Select regions:",
            choices=[
                Choice("ap-southeast-2", name="Sydney"),
                Choice("ap-southeast-1", name="Singapore"),
                Separator(),
                "us-east-1",
                "us-east-2",
            ],
            multiselect=True,
            transformer=lambda result: f"{len(result)} region{'s' if len(result) > 1 else ''} selected",
        ).execute()


if __name__ == "__main__":
    main()

# from InquirerPy import inquirer


# def main():
#     proceed, service, confirm = False, False, False
#     proceed = inquirer.confirm(message="Proceed?", default=True).execute()
#     if proceed:
#         service = inquirer.confirm(message="Require 1 on 1?").execute()
#     if service:
#         confirm = inquirer.confirm(message="Confirm?").execute()


# if __name__ == "__main__":
#     main()




# from InquirerPy import inquirer

# name = inquirer.text(message="What's your name:").execute()
# fav_lang = inquirer.select(
#     message="What's your favourite programming language:",
#     choices=["Go", "Python", "Rust", "JavaScript"],
# ).execute()
# confirm = inquirer.confirm(message="Confirm?").execute()