import random


def guess_number_game():
    secret_number = random.randint(1, 100)
    attempts = 0

    print("欢迎来到猜数字游戏！我已经想好了一个1到100之间的数字。")

    while True:
        try:
            guess = int(input("请输入你的猜测："))
        except ValueError:
            print("请输入有效的整数！")
            continue

        attempts += 1

        if guess < secret_number:
            print("你猜的数字太小了，请继续猜！")
        elif guess > secret_number:
            print("你猜的数字太大了，请继续猜！")
        else:
            print(f"恭喜你，你猜对了！你用了{attempts}次猜中了答案。")
            break


if __name__ == "__main__":
    guess_number_game()
