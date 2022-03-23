from setuptools import setup

setup(
    name="notifications_android_tv",
    version="0.1.4",
    description="Notifications for Android/Fire TVs",
    url="https://github.com/engrbm87/notifications_android_tv",
    download_url="https://github.com/engrbm87/notifications_android_tv/archive/refs/tags/0.1.3.tar.gz",
    author="Rami Mousleh",
    author_email="engrbm87@gmail.com",
    install_requires=["requests", "types-requests"],
    license="MIT",
    package_data={"notifications_android_tv": ["py.typed"]},
    packages=["notifications_android_tv"],
    keywords = ["android tv", "fire tv", "notifications"],
    zip_safe=False,
    python_requires=">=3.8",
)
