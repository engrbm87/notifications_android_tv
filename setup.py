from setuptools import setup

setup(
    name="notifications_android_tv",
    version="0.1.2",
    description="Notifications for Android/Fire TVs",
    url="https://github.com/engrbm87/notifications_android_tv",
    download_url="https://github.com/engrbm87/notifications_android_tv/archive/refs/tags/0.1.2.tar.gz",
    author="Rami Mousleh",
    author_email="engrbm87@gmail.com",
    install_requires=["requests"],
    license="MIT",
    packages=["notifications_android_tv"],
    keywords = ["android tv", "fire tv", "notifications"],
    zip_safe=False,
)
