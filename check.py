import sys

import django


def check_python_version():
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 11):
        print("❌ Python version is too old")
        return False
    elif sys.version_info >= (3, 12):
        print("⚠️ Python version is newer than tested")
    else:
        print("✅ Python version is compatible")
    return True


def check_django_version():
    print(f"Django version: {django.get_version()}")
    if django.VERSION < (4, 2):
        print("❌ Django version is too old")
        return False
    elif django.VERSION >= (5, 0):
        print("⚠️ Django version is newer than tested")
    else:
        print("✅ Django version is compatible")
    return True


if __name__ == "__main__":
    print("=== Проверка совместимости версий ===\n")
    check_python_version()
    print()
    check_django_version()
    print("\n=== Все проверки выполнены ===")
